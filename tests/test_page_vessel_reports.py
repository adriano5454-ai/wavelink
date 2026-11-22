"""Page-level report searches keep vessel, permission and pagination scopes together."""
import json
from uuid import uuid4

import pytest

from app import work_locations
from app.store import pack
from test_work_locations import project


@pytest.mark.parametrize(('route','table'), [('/api/faults','fault_reports'), ('/api/qshe','qshe_reports')])
def test_report_search_filters_the_entire_register(project, route, table):
    store, actors, client, headers = project
    active = client.get(route, params={'status':'all'}, headers=headers).json()['items']
    assert active
    marker = 'Survey page ' + str(uuid4())
    with store.connection(True) as con:
        vessels = {site['code']:site for site in work_locations.catalog(con,actors['demo.admin'])}
        ship, other, base = (vessels[k] for k in ('DEMO-MERIDIAN','DEMO-HORIZON','DEMO-SHORE'))
        first = json.loads(con.execute(f'SELECT body FROM {table} WHERE id=?',(active[0]['id'],)).fetchone()[0])
        def insert(site, label, location=''):
            row = dict(first, id=str(uuid4()), title=marker+' '+label, work_site=site, location=location)
            con.execute(f'INSERT INTO {table} VALUES(?,?)',(row['id'],pack(row)))
            return row['id']
        ids = {insert(ship,str(i)) for i in range(101)}
        # Older records can carry an exact vessel name or code; a saved ID always wins.
        ids.add(insert(None,'legacy',ship['code'].lower()))
        insert(other,'other',ship['name'])
        insert(dict(id=str(uuid4())),'missing saved ship',ship['code'])
        insert(base,'base',ship['name'])
        insert(None,'unnamed')

    params = {'query':marker,'vessel_id':ship['id'],'status':'all'}
    for offset, size in ((0,100),(100,2)):
        response = client.get(route, headers=headers, params={**params,'offset':offset})
        assert response.status_code == 200, response.text
        page = response.json()
        assert page['total'] == 102 and len(page['items']) == size
        for row in page['items']:
            ids.remove(row['id'])
    assert not ids
    assert client.get(route,headers=headers,params={**params,'query':marker+' legacy'}).json()['total'] == 1
    assert client.get(route,headers=headers,params={**params,'vessel_id':other['id']}).json()['total'] == 1
    for vessel_id in (base['id'],str(uuid4())):
        assert client.get(route,headers=headers,params={**params,'vessel_id':vessel_id}).json()['total'] == 0
    assert client.get(route,headers=headers,params={'query':marker,'status':'all'}).json()['total'] == 106


def test_toolbox_returns_the_accessible_location_directory(project):
    _, _, client, headers = project
    response = client.get('/api/toolbox',headers=headers)
    assert response.status_code == 200, response.text
    sites = client.get('/api/fleet/work-locations',headers=headers).json()['sites']
    assert response.json()['sites'] == sites
