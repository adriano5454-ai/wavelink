"""The Handovers journal, its totals and its PDF share the same vessel selection."""
from uuid import uuid4

from tests.browser_admin.test_admin import h
from tests.handovers.test_handovers import create, publish, wording


def test_handover_journal_vessel_scope(h):
    def site(name, code):
        return h.store.fleet.run('save_site', {'name': name, 'code': code}, h.admin, str(uuid4()))

    first = site('Atlantic Dawn', 'ATD')
    second = site('Pacific Dawn', 'PAD')
    initial = publish(h, create(h, dict(wording(h), location=first['name'])))
    create(h, dict(wording(h), location='atd'))
    publish(h, create(h, dict(wording(h), location=second['name'])))

    def get(endpoint, **params):
        return h.client.get('/api/handovers/overview/' + endpoint, headers=h.headers(), params=params)

    all_subjects = get('subjects').json()
    assert 'vessel_id' not in all_subjects
    assert {s['subject'] for s in all_subjects['subjects']} >= {'Atlantic Dawn', 'Pacific Dawn', 'atd'}
    scoped = get('subjects', vessel_id=first['id']).json()
    assert scoped['vessel_id'] == first['id']
    assert {s['subject'] for s in scoped['subjects']} == {'Atlantic Dawn', 'atd'}
    assert get('subjects', vessel_id=str(uuid4())).json()['subjects'] == []
    subject = next(s['key'] for s in scoped['subjects'] if s['subject'] == 'Atlantic Dawn')
    limited = get('days', subject_key=subject, vessel_id=first['id']).json()
    assert limited['total_records'] == limited['published_count'] == 1
    assert [r['id'] for r in limited['rows']] == [initial['id']]
    assert get('days', subject_key=subject, vessel_id=second['id']).status_code == 404
    assert get('pdf', subject_key=subject, vessel_id=second['id'], expected=limited['export_token']).status_code == 404
    assert get('pdf', subject_key=subject, expected=limited['export_token']).status_code == 409
    assert get('pdf', subject_key=subject, vessel_id=first['id'], expected=limited['export_token']).status_code == 200

    worker = h.client.get('/api/handovers/overview/subjects', headers=h.headers(h.wt), params={'vessel_id':first['id']})
    assert worker.status_code == 200
    assert {s['subject'] for s in worker.json()['subjects']} == {'Atlantic Dawn'}
