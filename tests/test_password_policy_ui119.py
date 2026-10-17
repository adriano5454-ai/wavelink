"""Fictional local accounts/mail only; never contacts a real mailbox."""
import json, re, uuid
import pytest
from app.password_policy import password_min_length
from app.store import Problem
from app.accounts import password_hash, password_matches
from app.localization import locale_bootstrap, translate_message
from tests.test_password_recovery_ui97 import recovery, request, payload, reset, login, OLD
from tests.ui64_membership.conftest import h
from tests.ui64_membership.test_membership import approve

def corcovado(monkeypatch):
    monkeypatch.setenv('WAVELINK_DEPLOYMENT_MODE','COMPANY')
    monkeypatch.setenv('COMPANY_ID','corcovado')

@pytest.mark.parametrize('mode,company,secure,legacy',[
    ('COMPANY','corcovado',8,8),('DEMO','corcovado',14,6),
    ('COMPANY','sulmara',14,6),('COMPANY','demo',14,6),('','corcovado',14,6)])
def test_policy_is_operator_scoped(mode,company,secure,legacy):
    env={'WAVELINK_DEPLOYMENT_MODE':mode,'COMPANY_ID':company}
    assert password_min_length(environment=env)==secure
    assert password_min_length(6,environment=env)==legacy

def test_invitation_rejects_seven_then_accepts_eight_and_logs_in(h,monkeypatch):
    corcovado(monkeypatch)
    email='new.policy@example.test'
    h.m.issue(h.admin,dict(op_id=str(uuid.uuid4()),email=email,department_id=h.dept['id']))
    token=h.mail.invite();challenge=h.m.send_code(token,email)
    p=dict(op_id=str(uuid.uuid4()),challenge=challenge['challenge'],code=h.mail.code(),
           email=email,login_id='policy.member',name='Fictional Policy',password='Abc123!')
    with h.s.connection() as c: before=c.execute('SELECT count(*) FROM users').fetchone()[0]
    with pytest.raises(Problem) as e:h.m.accept(token,p)
    assert e.value.code==422
    with h.s.connection() as c: assert c.execute('SELECT count(*) FROM users').fetchone()[0]==before
    p['password']='Abc123!z';result=h.m.accept(token,p);assert result['accepted']
    with h.s.connection() as c: user=c.execute('SELECT * FROM users WHERE login_id=?',('policy.member',)).fetchone()
    assert password_matches(p['password'],user['password_hash'])
    from types import SimpleNamespace
    approve(h,SimpleNamespace(uid=user['id']))
    assert h.a.login('policy.member',p['password'],'fictional-device')[1]['user_id']==user['id']

def test_recovery_eight_rejects_seven_and_preserves_identity(recovery,monkeypatch):
    app,c,u=recovery;corcovado(monkeypatch)
    signed=login(app,c,OLD).json();start=request(app,c)
    good=re.search(r'\b[0-9]{8}\b',app.state.company_membership.mailer.messages[-1][2])[0]
    p=payload(start,good);p.update(password='Abc123!',confirm_password='Abc123!')
    assert reset(app,c,p).status_code==422
    assert login(app,c,OLD).status_code==200
    p.update(password='Abc123!z',confirm_password='Abc123!z')
    assert reset(app,c,p).status_code==200
    with pytest.raises(Problem):app.state.store.session(signed['token'])
    assert login(app,c,'Abc123!z').status_code==200
    assert login(app,c,OLD).status_code==403
    with app.state.store.connection() as con:
        after=con.execute('SELECT * FROM users WHERE id=?',(u['id'],)).fetchone()
        assert after['login_id']==u['login_id'] and after['role']==u['role']
        assert con.execute('SELECT verified_at FROM company_memberships WHERE user_id=?',(u['id'],)).fetchone()[0]

def test_default_recovery_still_requires_fourteen(recovery,monkeypatch):
    app,c,u=recovery;monkeypatch.delenv('COMPANY_ID',raising=False)
    start=request(app,c);good=re.search(r'\b[0-9]{8}\b',app.state.company_membership.mailer.messages[-1][2])[0]
    p=payload(start,good);p.update(password='Abc123!z',confirm_password='Abc123!z')
    assert reset(app,c,p).status_code==422
    p.update(password='Abc123!zAbc123!',confirm_password='Abc123!zAbc123!')
    assert reset(app,c,p).status_code==200

def test_own_change_and_admin_reset_share_minimum(h,monkeypatch):
    corcovado(monkeypatch)
    with pytest.raises(Problem):h.a.change_own_password(h.admin,h.pw,'Abc123!')
    h.a.change_own_password(h.admin,h.pw,'Abc123!z')
    token,actor=h.a.login('training.admin','Abc123!z','new-device')
    with pytest.raises(Problem):h.a.reset_password(h.w['id'],'Abc123!',actor)
    h.a.reset_password(h.w['id'],'Xyz789!q',actor)
    assert h.a.login(h.w['login_id'],'Xyz789!q','worker-device')[1]['user_id']==h.w['id']

def test_maximum_and_diversity_remain(recovery,monkeypatch):
    app,c,u=recovery;corcovado(monkeypatch);start=request(app,c)
    good=re.search(r'\b[0-9]{8}\b',app.state.company_membership.mailer.messages[-1][2])[0]
    for pw in ['a'*8,'Abc123!z'*17]:
        p=payload(start,good);p.update(password=pw,confirm_password=pw)
        assert reset(app,c,p).status_code==422

def test_public_policy_and_portuguese_errors(monkeypatch):
    corcovado(monkeypatch)
    script=locale_bootstrap('pt-BR')
    assert '"membership_min": 8' in script and '"account_min": 8' in script
    assert translate_message('Use 8 to 128 characters with at least six different characters.','pt-BR').startswith('Use de 8 a 128')
    monkeypatch.setenv('WAVELINK_DEPLOYMENT_MODE','DEMO')
    script=locale_bootstrap('en')
    assert '"membership_min": 14' in script and '"account_min": 6' in script
