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


def test_public_original_workspace_folders(company):
    from hashlib import sha256
    s, client = company
    auth = headers(s)
    catalog = client.get('/api/original-documents/library?workspaces=true',headers=auth)
    assert catalog.status_code == 200, catalog.text
    rows = catalog.json()['workspace_files']
    assert {r['group'] for r in rows} >= {'toolbox','checklist','hr-documents','hr-expenses','hr-travel','it'}
    assert catalog.json()['documents']
    for item in rows:
        response = client.get(item['url'],headers=auth)
        assert response.status_code == 200, (item['group'],response.text[:100])
        assert sha256(response.content).hexdigest() == item['sha256']
    entry = client.get('/__demo/public?area=original-files').text
    assert '&public_demo=1#original-files' in entry


def test_workspace_index_uses_employee_and_ticket_access(company):
    from app import access
    from starlette.testclient import TestClient
    s, _ = company
    store, accounts = s.core.state.store, s.core.state.accounts
    with store.connection() as db:
        person = accounts.session_person_in_connection(db,s.team[1]['user_id'])
    policy = access.read(store,s.manager,person['user_id'])
    rights = dict(policy['permissions'], **{'originals.view':True})
    access.save(store,s.manager,person['user_id'],rights,policy['version'],'Fictional library test')
    with store.connection() as db:
        person = accounts.session_person_in_connection(db,person['user_id'])
    token, _ = accounts.issue_session(person,'fictional-library-test')
    auth = {'Authorization':'Bearer '+token,'X-AJ-Hub-ID':s.hub_id}
    manager = dict(auth,Authorization='Bearer '+s.reader_token())
    route = '/api/original-documents/library?workspaces=true'
    with TestClient(s.core) as core:
        all_rows = core.get(route,headers=manager).json()['workspace_files']
        own = core.get(route,headers=auth)
        assert own.status_code == 200, own.text
        visible = {r['url'] for r in own.json()['workspace_files']}
        denied = []
        for row in all_rows:
            if row['group'].startswith('hr-') or row['group'] == 'it':
                permitted = core.get(row['url'],headers=auth).status_code == 200
                assert (row['url'] in visible) == permitted
                if not permitted:
                    denied.append(row['group'])
        assert 'it' in denied and any(group.startswith('hr-') for group in denied)


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

def test_demo_crew_seed_is_idempotent_and_isolated(company, tmp_path):
    from types import SimpleNamespace
    from deploy.showcase_crew import populate_crew, CREW, fixture_id
    showcase, _ = company
    store = showcase.core.state.store

    def snapshot():
        with store.connection() as c:
            return tuple(tuple(map(tuple, c.execute(query))) for query in (
                'SELECT id,enabled,password_hash FROM users ORDER BY id',
                'SELECT id,body FROM hr_records ORDER BY id',
                'SELECT id,body FROM hr_timesheet_projects ORDER BY id',
                'SELECT id FROM company_member_invites ORDER BY id',
            ))

    before = snapshot()
    crew_ids = {fixture_id(name) for name, _, _ in CREW}
    synthetic = [r for r in before[0] if r[0] in crew_ids]
    assert len(synthetic) == 12 and all(row[1:] == (0, '') for row in synthetic)
    populate_crew(showcase)
    assert snapshot() == before
    for public, folder in [(False, showcase.temp.name), (True, str(tmp_path))]:
        other = SimpleNamespace(core=showcase.core, temp=SimpleNamespace(name=folder),
                                gate=SimpleNamespace(public_entry=public))
        with pytest.raises(ValueError, match='disposable public showcase'):
            populate_crew(other)
    assert snapshot() == before

def test_shift_seed_reentry_and_private_guard(company):
    from deploy.showcase_seed import populate
    from types import SimpleNamespace
    showcase, _ = company
    def counts():
        with showcase.core.state.store.connection() as db:
            tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")
                      if r[0] in ('users', 'hr_records') or 'handover' in r[0]]
            return {table: db.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0] for table in tables}

    before = counts()
    assert populate(showcase) == (showcase.manager, showcase.team)
    assert counts() == before
    private = SimpleNamespace(core=showcase.core, temp=showcase.temp, gate=SimpleNamespace(public_entry=False))
    with pytest.raises(ValueError, match='disposable public showcase'):
        populate(private)

def test_guest_example_is_transient_and_private_chart_is_empty(company):
    from app import org_positions
    showcase, visitor = company
    with showcase.core.state.store.connection() as c:
        assert c.execute('SELECT count(*) FROM hr_org_positions').fetchone()[0] == 0
        assert org_positions.snapshot(c,showcase.manager,False)['positions'] == []
    for _ in range(2):
        chart = visitor.get('/api/hr/org-positions', headers=headers(showcase)).json()
        assert chart['example'] and not chart['editor']
        rows = chart['positions']
        assert len(rows) == 19 and len({r['person'] for r in rows if r['person']}) == 18
        from app.departments import membership_ids
        with showcase.core.state.store.connection() as db:
            for row in rows:
                if row['person']:
                    assert row['department'] in membership_ids(db, row['person'],active_only=True)
                if row['role'] in ('operations','chief','it','finance','ceo'):
                    assert db.execute('SELECT 1 FROM department_heads WHERE department_id=? AND user_id=?',
                                      (row['department'],row['person'])).fetchone()
        from app import work_locations
        with showcase.core.state.store.connection() as c:
            sites={s['code']:s for s in work_locations.catalog(c,showcase.manager)}
        by_id={r['id']:r for r in rows}
        chiefs=[r for r in rows if r['parent'] and by_id[r['parent']]['role']=='offshore']
        assert {r['vessel_id'] for r in chiefs} == {sites[k]['id'] for k in ('AUR','DEMO-MERIDIAN')}
        assert len({r['person'] for r in chiefs})==2
        for r in rows:
            if r['parent'] and by_id[r['parent']]['vessel_id']:
                assert r['vessel_id'] == by_id[r['parent']]['vessel_id']
        trainee = [r for r in rows if r['role_name']=='Trainee']
        assert len(trainee)==2 and sum(r['person'] is None for r in trainee)==1
        assert all('Technician' in next(p['role_name'] for p in rows if p['id']==r['parent']) for r in trainee)
    with showcase.core.state.store.connection() as c:
        assert c.execute('SELECT count(*) FROM hr_org_positions').fetchone()[0] == 0

def test_lia_demo_timesheets(company, tmp_path):
    from types import SimpleNamespace
    from deploy.showcase_seed import populate
    showcase, client = company
    def weeks():
        with showcase.core.state.store.connection() as db:
            person = db.execute("SELECT id FROM users WHERE login_id='demo.shift1'").fetchone()[0]
        response = client.get('/api/hr/overview?user_id='+person, headers=headers(showcase))
        assert response.status_code == 200
        return response.json()['timesheets']
    original = weeks()
    assert {r['status']:r['total_hours'] for r in original} == {
        'draft':'16.00', 'submitted':'8.00', 'approved':'41.00'}
    assert len({r['week_start'] for r in original}) == 3
    assert {r['project'] if isinstance(r['project'], str) else r['project']['name'] for r in original} == {'Aurora survey'}
    populate(showcase)
    assert [r['id'] for r in weeks()] == [r['id'] for r in original]
    for public, path in [(False,showcase.temp.name),(True,str(tmp_path))]:
        other = SimpleNamespace(core=showcase.core,gate=SimpleNamespace(public_entry=public),temp=SimpleNamespace(name=path))
        with pytest.raises(ValueError,match='disposable public showcase'):
            populate(other)
    assert weeks() == original
