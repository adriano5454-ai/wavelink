from pathlib import Path
import json
import hashlib
import os
import pytest
from deploy.extract_source import extract_parts, SOURCE_SHA256
from deploy.nginx_config import render

ROOT=Path(__file__).resolve().parents[1]

def test_reassembled_source_is_exact(tmp_path):
    count=extract_parts(ROOT/'vendor/source_parts.json',tmp_path/'source')
    assert count==1605
    source=Path(os.environ['WAVELINK_TEST_SOURCE'])
    manifest=json.loads((source/'RELEASE_FILES.json').read_text())
    assert all((tmp_path/'source'/name).read_bytes()==(source/name).read_bytes() for name in manifest['files'])

def test_parts_are_small_and_hash_checked():
    manifest=json.loads((ROOT/'vendor/source_parts.json').read_text())
    assert len(manifest['parts'])==5 and manifest['archive_sha256']==SOURCE_SHA256
    assert all(p['bytes']<=8*1024*1024 for p in manifest['parts'])

def test_presentation_rules_only_apply_to_application_script(tmp_path):
    cfg=render('demo.example.test',19085,tmp_path/'nginx')
    scripted=cfg.split('location = /static/app.js {',1)[1].split('\n        }',1)[0]
    general=cfg.rsplit('location / {',1)[1]
    assert 'sub_filter ' in scripted
    assert 'sub_filter ' not in general
    assert 'auth_request /_demo_verify' in scripted

def test_forwarded_headers_whitelisted(tmp_path):
    cfg=render('demo.example.test',19085,tmp_path/'nginx')
    assert 'proxy_pass_request_headers off' in cfg
    assert 'proxy_set_header Authorization $http_authorization' in cfg
    assert 'proxy_set_header X-AJ-Hub-ID $http_x_aj_hub_id' in cfg
    assert 'proxy_set_header X-Forwarded-For $remote_addr' in cfg

@pytest.mark.parametrize('bad',['demo.example;bad','demo.example\nother','demo.example/abc','*.example.test'])
def test_gateway_authority_injection_refused(tmp_path,bad):
    with pytest.raises(ValueError):render(bad,19085,tmp_path/'nginx')

def test_no_real_project_or_secret_files_packaged():
    names=[p.name for p in ROOT.rglob('*') if p.is_file()]
    assert 'dives.sqlite3' not in names and 'hub.json' not in names and 'gate.key' not in names


def test_ui70_overlay_parent_and_m01_launcher_are_exact():
    from deploy.extract_source import (
        UI_PATCH_ID,
        UI66_PATCH_ID,
        UI67_PATCH_ID,
        UI68_PATCH_ID,
        UI69_PATCH_ID,
        UI70_PATCH_ID,
        _UI66_FILES,
        _UI67_FILES,
        _UI68_FILES,
        _UI69_FILES,
        _UI70_FILES,
    )
    assert UI_PATCH_ID == 'workspace-ui65-role-ready-invitations-2026-09-29'
    assert UI66_PATCH_ID == 'workspace-ui66-profiles-recognition-2026-09-29'
    assert UI67_PATCH_ID == 'workspace-ui67-experience-foundation-2026-09-30'
    assert UI68_PATCH_ID == 'workspace-ui68-data-grounded-home-profile-2026-09-30'
    assert UI69_PATCH_ID == 'workspace-ui69-work-execution-experience-2026-09-30'
    assert UI70_PATCH_ID == 'workspace-ui70-equipment-logistics-experience-2026-09-30'
    assert len(_UI66_FILES) == 33
    assert len(_UI67_FILES) == 41
    assert len(_UI68_FILES) == 11
    assert len(_UI69_FILES) == 9
    assert len(_UI70_FILES) == 8
    assert len([name for name in _UI67_FILES if name.startswith('app/static/badges/')]) == 30
    assert hashlib.sha256((ROOT/'deploy/company_entrypoint.py').read_bytes()).hexdigest() == '2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371'
    assert (ROOT/'docs/WORKSPACE_UI65.md').is_file()
    assert (ROOT/'docs/UI65_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI66.md').is_file()
    assert (ROOT/'docs/UI66_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI67.md').is_file()
    assert (ROOT/'docs/UI67_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI68.md').is_file()
    assert (ROOT/'docs/UI68_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI69.md').is_file()
    assert (ROOT/'docs/UI69_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI70.md').is_file()
    assert (ROOT/'docs/UI70_SOURCE_PROVENANCE.json').is_file()


def test_ui65_release_keeps_operator_secret_examples_blank():
    values = {}
    for line in (ROOT/'deploy/membership.env.example').read_text().splitlines():
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            values[key] = value
    assert values.get('MEMBERSHIP_SMTP_PASSWORD') == ''
    assert not any((ROOT/name).exists() for name in ('hub.json','gate.key','.env','secrets.json'))
