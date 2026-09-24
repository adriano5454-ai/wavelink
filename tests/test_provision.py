from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import pytest
from deploy.provision import prepare, DemoError, ADMIN_LOGIN
from deploy.entrypoint import minimal_environment, mounted

SOURCE=Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
ROOT=Path(__file__).resolve().parents[1]
ENV={'PUBLIC_URL':'https://demo.example.test','DEMO_ACCESS_PASSWORD':'Fictional-invitation-password-2026',
     'INITIAL_ADMIN_PASSWORD':'Fictional-administrator-password-2026','INITIALISE_FICTIONAL_DEMO':'YES_FIRST_DEPLOY_ONLY'}

@pytest.fixture
def initialized(tmp_path):
    root=tmp_path/'demo'
    cfg=prepare(root,SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',ENV)
    return root,cfg

def test_seed_once_identity_and_disabled_samples(initialized):
    root,cfg=initialized
    with closing(sqlite3.connect(root/'project/dives.sqlite3')) as c:
        users=c.execute('SELECT login_id,enabled FROM users').fetchall()
        assert [row for row in users if row[1]]==[(ADMIN_LOGIN,1)]
    first=(root/'project/dives.sqlite3').read_bytes()
    cfg2=prepare(root,SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',{**ENV,'INITIALISE_FICTIONAL_DEMO':'NO','INITIAL_ADMIN_PASSWORD':'ignored now'})
    assert cfg2['hub_id']==cfg['hub_id']
    assert first==(root/'project/dives.sqlite3').read_bytes()

def test_first_deploy_permission_required(tmp_path):
    with pytest.raises(DemoError,match='authorisation'):
        prepare(tmp_path/'demo',SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',{**ENV,'INITIALISE_FICTIONAL_DEMO':'NO'})

def test_unknown_directory_not_overwritten(tmp_path):
    root=tmp_path/'demo';root.mkdir();(root/'important.txt').write_text('KEEP')
    with pytest.raises(DemoError,match='unknown'):
        prepare(root,SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',ENV)
    assert (root/'important.txt').read_text()=='KEEP'

def test_lost_database_never_reseeded(initialized):
    root,cfg=initialized
    (root/'project/dives.sqlite3').unlink()
    from app.hosted_config import HostedError
    with pytest.raises(HostedError):prepare(root,SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',ENV)
    assert not (root/'project/dives.sqlite3').exists()

def test_lost_signing_key_fails(initialized):
    root,cfg=initialized
    cfg['gate_key'].unlink()
    with pytest.raises(DemoError,match='key'):
        prepare(root,SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',ENV)

def test_distinct_projects_unique_identity(tmp_path):
    a=prepare(tmp_path/'a',SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',ENV)
    b=prepare(tmp_path/'b',SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',ENV)
    assert a['hub_id']!=b['hub_id']
    assert a['gate_key'].read_bytes()!=b['gate_key'].read_bytes()

def test_tampered_seed_rejected(tmp_path):
    bad=tmp_path/'wrong.ajproject';bad.write_bytes(b'wrong')
    with pytest.raises(DemoError,match='checksum'):prepare(tmp_path/'demo',SOURCE,bad,ENV)

@pytest.mark.parametrize('value',['','short',' '+ 'x'*30,'x'*129])
def test_weak_gate_secret_rejected(tmp_path,value):
    with pytest.raises(DemoError,match='secret'):prepare(tmp_path/'demo',SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',{**ENV,'DEMO_ACCESS_PASSWORD':value})

def test_same_passwords_rejected(tmp_path):
    with pytest.raises(DemoError,match='different'):prepare(tmp_path/'demo',SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',{**ENV,'INITIAL_ADMIN_PASSWORD':ENV['DEMO_ACCESS_PASSWORD']})

def test_public_url_fallback(initialized):
    root,cfg=initialized
    env={k:v for k,v in ENV.items() if k!='PUBLIC_URL'};env['RENDER_EXTERNAL_URL']='https://candidate.onrender.com'
    cfg=prepare(root,SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',env)
    assert cfg['origin']=='https://candidate.onrender.com'

def test_secrets_not_in_generated_configuration(initialized):
    root,cfg=initialized
    for file in (root/'DEPLOYMENT.json',cfg['config'],root/'project/hub.json'):
        assert ENV['INITIAL_ADMIN_PASSWORD'] not in file.read_text()
        assert ENV['DEMO_ACCESS_PASSWORD'] not in file.read_text()

def test_clean_child_env_does_not_leak_credentials(monkeypatch):
    monkeypatch.setenv('INITIAL_ADMIN_PASSWORD','SECRET')
    monkeypatch.setenv('DEMO_ACCESS_PASSWORD','SECRET')
    monkeypatch.setenv('WEB_CONCURRENCY','8')
    env=minimal_environment()
    assert 'INITIAL_ADMIN_PASSWORD' not in env and 'DEMO_ACCESS_PASSWORD' not in env and 'WEB_CONCURRENCY' not in env

def test_ephemeral_directory_is_not_mount(tmp_path):
    assert not mounted(tmp_path)
