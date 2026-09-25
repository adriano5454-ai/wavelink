
"""G01 public demo entry checks; only fictional credentials and controlled API replies."""
from pathlib import Path
import re
import copy
import pytest
from starlette.testclient import TestClient
from deploy.gate import Gate, COOKIE, public_entry_enabled

ORIGIN = 'https://demo.example.test'
PASSWORD = 'Fictional-example-gate-password-2026'
GUEST_PASSWORD = 'FictionalGuest-Test-2026'
AUTH = {'token':'fictional-session-token','person':{'user_id':'fictional-guest',
        'login_id':'guest.demo','role':'technician','name':'Demo guest','device_id':'device-1'},
        'hub_id':'fictional-project'}

@pytest.fixture
def pub(monkeypatch):
    clock=[1000.]
    gate=Gate(ORIGIN, PASSWORD, b'g'*32, 'guest.demo', GUEST_PASSWORD,
              public_entry=True, clock=lambda:clock[0])
    monkeypatch.setattr(gate,'authenticate_guest', lambda:copy.deepcopy(AUTH))
    return gate,TestClient(gate.app(),base_url=ORIGIN),clock

@pytest.mark.parametrize('value',[None,'','NO',' NO '])
def test_default_or_explicit_no_is_private(value):
    assert public_entry_enabled(value) is False

@pytest.mark.parametrize('value',['YES',' YES '])
def test_only_yes_enables(value):
    assert public_entry_enabled(value) is True

@pytest.mark.parametrize('value',['yes','true','1','FALSE','Y','OFF','NO!'])
def test_bad_setting_is_rejected(value):
    with pytest.raises(ValueError,match='DEMO_PUBLIC_ENTRY'):
        public_entry_enabled(value)

def test_nonboolean_constructor_refused():
    with pytest.raises(ValueError):
        Gate(ORIGIN,PASSWORD,b'g'*32,'guest.demo',GUEST_PASSWORD,public_entry='YES')

def test_default_public_route_is_closed(monkeypatch):
    gate=Gate(ORIGIN,PASSWORD,b'g'*32,'guest.demo',GUEST_PASSWORD)
    def forbidden():raise AssertionError('must not sign in')
    monkeypatch.setattr(gate,'authenticate_guest',forbidden)
    c=TestClient(gate.app(),base_url=ORIGIN)
    assert c.get('/__demo/public').status_code==404
    assert c.get('/__demo/check').status_code==401

def test_public_mode_alone_does_not_bypass_gate(pub):
    _,c,_=pub
    assert c.get('/__demo/check').status_code==401

def test_root_navigation_enters_public(pub):
    _,c,_=pub
    r=c.get('/__demo/required',headers={'X-Demo-Original-URI':'/',
            'X-Demo-Original-Method':'GET','Accept':'text/html'},follow_redirects=False)
    assert r.status_code==303 and r.headers['location']=='/__demo/public'

@pytest.mark.parametrize('path',['/admin','/admin/users','/fleet'])
def test_staff_destinations_still_use_private_signin(pub,path):
    _,c,_=pub
    r=c.get('/__demo/required',headers={'X-Demo-Original-URI':path,
            'Accept':'text/html'},follow_redirects=False)
    assert r.status_code==303 and r.headers['location']=='/__demo/login'

@pytest.mark.parametrize('path',['/api/tasks','/static/app.js'])
def test_non_navigation_is_not_auto_authenticated(pub,path):
    _,c,_=pub
    r=c.get('/__demo/required',headers={'X-Demo-Original-URI':path},follow_redirects=False)
    assert r.status_code==401 and r.json()['demo_access_required']

def test_post_root_is_not_redirected_to_guest(pub):
    _,c,_=pub
    r=c.post('/__demo/required',headers={'X-Demo-Original-URI':'/',
             'X-Demo-Original-Method':'POST','Accept':'text/html'})
    assert r.status_code==401

def test_public_session_cookie_no_credential_leak(pub):
    gate,c,_=pub
    r=c.get('/__demo/public')
    assert r.status_code==200
    assert 'fictional-session-token' in r.text
    assert PASSWORD not in r.text and GUEST_PASSWORD not in r.text
    assert 'type="password"' not in r.text
    assert 'Normal staff sign-in' in r.text
    assert r.headers['cache-control']=='no-store'
    assert r.headers['referrer-policy']=='no-referrer'
    assert r.headers['x-frame-options']=='DENY'
    cookie=c.cookies.get(COOKIE)
    assert gate.valid(cookie,'public-session')
    assert not gate.valid(cookie,'session')
    assert c.get('/__demo/check').status_code==204
    for v in ('Secure','HttpOnly','SameSite=strict','Path=/'):
        assert v.lower() in r.headers['set-cookie'].lower()

def test_disabling_public_rejects_public_admission(pub):
    gate,c,_=pub
    c.get('/__demo/public')
    gate.public_entry=False
    assert c.get('/__demo/check').status_code==401
    assert c.get('/__demo/public').status_code==404

def test_normal_password_session_survives_disabling_public(pub):
    gate,c,_=pub
    r=c.get('/__demo/login')
    csrf=re.search('name="csrf" value="([^"]+)"',r.text).group(1)
    r=c.post('/__demo/login',data={'csrf':csrf,'password':PASSWORD},follow_redirects=False)
    assert r.status_code==303 and r.headers['location']=='/'
    gate.public_entry=False
    assert c.get('/__demo/check').status_code==204

def test_public_cookie_is_not_a_csrf_token(pub):
    _,c,_=pub
    c.get('/__demo/public')
    token=c.cookies.get(COOKIE)
    c.cookies.set('__Host-wavelink-demo-csrf',token,domain='demo.example.test',path='/')
    assert c.post('/__demo/login',data={'csrf':token,'password':PASSWORD}).status_code==403

def test_public_cookie_expiry(pub):
    _,c,t=pub
    c.get('/__demo/public')
    t[0]+=8*3600+1
    assert c.get('/__demo/check').status_code==401

@pytest.mark.parametrize('role',['admin','unknown','',None])
def test_refuse_administrator_or_unknown_role(pub,monkeypatch,role):
    gate,c,_=pub
    auth=copy.deepcopy(AUTH);auth['person']['role']=role
    monkeypatch.setattr(gate,'authenticate_guest',lambda:auth)
    r=c.get('/__demo/public')
    assert r.status_code==503 and AUTH['token'] not in r.text
    assert 'set-cookie' not in r.headers
    assert c.get('/__demo/check').status_code==401

@pytest.mark.parametrize('mutation',[
    ('login','another.user'),('user',''),('token',''),('token',None),('hub',''),('hub',None)])
def test_refuse_incomplete_or_wrong_identity(pub,monkeypatch,mutation):
    gate,c,_=pub;auth=copy.deepcopy(AUTH)
    field,value=mutation
    if field=='login':auth['person']['login_id']=value
    if field=='user':auth['person']['user_id']=value
    if field=='token':auth['token']=value
    if field=='hub':auth['hub_id']=value
    monkeypatch.setattr(gate,'authenticate_guest',lambda:auth)
    r=c.get('/__demo/public')
    assert r.status_code==503 and 'set-cookie' not in r.headers

@pytest.mark.parametrize('error',[RuntimeError('secret detail'),OSError('secret detail')])
def test_guest_failure_is_closed_and_sanitised(pub,monkeypatch,error):
    gate,c,_=pub
    def fail():raise error
    monkeypatch.setattr(gate,'authenticate_guest',fail)
    r=c.get('/__demo/public')
    assert r.status_code==503 and 'secret detail' not in r.text
    assert 'set-cookie' not in r.headers

def test_public_attempt_limit_does_not_lock_staff(pub):
    _,c,t=pub
    for _ in range(20):
        assert c.get('/__demo/public').status_code==200
    r=c.get('/__demo/public')
    assert r.status_code==429 and r.headers['retry-after']=='300'
    r=c.get('/__demo/login')
    csrf=re.search('name="csrf" value="([^"]+)"',r.text).group(1)
    assert c.post('/__demo/login',data={'csrf':csrf,'password':PASSWORD},
                  follow_redirects=False).status_code==303
    t[0]+=301
    assert c.get('/__demo/public').status_code==200

def test_staff_attempt_limit_does_not_lock_public(pub):
    _,c,_=pub
    for _ in range(20):assert c.get('/__demo/quick',params={'key':'bad'}).status_code==403
    assert c.get('/__demo/public').status_code==200

@pytest.mark.parametrize('method',['HEAD','POST','PUT','DELETE'])
def test_non_get_does_not_mint_guest(pub,monkeypatch,method):
    gate,c,_=pub
    def forbidden():raise AssertionError('must not sign in')
    monkeypatch.setattr(gate,'authenticate_guest',forbidden)
    assert c.request(method,'/__demo/public').status_code==405

def test_script_escaping():
    auth=copy.deepcopy(AUTH);auth['person']['name']='</script><script>bad()</script>'
    page=Gate.public_bootstrap_page(auth)
    assert '</script><script>bad' not in page
    assert '\\u003c/script\\u003e' in page

def test_same_auth_modes_do_not_cross_hosts(pub):
    gate,c,_=pub;c.get('/__demo/public')
    other=Gate('https://other.example.test',PASSWORD,b'g'*32,'guest.demo',GUEST_PASSWORD,
                public_entry=True,clock=lambda:1000.)
    assert not other.valid(c.cookies.get(COOKIE),'public-session')

def test_supervisor_guest_retains_existing_role(pub,monkeypatch):
    gate,c,_=pub;auth=copy.deepcopy(AUTH);auth['person']['role']='supervisor'
    monkeypatch.setattr(gate,'authenticate_guest',lambda:auth)
    r=c.get('/__demo/public')
    assert r.status_code==200 and '"role":"supervisor"' in r.text

def test_entrypoint_forwards_explicit_setting_and_keeps_password_required():
    src=(Path(__file__).resolve().parents[1]/'deploy/entrypoint.py').read_text()
    assert "DEMO_PUBLIC_ENTRY='YES' if public_entry else 'NO'" in src
    assert "required_env = ('DEMO_ACCESS_PASSWORD', 'DEMO_GUEST_LOGIN', 'DEMO_GUEST_PASSWORD')" in src
    assert src.index('public_entry = public_entry_enabled(') < src.index('cfg = prepare(')
