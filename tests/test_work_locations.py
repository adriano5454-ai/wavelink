from pathlib import Path
from uuid import uuid4
import json

import pytest
from starlette.testclient import TestClient

from app.store import Problem, pack
from app import work_locations
from deploy.gate import Gate
from deploy.native_showcase import NativeShowcase


@pytest.fixture(scope='module')
def project():
    gate = Gate('https://demo.example.test','fictional-demo-password',b's'*32,'guest.demo','fictional-pass',public_entry=True)
    show = NativeShowcase(gate,Path(__file__).resolve().parents[1]/'vendor/FICTIONAL_DEMO.ajproject')
    gate.showcase = show
    store = show.core.state.store
    actors = {}
    with store.connection() as c:
        for row in c.execute("SELECT id,login_id FROM users WHERE login_id LIKE 'demo.%'"):
            actors[row['login_id']] = show.core.state.accounts.session_person_in_connection(c,row['id'])
    with TestClient(gate.app(),base_url=gate.origin) as client:
        auth=show.admission()
        yield store,actors,client,{'Authorization':'Bearer '+auth['token'],'X-AJ-Hub-ID':auth['hub_id']}
    show.temp.cleanup()


def test_filter_and_keyword_cover_native_sources(project):
    store,actors,client,headers=project
    response=client.get('/api/fleet/work-locations',headers=headers)
    assert response.status_code==200,response.text
    sites=response.json()['sites']
    assert all(set(s)=={'name','kind','code','active','id'} for s in sites)
    ship=next(s for s in sites if s['code']=='DEMO-MERIDIAN')
    response=client.get('/api/search',params={'site_id':ship['id'],'limit':50},headers=headers)
    assert response.status_code==200,response.text
    found=response.json()
    assert found['unavailable']==[]
    assert {'tasks','maintenance','faults','qshe','checklists','toolbox'} <= {r['kind'] for r in found['items']}
    assert all(ship['id'] in {loc['id'] for loc in r['locations']} for r in found['items'])
    words=client.get('/api/search',params={'q':'meridian','kinds':'tasks,faults,maintenance'},headers=headers).json()
    assert {'tasks','faults','maintenance'} == {r['kind'] for r in words['items']}
    aurora=next(s for s in sites if s['code']=='AUR')
    company=client.get('/api/search',params={'site_id':aurora['id'],'limit':50},headers=headers).json()
    assert company['unavailable']==[]
    assert {'it','handovers','tasks','hr'} <= {r['kind'] for r in company['items']}
    assert client.get('/api/search',params={'site_id':str(uuid4())},headers=headers).status_code==404
    assert client.get('/api/search',params={'q':''},headers=headers).status_code==422


def test_write_replay_rename_and_retirement(project):
    store,actors,client,headers=project
    a=actors['demo.admin']
    site=store.fleet.run('save_site',dict(name='Base São Tomé',kind='shore_base',code='STB'),a,str(uuid4()))
    fields=dict(kind='general',title='Inspect the training rack',instructions='Check the training label against the list.',
                assignee_ids=[a['user_id']],priority='normal',confirmed=True,work_site_id=site['id'])
    op=str(uuid4())
    task=store.tasks.run('create_general',fields,a,op)
    assert store.tasks.run('create_general',fields,a,op)['id']==task['id']
    assert task['work_site']['id']==site['id']
    assert store.global_search.search(a,'sao tome','tasks')['items'][0]['id']==task['id']
    wrong=fields | {'work_site_id':str(uuid4())}
    with pytest.raises(Problem) as exc:store.tasks.run('create_general',wrong,a,str(uuid4()))
    assert exc.value.code==422
    fault=store.faults.run('create',dict(title='Marker damaged',description='Marker on the training rack needs checking.',
                          priority='normal',department_id='',work_site_id=site['id']),a,str(uuid4()))
    assert fault['work_site']['id']==site['id']
    with store.connection() as c:
        count=c.execute('SELECT count(*) FROM fault_reports').fetchone()[0]
    with pytest.raises(Problem):store.faults.run('create',{'title':'X','description':'X','work_site_id':'wrong'},a,str(uuid4()))
    with store.connection() as c:
        assert count==c.execute('SELECT count(*) FROM fault_reports').fetchone()[0]
    changed=store.fleet.run('save_site',dict(id=site['id'],version=site['version'],name='South survey base',kind='shore_base',code='STB',active=False,reason='Test retirement'),a,str(uuid4()))
    rows=store.global_search.search(a,'South survey base','tasks,faults')['items']
    assert {r['id'] for r in rows}=={task['id'],fault['id']}
    assert all(r['locations'][0]['name']==changed['name'] for r in rows)
    with pytest.raises(Problem) as exc:store.tasks.run('create_general',fields,a,str(uuid4()))
    assert exc.value.code==422
    private=store.global_search.search(actors['demo.shift2'],'','tasks',50,site['id'])
    assert task['id'] not in {r['id'] for r in private['items']}


def test_location_search_continues_past_first_native_fault_page(project):
    store,actors,_,_=project
    a=actors['demo.admin']
    with store.connection(True) as c:
        ship=next(s for s in work_locations.catalog(c,a) if s['code']=='DEMO-HORIZON')
        sample=json.loads(c.execute('SELECT body FROM fault_reports LIMIT 1').fetchone()[0])
        for i in range(106):
            row={**sample,'id':str(uuid4()),'title':f'Bulk survey marker {i:03}','work_site':ship}
            c.execute('INSERT INTO fault_reports VALUES(?,?)',(row['id'],pack(row)))
    seen=[]
    for offset in (0,40,80):
        data=store.global_search.search(a,'bulk survey','faults',40,ship['id'],offset)
        assert data['total']==106 and not data['unavailable']
        seen.extend(r['id'] for r in data['items'])
    assert len(set(seen))==106
