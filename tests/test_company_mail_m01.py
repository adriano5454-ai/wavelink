"""M01 process-boundary regressions. Fictional mail only; no network or live data.

Run from the upload repository with the extracted current UI89 runtime on PYTHONPATH:
  WAVELINK_TEST_SOURCE=/path/to/runtime python -m pytest -q tests/test_company_mail_m01.py
The UI89 runtime must retain the supplied M01 launcher contract. No SMTP credentials are needed.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import signal
import shutil
import subprocess
import sys
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from deploy import company_entrypoint as ce, entrypoint as entry
from deploy.provision import DemoError
from app.membership_mail import MembershipSettings, SMTPMembershipMailer

SOURCE = Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
SMTP_KEYS = ('MEMBERSHIP_SMTP_HOST', 'MEMBERSHIP_SMTP_PORT', 'MEMBERSHIP_SMTP_TLS',
             'MEMBERSHIP_SMTP_USERNAME', 'MEMBERSHIP_SMTP_PASSWORD', 'MEMBERSHIP_SMTP_FROM')
FAKE_ENV = dict(WAVELINK_DEPLOYMENT_MODE='COMPANY', COMPANY_ID='fictional-company',
               COMPANY_NAME='Fictional Company', PUBLIC_URL='https://company.example.test/',
               WAVELINK_MEMBERSHIP_MODE='INVITE_ONLY', MEMBERSHIP_SMTP_HOST='smtp.example.test',
               MEMBERSHIP_SMTP_PORT='465', MEMBERSHIP_SMTP_TLS='SSL',
               MEMBERSHIP_SMTP_USERNAME='sender@example.test',
               MEMBERSHIP_SMTP_PASSWORD='Fictional-only #=credential with spaces.',
               MEMBERSHIP_SMTP_FROM='sender@example.test')
ORIGIN = 'https://company.example.test'


def child_env(source=None):
    return ce.company_application_environment(dict(FAKE_ENV if source is None else source), origin=ORIGIN)


def parsed(env):
    with patch.dict(os.environ, env, clear=True):
        return MembershipSettings.from_environment()


def test_exact_allowlist_and_validated_origin():
    source = {**FAKE_ENV, 'EXTRA_PRIVATE_SETTING': 'never-pass', 'COMPANY_SETUP_KEY': 'never-pass',
              'COMPANY_INITIAL_PASSWORD': 'never-pass', 'DEMO_ACCESS_PASSWORD': 'never-pass',
              'DEMO_GUEST_PASSWORD': 'never-pass', 'MEMBERSHIP_SMTP_DEBUG': 'never-pass',
              'PYTHONPATH': 'untrusted-operator-path', 'LD_PRELOAD': 'never-pass'}
    env = child_env(source)
    assert set(env) == set(entry.minimal_environment()) | set(SMTP_KEYS) | {
        'PYTHONPATH', 'WAVELINK_DEPLOYMENT_MODE', 'WAVELINK_MEMBERSHIP_MODE',
        'COMPANY_ID', 'COMPANY_NAME', 'PUBLIC_URL'}
    assert env['PUBLIC_URL'] == ORIGIN and env['PUBLIC_URL'] != source['PUBLIC_URL']
    assert env['PYTHONPATH'] == str(ce.BASE/'app')
    assert env['MEMBERSHIP_SMTP_PASSWORD'] == FAKE_ENV['MEMBERSHIP_SMTP_PASSWORD']
    s = parsed(env)
    assert s.enabled and not s.configuration_error and SMTPMembershipMailer(s).ready
    assert s.smtp_password not in repr(s)
    assert source['PUBLIC_URL'].endswith('/')  # Source mapping not modified.


@pytest.mark.parametrize('mode', [None, 'OFF', 'YES', 'invite_only', 'INVITE_ONLY '])
def test_off_or_invalid_mode_never_enables_or_forwards_credentials(mode):
    source = dict(FAKE_ENV)
    if mode is None:
        source.pop('WAVELINK_MEMBERSHIP_MODE')
    else:
        source['WAVELINK_MEMBERSHIP_MODE'] = mode
    env = child_env(source)
    assert not set(SMTP_KEYS) & set(env)
    s = parsed(env)
    assert not s.enabled and not SMTPMembershipMailer(s).ready
    assert s.configuration_error == (mode not in (None, 'OFF'))


@pytest.mark.parametrize('mode', [None, 'DEMO', 'company', 'OTHER'])
def test_company_helper_cannot_enable_demo_or_unknown_mode(mode):
    source = dict(FAKE_ENV)
    if mode is None:
        source.pop('WAVELINK_DEPLOYMENT_MODE')
    else:
        source['WAVELINK_DEPLOYMENT_MODE'] = mode
    with pytest.raises(DemoError, match='COMPANY mode'):
        child_env(source)


@pytest.mark.parametrize('key', ['MEMBERSHIP_SMTP_HOST', 'MEMBERSHIP_SMTP_USERNAME',
                                 'MEMBERSHIP_SMTP_PASSWORD', 'MEMBERSHIP_SMTP_FROM'])
def test_incomplete_mail_configuration_fails_closed(key):
    source = dict(FAKE_ENV); source.pop(key)
    s = parsed(child_env(source))
    assert not s.enabled and s.configuration_error


@pytest.mark.parametrize('key,value', [('MEMBERSHIP_SMTP_PORT','not-a-port'),
                                      ('MEMBERSHIP_SMTP_PORT','0'),
                                      ('MEMBERSHIP_SMTP_TLS','PLAIN'),
                                      ('MEMBERSHIP_SMTP_FROM','invalid\r\n@example.test')])
def test_invalid_mail_configuration_is_not_normalised_into_authority(key, value):
    source = dict(FAKE_ENV); source[key] = value
    s = parsed(child_env(source))
    assert not s.enabled and s.configuration_error


@pytest.mark.parametrize('mode,port', [('SSL', '465'), ('STARTTLS', '587')])
def test_supported_tls_pairs_pass_through_unchanged(mode, port):
    s = parsed(child_env({**FAKE_ENV, 'MEMBERSHIP_SMTP_TLS': mode, 'MEMBERSHIP_SMTP_PORT': port}))
    assert s.enabled and s.tls_mode == mode and s.smtp_port == int(port)


def test_minimal_proxy_and_demo_environment_stays_clean(monkeypatch):
    for k,v in FAKE_ENV.items():
        monkeypatch.setenv(k,v)
    env = entry.minimal_environment()
    assert not set(SMTP_KEYS) & set(env)
    assert 'WAVELINK_MEMBERSHIP_MODE' not in env and 'COMPANY_ID' not in env
    assert not parsed(env).enabled


# This runs in a genuinely fresh Python process with ONLY the supervisor's env.
# No in-process mutation of MembershipSettings and no overriding mailer.ready.
PROBE = r'''
import json, os, sys
from app.membership_mail import MembershipSettings, SMTPMembershipMailer
s = MembershipSettings.from_environment()
assert not any(x in os.environ for x in (
 'COMPANY_SETUP_KEY','COMPANY_INITIAL_PASSWORD','DEMO_ACCESS_PASSWORD',
 'DEMO_GUEST_PASSWORD','EXTRA_PRIVATE_SETTING','LD_PRELOAD'))
assert s.smtp_password not in repr(s) if s.smtp_password else True
print(json.dumps({'enabled':s.enabled, 'configuration_error':s.configuration_error,
 'ready':SMTPMembershipMailer(s).ready,
 'has_password':bool(s.smtp_password), 'company_id':s.company_id,
 'smtp_keys_present':sorted(k for k in os.environ if k.startswith('MEMBERSHIP_SMTP_')),
 'origin':s.origin}))
'''


def launch_under_supervisor(tmp_path, monkeypatch, source):
    base = tmp_path/'container'; base.mkdir()
    (base/'app').symlink_to(SOURCE, target_is_directory=True)
    mount = tmp_path/'disk'; mount.mkdir()
    data = mount/'wavelink-company'
    gateway = tmp_path/'gateway'
    real_path = Path
    def scoped_path(p):
        return gateway if str(p) == '/tmp/wavelink-company-gateway' else real_path(p)
    monkeypatch.setattr(ce, 'BASE', base)
    monkeypatch.setattr(ce, 'MOUNT', mount)
    monkeypatch.setattr(ce, 'DATA', data)
    monkeypatch.setattr(ce, 'Path', scoped_path)
    monkeypatch.setattr(ce.os, 'geteuid', lambda:10001)
    monkeypatch.setattr(ce.os, 'umask', lambda _:0o077)
    monkeypatch.setattr(entry, 'mounted', lambda p: p == mount)
    monkeypatch.setattr(ce, 'prepare_company', lambda *a,**k: dict(
        authority='company.example.test', origin=ORIGIN, config=data/'operator/hosted.json'))
    callbacks = {}; nginx_envs = []; observations = []
    monkeypatch.setattr(ce.signal, 'signal', lambda sig,cb: callbacks.setdefault(sig,cb))
    def nginx_check(command, **kw):
        assert command[:2] == ['nginx','-t']
        nginx_envs.append(kw['env'])
        return SimpleNamespace(returncode=0, stderr='')
    original_popen = subprocess.Popen
    class FinishedProbe:
        def __init__(self): self.stopped=False
        def poll(self): return 0 if self.stopped else None
        def terminate(self): self.stopped=True
        def wait(self, **kw): self.stopped=True; return 0
    def start(command, **kw):
        if command[0] == 'nginx':
            nginx_envs.append(kw['env'])
            callbacks[signal.SIGTERM](signal.SIGTERM,None)
        else:
            assert command[:3] == [sys.executable,'-m','deploy.company_runtime']
            p=original_popen([sys.executable,'-c',PROBE],env=kw['env'],cwd=kw['cwd'],
                             stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            out,err=p.communicate(timeout=25)
            assert p.returncode == 0, err
            observations.append(json.loads(out.strip().splitlines()[-1]))
        return FinishedProbe()
    monkeypatch.setattr(ce.subprocess,'run',nginx_check)
    monkeypatch.setattr(ce.subprocess,'Popen',start)
    monkeypatch.setattr(entry,'wait_ready',lambda *a,**kw: None)
    with patch.dict(os.environ, {**source, 'COMPANY_SETUP_KEY':'fictional-not-forwarded',
                                'EXTRA_PRIVATE_SETTING':'fictional-not-forwarded'}, clear=True):
        assert ce.run_company()==0
    assert len(nginx_envs)==2
    for env in nginx_envs:
        assert not set(SMTP_KEYS) & set(env)
        assert 'WAVELINK_MEMBERSHIP_MODE' not in env
        assert 'COMPANY_SETUP_KEY' not in env
    assert len(observations)==1
    return observations[0]


@pytest.mark.parametrize('mode,expected', [('INVITE_ONLY',True), ('OFF',False), ('YES',False)])
def test_actual_supervisor_launches_child_with_intended_settings(tmp_path,monkeypatch,mode,expected):
    result=launch_under_supervisor(tmp_path,monkeypatch,{**FAKE_ENV,'WAVELINK_MEMBERSHIP_MODE':mode})
    assert result['enabled'] is expected and result['ready'] is expected
    assert result['has_password'] is expected
    if expected:
        assert result['company_id']=='fictional-company' and result['origin']==ORIGIN
        assert result['smtp_keys_present']==sorted(SMTP_KEYS)
    else:
        assert not result['smtp_keys_present']


# Same released C01 ASGI app and account services, settings obtained solely from
# the corrected child environment. Transport stub only: no real email is sent.
HOSTED_PROBE = r'''
import json,os,re,sys,uuid
from pathlib import Path
from fastapi.testclient import TestClient
from deploy.company_provision import prepare_company, read_marker
from deploy.company_runtime import create_company_app
from app.hosted_config import HostedSettings
import app.membership_mail as mm
from app.membership_mail import MembershipSettings

root=Path(sys.argv[1]);source=Path(sys.argv[2]);mode=sys.argv[3]
assert MembershipSettings.from_environment().enabled == (mode=='INVITE_ONLY')
setup={**os.environ,'INITIALISE_COMPANY':'YES_FIRST_DEPLOY_ONLY',
 'COMPANY_ADMIN_LOGIN':'admin','COMPANY_INITIAL_PASSWORD':'test-initial-only',
 'COMPANY_SETUP_KEY':'Fictional-M01-test-only-setup-key-0123456789'}
pw='Fictional M01 permanent passphrase 789.'
messages=[]
class SMTP:
 def __init__(self,host,port,**kw):
  assert host=='smtp.example.test' and port==465 and kw['context'].check_hostname
 def __enter__(self): return self
 def __exit__(self,*a): pass
 def ehlo(self): pass
 def login(self,u,p):
  assert u==os.environ['MEMBERSHIP_SMTP_USERNAME'] and p==os.environ['MEMBERSHIP_SMTP_PASSWORD']
 def send_message(self,msg): messages.append(msg); return {}
mm.smtplib.SMTP_SSL=SMTP
cfg=prepare_company(root,source,setup)
settings=HostedSettings.from_file(cfg['config'],environ={})
app=create_company_app(settings,root)
h={'Host':settings.authority,'X-Forwarded-Proto':'https','X-Forwarded-For':'192.0.2.17','Origin':settings.external_origin}
results={}
with TestClient(app,base_url=settings.external_origin,headers=h,client=('127.0.0.1',1234)) as client:
 assert not app.state.core.state.company_membership.settings.enabled == (mode!='INVITE_ONLY')
 assert client.get('/join-team').status_code==423
 r=client.post('/company-setup/activate',headers={'Authorization':'Bearer '+setup['COMPANY_SETUP_KEY']},
  json=dict(request_id=str(uuid.uuid4()),login_id='admin',temporary_password=setup['COMPANY_INITIAL_PASSWORD'],
            new_password=pw,confirm_password=pw)); assert r.status_code==200,r.text
 token=client.post('/api/login',json=dict(login_id='admin',password=pw,device_id='fictional-m01-admin')).json()['token']
 auth={'Authorization':'Bearer '+token,'X-AJ-Hub-ID':settings.expected_hub_id}
 ctx=client.get('/api/memberships/context',headers=auth);assert ctx.status_code==200,ctx.text
 assert os.environ.get('MEMBERSHIP_SMTP_PASSWORD','UNUSED_SENTINEL') not in ctx.text
 c=ctx.json();results['old_admin_allowed']=True;results['context']=c['email_delivery']
 assert c['email_delivery']==('configured_not_delivery_tested' if mode=='INVITE_ONLY' else 'off')
 request=dict(action='invite',data=dict(op_id=str(uuid.uuid4()),email='recipient@example.test',department_id=''))
 r=client.post('/api/memberships/action',headers=auth,json=request)
 if mode=='OFF':
  assert r.status_code==503 and not messages
  results['off_invite_refused']=True
 else:
  assert r.status_code==200,r.text;assert len(messages)==1
  assert client.post('/api/memberships/action',headers=auth,json=request).status_code==200
  assert len(messages)==1
  invite=re.search(r'#invite=([A-Za-z0-9_-]+)',messages[-1].get_content())[1]
  ih={'Authorization':'Bearer '+invite}
  r=client.post('/api/membership-entry/code',headers=ih,json={'email':'recipient@example.test'});assert r.status_code==200,r.text
  code=re.search(r'\b\d{8}\b',messages[-1].get_content())[0]
  p=dict(op_id=str(uuid.uuid4()),email='recipient@example.test',challenge=r.json()['challenge'],code=code,
         name='Fictional Pending Member',login_id='fictional.pending',password=pw)
  r=client.post('/api/membership-entry/accept',headers=ih,json=p);assert r.status_code==200,r.text
  assert client.post('/api/login',json=dict(login_id='fictional.pending',password=pw,device_id='fake-pending')).status_code==423
  r=client.post('/api/membership-entry/login',json={'login':'fictional.pending','password':pw});assert r.status_code==200,r.text
  st=r.json()['status_token']; sh={'Authorization':'Bearer '+st,'X-AJ-Hub-ID':settings.expected_hub_id}
  own=client.get('/api/membership-entry/status',headers=sh); assert own.status_code==200 and not own.json()['operational_access']
  for path in ('/api/records','/api/home/personal','/api/fleet/sites','/api/original-documents','/api/memberships/context'):
   assert client.get(path,headers=sh).status_code in (401,403,423),path
  results.update(invite_submitted_to_stub=True,exact_retry_no_second_mail=True,verification_code_stub=True,pending_isolated=True)
 assert client.post('/api/login',json=dict(login_id='admin',password=pw,device_id='m01-admin-again')).status_code==200
 results['old_admin_still_signs_in']=True
for p in (root/'COMPANY_DEPLOYMENT.json',cfg['config'],root/'project/hub.json'):
 assert os.environ.get('MEMBERSHIP_SMTP_PASSWORD','UNUSED_SENTINEL') not in p.read_text()
print(json.dumps(results))
'''


@pytest.mark.parametrize('mode', ['INVITE_ONLY', 'OFF'])
def test_fresh_hosted_child_uses_environment_not_injected_settings(tmp_path,monkeypatch,mode):
    base=tmp_path/'base';base.mkdir()
    (base/'app').symlink_to(SOURCE,target_is_directory=True)
    deploy_source=Path(ce.__file__).parent
    shutil.copytree(deploy_source,base/'deploy',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    fixture_logo=base/'deploy/company_logos/fictional-company/logo.png'
    fixture_logo.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(deploy_source/'company_logos/sulmara/logo.png',fixture_logo)
    (base/'deploy/company_identities.json').write_text(json.dumps({
        'fictional-company': {'name':'Fictional Company','logo':'logo.png'}
    })+'\n')
    monkeypatch.setattr(ce,'BASE',base)
    env=child_env({**FAKE_ENV,'WAVELINK_MEMBERSHIP_MODE':mode})
    result=subprocess.run([sys.executable,'-c',HOSTED_PROBE,str(tmp_path/'company'),str(SOURCE),mode],
                           env=env,cwd=base,capture_output=True,text=True,timeout=45)
    assert result.returncode==0,result.stderr
    out=json.loads(result.stdout.strip().splitlines()[-1])
    assert out['old_admin_allowed'] and out['old_admin_still_signs_in']
    if mode=='INVITE_ONLY':
        assert out['pending_isolated'] and out['exact_retry_no_second_mail']
    else:
        assert out['off_invite_refused']
