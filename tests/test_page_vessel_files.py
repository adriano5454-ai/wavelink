"""Exercise the Original Files read model against a fictional authenticated company."""
import json
from hashlib import sha256
from uuid import uuid4

from app import library_import_sources as imports
from app.library_workspace_files import catalogue
from app.original_documents import reference
from app.store import pack
from test_work_locations import project


def library(client, headers):
    response = client.get('/api/original-documents/library?workspaces=true', headers=headers)
    assert response.status_code == 200, response.text
    return response.json()


def test_files_inherit_only_their_accessible_source(project):
    store, actors, client, headers = project
    data = library(client, headers)
    assert all(site['kind'] == 'vessel' for site in data['vessels'])
    ships = {s['code']:s['id'] for s in data['vessels']}
    files = data['workspace_files']
    aurora = {f['group'] for f in files if ships['AUR'] in f['vessel_ids']}
    meridian = {f['group'] for f in files if ships['DEMO-MERIDIAN'] in f['vessel_ids']}
    assert {'it','handovers'} <= aurora
    assert {'fleet','certificates'} <= meridian
    assert all(not f['vessel_ids'] for f in files if f['group'] in ('toolbox','checklist') and '/imports/' in f['url'])
    actor = actors['demo.logistics']
    own = catalogue(store, actor, None, {d['id']:d for d in data['documents']})
    private = {f['url'] for f in files if f['group'] in ('it','handovers')}
    assert private and private.isdisjoint(f['url'] for f in own['workspace_files'])


def test_same_original_can_belong_to_two_vessels_and_imported_book_to_one(project):
    store, _, client, headers = project
    data = library(client, headers)
    by_code = {site['code']:site for site in data['vessels']}
    ships = [by_code['DEMO-HORIZON'], by_code['DEMO-MERIDIAN']]
    with store.connection(True) as c:
        ref = reference(c.execute('SELECT * FROM original_documents LIMIT 1').fetchone())
        jobs = [json.loads(row[0]) for row in c.execute('SELECT body FROM maintenance_jobs ORDER BY id LIMIT 2')]
        assert len(jobs) == 2
        for job, ship in zip(jobs, ships):
            job['template']['source_documents'] = [ref]
            job['work_site'] = ship
            c.execute('UPDATE maintenance_jobs SET body=? WHERE id=?', (pack(job),job['id']))
        book = c.execute('SELECT book_id FROM fleet_log_scope WHERE site_id=? LIMIT 1', (ships[1]['id'],)).fetchone()[0]
        raw = b'An imported book with an allocated vessel'
        imports.retain(c,str(uuid4()),'logbook',dict(id=book,title='Allocated book'), 'allocated-logbook.txt',raw,sha256(raw).hexdigest())
    files = library(client, headers)['workspace_files']
    saved, = [f for f in files if f['original_id'] == ref['id'] and f['group'] == 'maintenance']
    assert set(saved['vessel_ids']) == {s['id'] for s in ships}
    imported, = [f for f in files if f['filename'] == 'allocated-logbook.txt']
    assert imported['vessel_ids'] == [ships[1]['id']]
