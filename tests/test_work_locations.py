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


def test_logbook_location_is_inherited_and_does_not_enable_vessel_access(project):
    from app.browser_logs import BrowserLogs
    from app.log_schema import BUILTINS

    store, actors, _, headers = project
    manager = actors['demo.admin']
    service = BrowserLogs(store, {'hub_id':headers['X-AJ-Hub-ID'], 'supervisor_code':'fictional-test-secret'})
    with store.connection() as con:
        sites={s['code']:s for s in work_locations.catalog(con,manager)}
        grants=con.execute('SELECT count(*) FROM fleet_log_permissions').fetchone()[0]
    ship=sites['DEMO-MERIDIAN']['id']
    base=sites['DEMO-SHORE']['id']
    design=dict(name='Location at creation',description='',definitions=[BUILTINS[0]],work_site_id=base)
    reviewed=service.review(design,manager)
    request=dict(op_id=str(uuid4()),confirmed=True,design=reviewed['design'],review_token=reviewed['review_token'])
    with pytest.raises(Problem) as invalidated:
        service.create(dict(request,design=dict(request['design'],work_site_id=ship)),manager)
    assert invalidated.value.code==409
    saved=service.create(request,manager)
    assert service.create(request,manager)==saved
    book=store.logs.get(saved['id'],manager)
    assert book['vessel_scope']['site_id']==base and not book['vessel_scope']['enabled']
    assert saved['id'] not in {b['id'] for b in store.vessel_logs.books(manager,base)}
    with store.connection() as con:
        assert con.execute('SELECT count(*) FROM fleet_log_permissions').fetchone()[0]==grants
    for invalid in ('',str(uuid4())):
        with pytest.raises(Problem) as error:
            service.review(dict(design,work_site_id=invalid),manager)
        assert error.value.code==422
    with pytest.raises(Problem):
        store.logs.create('Invalid site rollback','',[BUILTINS[0]],manager,work_site_id=str(uuid4()))
    assert 'Invalid site rollback' not in [b['name'] for b in store.logs.list(manager)]
    legacy=store.logs.create('Historical log without a site','',[BUILTINS[0]],manager)
    assert store.logs.get(legacy['id'],manager)['vessel_scope'] is None
    store.vessel_logs.set_scope(manager,legacy['id'],base,0,False,'History belongs to this base',True)
    assert store.logs.get(legacy['id'],manager)['vessel_scope']['site_id']==base

    results=store.global_search.search(manager,'','logs',50,ship)
    assert not results['unavailable']
    assert any(row['href'].startswith('#logentry/') for row in results['items'])
    assert any(row['href'].startswith('#logs/') for row in results['items'])
    assert all([site['id'] for site in row['locations']]==[ship] for row in results['items'])
    assert {saved['id'],legacy['id']}.isdisjoint(row['id'] for row in results['items'])


def test_log_import_uses_selected_location_and_preserves_retry_receipt(project,tmp_path):
    from base64 import b64encode
    from app.builder_hub import BuilderHub
    from app.log_exports import export_bundle

    store, actors, _, headers=project
    manager=actors['demo.admin']
    service=BuilderHub(store, {'hub_id':headers['X-AJ-Hub-ID'], 'supervisor_code':'fictional-test-secret'})
    with store.connection() as con:
        sites={s['code']:s for s in work_locations.catalog(con,manager)}
    original=next(book for book in store.logs.list(manager) if book['name']=='DEMO Meridian Operations Log')
    path=tmp_path/'site-test.ajlogs'
    export_bundle(store,original['id'],manager,path)
    payload={'kind':'logbook','file':{'name':path.name,'data':b64encode(path.read_bytes()).decode()}}
    review=service.preview(payload,manager)
    request=dict(payload,op_id=str(uuid4()),work_site_id=sites['DEMO-SHORE']['id'],review_token=review['review_token'])
    with pytest.raises(Problem) as invalid:
        service.import_file(dict(request,work_site_id=str(uuid4())),manager)
    assert invalid.value.code==422
    saved=service.import_file(request,manager)
    assert service.import_file(request,manager)==saved
    assert saved['id']!=original['id']
    book=store.logs.get(saved['id'],manager)
    assert book['vessel_scope']['site_id']==sites['DEMO-SHORE']['id']
    assert not book['vessel_scope']['enabled']
    with pytest.raises(Problem) as conflict:
        service.import_file(dict(request,work_site_id=sites['DEMO-HORIZON']['id']),manager)
    assert conflict.value.code==409


def test_document_log_import_keeps_its_selected_base(project):
    from base64 import b64encode
    from app.document_import import DocumentImport

    store,actors,_,headers=project
    manager=actors['demo.admin']
    imports=DocumentImport(store,{'hub_id':headers['X-AJ-Hub-ID'],'supervisor_code':'fictional-test-secret'})
    with store.connection() as con:
        sites={site['code']:site['id'] for site in work_locations.catalog(con,manager)}
    file={'name':'training-log.csv','data':b64encode(b'Date,Time,Event\n2026-11-01,05:00,Handover\n').decode()}
    scan=imports.scan(dict(kind='logbook',file=file,language='eng'),manager,None)
    draft=dict(kind='logbook',source=scan['source'],source_token=scan['source_token'],draft=scan['draft'])
    review=imports.reviewed(draft,manager,None)
    request=dict(draft,review_token=review['review_token'],confirmed=True,op_id=str(uuid4()),
                 work_site_id=sites['DEMO-SHORE'],file=file)
    saved=imports.reviewed(request,manager,None,save=True)
    assert imports.reviewed(request,manager,None,save=True)==saved
    book=store.logs.get(saved['id'],manager)
    assert book['vessel_scope']['site_id']==sites['DEMO-SHORE'] and not book['vessel_scope']['enabled']
    with pytest.raises(Problem) as changed:
        imports.reviewed(dict(request,work_site_id=sites['DEMO-HORIZON']),manager,None,save=True)
    assert changed.value.code==409
