import re
import pytest
from starlette.testclient import TestClient
from deploy.gate import Gate, COOKIE, CSRF_COOKIE

ORIGIN='https://demo.example.test'
PASSWORD='Fictional-example-gate-password-2026'

@pytest.fixture
def setup():
    clock=[1000.0]
    g=Gate(ORIGIN,PASSWORD,b'g'*32,clock=lambda:clock[0])
    return g,TestClient(g.app(),base_url=ORIGIN),clock

def fields(c):
    r=c.get('/__demo/login')
    return re.search('name="csrf" value="([^"]+)"',r.text).group(1)

def test_no_cookie_blocks(setup):
    g,c,t=setup
    assert c.get('/__demo/check').status_code==401

def test_password_login_cookie_and_app_auth_separation(setup):
    g,c,t=setup
    csrf=fields(c)
    r=c.post('/__demo/login',data={'csrf':csrf,'password':PASSWORD},headers={'Origin':ORIGIN},follow_redirects=False)
    assert r.status_code==303 and r.headers['location']=='/'
    assert 'secure' in r.headers['set-cookie'].lower() and 'httponly' in r.headers['set-cookie'].lower()
    assert 'samesite=strict' in r.headers['set-cookie'].lower()
    assert c.get('/__demo/check').status_code==204
    assert 'authorization' not in r.headers

def test_wrong_password(setup):
    g,c,t=setup
    assert c.post('/__demo/login',data={'csrf':fields(c),'password':'bad'},headers={'Origin':ORIGIN}).status_code==403
    assert c.get('/__demo/check').status_code==401

@pytest.mark.parametrize('origin',[None,'https://evil.example','null',ORIGIN+', https://evil.example'])
def test_cross_origin_login_rejected(setup,origin):
    g,c,t=setup
    headers={} if origin is None else {'Origin':origin}
    assert c.post('/__demo/login',data={'csrf':fields(c),'password':PASSWORD},headers=headers).status_code==403

def test_csrf_mismatch(setup):
    g,c,t=setup
    fields(c)
    assert c.post('/__demo/login',data={'csrf':'bad','password':PASSWORD},headers={'Origin':ORIGIN}).status_code==403
    assert c.post('/__demo/login',data={'csrf':'não é um token','password':PASSWORD},headers={'Origin':ORIGIN}).status_code==403

def test_cookie_expiry(setup):
    g,c,t=setup
    token=g.token('session',10)
    assert g.valid(token,'session')
    t[0]+=11
    assert not g.valid(token,'session')

def test_cookie_rotation_invalidates(setup):
    g,c,t=setup
    token=g.token('session',10)
    other=Gate(ORIGIN,PASSWORD+'rotated',b'g'*32,clock=lambda:t[0])
    assert not other.valid(token,'session')

def test_cookie_other_hostname_invalid(setup):
    g,c,t=setup
    token=g.token('session',10)
    other=Gate('https://another.example.test',PASSWORD,b'g'*32,clock=lambda:t[0])
    assert not other.valid(token,'session')

@pytest.mark.parametrize('token',['garbage','a.b','a.b.c','é.bad','x'*2000,''])
def test_invalid_cookie(setup,token):
    assert not setup[0].valid(token,'session')

def test_tampered_cookie(setup):
    g,c,t=setup
    token=g.token('session',10)
    assert not g.valid(token[:-1]+('a' if token[-1]!='a' else 'b'),'session')

def test_csrf_cookie_not_session(setup):
    g,c,t=setup
    assert not g.valid(g.token('csrf',10),'session')

def test_global_bruteforce_budget(setup):
    g,c,t=setup
    for _ in range(20):
        r=c.post('/__demo/login',data={'csrf':fields(c),'password':'bad'},headers={'Origin':ORIGIN})
        assert r.status_code==403
    assert c.post('/__demo/login',data={'csrf':fields(c),'password':PASSWORD},headers={'Origin':ORIGIN}).status_code==429
    t[0]+=301
    assert c.post('/__demo/login',data={'csrf':fields(c),'password':PASSWORD},headers={'Origin':ORIGIN},follow_redirects=False).status_code==303

def test_api_expiry_is_json_not_redirect(setup):
    _,c,_=setup
    r=c.get('/__demo/required',headers={'X-Demo-Original-URI':'/api/tasks','Accept':'application/json'},follow_redirects=False)
    assert r.status_code==401 and r.json()['demo_access_required']

def test_navigation_expiry_redirect(setup):
    _,c,_=setup
    r=c.get('/__demo/required',headers={'X-Demo-Original-URI':'/','Accept':'text/html'},follow_redirects=False)
    assert r.status_code==303 and r.headers['location']=='/__demo/login'

def test_logout_csrf_and_cookie_clear(setup):
    g,c,t=setup
    c.post('/__demo/login',data={'csrf':fields(c),'password':PASSWORD},headers={'Origin':ORIGIN},follow_redirects=False)
    assert c.get('/__demo/check').status_code==204
    r=c.get('/__demo/logout');csrf=re.search('name="csrf" value="([^"]+)"',r.text).group(1)
    assert c.post('/__demo/logout',data={'csrf':csrf},headers={'Origin':ORIGIN},follow_redirects=False).status_code==303
    assert c.get('/__demo/check').status_code==401

def test_oversize_form_rejected(setup):
    _,c,_=setup
    assert c.post('/__demo/login',content=b'x=' + b'x'*5000,headers={'Origin':ORIGIN,'Content-Type':'application/x-www-form-urlencoded'}).status_code==403
