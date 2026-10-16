"""Offline transition failure tests; never read live company storage."""
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import uuid

from PIL import Image
import pytest

from ops import rename_company as tool
from deploy.company_provision import prepare_company
from deploy.provision import DemoError


def dump(path, value):
    path.write_text(json.dumps(value), encoding='utf-8')


@pytest.fixture
def installation(tmp_path):
    root = tmp_path / 'company'
    (root / 'project' / 'originals').mkdir(parents=True)
    (root / 'operator').mkdir()
    (root / 'backup-spool').mkdir()
    hub_id = str(uuid.uuid4())
    marker = dict(format='wavelink-company-c01', company_id='sulmara', company_name='Sulmara',
        hub_id=hub_id, installation_id=str(uuid.uuid4()), admin_id=str(uuid.uuid4()),
        admin_login='admin', initial_hash='pbkdf2_sha256$fixture', initial_credential_version=1,
        setup_key_sha256='a' * 64, created_at='2026-10-01T00:00:00Z', created_epoch=1,
        setup_expires_epoch=86401)
    dump(root / 'COMPANY_DEPLOYMENT.json', marker)
    dump(root / 'project' / 'hub.json', dict(hub_id=hub_id, label='Wavelink', project_name='Sulmara',
        defaults=dict(company='Sulmara', project='Sulmara', client='Sulmara', vessel='Survey vessel', vehicle='AUV')))
    dump(root / 'operator' / 'hosted.json', dict(external_origin='https://sulmara.mywavelink.com'))
    (root / 'project' / 'originals' / 'signed.pdf').write_bytes(b'Historical Sulmara PDF: preserve exactly.')
    with closing(sqlite3.connect(root / 'project' / 'dives.sqlite3')) as con:
        con.executescript('''CREATE TABLE users(id TEXT, password_hash TEXT);
            CREATE TABLE records(body TEXT); CREATE TABLE company_report_profile(body TEXT);
            INSERT INTO users VALUES('retained-user','retained-password-hash');
            INSERT INTO records VALUES('Sulmara historical record');
            INSERT INTO company_report_profile VALUES('Sulmara saved report profile');''')
        con.commit()
    deploy = tmp_path / 'deploy'
    identities = {}
    for company_id, name in (('sulmara', 'Sulmara'), ('corcovado', 'Corcovado')):
        folder = deploy / 'company_logos' / company_id
        folder.mkdir(parents=True)
        Image.new('RGB', (40, 20), color='navy').save(folder / 'logo.png')
        identities[company_id] = dict(name=name, logo='logo.png')
    dump(deploy / 'company_identities.json', identities)
    return root, deploy


def arguments(installation):
    root, deploy = installation
    return (root, deploy, 'sulmara', 'Sulmara', 'corcovado', 'Corcovado',
            'https://corcovado.mywavelink.com')


def complete_snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mode)
            for p in root.rglob('*') if p.is_file()}


def test_default_is_read_only_and_cli_has_no_credentials(installation, capsys):
    root, _ = installation
    before = complete_snapshot(root)
    result = tool.rename(*arguments(installation))
    assert result['status'] == 'dry_run'
    assert complete_snapshot(root) == before
    assert not (root.parent / 'company-rename-backups').exists()
    assert tool.main(['--root', str(root), '--deploy-dir', str(installation[1]),
        '--from-id', 'sulmara', '--from-name', 'Sulmara', '--to-id', 'corcovado',
        '--to-name', 'Corcovado', '--public-url', 'https://corcovado.mywavelink.com']) == 0
    output = capsys.readouterr().out
    assert 'pbkdf2_sha256' not in output and 'retained-password-hash' not in output
    assert complete_snapshot(root) == before


def test_apply_preserves_database_records_accounts_files_and_ids(installation):
    root, _ = installation
    before = tool.inventory(root)
    old_marker = tool.read_json(root / 'COMPANY_DEPLOYMENT.json')
    result = tool.rename(*arguments(installation), apply=True, service_stopped=True)
    assert result['status'] == 'renamed_offline' and result['database_unchanged']
    new_marker = tool.read_json(root / 'COMPANY_DEPLOYMENT.json')
    assert new_marker == {**old_marker, 'company_id': 'corcovado', 'company_name': 'Corcovado'}
    hub = tool.read_json(root / 'project/hub.json')
    assert hub['project_name'] == 'Corcovado' and hub['defaults']['company'] == 'Corcovado'
    assert hub['defaults']['client'] == hub['defaults']['project'] == 'Corcovado'
    assert hub['defaults']['vehicle'] == 'AUV' and hub['label'] == 'Wavelink'
    after = tool.inventory(root)
    assert {k:v for k,v in before.items() if k not in tool.FILES} == {k:v for k,v in after.items() if k not in tool.FILES}
    assert tool.inventory(Path(result['backup']) / 'company') == before
    assert (Path(result['backup']) / 'company' / 'backup-spool').is_dir()
    assert not (root / tool.PENDING).exists()
    if os.name == 'posix':
        for p in Path(result['backup']).rglob('*'):
            assert p.stat().st_mode & 0o077 == 0


def test_repeat_after_success_is_read_only_and_reports_completed(installation):
    root, _ = installation
    tool.rename(*arguments(installation), apply=True, service_stopped=True)
    before = complete_snapshot(root)
    backups = list((root.parent / 'company-rename-backups').iterdir())
    result = tool.rename(*arguments(installation), apply=True, service_stopped=True)
    assert result['status'] == 'already_renamed_offline' and result['changed_fields'] == []
    assert complete_snapshot(root) == before
    assert list((root.parent / 'company-rename-backups').iterdir()) == backups


def test_different_maintenance_owner_refused_before_private_writes(installation, monkeypatch):
    root, _ = installation
    before = complete_snapshot(root)
    actual_uid = os.geteuid()
    monkeypatch.setattr(tool.os, 'geteuid', lambda: actual_uid + 1)
    with pytest.raises(tool.Refusal, match='existing installation owner'):
        tool.rename(*arguments(installation), apply=True, service_stopped=True)
    assert complete_snapshot(root) == before


def test_custom_values_are_preserved_without_substring_replacement(installation):
    root, _ = installation
    hub = tool.read_json(root / 'project/hub.json')
    hub['project_name'] = 'Sulmara offshore campaign'
    hub['defaults']['client'] = 'Different client'
    hub['defaults']['project'] = 'Sulmara campaign 12'
    dump(root / 'project/hub.json', hub)
    result = tool.rename(*arguments(installation), apply=True, service_stopped=True)
    after = tool.read_json(root / 'project/hub.json')
    assert after['project_name'] == hub['project_name']
    assert after['defaults']['client'] == 'Different client'
    assert after['defaults']['project'] == 'Sulmara campaign 12'
    assert after['defaults']['company'] == 'Corcovado'
    assert set(result['retained_custom_fields']) == {'project_name', 'defaults.project', 'defaults.client'}


def test_stop_confirmation_required_before_any_mutation(installation):
    root, _ = installation
    before = complete_snapshot(root)
    with pytest.raises(tool.Refusal, match='service-stopped'):
        tool.rename(*arguments(installation), apply=True)
    assert complete_snapshot(root) == before


@pytest.mark.parametrize('change', ['company_id', 'company_name', 'hub_id'])
def test_wrong_source_or_hub_refused(installation, change):
    root, _ = installation
    if change == 'hub_id':
        path = root / 'project/hub.json'
        value = tool.read_json(path); value[change] = str(uuid.uuid4()); dump(path, value)
    else:
        path = root / 'COMPANY_DEPLOYMENT.json'
        value = tool.read_json(path); value[change] = 'other'; dump(path, value)
    before = complete_snapshot(root)
    with pytest.raises(tool.Refusal):
        tool.rename(*arguments(installation), apply=True, service_stopped=True)
    assert complete_snapshot(root) == before


@pytest.mark.parametrize('change', ['missing_identity', 'wrong_name', 'missing_logo', 'invalid_logo'])
def test_unreviewed_destination_refused(installation, change):
    _, deploy = installation
    if change in ('missing_identity', 'wrong_name'):
        identity = tool.read_json(deploy / 'company_identities.json')
        if change == 'missing_identity': del identity['corcovado']
        else: identity['corcovado']['name'] = 'Wrong name'
        dump(deploy / 'company_identities.json', identity)
    elif change == 'missing_logo':
        (deploy / 'company_logos/corcovado/logo.png').unlink()
    else:
        (deploy / 'company_logos/corcovado/logo.png').write_bytes(b'Not an image')
    with pytest.raises(tool.Refusal):
        tool.rename(*arguments(installation), apply=True, service_stopped=True)


@pytest.mark.parametrize('url', ['http://corcovado.mywavelink.com', 'https://demo.mywavelink.com',
    'https://corcovado.mywavelink.com/path', 'https://user:secret@corcovado.mywavelink.com',
    'https://corcovado.mywavelink.com:443', 'https://corcovado.mywavelink.com/'])
def test_noncanonical_or_demo_url_refused(installation, url):
    args = (*arguments(installation)[:-1], url)
    with pytest.raises(tool.Refusal):
        tool.rename(*args)


def test_running_service_lease_prevents_rename(installation):
    root, _ = installation
    before = tool.inventory(root)
    with tool.Lease(root / 'project/.server.lock'):
        with pytest.raises(tool.Refusal, match='still using'):
            tool.rename(*arguments(installation), apply=True, service_stopped=True)
    assert tool.inventory(root) == before and not (root / tool.PENDING).exists()


def test_insufficient_backup_space_refused_before_replacement(installation, monkeypatch):
    root, _ = installation
    before = tool.inventory(root)
    usage = tool.shutil.disk_usage(root)
    monkeypatch.setattr(tool.shutil, 'disk_usage', lambda _: type(usage)(usage.total, usage.total - 1, 1))
    with pytest.raises(tool.Refusal, match='Insufficient free space'):
        tool.rename(*arguments(installation), apply=True, service_stopped=True)
    assert tool.inventory(root) == before and not (root / tool.PENDING).exists()


def test_directory_read_error_fails_closed_before_backup_claim(installation, monkeypatch):
    root, _ = installation
    before = complete_snapshot(root)
    def failed_walk(*_, **kwargs):
        kwargs['onerror'](PermissionError('simulated unreadable project subdirectory'))
    monkeypatch.setattr(tool.os, 'walk', failed_walk)
    with pytest.raises(tool.Refusal, match='could not be fully read'):
        tool.rename(*arguments(installation), apply=True, service_stopped=True)
    # New leases may exist; the configuration and every pre-existing file remain exact.
    after = complete_snapshot(root)
    assert all(after[name] == value for name, value in before.items())
    assert not (root / tool.PENDING).exists()


def test_ordinary_write_failure_rolls_back_both_files(installation, monkeypatch):
    root, _ = installation
    before = tool.inventory(root)
    actual = tool.atomic_write
    failed = False
    def fail_once(path, data):
        nonlocal failed
        if path == root / 'COMPANY_DEPLOYMENT.json' and not failed:
            failed = True
            raise OSError('simulated stopped-disk write failure')
        actual(path, data)
    monkeypatch.setattr(tool, 'atomic_write', fail_once)
    with pytest.raises(tool.Refusal, match='both original JSON files were restored'):
        tool.rename(*arguments(installation), apply=True, service_stopped=True)
    assert tool.inventory(root) == before
    assert not (root / tool.PENDING).exists()


def interrupt_after_hub(installation, monkeypatch):
    root, _ = installation
    actual = tool.atomic_write
    def interrupt(path, data):
        if path == root / 'COMPANY_DEPLOYMENT.json':
            raise KeyboardInterrupt('simulated abrupt process interruption')
        actual(path, data)
    monkeypatch.setattr(tool, 'atomic_write', interrupt)
    with pytest.raises(KeyboardInterrupt):
        tool.rename(*arguments(installation), apply=True, service_stopped=True)
    monkeypatch.setattr(tool, 'atomic_write', actual)


def test_abrupt_interruption_blocks_boot_and_can_recover(installation, monkeypatch):
    root, _ = installation
    before = tool.inventory(root)
    interrupt_after_hub(installation, monkeypatch)
    assert (root / tool.PENDING).exists()
    assert tool.read_json(root / 'project/hub.json')['project_name'] == 'Corcovado'
    assert tool.read_json(root / 'COMPANY_DEPLOYMENT.json')['company_name'] == 'Sulmara'
    with pytest.raises(DemoError, match='interrupted'):
        prepare_company(root, Path('/nonexistent/source'), {})
    pending = complete_snapshot(root)
    assert tool.recover(root)['status'] == 'recovery_dry_run'
    assert complete_snapshot(root) == pending
    with pytest.raises(tool.Refusal, match='service-stopped'):
        tool.recover(root, apply=True)
    assert tool.recover(root, apply=True, service_stopped=True)['status'] == 'recovered_original_identity'
    assert tool.inventory(root) == before and not (root / tool.PENDING).exists()


def test_recovery_refuses_external_edit_and_retains_evidence(installation, monkeypatch):
    root, _ = installation
    interrupt_after_hub(installation, monkeypatch)
    hub = tool.read_json(root / 'project/hub.json')
    hub['defaults']['vessel'] = 'External operator edit'
    dump(root / 'project/hub.json', hub)
    before = complete_snapshot(root)
    with pytest.raises(tool.Refusal, match='edited after interruption'):
        tool.recover(root, apply=True, service_stopped=True)
    assert complete_snapshot(root) == before


def test_recovery_refuses_damaged_backup(installation, monkeypatch):
    root, _ = installation
    interrupt_after_hub(installation, monkeypatch)
    journal = tool.read_json(root / tool.PENDING)
    (Path(journal['backup']) / 'company/project/originals/signed.pdf').write_bytes(b'corrupted backup')
    before = complete_snapshot(root)
    with pytest.raises(tool.Refusal, match='backup has changed'):
        tool.recover(root, apply=True, service_stopped=True)
    assert complete_snapshot(root) == before


def test_links_are_refused_without_touching_target(installation, tmp_path):
    root, _ = installation
    external = tmp_path / 'outside-secret'
    external.write_bytes(b'private unrelated file')
    (root / 'project/link').symlink_to(external)
    with pytest.raises(tool.Refusal, match='links are refused'):
        tool.rename(*arguments(installation), apply=True, service_stopped=True)
    assert external.read_bytes() == b'private unrelated file'
    assert not (root / tool.PENDING).exists()
