"""Domain searches must apply vessel selection before counts, pagination and export."""
from datetime import date, timedelta
import json
from uuid import uuid4

from test_work_locations import project


def test_it_queue_vessel_filter(project):
    store, _, client, headers = project
    sites = client.get('/api/fleet/work-locations', headers=headers).json()['sites']
    aurora = next(s for s in sites if s['code'] == 'AUR')
    base = next(s for s in sites if s['code'] == 'DEMO-SHORE')
    def queue(**filters):
        response = client.get('/api/it/workspace', params={'view':'queue', **filters}, headers=headers)
        assert response.status_code == 200, response.text
        return response.json()
    matching = queue(vessel_id=aurora['id'], limit=1)
    assert matching['total'] > 1 and len(matching['requests']) == 1
    assert sum(matching['counts'].values()) == matching['total']
    second = queue(vessel_id=aurora['id'], limit=1, offset=1)
    assert second['requests'][0]['id'] != matching['requests'][0]['id']
    assert queue(vessel_id=str(uuid4()))['total']==0
    assert queue(vessel_id=aurora['id'],query='nonexistent-title-'+str(uuid4()))['total']==0
    printer = queue(vessel_id=base['id'],query='printer',priority='low')
    assert len(printer['requests'])==1 and sum(printer['counts'].values())==1
    saved=printer['requests'][0]
    assert saved['work_site']['id']==base['id']
    assert queue(vessel_id=base['id'],query='printer',priority='low',status=saved['status'])['total']==1
    assert queue(vessel_id=base['id'],query='printer',priority='urgent')['total']==0
    assert queue(vessel_id=aurora['id'],query='printer')['total']==0
    assert queue(view='mine',vessel_id=base['id'],query='printer')['total']==0
    assert queue(view='mine',vessel_id=aurora['id'])['total'] > 0
    marker='Location verification '+str(uuid4())
    with store.connection(True) as c:
        sample=json.loads(c.execute('SELECT body FROM it_request_records WHERE id=?',(saved['id'],)).fetchone()[0])
        def save(location,reference):
            row=dict(sample,id=str(uuid4()),title=marker,location=location,work_site=reference)
            store.it_requests._put(c,row)
            return row['id']
        old=save(base['code'].lower(),None)
        explicit=save(base['name'],aurora)
        save(base['code'],{'id':str(uuid4())})
    assert [r['id'] for r in queue(vessel_id=base['id'],query=marker)['requests']]==[old]
    assert [r['id'] for r in queue(vessel_id=aurora['id'],query=marker)['requests']]==[explicit]


def test_calendar_and_hr_vessel_projection(project):
    store, actors, client, headers = project
    sites = client.get('/api/fleet/work-locations', headers=headers).json()['sites']
    ship = next(s for s in sites if s['code']=='AUR')
    start = (date.today()-timedelta(days=40)).isoformat()
    end = (date.today()+timedelta(days=40)).isoformat()
    kinds = 'maintenance,tasks,certificates,inventory,logs,manifests,toolbox,checklists'
    def get(route, **params):
        response = client.get(route, headers=headers, params=params)
        assert response.status_code == 200, response.text
        return response.json()
    calendar = get('/api/calendar',start=start,end=end,kinds=kinds,vessel_id=ship['id'])
    assert {'maintenance','tasks'} <= {row['kind'] for row in calendar['events']}
    assert 0 < calendar['total'] < get('/api/calendar',start=start,end=end,kinds=kinds)['total']
    assert get('/api/calendar',start=start,end=end,kinds=kinds,vessel_id=str(uuid4()))['events'] == []
    params = dict(start_on=start,end_on=end,vessel_id=ship['id'])
    hr = get('/api/hr/workspace',**params)
    shift = next(row for row in hr['records'] if row['kind']=='shifts')
    assert hr['vessel_name']==ship['name']
    source = get('/api/hr/records',kind='shifts',user_id=shift['user_id'],vessel_id=ship['id'])
    assert shift['id'] in {r['id'] for r in source['items']}
    assert get('/api/hr/records',kind='shifts',user_id=shift['user_id'],vessel_id=str(uuid4()))['total']==0
    assert get('/api/hr/workspace',**{**params,'vessel_id':str(uuid4())})['records']==[]
    export = client.get('/api/hr/reports/shifts.xlsx',headers=headers,params={**params,'token':hr['report_tokens']['shifts']})
    assert export.status_code == 200, export.text[:120] if export.status_code != 200 else ''
    wrong = client.get('/api/hr/reports/shifts.xlsx',headers=headers,params={
        **params,'vessel_id':str(uuid4()),'token':hr['report_tokens']['shifts']})
    assert wrong.status_code == 409
