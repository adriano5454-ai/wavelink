"""Native inventory positions, whole-list counts and the opt-in HTTP contract."""
from uuid import uuid4

import pytest

from app import work_locations
from app.fieldwork_common import base, put
from app.fleet import _custody
from app.inventory import equipment_sites
from app.store import Problem
from test_work_locations import project  # existing isolated, authenticated native-demo fixture


def test_vessel_catalogue_and_positions(project):
    store, actors, client, headers = project
    admin = actors['demo.admin']
    ship = store.fleet.run('save_site', {'name': 'Vessel São Luís', 'code': 'VSA'}, admin, str(uuid4()))
    other = store.fleet.run('save_site', {'name': 'Vessel Ria', 'code': 'RIA'}, admin, str(uuid4()))
    shore = store.fleet.run('save_site', {'name': 'Base Vale', 'code': 'RIA', 'kind':'shore_base'}, admin, str(uuid4()))
    retired = store.fleet.run('save_site', {'name':'Training Former Vessel','active':False}, admin, str(uuid4()))
    inventory = store.inventory.run('create_list', {'name':'Vessel filter training catalogue'}, admin, str(uuid4()))
    bid = inventory['id']
    with store.connection(True) as c:
        def item(name, **values):
            row = dict(base(admin), list_id=bid, name=name, archived=False, location='Shelf A')
            row.update(values)
            put(c, 'inventory_items', row, bid, True)
            return row['id']
        box = item('Outer box', is_container=True, work_site=ship)
        nested_box = item('Inside box', is_container=True, container_id=box)
        child = item('Meter in box', container_id=nested_box)
        alias = item('Folded name', location=' vessel sao luís ')
        duplicate = item('Ambiguous code', location='ria')
        assigned = item('Assigned explicitly', work_site=other)
        in_transit = item('Dispatched', work_site=ship)
        held_ashore = item('Recently received at base', work_site=ship)
        archived = item('Historical equipment', archived=True, work_site=ship)
        known_retired = item('Historical vessel still referenced', work_site=retired)
        hidden_ref = item('Unknown explicit position', work_site={'id':str(uuid4())}, location='VSA')
        _custody(c, in_transit, dict(state='in_transit', site_id='', origin_id=ship['id'], destination_id=other['id']))
        _custody(c, held_ashore, dict(state='awaiting_placement', site_id=shore['id']))

    default = client.get('/api/inventory/lists', headers=headers).json()
    assert isinstance(default, list) and all('vessel_counts' not in row for row in default)
    cards = client.get('/api/inventory/lists', params={'include_vessels':True}, headers=headers)
    assert cards.status_code == 200, cards.text
    page = cards.json()
    assert all(s['kind'] == 'vessel' for s in page['vessels'])
    assert any(s['id'] == retired['id'] and not s['active'] for s in page['vessels'])
    counts = next(b['vessel_counts'] for b in page['lists'] if b['id'] == bid)
    assert counts == {ship['id']:4, other['id']:1, retired['id']:1}
    details = client.get('/api/inventory/lists/' + bid, headers=headers).json()
    assert details['vessels'] == page['vessels']
    by_id = {i['id']:i for i in details['items']}
    assert all(by_id[i]['vessel_id'] == ship['id'] for i in (box, nested_box, child, alias, archived))
    assert by_id[held_ashore]['equipment_work_site']['id'] == shore['id']
    assert all(not by_id[i]['vessel_id'] for i in (in_transit, duplicate, held_ashore, hidden_ref))
    with store.connection() as c:
        missing = str(uuid4())
        selected = equipment_sites(c, admin, [child, assigned, duplicate, held_ashore, child, missing])
        assert set(selected) == {child, assigned, duplicate, held_ashore}
        assert selected[child]['id'] == ship['id']
        assert selected[held_ashore]['id'] == shore['id']
        assert selected[assigned]['id'] == other['id'] and selected[duplicate] is None
        saved = c.execute('SELECT body FROM inventory_items WHERE id=?', (child,)).fetchone()[0]
        assert 'vessel_id' not in saved and 'equipment_work_site' not in saved
        lookup = work_locations.SiteLookup(work_locations.catalog(c, admin))
        assert lookup.resolve(by_id[child], kind='inventory') == [selected[child]]
    with pytest.raises(Problem):
        store.inventory.list({}, include_vessels=True)
