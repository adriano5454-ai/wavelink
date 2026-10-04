"""UI98 real hosted company middleware, fictional project and captured mail."""
from dataclasses import replace
import re
import uuid
import pytest
from test_company_c01 import instance, client, activate, login, PASS
from app.store import utcnow, Problem
from app.account_security import _totp
import base64,time
from deploy.nginx_config import render

NEW='Fictional-ui98-replacement-password-72'

class Mailbox:
    ready=True
    def __init__(self):self.messages=[]
    def send(self,to,subject,body):self.messages.append((to,subject,body))

def configured(core,settings):
    membership=core.state.company_membership
    membership.settings=replace(membership.settings,enabled=True,origin=settings.external_origin,company_name='Fictional Company')
    membership.mailer=Mailbox()
    with core.state.store.connection(True) as c:
        uid=c.execute("SELECT id FROM users WHERE login_id='admin'").fetchone()[0]
        c.execute("INSERT INTO company_memberships VALUES(?,?,'approved','','',1,?,?,?,?,?,'')",(uid,'admin@example.test',utcnow(),utcnow(),utcnow(),uid,uid))
    return membership.mailer

def hub(instance):return {'X-AJ-Hub-ID':instance[2].expected_hub_id}

def totp(secret,offset=0):
    raw=base64.b32decode(secret+'='*((8-len(secret)%8)%8))
    return _totp(raw,int(time.time()//30)+offset)

def test_recovery_bootstrap_before_normal_login(instance):
    with client(instance) as c:
        activate(c)
        page=c.get('/reset-password');assert page.status_code==200
        info=c.get('/api/password-recovery/info');assert info.status_code==200,info.text
        assert set(info.json())=={'available','hub_id','company'}
        assert info.json()['available'] is False
        assert info.headers['Cache-Control']=='no-store'
        assert c.post('/api/password-recovery/request',json={'identifier':'admin'},headers=hub(instance)).status_code==403
        assert c.get('/api/me').status_code==401

def test_full_reset_through_hosted_company_boundary_without_session(instance):
    with client(instance) as c:
        activate(c);core=c.app.state.core;mail=configured(core,instance[2]);old_token=login(c)
        request=c.post('/api/password-recovery/request',json={'identifier':'admin@example.test'},headers=hub(instance))
        assert request.status_code==200,request.text
        assert len(mail.messages)==1
        code=re.search(r'code is (\d{8})',mail.messages[-1][2])[1]
        payload=dict(challenge=request.json()['challenge'],code=code,password=NEW,confirm_password=NEW,op_id=str(uuid.uuid4()))
        result=c.post('/api/password-recovery/reset',json=payload,headers=hub(instance));assert result.status_code==200,result.text
        assert result.json()['sign_in_required'] and 'token' not in result.json()
        assert c.post('/api/password-recovery/reset',json=payload,headers=hub(instance)).json()['duplicate']
        assert len(mail.messages)==2
        assert c.get('/api/me',headers={'Authorization':'Bearer '+old_token}).status_code==401
        assert c.post('/api/login',json={'login_id':'admin','password':PASS,'device_id':'fictional-old'}).status_code==403
        assert login(c,NEW)
        assert c.get('/api/records').status_code==401

def test_real_mfa_completion_before_operational_session(instance):
    with client(instance) as c:
        activate(c);token=login(c);h={**hub(instance),'Authorization':'Bearer '+token}
        start=c.post('/api/security/mfa/start',json={'current_password':PASS},headers=h);assert start.status_code==200,start.text
        setup=start.json();confirm=c.post('/api/security/mfa/confirm',json={'current_password':PASS,'code':totp(setup['secret']),'version':setup['version']},headers=h);assert confirm.status_code==200,confirm.text
        first=c.post('/api/login',json={'login_id':'admin','password':PASS,'device_id':'fictional-mfa-login'})
        assert first.json()['mfa_required'] and 'token' not in first.json()
        assert c.get('/api/me').status_code==401
        result=c.post('/api/login/mfa',json={'challenge':first.json()['challenge'],'code':totp(setup['secret'],1),'method':'totp'})
        assert result.status_code==200,result.text
        assert c.get('/api/me',headers={'Authorization':'Bearer '+result.json()['token']}).status_code==200

@pytest.mark.parametrize('path,method',[('/api/password-recovery/info','GET'),('/api/password-recovery/request','POST'),('/api/password-recovery/reset','POST'),('/api/login/mfa','POST'),('/reset-password','GET')])
def test_pending_first_admin_setup_still_blocks_new_public_routes(instance,path,method):
    with client(instance) as c:
        r=c.request(method,path,json={} if method=='POST' else None)
        assert r.status_code==423,r.text

@pytest.mark.parametrize('path,method',[('/api/password-recovery/info','POST'),('/api/password-recovery/request','GET'),('/api/password-recovery/reset','GET'),('/api/password-recovery/reset/extra','POST'),('/api/password-recovery/unknown','POST'),('/api/login/mfa','GET'),('/api/login/mfa-extra','POST'),('/api/login/other','POST'),('/api/security/status','GET'),('/api/security/mfa/start','POST'),('/api/records','GET'),('/api/me','GET')])
def test_unrelated_or_wrong_method_apis_do_not_bypass_normal_session(instance,path,method):
    with client(instance) as c:
        activate(c)
        r=c.request(method,path,json={} if method=='POST' else None)
        assert r.status_code==401,r.text

@pytest.mark.parametrize('kind,expected',[('origin',403),('hub',409),('authorization',422),('body',422),('large',413),('type',415),('host',400),('tls',400),('forwarded',400)])
def test_core_and_ingress_guards_still_apply_to_recovery(instance,kind,expected):
    with client(instance) as c:
        activate(c);configured(c.app.state.core,instance[2]);h={**hub(instance),'Content-Type':'application/json'};body='{"identifier":"admin"}'
        if kind=='origin':h['Origin']='https://other.example.test'
        elif kind=='hub':h['X-AJ-Hub-ID']='other-hub'
        elif kind=='authorization':h['Authorization']='Bearer normal-session'
        elif kind=='body':body='{"identifier":"admin","email":"attacker@example.test"}'
        elif kind=='large':body='{"identifier":"'+('x'*5000)+'"}'
        elif kind=='type':h['Content-Type']='text/plain'
        elif kind=='host':h['Host']='wrong.example.test'
        elif kind=='tls':h['X-Forwarded-Proto']='http'
        elif kind=='forwarded':h['X-Forwarded-For']='192.0.2.1, 192.0.2.2'
        r=c.post('/api/password-recovery/request',content=body,headers=h);assert r.status_code==expected,r.text
        assert not c.app.state.core.state.company_membership.mailer.messages

def test_demo_recovery_locations_are_exact_and_retain_host_tls_and_header_guards(tmp_path):
    config=render('demo.example.test',19055,tmp_path/'nginx')
    for path,method in [('/api/password-recovery/info','GET'),('/api/password-recovery/request','POST'),('/api/password-recovery/reset','POST')]:
        marker='        location = '+path+' {';assert config.count(marker)==1
        route=config.split(marker,1)[1].split('\n        }',1)[0]
        assert 'auth_request' not in route and '@demo_denied' not in route
        assert 'limit_except '+method+' { deny all; }' in route
        for required in ['if ($demo_tls_ok = 0)','if ($http_host != "demo.example.test")','client_max_body_size 4k','proxy_pass_request_headers off','Origin $http_origin','X-AJ-Hub-ID $http_x_aj_hub_id','X-Forwarded-For $remote_addr','X-Forwarded-Proto https']:assert required in route
    assert 'location ^~ /api/password-recovery/' not in config
    # Normal app/API and app.js still use the existing admission gate.
    for marker in ['        location / {\n            if ($demo_tls_ok','        location = /static/app.js {']:
        route=config.split(marker,1)[1].split('\n        }',1)[0];assert 'auth_request /_demo_verify' in route
