"""Use real intake and download routes with a new, fictional company."""
from hashlib import sha256
from uuid import uuid4

import pytest

from tests.browser_admin.test_admin import h
from tests.test_document_import_ui95 import file, request, review, scan
from tests.ui45_review.test_builder_baseline import grant, import_file, toolbox_package

LIBRARY = '/api/original-documents/library?workspaces=true'


def entries(h, token=None):
    result = h.client.get(LIBRARY, headers=h.headers(token))
    assert result.status_code == 200, result.text
    return result.json()['workspace_files']


@pytest.mark.parametrize('kind', ['checklist', 'toolbox'])
def test_confirmed_source_keeps_exact_bytes_in_its_workspace(h, kind):
    name = 'crew-file.txt'
    raw = b'Crew briefing\n# Handover\n- Read the shift log\n- Check the noticeboard'
    scanned = scan(h, name, raw, kind=kind)
    if kind == 'toolbox':
        scanned['draft']['declaration'] = 'I understood the crew briefing.'
        scanned['draft']['questions'] = 'Where is the shift log?'
    checked = review(h, scanned)
    assert not [item for item in entries(h) if item['filename'] == name]
    payload = request(scanned, op_id=str(uuid4()), confirmed=True, review_token=checked['review_token'],
                      file=file(name,raw[:-1]+b'!'))
    def confirm():
        return h.client.post('/api/builders/document/action', headers=h.headers(), json=payload)
    assert confirm().status_code == 409
    with h.store.connection() as db:
        assert not db.execute('SELECT 1 FROM workspace_file_imports').fetchone()
    payload['file'] = file(name, raw)
    saved = confirm()
    assert saved.status_code == 200, saved.text
    assert saved.json()['source_folder'] == kind
    assert confirm().json() == saved.json()
    items = [item for item in entries(h) if item['filename'] == name]
    assert len(items) == 1
    item = items[0]
    assert (item['group'],item['size'],item['sha256']) == (kind,len(raw),sha256(raw).hexdigest())
    assert item['record'].endswith('/'+saved.json()['id'])
    response = h.client.get(item['url'], headers=h.headers())
    assert response.status_code == 200 and response.content == raw
    assert response.headers['cache-control'] == 'no-store'


def test_package_source_respects_both_permissions(h):
    raw = toolbox_package()
    saved, payload = import_file(h, None, 'toolbox', 'briefing.ajtoolbox', raw)
    again = h.client.post('/api/builders/import/action', headers=h.headers(), json=payload)
    assert again.json() == saved
    item, = [r for r in entries(h) if r['filename'] == 'briefing.ajtoolbox']
    assert h.client.get(item['url'], headers=h.headers()).content == raw
    assert h.client.get(item['url']).status_code == 401
    from tests.browser_admin.test_admin import user, version_payload, post
    member = user(h)
    flags = dict(member['policy']['permissions'], **{'originals.view':True, 'builders.toolbox':False})
    assert post(h,'permissions',dict(**version_payload(member),permissions=flags,backup_confirmed=False)).status_code == 200
    token, _ = h.accounts.login('training.worker',h.pw,'read-files')
    assert item['url'] not in {r['url'] for r in entries(h, token)}
    assert h.client.get(item['url'], headers=h.headers(token)).status_code == 403
    token, _ = grant(h,'builders.toolbox','originals.view')
    assert item['url'] in {r['url'] for r in entries(h, token)}
    assert h.client.get(item['url'], headers=h.headers(token)).content == raw
    member = user(h)
    flags = dict(member['policy']['permissions'], **{'originals.view':False})
    assert post(h,'permissions',dict(**version_payload(member),permissions=flags,backup_confirmed=False)).status_code == 200
    token, _ = h.accounts.login('training.worker',h.pw,'restricted-files')
    assert h.client.get(LIBRARY, headers=h.headers(token)).status_code == 403
    assert h.client.get(item['url'],headers=h.headers(token)).status_code == 403


def test_selective_exports_keep_only_jointly_selected_workspace_originals(h, tmp_path):
    import sqlite3
    from app.project_modules import prune_snapshot
    raw = toolbox_package()
    import_file(h, None, 'toolbox', 'briefing.ajtoolbox', raw)
    for n, (selected, expected) in enumerate([
        (['toolbox','documents'],1), (['documents'],0), (['toolbox'],0),
    ]):
        target = tmp_path / ('export-'+str(n)+'.sqlite')
        with h.store.connection() as source, sqlite3.connect(target) as destination:
            source.backup(destination)
        prune_snapshot(target, selected)
        with sqlite3.connect(target) as exported:
            assert exported.execute('SELECT count(*) FROM workspace_file_imports').fetchone()[0] == expected
    assert any(item['filename'] == 'briefing.ajtoolbox' for item in entries(h))
