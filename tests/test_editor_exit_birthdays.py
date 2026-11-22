"""Exercise voluntary month/day sharing through the real private and public APIs."""
from datetime import datetime, timezone
from pathlib import Path

from starlette.testclient import TestClient

from deploy.gate import Gate
from deploy.native_showcase import NativeShowcase
from test_feed_news import member, project, session, set_sites


MINE = '/api/recognition/birthday'
TEAM = '/api/recognition/birthdays'


def save(project, headers, month, day, version):
    return project.client.post(MINE, headers=headers, json=dict(month=month, day=day, version=version))


def upcoming(project, headers, **params):
    response = project.client.get(TEAM, headers=headers, params=params)
    assert response.status_code == 200, response.text
    return response.json()


def test_opt_in_correction_removal_and_permissions(project, monkeypatch):
    monkeypatch.setattr(project.app.state.team_birthdays, 'clock', lambda: datetime(2027, 12, 20, 12, tzinfo=timezone.utc))
    uid, writer = member(project, 'birth-writer')
    _, reader = member(project, 'birth-reader')
    for route in (MINE, TEAM):
        assert project.client.get(route).status_code == 401
        assert project.client.get(route, headers={'Authorization': writer['Authorization']}).status_code == 409
    current = project.client.get(MINE, headers=writer).json()
    assert current == {'month': None, 'day': None, 'version': 0}
    assert upcoming(project, reader)['items'] == []
    payload = dict(month=12, day=20, version=0)
    for changed in ({'day':32}, {'month':2,'day':30}, {'month':None}, {'day':None},
                    {'year':1995}, {'user_id':uid}, {'month':True}):
        assert project.client.post(MINE, headers=writer, json={**payload, **changed}).status_code == 422
    result = save(project, writer, 12, 20, 0)
    assert result.status_code == 200, result.text
    assert project.client.get(MINE, headers=writer).json() == {'month':12, 'day':20, 'version':1}
    assert project.client.get(MINE, headers=reader).json() == current
    rows = upcoming(project, reader)['items']
    assert rows == [{'user_id':uid, 'name':'Fictional birth-writer', 'month':12, 'day':20, 'days_until':0}]
    assert save(project, writer, 1, 2, 0).status_code == 409
    assert save(project, writer, 1, 2, 1).status_code == 200
    assert upcoming(project, reader)['items'][0]['days_until'] == 13
    assert save(project, writer, None, None, 2).status_code == 200
    assert upcoming(project, reader)['items'] == []
    assert project.client.get(MINE, headers=writer).json() == {'month':None, 'day':None, 'version':3}

    assert save(project, writer, 12, 20, 3).status_code == 200
    set_sites(project, uid, [project.ship], mode='vessel_only')
    restricted = session(project, uid)
    for route in (MINE, TEAM):
        assert project.client.get(route, headers=restricted).status_code == 403
    assert save(project, restricted, 12, 21, 4).status_code == 403
    assert upcoming(project, reader)['items'] == []


def test_window_pagination_and_leap_day(project, monkeypatch):
    now = [datetime(2028, 2, 1, 15, tzinfo=timezone.utc)]
    monkeypatch.setattr(project.app.state.team_birthdays, 'clock', lambda: now[0])
    _, reader = member(project, 'birth-window-reader')
    expected = []
    for name, month, day in [('leap',2,29), ('outside',3,2), ('last',3,1), ('today',2,1)]:
        uid, writer = member(project, 'birth-' + name)
        assert save(project, writer, month, day, 0).status_code == 200
        if name != 'outside':
            expected.append(uid)
    first = upcoming(project, reader, limit=2)
    second = upcoming(project, reader, limit=2, offset=2)
    assert first['total'] == second['total'] == 3
    assert [r['user_id'] for r in first['items'] + second['items']] == [expected[2], expected[0], expected[1]]
    assert [r['days_until'] for r in first['items'] + second['items']] == [0, 28, 29]
    now[0] = datetime(2029, 2, 1, 15, tzinfo=timezone.utc)
    assert expected[0] not in {r['user_id'] for r in upcoming(project, reader)['items']}


def test_demo_birthday_examples_are_read_only_for_all_visitors():
    gate = Gate('https://demo.example.test', 'fictional-demo-password', b's' * 32,
                'guest.demo', 'fictional-pass', public_entry=True)
    archive = Path(__file__).resolve().parents[1] / 'vendor' / 'FICTIONAL_DEMO.ajproject'
    gate.showcase = NativeShowcase(gate, archive)
    try:
        with TestClient(gate.app(), base_url=gate.origin) as client:
            for _ in range(2):
                visit = gate.showcase.admission()
                auth = {'Authorization':'Bearer ' + visit['token'], 'X-AJ-Hub-ID':visit['hub_id']}
                response = client.get(TEAM, headers=auth)
                assert response.status_code == 200, response.text
                assert [(r['name'], r['days_until']) for r in response.json()['items']] == [('Lia Costa',0), ('Rafael Lima',4)]
                denied = client.post(MINE, headers=auth, json=dict(month=3, day=7, version=0))
                assert denied.status_code == 403 and denied.json()['demo_read_only']
    finally:
        gate.showcase.temp.cleanup()
