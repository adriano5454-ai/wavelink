"""UI117 must replay from exact UI116 and preserve every unrelated runtime resource."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = Path(os.environ['WAVELINK_UI116_TEST_SOURCE'])
SOURCE = Path(os.environ['WAVELINK_UI117_TEST_SOURCE'])
PARENT_MANIFEST = 'a45ff3edb65df12fcb31d64eb2eedc3da135ad89393aa506683be797276106ec'
ADDED = {'app/hr.py','app/hr_api.py','app/static/hr_workspace.js','app/static/hr_workspace.css','tests/test_hr_backup_ui117.py','tests/test_hr_integration_ui117.py','tests/test_hr_ui117.py'}
SHA = lambda data: hashlib.sha256(data).hexdigest()
ALLOWED_CHANGED = {'app/hub_manager.py', 'app/static/action_center_ui82.js', 'app/project_transfer.py', 'docs/user/topics/certificates.html', 'app/static/recognition_workspace.js', 'app/store.py', 'UI_PATCH.json', 'app/project_modules.py', 'app/static/hr_workspace.js', 'docs/user/topics/users.html', 'app/access.py', 'app/static/certificate_workspace.js', 'app/static/index.html', 'app/static/workspace_catalogue.js', 'app/server.py', 'app/hr_api.py', 'app/static/browser_admin.js', 'app/static/help_topics/users.html', 'tests/test_hr_backup_ui117.py', 'app/hr.py', 'app/static/hr_workspace.css', 'app/membership_policy.py', 'app/static/sw.js', 'app/project_module_ui.py', 'app/static/help_catalogue.json', 'tests/test_hr_integration_ui117.py', 'app/action_center.py', 'app/export_policy.py', 'app/static/app.js', 'app/company_roles.py', 'app/static/help_topics/certificates.html', 'tests/test_hr_ui117.py', 'app/email_alerts.py'}



def overlay():
    spec = importlib.util.spec_from_file_location('ui117_overlay', ROOT / 'deploy/apply_ui117.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(path):
    return {p.relative_to(path).as_posix(): SHA(p.read_bytes())
            for p in path.rglob('*') if p.is_file()}


def clone(path):
    shutil.copytree(BASE, path, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache'))


def test_exact_overlay_replay_and_refusal_to_apply_twice(tmp_path):
    path = tmp_path / 'runtime'
    clone(path)
    module = overlay()
    assert SHA((path / 'RELEASE_FILES.json').read_bytes()) == PARENT_MANIFEST
    assert module.PARENT_MANIFEST_SHA256 == PARENT_MANIFEST
    module.apply(path)
    target = json.loads((SOURCE / 'RELEASE_FILES.json').read_text())
    assert (path / 'RELEASE_FILES.json').read_bytes() == (SOURCE / 'RELEASE_FILES.json').read_bytes()
    for name, digest in target['files'].items():
        assert SHA((path / name).read_bytes()) == digest, name
    before = snapshot(path)
    with pytest.raises(ValueError, match='exact UI116'):
        module.apply(path)
    assert snapshot(path) == before


@pytest.mark.parametrize('name', [
    'app/server.py',
    'app/access.py',
    'app/membership_mail.py',
    'app/template_schema.py',
    'app/static/operations.js',
    'RELEASE_FILES.json',
])
def test_modified_parent_refused_before_writes(tmp_path, name):
    path = tmp_path / 'runtime'
    clone(path)
    (path / name).write_text('modified parent')
    before = snapshot(path)
    with pytest.raises(ValueError):
        overlay().apply(path)
    assert snapshot(path) == before


@pytest.mark.parametrize('field,value', [
    ('after', '0' * 64),
    ('bytes', 1),
    ('payload', 'Not valid base64!'),
])
def test_bad_overlay_payload_refused_before_writes(tmp_path, field, value):
    path = tmp_path / 'runtime'
    clone(path)
    before = snapshot(path)
    module = overlay()
    module.FILES = copy.deepcopy(module.FILES)
    module.FILES['app/hr.py'][field] = value
    with pytest.raises(ValueError):
        module.apply(path)
    assert snapshot(path) == before


def test_runtime_delta_and_all_unrelated_boundaries_are_preserved():
    parent = json.loads((BASE / 'RELEASE_FILES.json').read_text())
    target = json.loads((SOURCE / 'RELEASE_FILES.json').read_text())
    module = overlay()
    delta = {name for name, digest in target['files'].items()
             if parent['files'].get(name) != digest}
    added = set(target['files']) - set(parent['files'])
    assert added == ADDED
    assert delta == ALLOWED_CHANGED
    assert delta == set(module.FILES)
    assert set(parent['files']) <= set(target['files'])
    for name, digest in target['files'].items():
        assert SHA((SOURCE / name).read_bytes()) == digest, name
        if name not in delta:
            assert digest == parent['files'][name], name
            assert (SOURCE / name).read_bytes() == (BASE / name).read_bytes(), name
    # The strict delta allow-list protects retained inventory/import, account
    # credentials, schemas, artwork and operational writers while allowing HR integration.
    assert not any(name in delta for name in ('app/accounts.py','app/inventory.py','app/document_import.py','app/document_extract.py','app/template_schema.py'))
    assert not any(Path(name).suffix.lower() in
                   ('.svg', '.png', '.webp', '.ico', '.jpg', '.jpeg', '.gif') for name in delta)


def test_deployment_assets_and_chain_order_are_complete():
    html = (SOURCE / 'app/static/index.html').read_text()
    worker = (SOURCE / 'app/static/sw.js').read_text()
    for asset in ('hr_workspace.js','hr_workspace.css','app.js','recognition_workspace.js','workspace_catalogue.js','action_center_ui82.js','browser_admin.js','certificate_workspace.js'):
        url = '/static/' + asset + '?v=1.34.19-ui117'
        assert url in html and url in worker
        assert '?v=1.34.19-ui116' not in next(
            line for line in html.splitlines() if '/static/' + asset in line)
    assert '/static/document_import.js?v=1.34.19-ui116' in html and '/static/document_import.css?v=1.34.19-ui116' in html
    assert "const CACHE='pxgeo-dive-check-shell-1.34.19-ui117'" in worker
    docker = (ROOT / 'Dockerfile').read_text()
    assert docker.count('&& python apply_ui117.py /opt/wavelink/app') == 1
    assert docker.index('&& python apply_ui116.py') < docker.index('&& python apply_ui117.py')
    assert docker.index('&& python apply_ui117.py') < docker.index('&& rm vendor/source.part*')
    assert 'deploy/apply_ui117.py' in next(line for line in docker.splitlines()
                                        if line.startswith('COPY deploy/extract_source.py'))


@pytest.mark.parametrize('collision', ['file', 'symlink'])
def test_new_resource_collision_refused_before_any_writes(tmp_path, collision):
    path = tmp_path / 'runtime'
    clone(path)
    module = overlay()
    name = next(name for name, record in module.FILES.items() if record['before'] is None)
    p = path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if collision == 'symlink':
        p.symlink_to(path / 'nonexistent-local-resource')
    else:
        p.write_bytes(b'Existing local resource')
    before = snapshot(path)
    with pytest.raises(ValueError, match='new resource already exists'):
        module.apply(path)
    assert snapshot(path) == before
    if collision == 'symlink':
        assert p.is_symlink()
        assert p.readlink() == path / 'nonexistent-local-resource'
