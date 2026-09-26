"""Disposable C01 installation/entry tests. No real company data or credentials."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import copy
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import uuid
import pytest
from fastapi.testclient import TestClient

from deploy.company_provision import prepare_company, read_marker, ACTIVATION, verify_activation
from deploy.company_runtime import create_company_app, ActivationService, SetupError
from deploy.company_nginx import render_company
from deploy.provision import DemoError
from app.hosted_config import HostedSettings, HostedError
from app.hosted_storage import PreparedProject
from app.accounts import password_matches
from app.store import Problem

SOURCE=Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
ENV=dict(COMPANY_ID='fictional-company',COMPANY_NAME='Fictional Company',PUBLIC_URL='https://company.example.test',
         INITIALISE_COMPANY='YES_FIRST_DEPLOY_ONLY',COMPANY_ADMIN_LOGIN='admin',COMPANY_INITIAL_PASSWORD='init12',
         COMPANY_SETUP_KEY='Fictional-only-setup-key-abcdef0123456789')
PASS='Fictional permanent passphrase 654.'

@pytest.fixture
def instance(tmp_path):
    root=tmp_path/'company'
    cfg=prepare_company(root,SOURCE,ENV)
    settings=HostedSettings.from_file(cfg['config'],environ={})
    return root,cfg,settings


def headers(s):
    return {'Host':s.authority,'X-Forwarded-Proto':'https','X-Forwarded-For':'192.0.2.15','Origin':s.external_origin}


def client(instance):
    root,cfg,s=instance
    return TestClient(create_company_app(s,root),base_url=s.external_origin,headers=headers(s),client=('127.0.0.1',1234))


def body():
    return dict(request_id=str(uuid.uuid4()),login_id='admin',temporary_password=ENV['COMPANY_INITIAL_PASSWORD'],
                new_password=PASS,confirm_password=PASS)


def service(instance):
    root,cfg,s=instance
    return ActivationService(PreparedProject(s),read_marker(root))


def activate(c):
    r=c.post('/company-setup/activate',json=body(),headers={'Authorization':'Bearer '+ENV['COMPANY_SETUP_KEY']})
    assert r.status_code==200,r.text


def login(c,password=PASS):
    r=c.post('/api/login',json={'login_id':'admin','password':password,'device_id':'test-company-device'})
    assert r.status_code==200,r.text
    return r.json()['token']


def test_fresh_company_is_empty_not_demo(instance):
    root,cfg,s=instance
    with closing(PreparedProject(s).connect(readonly=True)) as con:
        users=con.execute('SELECT * FROM users').fetchall()
        assert len(users)==1 and users[0]['login_id']==users[0]['name']=='admin' and users[0]['role']=='admin'
        assert password_matches(ENV['COMPANY_INITIAL_PASSWORD'],users[0]['password_hash'])
        for t in ('records','inventory_items','toolbox_talks','handover_records','maintenance_jobs','document_invites','document_signatures','original_documents','sessions'):
            assert con.execute('SELECT count(*) FROM '+t).fetchone()[0]==0,t
        assert con.execute('SELECT state FROM checklist_original_lifecycle').fetchone()[0]=='purged'
        assert con.execute('SELECT count(*) FROM checklist_revisions_v2').fetchone()[0]==0
    hub=json.loads((root/'project/hub.json').read_text())
    assert hub['project_name']==ENV['COMPANY_NAME'] and hub['allow_legacy_codes'] is False
    assert hub['defaults']['vessel']=='' and hub['defaults']['company']==ENV['COMPANY_NAME']
    for path in (root/'COMPANY_DEPLOYMENT.json',root/'project/hub.json',cfg['config']):
        assert ENV['COMPANY_INITIAL_PASSWORD'] not in path.read_text()
        assert ENV['COMPANY_SETUP_KEY'] not in path.read_text()


def test_repeat_preparation_does_not_reset_or_reseed(instance):
    root,cfg,s=instance
    original=(root/'project/dives.sqlite3').read_bytes()
    env={k:v for k,v in ENV.items() if k not in ('COMPANY_INITIAL_PASSWORD','COMPANY_SETUP_KEY')}
    result=prepare_company(root,SOURCE,{**env,'INITIALISE_COMPANY':'NO'})
    assert result['hub_id']==cfg['hub_id'] and not result['active']
    assert (root/'project/dives.sqlite3').read_bytes()==original


@pytest.mark.parametrize('key,value',[
 ('DEMO_PUBLIC_ENTRY','YES'),('INITIALISE_FICTIONAL_DEMO','YES_FIRST_DEPLOY_ONLY'),('DEMO_GUEST_LOGIN','guest.demo'),
 ('DEMO_GUEST_PASSWORD','not-used'),('DEMO_ACCESS_PASSWORD','not-used'),('INITIAL_ADMIN_PASSWORD','not-used'),
 ('COMPANY_ID','../demo'),('COMPANY_ID',''),('COMPANY_NAME',' bad '),('PUBLIC_URL','http://company.example.test'),
 ('PUBLIC_URL','https://demo.mywavelink.com'),('INITIALISE_COMPANY','YES'),('COMPANY_SETUP_KEY','short'),
 ('COMPANY_SETUP_KEY','x'*20),('COMPANY_INITIAL_PASSWORD','abc'),('COMPANY_ADMIN_LOGIN','!'),
])
def test_invalid_or_demo_settings_refused_before_project_creation(tmp_path,key,value):
    root=tmp_path/'company'
    with pytest.raises((DemoError,HostedError,Problem)):
        prepare_company(root,SOURCE,{**ENV,key:value})
    assert not (root/'project/dives.sqlite3').exists()


def test_unknown_data_not_overwritten(tmp_path):
    root=tmp_path/'unknown';root.mkdir();(root/'keep').write_text('precious')
    with pytest.raises(DemoError,match='Unknown'):prepare_company(root,SOURCE,ENV)
    assert (root/'keep').read_text()=='precious' and not (root/'project').exists()


def test_explicit_initialize_required(tmp_path):
    with pytest.raises(DemoError,match='authorization'):
        prepare_company(tmp_path/'new',SOURCE,{**ENV,'INITIALISE_COMPANY':'NO'})


def test_lost_database_not_replaced(instance):
    root,cfg,s=instance
    (root/'project/dives.sqlite3').unlink()
    with pytest.raises(HostedError):prepare_company(root,SOURCE,ENV)
    assert not (root/'project/dives.sqlite3').exists()


def test_symlink_refused(tmp_path):
    actual=tmp_path/'actual';actual.mkdir();linked=tmp_path/'linked';linked.symlink_to(actual,target_is_directory=True)
    with pytest.raises(DemoError):prepare_company(linked,SOURCE,ENV)
    assert list(actual.iterdir())==[]


@pytest.mark.parametrize('field', ['COMPANY_ID','COMPANY_NAME'])
def test_wrong_company_cannot_adopt_existing_disk(instance,field):
    root,cfg,s=instance
    with pytest.raises(DemoError,match='match'):prepare_company(root,SOURCE,{**ENV,field:'other-company'})
    assert read_marker(root)['hub_id']==cfg['hub_id']


@pytest.mark.parametrize('path,method', [('/api/login','POST'),('/api/records','GET'),('/api/me','GET'),('/api/info','GET'),
 ('/api/document-sign/info','POST'),('/sign','GET'),('/api/backup','GET'),('/api/admin/users','GET'),('/static/app.js','GET')])
def test_pending_workspace_is_closed(instance,path,method):
    with client(instance) as c:
        r=c.request(method,path,json={'login_id':'admin','password':ENV['COMPANY_INITIAL_PASSWORD'],'device_id':'test-device'} if method=='POST' else None)
        assert r.status_code==423,r.text


def test_pending_front_page_and_no_secret_in_html(instance):
    with client(instance) as c:
        for path in ('/','/company-setup','/company-setup/setup.js','/company-setup/setup.css','/company-setup/icon.svg'):
            r=c.get(path);assert r.status_code==200
            assert ENV['COMPANY_SETUP_KEY'] not in r.text and ENV['COMPANY_INITIAL_PASSWORD'] not in r.text
            assert r.headers['cache-control']=='no-store'
        assert 'First sign-in pending' in c.get('/').text


@pytest.mark.parametrize('field,value,status', [('login_id','someone',403),('temporary_password','wrong',403),
 ('new_password','short',422),('confirm_password','not the same',422),('request_id','invalid',422)])
def test_setup_validates_before_mutation(instance,field,value,status):
    data=body();data[field]=value
    with client(instance) as c:
        r=c.post('/company-setup/activate',json=data,headers={'Authorization':'Bearer '+ENV['COMPANY_SETUP_KEY']})
        assert r.status_code==status,r.text
        assert c.get('/api/records').status_code==423
    assert not service(instance).status()


def test_setup_requires_separate_private_key_and_exact_origin(instance):
    with client(instance) as c:
        for key in ('', 'wrong'*10):
            assert c.post('/company-setup/activate',json=body(),headers={'Authorization':'Bearer '+key}).status_code==403
        h={'Authorization':'Bearer '+ENV['COMPANY_SETUP_KEY'],'Origin':'https://other.example.test'}
        assert c.post('/company-setup/activate',json=body(),headers=h).status_code==403
        h={'Authorization':'Bearer '+ENV['COMPANY_SETUP_KEY'],'Origin':''}
        assert c.post('/company-setup/activate',json=body(),headers=h).status_code==403


def test_setup_body_limit_content_type_and_duplicates(instance):
    with client(instance) as c:
        h={'Authorization':'Bearer '+ENV['COMPANY_SETUP_KEY'],'Content-Type':'application/json'}
        assert c.post('/company-setup/activate',content='x'*4100,headers=h).status_code==413
        assert c.post('/company-setup/activate',content='{"login_id":"a","login_id":"b"}',headers=h).status_code==422
        assert c.post('/company-setup/activate',content='{}',headers={**h,'Content-Type':'text/plain'}).status_code==415


def test_first_signin_retries_idempotently_no_normal_token(instance):
    data=body()
    with client(instance) as c:
        h={'Authorization':'Bearer '+ENV['COMPANY_SETUP_KEY']}
        result=c.post('/company-setup/activate',json=data,headers=h)
        assert result.status_code==200 and set(result.json())=={'completed','sign_in_required'}
        assert c.post('/company-setup/activate',json=data,headers=h).json()==result.json()
        assert c.post('/company-setup/activate',json=body(),headers=h).status_code==409
        assert c.post('/company-setup/outcome',json={'request_id':data['request_id']},headers=h).json()['completed']
        assert not c.post('/company-setup/outcome',json={'request_id':str(uuid.uuid4())},headers=h).json()['completed']
        assert c.get('/api/me').status_code==401
        assert c.post('/api/login',json={'login_id':'admin','password':ENV['COMPANY_INITIAL_PASSWORD'],'device_id':'test-device'}).status_code==403
        tok=login(c)
        r=c.get('/api/me',headers={'Authorization':'Bearer '+tok})
        assert r.status_code==200 and r.json()['role']=='admin' and r.json()['credential_version']==2
        assert c.get('/api/templates',headers={'Authorization':'Bearer '+tok}).json()==[]
    with closing(PreparedProject(instance[2]).connect(readonly=True)) as con:
        rows=con.execute('SELECT detail FROM user_audit WHERE action=?',(ACTIVATION,)).fetchall()
        assert len(rows)==1 and PASS not in rows[0][0] and ENV['COMPANY_INITIAL_PASSWORD'] not in rows[0][0]


def test_restart_retains_activation_and_never_resets_password(instance):
    svc=service(instance);svc.complete(ENV['COMPANY_SETUP_KEY'],body())
    root,cfg,s=instance
    again=prepare_company(root,SOURCE,{**ENV,'COMPANY_INITIAL_PASSWORD':'different-temp'})
    assert again['active']
    with client(instance) as c:
        assert c.get('/company-setup/status').json()['active']
        tok=login(c);assert c.get('/api/records',headers={'Authorization':'Bearer '+tok}).json()==[]


def test_expired_setup_keeps_company_locked(instance):
    svc=service(instance);svc.clock=lambda:svc.record['setup_expires_epoch']+1
    with pytest.raises(SetupError) as exc:svc.complete(ENV['COMPANY_SETUP_KEY'],body())
    assert exc.value.code==410 and not svc.status()


def test_concurrent_same_request_changes_password_once(instance):
    svc=service(instance);data=body()
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(lambda _:svc.complete(ENV['COMPANY_SETUP_KEY'],data),range(2)))
    assert all(r['completed'] for r in results)
    with closing(PreparedProject(instance[2]).connect(readonly=True)) as con:
        assert con.execute('SELECT count(*) FROM user_audit WHERE action=?',(ACTIVATION,)).fetchone()[0]==1
        assert con.execute('SELECT credential_version FROM users').fetchone()[0]==2


@pytest.mark.parametrize('path', ['/api/template','/api/templates','/api/records','/api/backup','/api/handovers',
 '/api/admin/users','/api/fleet/directory','/api/document-invitations/toolbox/unknown'])
def test_active_ordinary_api_requires_named_session(instance,path):
    service(instance).complete(ENV['COMPANY_SETUP_KEY'],body())
    with client(instance) as c:
        assert c.get(path).status_code==401
        assert c.get(path,headers={'Authorization':'Bearer unknown-token'}).status_code==401


def test_active_public_entry_only_normal_login_and_scoped_signing(instance):
    service(instance).complete(ENV['COMPANY_SETUP_KEY'],body())
    with client(instance) as c:
        r=c.get('/');assert r.status_code==200 and 'static/app.js' in r.text and 'pending' not in r.text.lower()[:100]
        info=c.get('/api/info');assert info.status_code==200 and info.json()['login_mode']=='accounts' and info.json()['defaults']=={}
        assert c.get('/__demo/public').status_code==404
        assert c.get('/__demo/login').status_code==404
        assert c.post('/api/join',json={}).status_code==403
        assert c.get('/sign').status_code==200
        assert c.get('/api/document-sign/document',headers={'Authorization':'Bearer not-a-grant'}).status_code in (401,403)


def test_cross_company_tokens_and_hub_headers_do_not_cross(instance,tmp_path):
    other_root=tmp_path/'other'
    env={**ENV,'COMPANY_ID':'other','COMPANY_NAME':'Other','PUBLIC_URL':'https://other.example.test'}
    cfg=prepare_company(other_root,SOURCE,env);s=HostedSettings.from_file(cfg['config'],environ={});other=(other_root,cfg,s)
    service(instance).complete(ENV['COMPANY_SETUP_KEY'],body());service(other).complete(ENV['COMPANY_SETUP_KEY'],body())
    assert cfg['hub_id']!=instance[1]['hub_id']
    with client(instance) as a, client(other) as b:
        tok=login(a)
        assert b.get('/api/me',headers={'Authorization':'Bearer '+tok}).status_code==401
        own=login(b)
        assert b.get('/api/handovers',headers={'Authorization':'Bearer '+own,'X-AJ-Hub-ID':instance[1]['hub_id']}).status_code==409
        assert b.get('/api/handovers',headers={'Authorization':'Bearer '+own,'X-AJ-Hub-ID':cfg['hub_id']}).status_code==200


def test_host_and_tls_checks_precede_setup(instance):
    with client(instance) as c:
        for h in ({'Host':'evil.example.test'},{'X-Forwarded-Proto':'http'},{'X-Forwarded-For':'192.0.2.2, 192.0.2.3'}):
            assert c.get('/company-setup/status',headers=h).status_code==400


def test_demo_nginx_unchanged_company_has_no_gate(tmp_path):
    text=render_company('company.example.test',19055,tmp_path/'nginx')
    assert 'auth_request' not in text and '8766' not in text and 'sub_filter' in text
    assert 'proxy_pass_request_headers off' in text and 'Authorization $http_authorization' in text
    assert 'client_max_body_size 4k' in text and 'client_max_body_size 100k' in text
    assert 'X-Forwarded-For $remote_addr' in text and 'access_log off' in text


@pytest.mark.parametrize('host',['company.example;bad','*.example.test','a\nother','company.example/path'])
def test_company_nginx_injection_refused(tmp_path,host):
    with pytest.raises(ValueError):render_company(host,19055,tmp_path/'nginx')


def test_explicit_mode_and_original_demo_default(monkeypatch):
    from deploy import entrypoint,company_entrypoint
    monkeypatch.setenv('WAVELINK_DEPLOYMENT_MODE','COMPANY')
    monkeypatch.setattr(company_entrypoint,'run_company',lambda:73)
    assert entrypoint.run()==73
    monkeypatch.setenv('WAVELINK_DEPLOYMENT_MODE','unexpected')
    with pytest.raises(DemoError,match='WAVELINK_DEPLOYMENT_MODE'):entrypoint.run()
    monkeypatch.delenv('WAVELINK_DEPLOYMENT_MODE')
    monkeypatch.setattr(entrypoint,'mounted',lambda p:False)
    with pytest.raises(DemoError,match='persistent disk'):entrypoint.run()


def test_clean_environment_no_company_secrets(monkeypatch):
    from deploy.entrypoint import minimal_environment
    for key in ENV:monkeypatch.setenv(key,ENV[key])
    assert not set(ENV)&set(minimal_environment())


def test_renew_pending_key_without_resetting_accounts(instance):
    root,cfg,s=instance
    before=(root/'project/dives.sqlite3').read_bytes()
    newkey='Different-fictional-setup-key-9876543210'
    prepare_company(root,SOURCE,{**ENV,'INITIALISE_COMPANY':'NO','COMPANY_RENEW_SETUP':'YES','COMPANY_SETUP_KEY':newkey})
    assert before==(root/'project/dives.sqlite3').read_bytes()
    svc=service(instance)
    with pytest.raises(SetupError):svc.complete(ENV['COMPANY_SETUP_KEY'],body())
    assert svc.complete(newkey,body())['completed']
    with pytest.raises(DemoError,match='cannot be renewed'):
        prepare_company(root,SOURCE,{**ENV,'COMPANY_RENEW_SETUP':'YES','COMPANY_SETUP_KEY':'Other-new-fictional-setup-key-abcdef12345'})


def test_renew_refuses_running_project(instance):
    from app.hosted_runtime import project_leases
    root,cfg,s=instance
    with project_leases(s):
        with pytest.raises(ValueError,match='already open'):
            prepare_company(root,SOURCE,{**ENV,'COMPANY_RENEW_SETUP':'YES','COMPANY_SETUP_KEY':'Different-fictional-setup-key-9876543210'})
    assert read_marker(root)['setup_key_sha256']==hashlib.sha256(ENV['COMPANY_SETUP_KEY'].encode()).hexdigest()


def test_corrupt_activation_evidence_never_opens_initial_password(instance):
    svc=service(instance);svc.complete(ENV['COMPANY_SETUP_KEY'],body())
    p=PreparedProject(instance[2])
    with closing(p.connect()) as con:
        con.execute('UPDATE users SET password_hash=?,credential_version=? WHERE id=?',
                    (svc.record['initial_hash'],svc.record['initial_credential_version'],svc.record['admin_id']))
    with pytest.raises(DemoError,match='conflict'):svc.status()
    with client(instance) as c:assert c.get('/api/info').status_code==503


def test_backup_snapshot_with_marker_restores_exact_company_activation(instance,tmp_path):
    import shutil
    svc=service(instance);svc.complete(ENV['COMPANY_SETUP_KEY'],body())
    root,cfg,s=instance
    restore=tmp_path/'restored';(restore/'project').mkdir(parents=True);(restore/'operator').mkdir()
    shutil.copy2(root/'project/hub.json',restore/'project/hub.json')
    shutil.copy2(root/'COMPANY_DEPLOYMENT.json',restore/'COMPANY_DEPLOYMENT.json')
    with closing(PreparedProject(s).connect(readonly=True)) as reader, closing(sqlite3.connect(restore/'project/dives.sqlite3')) as writer:
        reader.backup(writer);writer.execute('DELETE FROM sessions');writer.execute('DELETE FROM participants');writer.commit()
    restored=prepare_company(restore,SOURCE,{**ENV,'INITIALISE_COMPANY':'NO'})
    assert restored['active'] and restored['hub_id']==cfg['hub_id']
    settings=HostedSettings.from_file(restored['config'],environ={})
    with client((restore,restored,settings)) as c:login(c)


def test_company_wrapper_does_not_access_main_browser_storage():
    text=(Path(__file__).resolve().parents[1]/'deploy/company_assets/setup.js').read_text()
    assert not any(term in text for term in ('indexedDB','localStorage','sessionStorage','document.cookie'))
    assert 'history.replaceState' in text and 'Retry unchanged setup' in text


def test_setup_expiry_and_revocation_leave_no_app_session(instance):
    root,cfg,s=instance
    svc=service(instance)
    for _ in range(10):
        with pytest.raises(SetupError):svc.complete('wrong-key'*6,body())
    with pytest.raises(SetupError) as exc:svc.complete(ENV['COMPANY_SETUP_KEY'],body())
    assert exc.value.code==429
    with closing(PreparedProject(s).connect(readonly=True)) as con:
        assert con.execute('SELECT count(*) FROM sessions').fetchone()[0]==0


def test_demo_mode_refuses_company_disk_without_creating_demo_folder(instance,monkeypatch):
    from deploy import entrypoint
    import shutil
    root,cfg,s=instance
    mount=root.parent/'mount';company=mount/'wavelink-company';company.mkdir(parents=True)
    shutil.copy2(root/'COMPANY_DEPLOYMENT.json',company/'COMPANY_DEPLOYMENT.json')
    monkeypatch.setattr(entrypoint,'MOUNT',mount)
    monkeypatch.delenv('WAVELINK_DEPLOYMENT_MODE',raising=False)
    with pytest.raises(DemoError,match='company installation'):entrypoint.run()
    assert not (mount/'wavelink').exists()


def test_new_company_cannot_start_as_a_key_renewal(tmp_path):
    with pytest.raises(DemoError,match='existing pending'):
        prepare_company(tmp_path/'new',SOURCE,{**ENV,'COMPANY_RENEW_SETUP':'YES'})
    assert not (tmp_path/'new/project/dives.sqlite3').exists()
