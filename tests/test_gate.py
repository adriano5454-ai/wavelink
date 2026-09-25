import re
import pytest
from starlette.testclient import TestClient
from deploy.gate import Gate, COOKIE, CSRF_COOKIE

ORIGIN='https://demo.example.test'
PASSWORD='Fictional-example-gate-password-2026'

@pytest.fixture
def setup():
    clock=[1000.0]
    g=Gate(ORIGIN,PASSWORD,b'g'*32,'guest.demo','FictionalGuest-Test-2026',clock=lambda:clock[0])
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
def test_origin_alone_without_signed_csrf_cannot_admit(setup,origin):
    # The confirmed demo no longer gates forms solely on Origin.
    # That historical test is preserved outside this upload tree. Neither
    # a missing nor any supplied Origin bypasses the signed CSRF pair.
    g,c,t=setup
    headers={} if origin is None else {'Origin':origin}
    assert c.post('/__demo/login',data={'csrf':'forged','password':PASSWORD},headers=headers).status_code==403
    assert c.get('/__demo/check').status_code==401

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
    other=Gate(ORIGIN,PASSWORD+'rotated',b'g'*32,'guest.demo','FictionalGuest-Test-2026',clock=lambda:t[0])
    assert not other.valid(token,'session')

def test_cookie_other_hostname_invalid(setup):
    g,c,t=setup
    token=g.token('session',10)
    other=Gate('https://another.example.test',PASSWORD,b'g'*32,'guest.demo','FictionalGuest-Test-2026',clock=lambda:t[0])
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


def test_confirmed_form_behavior_missing_origin_with_signed_pair(setup):
    _,c,_=setup
    response=c.post('/__demo/login',data={'csrf':fields(c),'password':PASSWORD},follow_redirects=False)
    assert response.status_code==303
    assert c.get('/__demo/check').status_code==204

def test_guest_method_name_not_shadowed(setup):
    g,_,_=setup
    assert g.guest_login_id=='guest.demo' and callable(g.authenticate_guest)

def test_missing_quick_key_does_not_authenticate(setup,monkeypatch):
    g,c,_=setup
    def forbidden(): raise AssertionError('must not authenticate')
    monkeypatch.setattr(g,'authenticate_guest',forbidden)
    r=c.get('/__demo/quick',follow_redirects=False)
    assert r.status_code==303 and r.headers['location']=='/__demo/login'

def test_bad_quick_key_does_not_authenticate(setup,monkeypatch):
    g,c,_=setup
    def forbidden(): raise AssertionError('must not authenticate')
    monkeypatch.setattr(g,'authenticate_guest',forbidden)
    r=c.get('/__demo/quick',params={'key':'wrong'})
    assert r.status_code==403 and c.get('/__demo/check').status_code==401

def test_quick_returns_session_not_password(setup,monkeypatch):
    g,c,_=setup
    auth={'token':'fictional-session-token','person':{'user_id':'synthetic-user','login_id':'guest.demo','name':'Guest','role':'technician'},'hub_id':'synthetic-hub'}
    monkeypatch.setattr(g,'authenticate_guest',lambda:auth)
    r=c.get('/__demo/quick',params={'key':PASSWORD},follow_redirects=False)
    assert r.status_code==200 and 'Opening Wavelink' in r.text
    assert 'fictional-session-token' in r.text
    assert PASSWORD not in r.text and g.guest_password not in r.text
    assert r.headers['cache-control']=='no-store' and r.headers['referrer-policy']=='no-referrer'
    assert c.get('/__demo/check').status_code==204

def test_failed_guest_remains_outside_gate(setup,monkeypatch):
    g,c,_=setup
    def fail():raise RuntimeError('Guest could not sign in.')
    monkeypatch.setattr(g,'authenticate_guest',fail)
    r=c.get('/__demo/quick',params={'key':PASSWORD},follow_redirects=False)
    assert r.status_code==503 and 'Guest demonstration unavailable' in r.text
    assert c.get('/__demo/check').status_code==401

def test_quick_uses_shared_attempt_limit(setup,monkeypatch):
    g,c,t=setup
    for _ in range(20):assert c.get('/__demo/quick',params={'key':'wrong'}).status_code==403
    assert c.get('/__demo/quick',params={'key':PASSWORD}).status_code==429

def test_bootstrap_escapes_script_terminator(setup):
    g,_,_=setup
    text=g.bootstrap_page({'token':'</script><script>bad</script>','person':{},'hub_id':'x'})
    assert '</script><script>bad' not in text
    assert 'pxgeo-dive-check-1' in text
    assert "store.get('lease')" in text and 'saved.fieldworkDrafts' in text
