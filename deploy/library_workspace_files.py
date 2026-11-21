"""Project source files into workspace folders without copying private attachments."""
import json
from itertools import chain
from urllib.parse import quote

from . import library_import_sources as imports
from .access import effective
from .fieldwork_common import member
from .original_folders import OriginalFolders
from .store import Problem


def present(group, title, file, endpoint, record='', *, archived=False, at='', linked=''):
    return dict(group=group, title=title, filename=file['filename'], mime=file['mime'],
                size=file['size'], sha256=file['sha256'], url=endpoint, record=record,
                archived=bool(archived), imported_at=file.get('added_at') or file.get('created_at') or at,
                original_id=linked)


def records_with(c, table, field):
    # Both identifiers are internal constants, never request parameters.
    for row in c.execute(f"SELECT body FROM {table} WHERE json_array_length(body, ?) > 0", ('$.'+field,)):
        yield json.loads(row[0])


def authorised(check, *args):
    try:
        check(*args)
        return True
    except Problem as exc:
        if exc.code in (403, 404):
            return False
        raise


def private_files(c, store, actor, caps):
    if caps.get('hr.view_own'):
        from .hr import current
        user, rights = current(c, actor)
        for rec in records_with(c, 'hr_records', 'attachments'):
            if not store.hr._read_allowed(rec, user, rights):
                continue
            kind, rid = rec['kind'], rec['id']
            for file in rec['attachments']:
                yield present('hr-'+kind, rec['title'], file, f"/api/hr/{kind}/{rid}/files/{file['id']}",
                              '#hr/staff/'+rec['user_id'], archived=rec.get('archived'), at=rec['updated_at'])
    if caps.get('it.view_own'):
        from .it_requests import current
        user, manage = current(c, actor)
        for rec in records_with(c, 'it_request_records', 'attachments'):
            if authorised(store.it_requests._read, rec, user, manage):
                for file in rec['attachments']:
                    yield present('it', rec['title'], file, f"/api/it/requests/{rec['id']}/files/{file['id']}",
                                  '#it/requests/'+rec['id'], at=rec['updated_at'])
    if caps.get('qshe.view'):
        from .qshe_reports import allowed
        for rec in records_with(c, 'qshe_reports', 'evidence'):
            if allowed(c, rec, actor):
                for file in rec['evidence']:
                    yield present('qshe', rec['title'], file, f"/api/qshe/{rec['id']}/evidence/{file['id']}",
                                  '#qshe/'+rec['id'], archived=rec.get('archived'), at=rec.get('updated_at',''))
    if caps.get('handovers.view'):
        from .context_documents import ContextDocuments
        context = ContextDocuments(store)
        for author, in c.execute("""SELECT DISTINCT r.author_id FROM handover_records r
                JOIN asset_files f ON f.owner_id=r.id WHERE f.owner_kind='handover'"""):
            for doc in context._authored_handovers(c, author, actor, caps):
                rev = doc['publication_revision']
                query = '?draft=true' if doc['draft'] else '?revision='+str(rev)
                route = '#handover/'+doc['id']+('' if doc['draft'] else '/'+str(rev))
                for file in doc['files']:
                    yield present('handovers', doc['title'], file, f"/api/handovers/{doc['id']}/attachments/{file['id']}{query}",
                                  route, archived=doc.get('archived'))


def operational_files(c, store, actor, caps, originals):
    if caps.get('certificates.view'):
        for rec in records_with(c, 'asset_certificates', 'attachments'):
            for file in rec['attachments']:
                yield present('certificates', rec['title'], file, f"/api/certificates/{rec['id']}/files/{file['id']}",
                              '#certificates/'+rec['id'], archived=rec.get('archived'))
    if caps.get('inventory.view'):
        from .fieldwork_common import raw
        for profile in records_with(c, 'asset_profiles', 'photos'):
            item = raw(c, 'inventory_items', profile['id'])
            for file in profile['photos']:
                yield present('inventory', item['name'], file, f"/api/assets/{item['id']}/photos/{file['id']}",
                              '#asset/'+item['id'], archived=item.get('archived'))
    from .fleet import _get, _manifest_access
    if authorised(store.fleet._person, c, actor):
        for mid, in c.execute('SELECT DISTINCT manifest_id FROM fleet_files'):
            manifest = _get(c, 'fleet_manifests', mid)
            if authorised(_manifest_access, c, manifest, actor):
                for file in store.fleet._files(c, mid):
                    yield present('fleet', manifest['title'], file, f"/api/fleet/manifests/{mid}/files/{file['id']}",
                                  '#fleet/manifest/'+mid)

    def referenced(group, template, route):
        for ref in (template or {}).get('source_documents', []):
            doc = originals.get(ref['id'])
            if doc and doc['sha256'] == ref['sha256']:
                yield present(group, doc['title'], doc, '/api/original-documents/'+doc['id']+'/file', route,
                              archived=doc['archived'], at=doc['imported_at'], linked=doc['id'])

    if caps.get('checklists.view'):
        from .context_checklist_documents import _record_documents, _reader
        person = _reader(c, actor)
        for key, in c.execute("""SELECT id FROM records r WHERE COALESCE(json_type(body,'$.deleted'),'null') IN ('null','false')
                AND (json_array_length(body,'$.template.source_documents') > 0
                OR EXISTS (SELECT 1 FROM json_each(r.body,'$.template.media'))
                OR EXISTS (SELECT 1 FROM ops_photo_evidence p WHERE p.record_id=r.id))"""):
            try:
                record = store._get(c, key)
            except Problem as exc:
                if exc.code in (404, 410):
                    continue
                raise
            for doc in _record_documents(store, c, record, actor, person):
                if doc['kind'] == 'checklist_original':
                    ref = originals.get(doc['id'])
                    if ref:
                        yield present('checklist', ref['title'], ref, '/api/original-documents/'+ref['id']+'/file',
                                      '#dive/'+key+'/'+doc['sources'][0]['phase'], linked=ref['id'],
                                      archived=ref['archived'], at=ref['imported_at'])
                    continue
                route = '#dive/'+key+'/'+doc['phase']
                for file in doc['files']:
                    url = (f"/api/records/{key}/photos/{file['id']}" if doc['kind']=='checklist_evidence' else
                           f"/api/context-documents/checklists/{key}/guidance/{file['id']}")
                    yield present('checklist', doc['title'], file, url, route, at=record.get('updated_at',''))
    if caps.get('maintenance.view'):
        from .maintenance import all_steps
        for body, in c.execute('SELECT body FROM maintenance_jobs'):
            job = json.loads(body)
            route = '#maintenance/'+job['id']
            yield from referenced('maintenance', job['template'], route)
            for step in all_steps(job['template']):
                entry = job['checks'].get(step['key'], {})
                for photo in entry.get('photos', []):
                    row = c.execute('SELECT mime,digest,length(content) FROM ops_photo_evidence WHERE id=? AND record_id=? AND phase=? AND item_id=?',
                                    (photo['id'],job['id'],step['phase'],step['definition']['id'])).fetchone()
                    if row:
                        file = dict(filename='evidence-'+photo['id']+'.jpg', mime=row[0],sha256=row[1],size=row[2])
                        yield present('maintenance', job['name'], file, f"/api/maintenance/jobs/{job['id']}/photos/{photo['id']}",
                                      route, at=job.get('updated_at',''))
    if caps.get('logs.references'):
        from .context_log_documents import _body
        from .logs import member as log_member
        from .vessel_logs import require_book
        user = log_member(c, actor)
        for ref in c.execute('SELECT id,book_id,sheet_name,released,body,reviewed_at FROM ops_log_references'):
            if (user['role']!='admin' and not ref['released']) or not authorised(require_book,c,actor,ref['book_id'],'logs.references'):
                continue
            for img in _body(ref['body']).get('images',[]):
                sha = img['sha256']
                row = c.execute('SELECT mime,length(data) FROM ops_log_media WHERE sha256=?',(sha,)).fetchone()
                if row:
                    ext = {'image/png':'png','image/jpeg':'jpg','image/gif':'gif'}[row[0]]
                    file = dict(filename='reference-'+sha[:16]+'.'+ext, mime=row[0], sha256=sha, size=row[1])
                    yield present('logbook', ref['sheet_name'], file, f"/api/logs/references/{ref['id']}/images/{sha}",
                                  '#logs/'+ref['book_id'], at=ref['reviewed_at'])


def catalogue(store, actor, token, originals):
    from .builder_hub import KINDS
    with store.connection() as c:
        OriginalFolders._authorise(c, actor)
        user = member(c, actor, 'originals.view')
        caps = effective(c, user['id'], user['role'])
        items = {}
        for row in chain(private_files(c, store, actor, caps), operational_files(c, store, actor, caps, originals)):
            items[row['group'], row['url']] = row
        destinations = []
        for group, (permission, *unused) in KINDS.items():
            if not caps.get(permission) or not authorised(imports.allowed,c,actor,token,group):
                continue
            destinations.append(group)
            for row in c.execute('SELECT id,record_id,title,filename,mime,size,sha256,added_at FROM workspace_file_imports WHERE kind=?',(group,)):
                file = dict(row)
                url = '/api/original-documents/imports/'+file['id']+'/file'
                items[group,url] = present(group, file['title'], file, url, import_route(group,file['record_id']))
        return dict(workspace_files=list(items.values()), workspace_imports=destinations)


def import_route(group, rid):
    if group in ('toolbox','checklist','maintenance'):
        return '#admin/templates/saved/'+group+'/'+rid
    return ('#admin/logbooks/saved/' if group=='logbook' else '#inventory/')+rid


def attach(app, store, credentials):
    from fastapi import Depends, Request
    from fastapi.responses import Response
    with store.connection(True) as c:
        imports.ensure(c)

    @app.get('/api/original-documents/imports/{file_id}/file')
    def read(file_id: str, req: Request, person=Depends(credentials)):
        raw, mime, name = imports.original_bytes(store, person, req.headers['authorization'].removeprefix('Bearer '), file_id)
        return Response(raw, media_type=mime, headers={'Cache-Control':'no-store', 'X-Content-Type-Options':'nosniff',
                        'Content-Security-Policy':"default-src 'none'; sandbox",
                        'Content-Disposition':"attachment; filename*=UTF-8''"+quote(name,safe='')})
