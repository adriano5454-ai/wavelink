"""The public visitor uses real product APIs, an isolated seed, and a visit-scoped mood."""
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from deploy.gate import Gate
from deploy.native_showcase import NativeShowcase
from app.store import Problem


@pytest.fixture(scope='module')
def company():
    g = Gate('https://demo.example.test','fictional-demo-password',b's'*32,'guest.demo','fictional-pass',public_entry=True)
    s = NativeShowcase(g,Path(__file__).resolve().parents[1]/'vendor'/'FICTIONAL_DEMO.ajproject')
    g.showcase = s
    with TestClient(g.app(),base_url=g.origin) as client:
        yield s,client
    s.temp.cleanup()


def headers(s):
    auth = s.admission()
    return {'Authorization':'Bearer '+auth['token'], 'X-AJ-Hub-ID':auth['hub_id']}


def test_native_company_routes(company):
    s,c = company
    h = headers(s)
    routes = ('me','home/personal','hr/directory','it/workspace?view=queue','recognition/profile','recognition/feed',
              'fleet/directory','fleet/manifests','admin/directory','admin/templates','memberships/context','backup/summary')
    for route in routes:
        response = c.get('/api/'+route,headers=h)
        assert response.status_code==200,(route,response.status_code)
    assert c.get('/api/it/workspace?view=queue',headers=h).json()['total']==3
    assert len(c.get('/api/recognition/feed',headers=h).json()['items'])>=2
    assert c.post('/api/presence/heartbeat',headers=h).json()['count']>=1
    with s.core.state.store.connection() as db:
        assert {r[0] for r in db.execute('SELECT DISTINCT kind FROM hr_records')} >= {
                'people','needs','documents','shifts','travel','expenses','timesheets'}
    entry = c.get('/__demo/public?area=hr&lang=pt', headers={'Accept-Language':'pt-BR'}).text
    assert '/__demo/native/pt?browser_workspace=' not in entry and '&public_demo=1#hr' in entry
    assert c.get('/__demo/native/pt', follow_redirects=False).headers['location']=='/__demo/public'
    assert c.get('/__demo/native/pt?browser_workspace=example&public_demo=1').headers['content-language']=='pt-BR'
    assert c.get('/__demo/check',headers={'X-Demo-Original-URI':'/'}).status_code==401
    assert c.get('/__demo/check',headers={'X-Demo-Original-URI':'/?browser_workspace=example&public_demo=1'}).status_code==204
    assert c.post('/api/me/language',headers=h,json={'language':'pt-BR'}).status_code==403


def test_visit_scope_and_read_only(company):
    s,c = company
    first,second = headers(s),headers(s)
    url = '/api/recognition/moods'
    day = c.get(url,headers=first).json()['day']
    def set_mood(value, selected=day):
        return c.post(url,headers={**first,'X-Wavelink-Mood-Day':selected},json={'mood':value})
    assert set_mood('focused').json()['mine']=='focused'
    assert c.get(url,headers=second).json()['mine'] is None
    assert set_mood('happy','2000-01-01').status_code==409
    assert set_mood(None).json()['mine'] is None
    # Neither live company credentials nor a backing Wavelink administrator session are issued.
    with pytest.raises(Problem):
        s.core.state.store.session(first['Authorization'][7:])
    for action in ('admin/users','hr/action','it/action','memberships/invite','fleet/action','password','login'):
        assert c.post('/api/'+action,headers=first,json={}).json()['demo_read_only']
    assert c.get('/api/backup',headers=first).status_code==403
    assert c.get('/api/admin/directory').status_code==401
    with c.websocket_connect('/__demo/native/ws',headers={'Origin':s.gate.origin}) as ws:
        ws.send_json({'token':first['Authorization'][7:]})
        assert ws.receive_json()['type']=='connected'
        ws.send_json({'type':'ping'})
        assert ws.receive_json()['type']=='pong'
    assert c.post('/api/logout',headers=first).json()['ok']
    assert c.get(url,headers=first).status_code==401
    assert c.get(url,headers=second).status_code==200
