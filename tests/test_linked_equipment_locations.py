"""Exercise native equipment links and frozen operational locations in a fictional project."""
from uuid import uuid4

import pytest

from app.store import Problem
from test_work_locations import project


def test_equipment_links_share_location_and_keep_record_history(project):
    store, actors, _, _ = project
    admin = actors['demo.admin']

    def run(service, action, **payload):
        return service.run(action, payload, admin, str(uuid4()))

    ship = run(store.fleet, 'save_site', name='Verification Vessel', kind='vessel')
    base = run(store.fleet, 'save_site', name='Verification Warehouse', kind='warehouse')
    book = run(store.inventory, 'create_list', name='Equipment site checks')
    gear = run(store.inventory, 'save_item', list_id=book['id'], work_site_id=ship['id'],
               values={'name':'Ranging instrument'})
    link = {'id':gear['id'], 'version':gear['version']}
    task_payload = dict(title='Inspect ranging instrument', instructions='Inspect the label.',
                        assignee_ids=[admin['user_id']], confirmed=True, context_link={'kind':'asset', **link})
    fault_payload = dict(title='Ranging instrument connector', description='Connector cover is missing.',
                         confirmed=True, asset_link=link)

    for service in (store.faults, store.qshe):
        assert service.links(admin, 'asset', gear['name'])['items'][0]['work_site']['id'] == ship['id']
    assert store.tasks.link_options(admin, 'asset', gear['name'])['items'][0]['work_site']['id'] == ship['id']
    assert store.assets.get(gear['id'], admin)['item']['equipment_work_site']['id'] == ship['id']
    for group in (store.assets.directory(admin)['inventories'], store.tasks.directory(admin)['inventories']):
        options = next(b for b in group if b['id']==book['id'])['items']
        assert options[0]['work_site']['id'] == ship['id']
    assert next(x for x in store.certificates.directory(admin)['items'] if x['id']==gear['id'])['work_site']['id'] == ship['id']

    task = run(store.tasks, 'create_general', **task_payload, equipment_site_hint=ship['id'])
    report = run(store.faults, 'create', **fault_payload)
    observation = run(store.qshe, 'create', **fault_payload, equipment_site_hint=ship['id'])
    routine = next(r for r in store.maintenance.list(admin)['routines'] if r['revision'] and not r['archived'])
    order = run(store.maintenance, 'create_job', name='Test work order', routine_id=routine['id'],
                revision=routine['revision'], asset_id=gear['id'], asset_name=gear['name'])
    cert_values = dict(title='Equipment record', asset_ids=[gear['id']])
    cert = run(store.certificates, 'save', values=cert_values)
    stock = run(store.tasks, 'create', title='Verify instrument', list_id=book['id'], item_ids=[gear['id']],
                assignee_ids=[admin['user_id']], equipment_site_hint=ship['id'])
    count = store.inventory.count(stock['count_id'], admin)
    for record in (task, report, observation, order, cert, stock, count):
        assert record['work_site']['id'] == ship['id']
    assert task['id'] in {r['id'] for r in store.global_search.search(admin, 'ranging instrument', 'tasks', 30, ship['id'])['items']}

    # Deliberately report work at an alternate site. The equipment itself stays onboard.
    assert run(store.faults, 'create', **fault_payload, work_site_id=base['id'])['work_site']['id'] == base['id']
    moved = run(store.inventory, 'save_item', list_id=book['id'], id=gear['id'], version=gear['version'],
                work_site_id=base['id'], values={'name':gear['name']})
    fresh_link = dict(id=moved['id'], version=moved['version'])
    assert store.tasks.get(task['id'], admin)['work_site']['id'] == ship['id']
    assert store.maintenance.get(order['id'], admin)['work_site']['id'] == ship['id']
    task_on_order = run(store.tasks, 'create_general', **{**task_payload, 'context_link':{
        'kind':'maintenance','id':order['id'],'version':order['version']}})
    assert task_on_order['work_site']['id'] == ship['id']
    with pytest.raises(Problem) as stale:
        run(store.faults, 'create', **{**fault_payload, 'asset_link':fresh_link}, equipment_site_hint=ship['id'])
    assert stale.value.code == 409
    assert run(store.faults, 'create', **{**fault_payload, 'asset_link':fresh_link})['work_site']['id'] == base['id']

    no_site = run(store.inventory, 'save_item', list_id=book['id'], values={'name':'Unallocated recorder'})
    second = run(store.inventory, 'save_item', list_id=book['id'], work_site_id=ship['id'],
                 values={'name':'Second onboard recorder'})
    for other in (second, no_site):
        mixed = {'title':'Mixed equipment', 'asset_ids':[moved['id'], other['id']]}
        assert not run(store.certificates, 'save', values=mixed)['work_site']
        with pytest.raises(Problem) as mismatch:
            run(store.certificates, 'save', values=mixed, equipment_site_hint=base['id'])
        assert mismatch.value.code == 409
        assert run(store.certificates, 'save', values=mixed, work_site_id=ship['id'])['work_site']['id'] == ship['id']
