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
