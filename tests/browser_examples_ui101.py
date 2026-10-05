"""Actual C01 browser imports of external examples in a disposable company.

Set WAVELINK_IMPORT_WORKBOOK and WAVELINK_IMPORT_LOGS to the supplied files.
Neither example is bundled. IndexedDB is real; WebSocket connections and service
worker registration are suppressed. Native package compaction uses a real Worker.
"""
import base64
import copy
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
from test_company_c01 import PASS, activate, client, instance

OUT = Path(os.environ.get('WAVELINK_UI101_EVIDENCE_DIR', '/tmp/wavelink-ui101/evidence/examples'))


def fixture(key):
    value = os.environ.get(key, '')
    path = Path(value) if value else None
    if path is None or not path.is_file():
        raise SystemExit('Set ' + key + ' to the supplied example; source files are not bundled.')
    return path


def mapped_rows(page):
    return list(csv.DictReader(io.StringIO(page.locator('#di-inventory_rows').input_value()), delimiter='\t'))


def main():
    workbook = fixture('WAVELINK_IMPORT_WORKBOOK')
    logs = fixture('WAVELINK_IMPORT_LOGS')
    with zipfile.ZipFile(logs) as source:
        source_log = json.loads(source.read('logbook.json'))
    expected_definitions = source_log['definitions']
    expected_omitted = {key: len(source_log[key]) for key in ('entries', 'history', 'references', 'media')}
    assert expected_omitted == {'entries': 561, 'history': 562, 'references': 30, 'media': 216}
    del source_log
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'checks': [], 'errors': [], 'widths': [1440, 390, 320], 'method': 'Actual fictional C01 HostedBoundary/CompanyAccess/core APIs, Chromium IndexedDB and native package Worker. Service-worker registration and WebSockets are suppressed.'}
    source_root = Path(os.environ['WAVELINK_TEST_SOURCE'])
    tracked = ('app/document_import.py', 'app/document_extract.py', 'app/builder_hub.py', 'app/static/document_import.js', 'app/static/document_import.css', 'app/static/setup_builders.js', 'app/static/admin_workspace_ui75.css', 'app/static/log_package_worker.js')
    report['source_hashes'] = {name: hashlib.sha256((source_root / name).read_bytes()).hexdigest() for name in tracked}
    report['served_asset_hashes'] = {}

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui101-examples-') as td:
        installation = instance.__wrapped__(Path(td))
        with client(installation) as c, sync_playwright() as pw:
            activate(c)
            origin = installation[2].external_origin
            store = c.app.state.core.state.store
            browser = pw.chromium.launch(headless=True, args=['--no-sandbox'])
            p = browser.new_page(viewport={'width': 1440, 'height': 1000})
            p.set_default_timeout(30000)
            p.on('pageerror', lambda error: report['errors'].append(str(error)))
            p.on('dialog', lambda dialog: dialog.accept())
            p.add_init_script("""class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();""")
            exchanges = []

            def route(r):
                req = r.request
                u = urlsplit(req.url)
                path = u.path + ('?' + u.query if u.query else '')
                response = c.request(req.method, path, headers=req.headers, content=req.post_data_buffer)
                if ('app' + u.path) in tracked and response.status_code == 200:
                    report['served_asset_hashes']['app' + u.path] = hashlib.sha256(response.content).hexdigest()
                if u.path.startswith('/api/builders/'):
                    exchanges.append({'path': u.path, 'status': response.status_code, 'request': json.loads(req.post_data or '{}'), 'request_bytes': len(req.post_data_buffer or b''), 'response': response.json()})
                r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

            p.route(origin + '/**', route)

            def latest(suffix):
                return next(row for row in reversed(exchanges) if row['path'].endswith(suffix))

            def counts():
                with store.connection() as con:
                    return {table: con.execute('SELECT count(*) FROM ' + table).fetchone()[0] for table in ('users', 'inventory_lists', 'inventory_items', 'inventory_counts', 'ops_logbooks', 'ops_log_entries', 'ops_log_audit', 'ops_log_references', 'ops_log_media', 'records')}

            def builder():
                p.evaluate("()=>{location.hash='#builders';render();}")
                expect(p.locator('#sb-document')).to_be_visible()
                p.locator('#sb-document').click()

            def show_top(locator):
                locator.evaluate('node=>node.scrollIntoView({block:"start"})')
                p.evaluate('()=>scrollBy(0,-80)')

            def screenshot(name, locator):
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    show_top(locator)
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name, width)
                    p.screenshot(path=str(OUT / (name + '_' + str(width) + '.png')))
                    ok(name.replace('_', ' ') + ' aligns at ' + str(width) + 'px without horizontal page overflow')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            def checked_inventory():
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                assert latest('/document/review')['status'] == 200, latest('/document/review')['response']
                assert p.locator('#sb-import-save').is_disabled()
                p.locator('#di-confirm').check()
                expect(p.locator('#sb-import-save')).to_be_enabled()

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                session_before = p.evaluate('({token:state.auth.token,user:state.auth.person.user_id,hub:state.hub_id})')
                before = counts()
                builder()
                p.locator('#sb-file').set_input_files(str(workbook))
                expect(p.locator('#di-sheet')).to_be_visible(timeout=90000)
                expect(p.locator('#sb-review')).to_be_enabled()
                scanned = latest('/document/scan')['response']
                assert scanned['kind'] == 'inventory'
                assert p.locator('#di-sheet').input_value() == 'All Source Items'
                assert {sheet['name'] for sheet in scanned['sheets']} == {'Source Reconciliation', 'All Source Items', 'Location Review'}
                roles = {sheet['name']: sheet for sheet in scanned['sheets']}
                assert roles['All Source Items']['role'] == 'data' and roles['All Source Items']['recommended']
                assert roles['Source Reconciliation']['role'] == 'summary'
                assert roles['Location Review']['role'] == 'review'
                assert p.locator('[data-di-column="8"]').input_value() == '8'
                rows = mapped_rows(p)
                assert len(rows) == 315
                assert sum(not row['location'] for row in rows) == 92
                assert all(not row['quantity'] and not row['is_container'] and not row['container_ref'] for row in rows)
                assert all(row['notes'] for row in rows)
                assert all('Source tab' in row['notes'] and 'Excel row' in row['notes'] for row in rows)
                assert any('Owning department' in row['notes'] for row in rows)
                assert any('Onboard date' in row['notes'] for row in rows)
                assert any('Source verification' in row['notes'] for row in rows)
                assert counts() == before
                ok('Workbook defaults to 315-row data worksheet; summary and eight review rows remain separate source sheets')
                ok('Imported location maps physical locations with 92 unassigned rows, unknown quantities and no inferred boxes')
                ok('Unmapped workbook/tab/row/department/date/verification evidence remains in source notes without asserting verification')
                screenshot('workbook_roles', p.locator('#di-sheet-role'))
                screenshot('workbook_mapping', p.locator('.di-mapping h3'))

                checked_inventory()
                p.locator('[data-di-column="8"]').select_option('7')
                assert p.locator('#sb-import-save').is_disabled() and not p.locator('#di-confirm').is_checked()
                p.locator('#sb-review').click()
                expect(p.locator('#sb-result')).to_contain_text('Apply')
                p.locator('#di-map').click()
                assert len(mapped_rows(p)) == 315
                p.locator('[data-di-column="8"]').select_option('8')
                p.locator('#di-map').click()
                assert sum(not row['location'] for row in mapped_rows(p)) == 92
                ok('Custom mapping edits invalidate review and require Apply; restoring physical location retains every data row')
                p.locator('#di-sheet').select_option('Location Review')
                assert len(mapped_rows(p)) == 8
                p.locator('#di-sheet').select_option('All Source Items')
                assert len(mapped_rows(p)) == 315
                assert p.locator('#sb-import-save').is_disabled()
                ok('Explicit review-sheet selection replaces only the unsaved proposal and never appends audit rows')
                checked_inventory()
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                inventory_result = latest('/document/action')['response']
                person = store.session(p.evaluate('state.auth.token'))
                inventory = store.inventory.get(inventory_result['id'], person)
                assert len(inventory['items']) == 315
                assert sum(row['location'] == 'Unassigned' for row in inventory['items']) == 92
                assert all(row['quantity'] is None and not row['is_container'] and not row['container_id'] for row in inventory['items'])
                assert not inventory['counts'] and all(row['notes'] for row in inventory['items'])
                assert counts()['inventory_lists'] == before['inventory_lists'] + 1
                assert counts()['records'] == before['records']
                ok('Actual company API persists one separate 315-item inventory with source notes and no verification history')
                p.locator('#sb-done').click()

                # Native package checks are completed below once the small,
                # permission-scoped worker result has been server reviewed.
                native_checks(p, c, store, logs, expected_definitions, expected_omitted, counts, before, latest, exchanges, builder, screenshot, ok)
                edge_checks(p, exchanges, counts, builder, ok)
                assert p.evaluate('({token:state.auth.token,user:state.auth.person.user_id,hub:state.hub_id})') == session_before
                assert counts()['users'] == before['users']
                ok('Imports preserve the existing named account, authenticated session and company scope')
                assert all(hashlib.sha256((source_root / name).read_bytes()).hexdigest() == sha for name, sha in report['source_hashes'].items()), 'Source files changed during acceptance; rerun against one frozen version.'
                assert all(sha == report['source_hashes'][name] for name, sha in report['served_asset_hashes'].items())
                assert not report['errors'], report['errors']
            except Exception:
                p.screenshot(path=str(OUT / 'failure.png'), full_page=True)
                print(json.dumps({'status': p.locator('#sb-result').inner_text() if p.locator('#sb-result').count() else '', 'api': [{'path': row['path'], 'status': row['status'], 'request_bytes': row['request_bytes']} for row in exchanges[-8:]], 'errors': report['errors']}))
                raise
            finally:
                report['summary'] = {'checks_passed': len(report['checks']), 'unexpected_errors': len(report['errors']), 'widths': report['widths']}
                (OUT / 'UI101_EXAMPLES_BROWSER_REVIEW.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


def native_checks(p, c, store, logs, expected_definitions, expected_omitted, counts, before, latest, exchanges, builder, screenshot, ok):
    builder()
    assert '.ajlogs' in p.locator('#sb-file').get_attribute('accept')
    p.locator('#sb-file').set_input_files(str(logs))
    expect(p.locator('#sb-preview h3')).to_have_text('Check this import', timeout=90000)
    expect(p.locator('#sb-import-save')).to_be_enabled()
    checked = latest('/import/review')
    assert checked['status'] == 200, checked['response']
    assert checked['request']['kind'] == checked['response']['kind'] == 'logbook'
    assert 'logbook' in p.locator('#sb-work .sb-form-heading .eyebrow').inner_text().lower()
    summary = checked['response']['summary']
    assert summary['sections'] == 9 and summary['fields'] == 103
    assert {key: summary['omitted_' + key] for key in expected_omitted} == expected_omitted
    assert summary['original_filename'] == logs.name and summary['original_bytes'] == logs.stat().st_size
    assert summary['original_sha256'] == hashlib.sha256(logs.read_bytes()).hexdigest()
    assert checked['request_bytes'] < 100_000 and checked['response']['bytes'] < 100_000
    prepared = base64.b64decode(checked['request']['file']['data'])
    with zipfile.ZipFile(io.BytesIO(prepared)) as z:
        manifest = json.loads(z.read('manifest.json'))
        clean = json.loads(z.read('logbook.json'))
    assert clean['definitions'] == expected_definitions
    assert all(not clean[key] for key in expected_omitted)
    assert manifest['options'] == {'entries': False, 'references': False, 'pictures': False}
    assert set(clean['source_manifest']) == {'browser_local_definitions'}
    assert clean['source_manifest']['browser_local_definitions']['omitted'] == expected_omitted
    assert counts()['ops_logbooks'] == before['ops_logbooks']
    assert len([row for row in exchanges if row['path'] == '/api/builders/import/review']) == 1
    ok('Generic Import identifies the 44.94 MB native logbook and its real Worker uploads only a small form-design package')
    ok('Nine sections and 103 fields preserve exact labels, types, units, required flags and choices; saved values and reference contents stay local')
    assert '561' in p.locator('#sb-preview').inner_text() and '562' in p.locator('#sb-preview').inner_text()
    assert '30' in p.locator('#sb-preview').inner_text() and '216' in p.locator('#sb-preview').inner_text()
    assert 'offset values' in p.locator('#sb-preview').inner_text()
    screenshot('logbook_omissions', p.locator('#sb-preview h3'))
    p.locator('#sb-preview summary').filter(has_text='File details').click()
    screenshot('logbook_source', p.locator('#sb-preview summary'))

    # Local metadata is descriptive; account, source and exact prepared bytes
    # remain bound by the server review proof before any creation.
    auth = {'Authorization': 'Bearer ' + p.evaluate('state.auth.token'), 'X-AJ-Hub-ID': p.evaluate('state.hub_id')}
    wrong_hub = dict(auth, **{'X-AJ-Hub-ID': '11111111-1111-4111-8111-111111111111'})
    denied = c.post('/api/builders/import/review', headers=wrong_hub, json=checked['request'])
    assert denied.status_code == 409, denied.text
    unauthenticated = c.post('/api/builders/import/review', json=checked['request'])
    assert unauthenticated.status_code == 401, unauthenticated.text
    tampered = copy.deepcopy(checked['request'])
    tampered.update(op_id='22222222-2222-4222-8222-222222222222', review_token='0' * 64)
    denied = c.post('/api/builders/import/action', headers=auth, json=tampered)
    assert denied.status_code in (409, 422), denied.text
    assert counts()['ops_logbooks'] == before['ops_logbooks']
    ok('Current-company auth, source review proof and hub scope block unauthorized native design creation')

    p.evaluate("""()=>{window.realNativeFetch=fetch;window.lostNativeResponse=false;window.nativeSaveBodies=[];window.fetch=async(path,opt={})=>{if(path==='/api/builders/import/action'){nativeSaveBodies.push(JSON.parse(opt.body));const response=await realNativeFetch(path,opt);if(!lostNativeResponse){lostNativeResponse=true;throw new TypeError('Fictional lost response');}return response;}return realNativeFetch(path,opt);};}""")
    p.locator('#sb-import-save').click()
    expect(p.locator('#sb-import-save')).to_have_text('Retry unchanged request')
    assert p.locator('#sb-file').is_disabled() and p.locator('#sb-review').is_disabled()
    assert p.locator('#sb-paste').is_disabled()
    assert counts()['ops_logbooks'] == before['ops_logbooks'] + 1
    p.locator('#sb-import-save').click()
    expect(p.locator('#sb-success')).to_be_visible()
    assert p.evaluate('JSON.stringify(nativeSaveBodies[0])===JSON.stringify(nativeSaveBodies[1])')
    result = latest('/import/action')['response']
    with store.connection() as con:
        row = con.execute('SELECT * FROM ops_logbooks WHERE id=?', (result['id'],)).fetchone()
        assert json.loads(row['definitions']) == expected_definitions
        imported = json.loads(row['import_manifest'])
        assert imported['browser_import']['omitted'] == expected_omitted
        assert imported['browser_local_definitions']['sha256'] == summary['original_sha256']
        assert row['source_hash'] == checked['response']['sha256']
    after = counts()
    assert after['ops_logbooks'] == before['ops_logbooks'] + 1
    assert all(after[key] == before[key] for key in ('ops_log_entries', 'ops_log_references', 'ops_log_media'))
    ok('Lost response freezes the native file; identical retry creates one empty logbook with all design fields and source metadata preserved')
    ok('Actual saved logbook has no imported entries, offset measurements, reference pages or media')
    p.locator('#sb-open-saved').click()
    expect(p.locator('#log-design-workspace')).to_be_visible()
    expect(p.locator('#ld-detail .ld-preview h2')).to_have_text(result['title'])
    assert p.locator('#ld-detail .ld-review-section').count() == 9
    assert p.locator('#ld-detail .ld-review-fields li').count() == 103
    ok('The current-company saved-structure viewer displays all nine sections and 103 fields')

def edge_checks(p, exchanges, counts, builder, ok):
    before = counts()
    builder()
    p.locator('#sb-file').set_input_files({'name': 'fictional-late-header.xlsx', 'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'buffer': late_header_workbook()})
    expect(p.locator('#di-header')).to_be_visible(timeout=90000)
    expect(p.locator('#sb-review')).to_be_enabled()
    assert p.locator('#di-header').input_value() == '22'
    rows = mapped_rows(p)
    assert len(rows) == 1 and rows[0]['name'] == 'Fictional pump'
    assert rows[0]['quantity'] == rows[0]['location'] == ''
    assert '[formula omitted]' in rows[0]['notes']
    assert 'formula' in p.locator('#di-mapping-quality').inner_text()
    p.locator('#sb-review').click()
    expect(p.locator('#di-confirm')).to_be_enabled()
    assert counts() == before
    ok('Header after 20 introduction rows maps correctly; formula-only names are skipped and formula quantity/location remain unknown with source evidence')
    p.locator('#sb-close').click()

    builder()
    p.evaluate('()=>{window.realNativeWorker=Worker;window.Worker=undefined;}')
    native_posts = len([row for row in exchanges if row['path'].startswith('/api/builders/import/')])
    p.locator('#sb-file').set_input_files({'name': 'fictional-history.ajlogs', 'mimeType': 'application/octet-stream', 'buffer': small_history_package()})
    expect(p.locator('#sb-result')).to_contain_text('browser cannot read logbook designs locally')
    expect(p.locator('#sb-review')).to_be_enabled()
    assert p.locator('#sb-import-save').is_disabled()
    assert len([row for row in exchanges if row['path'].startswith('/api/builders/import/')]) == native_posts
    assert counts() == before
    p.evaluate('()=>{window.Worker=window.realNativeWorker;}')
    p.locator('#sb-close').click()
    ok('Browser without Worker refuses a small history-bearing native package locally; no review/action POST or original history upload occurs')


def late_header_workbook():
    from tests.test_document_import_ui95 import archive
    ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    rows = ''.join('<row r="' + str(i) + '"><c r="A' + str(i) + '" t="inlineStr"><is><t>Fictional introduction ' + str(i) + '</t></is></c></row>' for i in range(1, 23))
    rows += '<row r="23">' + ''.join('<c r="' + chr(65 + i) + '23" t="inlineStr"><is><t>' + value + '</t></is></c>' for i, value in enumerate(['Name', 'Asset', 'Quantity', 'Location'])) + '</row>'
    rows += '<row r="24"><c r="A24" t="inlineStr"><is><t>Fictional pump</t></is></c><c r="B24" t="inlineStr"><is><t>P-1</t></is></c><c r="C24"><f>SUM(9,9)</f><v>18</v></c><c r="D24"><f>HYPERLINK(&quot;https://example.invalid&quot;,&quot;Fictional cached room&quot;)</f><v>Fictional cached room</v></c></row>'
    rows += '<row r="25"><c r="A25"><f>HYPERLINK(&quot;https://example.invalid&quot;,&quot;Fictional ghost&quot;)</f><v>Fictional ghost</v></c><c r="B25" t="inlineStr"><is><t>G-1</t></is></c></row>'
    return archive({'xl/workbook.xml': '<workbook xmlns="' + ns + '" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Fictional equipment" sheetId="1" r:id="s1"/></sheets></workbook>', 'xl/_rels/workbook.xml.rels': '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="s1" Target="worksheets/sheet1.xml"/></Relationships>', 'xl/worksheets/sheet1.xml': '<worksheet xmlns="' + ns + '"><sheetData>' + rows + '</sheetData></worksheet>'})


def small_history_package():
    entry_id = '33333333-3333-4333-8333-333333333333'
    who = {'user_id': '44444444-4444-4444-8444-444444444444', 'login_id': 'fictional.source', 'name': 'Fictional source'}
    definitions = [{'id': 'checks', 'name': 'Fictional checks', 'fields': [{'id': 'status', 'label': 'Status', 'type': 'select', 'unit': '', 'required': True, 'choices': ['Ready', 'Needs review']}]}]
    clean = {'name': 'Fictional history logbook', 'description': '', 'definitions': definitions, 'entries': [{'id': entry_id, 'kind': 'checks', 'event_utc': '2026-10-05T00:00:00Z', 'body': {'values': {'status': 'Ready'}}, 'version': 1, 'voided': 0, 'created_by': who, 'updated_by': who, 'created_at': '2026-10-05T00:00:00Z', 'updated_at': '2026-10-05T00:00:00Z'}], 'history': [{'entry_id': entry_id, 'actor': '{}', 'action': 'save', 'reason': 'Fictional history', 'before_body': '{}', 'after_body': '{}', 'at': '2026-10-05T00:00:00Z'}], 'references': [], 'media': {}, 'source_manifest': {}}
    raw = json.dumps(clean, separators=(',', ':')).encode()
    manifest = {'format': 'aj-opscheck-logs', 'format_version': 1, 'sha256': hashlib.sha256(raw).hexdigest(), 'options': {'entries': True, 'references': False, 'pictures': False}}
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_STORED) as z:
        z.writestr('manifest.json', json.dumps(manifest).encode())
        z.writestr('logbook.json', raw)
    return out.getvalue()


if __name__ == '__main__':
    main()
