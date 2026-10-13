"""UI111 inventory import safeguards in a disposable fictional C01 company.

Real Chromium/IndexedDB, actual HostedBoundary/CompanyAccess/core API requests,
native SQLite, and generated fictional XLSX only. Original files are not read.
"""
import copy
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
import uuid
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
from test_company_c01 import PASS, activate, client, instance
from browser_import_row_selection_ui105 import selection_workbook

OUT = Path(os.environ.get('WAVELINK_UI111_IMPORT_EVIDENCE_DIR', str(ROOT.parent / 'evidence-ui111/browser-import')))
TRACKED = ('app/document_import.py', 'app/document_structure.py', 'app/document_extract.py',
           'app/inventory.py', 'app/inventory_boxes.py', 'app/builder_hub.py',
           'app/static/document_import.js', 'app/static/document_import.css',
           'app/static/setup_builders.js', 'app/static/fieldwork.js',
           'app/static/inventory_workspace.js', 'app/static/verification.js',
           'app/static/browser_workspace.js', 'app/static/index.html', 'app/static/sw.js')
DECK, WORKSHOP = 'Fictional deck stock', 'Fictional workshop stock'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    fingerprint = lambda value: hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    chrome = Path(os.environ['WAVELINK_CHROMIUM_EXECUTABLE']).resolve()
    report = dict(checks=[], errors=[], widths=[1440, 1024, 390, 320], screenshots=[],
                  method='Real Chromium/IndexedDB, disposable fictional C01 HostedBoundary/CompanyAccess/core APIs and native SQLite; generated fictional XLSX only.',
                  source_hashes={name: sha(SOURCE / name) for name in TRACKED}, served_asset_hashes={},
                  harness_sha256=sha(Path(__file__)), runtime_manifest_sha256=sha(SOURCE / 'RELEASE_FILES.json'),
                  chromium_executable_sha256=sha(chrome),
                  repository_helper_hashes={name: sha(ROOT / 'tests' / name) for name in ['test_company_c01.py', 'browser_import_row_selection_ui105.py']},
                  limitations=['Service-worker registration and WebSockets are suppressed.',
                               'No production, Render, live email, physical camera, Windows display or worker-upgrade acceptance.',
                               'Captured local event callbacks exercise busy/stale ownership guards only; they are not user reload workflows.',
                               'Full mapped TSV editing intentionally clears source-row proof; the separate cancellation case verifies that this state is retained, then remapping restores original rows.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui111-import-safeguards-') as td:
        td = Path(td)
        header = ['Name', 'Asset reference', 'SN', 'PN', 'Qty expected', 'Qty counted', 'Remarks', 'Is box', 'Parent box reference', 'Location']
        fixtures = []
        for suffix in ('NEW', 'APPEND', 'MANUAL', 'STALE'):
            path = td / ('Fictional_UI111_' + suffix + '.xlsx')
            selection_workbook(path, [
                (DECK, [(5, header),
                 (9, ['Fictional deck crate ' + suffix, 'BOX-111-' + suffix, '000BOX111-' + suffix, '000-PN-BOX111', 1, 88, 'Fictional intact crate note', 'yes', '', 'Fictional deck']),
                 (13, ['Fictional cable ' + suffix, 'CABLE-111-' + suffix, '00000111-' + suffix, '000-PN-OLD', 0, 88, 'Fictional intact cable note', 'no', '', 'Fictional shelf']),
                 (17, ['Fictional excluded valve ' + suffix, 'VALVE-111-' + suffix, '00000117-' + suffix, '000-PN-VALVE', 2, 88, 'Fictional intact excluded note', 'no', '', 'Fictional deck']),
                 (21, header)]),
                (WORKSHOP, [(7, header),
                 (35, ['Fictional workshop spare ' + suffix, 'SPARE-111-' + suffix, '00000135-' + suffix, '000-PN-SPARE', 3, 88, 'Fictional intact workshop note', 'no', '', 'Fictional workshop'])])])
            fixtures.append(path)
        report['fictional_fixture_hashes'] = {path.name: sha(path) for path in fixtures}
        installation = instance.__wrapped__(td)
        with client(installation) as c, sync_playwright() as pw:
            activate(c)
            origin = installation[2].external_origin
            store = c.app.state.core.state.store
            browser = pw.chromium.launch(headless=True, args=['--no-sandbox'], executable_path=str(chrome))
            report['chromium_version'] = browser.version
            p = browser.new_page(viewport={'width': 1440, 'height': 1000})
            p.set_default_timeout(30000)
            p.on('pageerror', lambda error: report['errors'].append(str(error)))
            dialogs = {'accept_remap': True, 'messages': []}

            def handle_dialog(dialog):
                if dialog.type == 'confirm' and dialog.message.startswith('Apply mapping to worksheet'):
                    dialogs['messages'].append(dialog.message)
                    report['mapping_confirmations'] = dialogs['messages'].copy()
                    if dialogs['accept_remap']:
                        dialog.accept()
                    else:
                        dialog.dismiss()
                else:
                    dialog.accept()

            p.on('dialog', handle_dialog)
            p.add_init_script('class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();')
            exchanges, delayed = [], {'path': None, 'held': None}

            def route(r):
                req, u = r.request, urlsplit(r.request.url)
                response = c.request(req.method, u.path + ('?' + u.query if u.query else ''), headers=req.headers, content=req.post_data_buffer)
                source_name = 'app' + u.path
                if source_name in TRACKED and response.status_code == 200:
                    report['served_asset_hashes'][source_name] = hashlib.sha256(response.content).hexdigest()
                if u.path.startswith(('/api/builders/', '/api/inventory/', '/api/verification/')):
                    exchanges.append(dict(path=u.path, status=response.status_code, request=json.loads(req.post_data or '{}'), response=response.json()))
                if delayed['path'] == u.path:
                    delayed['path'], delayed['held'] = None, (r, response)
                    return
                r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

            p.route(origin + '/**', route)

            def latest(suffix):
                return next(x for x in reversed(exchanges) if x['path'].endswith(suffix))

            def reviews():
                return sum(x['path'].endswith('/document/review') for x in exchanges)

            def navigate(fragment, selector):
                p.evaluate('(hash)=>{location.hash=hash;render();}', fragment)
                expect(p.locator(selector)).to_be_visible()

            def open_builder(path, existing=None):
                if p.locator('#sb-close').count():
                    p.locator('#sb-close').click()
                if existing:
                    navigate('#inventory/' + existing, '#inv-import-items')
                    p.locator('#inv-import-items').click()
                else:
                    navigate('#builders', '#sb-document')
                    p.locator('#sb-document').click()
                p.locator('#sb-file').set_input_files(str(path))
                expect(p.locator('#di-sheet')).to_be_visible(timeout=90000)
                assert latest('/document/scan')['status'] == 200
                p.locator('#di-select-data').click()
                for index, sheet in enumerate(latest('/document/scan')['response']['sheets']):
                    p.locator('[data-di-sheet-location="' + str(index) + '"]').fill('Fictional deck' if sheet['name'] == DECK else 'Fictional workshop')
                switch(DECK)

            def switch(name):
                p.locator('#di-sheet').select_option(name)
                p.locator('#di-row-picker').evaluate('n=>n.open=true')

            def rows():
                return list(csv.DictReader(io.StringIO(p.locator('#di-inventory_rows').input_value()), delimiter='\t'))

            def write_rows(values):
                out = io.StringIO()
                writer = csv.DictWriter(out, fieldnames=list(values[0]), delimiter='\t', lineterminator='\n')
                writer.writeheader()
                writer.writerows(values)
                p.locator('#di-inventory_rows').evaluate('n=>n.closest("details").open=true')
                p.locator('#di-inventory_rows').fill(out.getvalue())

            def model():
                return p.evaluate('()=>JSON.parse(JSON.stringify(ui111Form.document.inventory_import))')

            def active():
                return next(s for s in model()['sheets'] if s['sheet'] == p.locator('#di-sheet').input_value())

            def signed():
                return p.evaluate('()=>JSON.stringify({review:ui111Form.review,request:ui111Form.request})')

            def check():
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                result = latest('/document/review')
                assert result['status'] == 200 and result['response']['summary']['inventory_review']['can_save'], result
                p.locator('#di-confirm').check()
                expect(p.locator('#sb-import-save')).to_be_enabled()
                return copy.deepcopy(result)

            def edit(position, name=None, serial=None, part=None):
                p.locator('[data-di-item-edit="' + str(position) + '"]').click()
                expect(p.locator('#di-item-editor[open]')).to_be_visible()
                for control, value in [('di-item-name', name), ('di-item-serial', serial), ('di-item-part-number', part)]:
                    if value is not None:
                        p.locator('#' + control).fill(value)
                p.locator('#di-item-apply').click()
                expect(p.locator('#di-item-editor')).not_to_be_visible()

            def relationship(position, field, value):
                p.locator('#di-relationships').evaluate('n=>n.open=true')
                node = p.locator('[data-di-relationship-row="' + str(position) + '"][data-di-relationship-field="' + field + '"]')
                if node.evaluate('n=>n.tagName') == 'SELECT':
                    node.select_option(value)
                else:
                    node.fill(value)

            def screenshot(name, locator, controls):
                p.wait_for_function('()=>!document.querySelector("#toast")?.classList.contains("visible")')
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    locator.evaluate('n=>n.scrollIntoView({block:"start"})')
                    if not p.locator('dialog[open]').count():
                        p.evaluate('()=>scrollBy(0,-80)')
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name, width)
                    bounds = p.locator(controls).evaluate_all('(ns)=>ns.map(n=>{const b=n.getBoundingClientRect();return {id:n.id,left:b.left,right:b.right};})')
                    assert not [b for b in bounds if b['left'] < -1 or b['right'] > width + 1], (name, width, bounds)
                    filename = name + '_' + str(width) + '.png'
                    p.screenshot(path=str(OUT / filename))
                    report['screenshots'].append(filename)
                    ok(name.replace('_', ' ') + ' fits ' + str(width) + 'px without page overflow or clipped controls')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            def snapshot():
                with store.connection() as con:
                    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE 'inventory_%' OR name IN ('work_tasks','fieldwork_audit')) ORDER BY name")]
                    return {name: [tuple(r) for r in con.execute('SELECT * FROM "' + name + '" ORDER BY rowid')] for name in tables}

            def inventory_action(name, payload):
                auth = p.evaluate('({token:state.auth.token,hub:state.hub_id})')
                response = c.post('/api/inventory/action', json=dict(action=name, payload=payload, op_id=str(uuid.uuid4())), headers={'Authorization': 'Bearer ' + auth['token'], 'x-aj-hub-id': auth['hub']})
                assert response.status_code == 200, response.text
                return response.json()

            def remap(accept):
                dialogs['accept_remap'] = accept
                before = len(dialogs['messages'])
                p.locator('#di-map').click()
                assert len(dialogs['messages']) == before + 1
                assert DECK in dialogs['messages'][-1]
                assert 'Cancel keeps this worksheet draft and its review.' in dialogs['messages'][-1]
                dialogs['accept_remap'] = True

            def browse_checked(checked):
                signature, total, before = signed(), p.locator('#di-inventory-review').inner_text(), reviews()
                switch(WORKSHOP)
                assert p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_enabled()
                assert p.locator('#di-inventory-review').inner_text() == total and signed() == signature and reviews() == before
                p.locator('#di-row-search').fill('00000135')
                assert p.locator('[data-di-item-edit]').count() == 1
                p.locator('#di-row-filter').select_option('included')
                p.locator('#di-header-chooser').evaluate('n=>n.open=true')
                p.locator('#di-header-search').fill('Excel row 35')
                assert p.locator('#di-confirm').is_checked() and signed() == signature
                switch(DECK)
                assert p.locator('#di-confirm').is_checked() and signed() == signature and reviews() == before
                assert p.locator('#di-inventory-review').inner_text() == total
                switch(WORKSHOP)
                assert p.locator('#di-confirm').is_checked() and signed() == signature and reviews() == before
                assert checked['request']['draft']['sheet'] != p.locator('#di-sheet').input_value()
                screenshot('checked_sheet_browsing_' + checked['request']['draft']['inventory_target']['mode'], p.locator('#di-inventory-review'), '#di-sheet,#di-confirm,#sb-import-save')
                return before

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                actor = store.session(p.evaluate('state.auth.token'))
                p.evaluate('''()=>{const n=window.AJDocumentImport;window.AJDocumentImport={...n,scan(f,h){window.ui111Form=f;window.ui111Hooks=h;return n.scan(f,h);},lock(f){window.ui111Form=f;return n.lock(f);}};}''')

                # Corrected fields, an explicit box relationship, source Notes,
                # confirmed coordinates and exclusions coexist in one proposal.
                open_builder(fixtures[0])
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                edit(2, 'Fictional corrected cable NEW', '00000111-EDIT-NEW', '000-PN-111-EDIT')
                relationship(2, 'container_ref', 'BOX-111-NEW')
                relationship(2, 'quantity', '7')
                switch(WORKSHOP)
                edit(1, 'Fictional corrected workshop spare NEW', '00000135-EDIT-NEW', '000-PN-WORKSHOP-EDIT')
                switch(DECK)
                check()
                before_model, before_rows, before_signed, before_db = model(), rows(), signed(), snapshot()
                assert active()['source_rows'] == [9, 13, 17, 21] and active()['selected_rows'] == [1, 2]
                assert rows()[1]['container_ref'] == 'BOX-111-NEW' and rows()[1]['quantity'] == '7'
                screenshot('corrected_remap_proposal', p.locator('.di-mapping'), '#di-map,#di-sheet')
                remap(False)
                assert model() == before_model and rows() == before_rows and signed() == before_signed
                assert p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_enabled()
                assert snapshot() == before_db
                assert p.locator('#di-map').evaluate('n=>document.activeElement===n')
                ok('Cancel remapping preserves corrected name/SN/PN, explicit box relation, all source Notes, expected quantity seven, exact Excel coordinates/exclusions, other worksheet edits and checked approval without any SQLite mutation')

                # A real confirmation replaces only the active worksheet rows.
                remap(True)
                remapped = model()
                original_deck = next(s for s in before_model['sheets'] if s['sheet'] == DECK)
                new_deck = next(s for s in remapped['sheets'] if s['sheet'] == DECK)
                assert next(s for s in remapped['sheets'] if s['sheet'] == WORKSHOP) == next(s for s in before_model['sheets'] if s['sheet'] == WORKSHOP)
                assert new_deck['selected_rows'] == original_deck['selected_rows'] and new_deck['source_rows'] == original_deck['source_rows']
                assert rows()[1]['name'] == 'Fictional cable NEW' and rows()[1]['serial'] == '00000111-NEW' and rows()[1]['part_number'] == '000-PN-OLD'
                assert not rows()[1]['container_ref'] and rows()[1]['quantity'] == '0' and 'Fictional intact cable note' in rows()[1]['notes']
                assert p.locator('#di-confirm').is_disabled() and not p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_disabled()
                assert snapshot() == before_db
                ok('Confirmed remapping restores only active deck source fields/relationships, retains proven exclusions and the corrected workshop worksheet, and requires a fresh Check and confirmation')
                edit(2, 'Fictional corrected cable NEW', '00000111-EDIT-NEW', '000-PN-111-EDIT')
                relationship(2, 'container_ref', 'BOX-111-NEW')
                relationship(2, 'quantity', '7')
                checked = check()
                review_count = browse_checked(checked)
                inspected_sheet = p.locator('#di-sheet').input_value()
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                saved = latest('/document/action')
                assert reviews() == review_count and saved['request']['draft'] == checked['request']['draft']
                assert saved['request']['review_token'] == checked['response']['review_token'] and saved['request']['confirmed'] is True
                report['new_inventory_save'] = dict(reviewed_draft_sha256=fingerprint(checked['request']['draft']), saved_draft_sha256=fingerprint(saved['request']['draft']), reviewed_sheet=checked['request']['draft']['sheet'], inspected_sheet_at_save=inspected_sheet, saved_sheet=saved['request']['draft']['sheet'], op_id=saved['request']['op_id'], additional_reviews=reviews()-review_count, exact_token_match=saved['request']['review_token']==checked['response']['review_token'])
                book = store.inventory.get(saved['response']['id'], actor)
                assert len(book['items']) == 3 and not book['counts']
                cable = next(x for x in book['items'] if x['name'] == 'Fictional corrected cable NEW')
                crate = next(x for x in book['items'] if x['name'] == 'Fictional deck crate NEW')
                assert cable['container_id'] == crate['id'] and cable['quantity'] == 7 and cable['serial'] == '00000111-EDIT-NEW' and cable['part_number'] == '000-PN-111-EDIT'
                assert cable['source']['source_row'] == 13 and cable['location'] == 'Fictional deck'
                assert 'Fictional intact cable note' in cable['notes'] and '88' in cable['notes'] and 'Fictional shelf' in cable['notes']
                assert not any('excluded' in x['name'] for x in book['items'])
                p.locator('#sb-done').click()
                ok('Checked worksheet browsing/search/filter retains overview and confirmation; real new-inventory Save sends the exact signed draft/token without another Review and SQLite records preserve corrected identity, Notes, manually reviewed expected seven and box containment')

                # The duplicate overview is diagnostic, not authorization.
                # Read-only navigation must retain it without enabling Save.
                open_builder(fixtures[0], book['id'])
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                blocked_before_db = snapshot()
                p.locator('#sb-review').click()
                expect(p.locator('#di-review-conflicts')).to_be_visible()
                blocked = latest('/document/review')['response']['summary']['inventory_review']
                assert not blocked['can_save'] and blocked['conflicts']['duplicate_count'] == 3
                blocked_summary, blocked_reviews = p.locator('#di-inventory-review').inner_text(), reviews()
                assert p.evaluate('ui111Form.review===null') and p.locator('#di-confirm').is_disabled() and p.locator('#sb-import-save').is_disabled()
                switch(WORKSHOP)
                assert p.locator('#di-inventory-review').inner_text() == blocked_summary and reviews() == blocked_reviews
                assert p.evaluate('ui111Form.review===null') and p.locator('#di-confirm').is_disabled() and p.locator('#sb-import-save').is_disabled()
                screenshot('blocked_duplicate_sheet_browsing', p.locator('#di-review-conflicts'), '#di-sheet,#di-confirm,#sb-import-save')
                switch(DECK)
                assert p.locator('#di-inventory-review').inner_text() == blocked_summary and snapshot() == blocked_before_db
                edit(2, name='Fictional edited blocked duplicate proposal')
                assert p.locator('#di-review-conflicts').count() == 0 and p.locator('#di-inventory-review').count() == 0
                assert p.locator('#di-confirm').is_disabled() and p.locator('#sb-import-save').is_disabled() and snapshot() == blocked_before_db
                p.locator('#sb-close').click()
                ok('Duplicate append stays blocked with no SQLite writes; browsing another worksheet retains exact conflict overview while approval/Save remain disabled; an actual field correction clears stale diagnostics')

                # Full mapped text is already intentionally unproven. Cancel
                # must preserve that custom quantity and relationship as well.
                open_builder(fixtures[2])
                custom = rows()
                custom[1].update(name='Fictional manually corrected cable', quantity='7', serial='000-MANUAL-SN', part_number='000-MANUAL-PN', container_ref='BOX-111-MANUAL')
                write_rows(custom)
                p.locator('#di-row-picker').evaluate('n=>n.open=true')
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                manual_before = model()
                assert active()['manual'] and 'source_rows' not in active()
                check()
                manual_signed = signed()
                remap(False)
                assert model() == manual_before and rows() == custom and signed() == manual_signed and p.locator('#di-confirm').is_checked()
                remap(True)
                assert not active()['manual'] and active()['source_rows'] == [9, 13, 17, 21]
                assert rows()[1]['quantity'] == '0' and rows()[1]['name'] == 'Fictional cable MANUAL' and not rows()[1]['container_ref']
                assert 'selected_rows' not in active() and p.locator('#di-confirm').is_disabled()
                ok('Native Cancel preserves manual quantity seven, edited identity/box text and explicit exclusions in the intentionally unproven TSV draft; confirmed reset restores original zero, Notes/source references and resets choices instead of inventing row matches')
                p.locator('#sb-close').click()

                # Append through the real destination, with fixed count history.
                fixed = inventory_action('start_count', dict(list_id=book['id'], name='Fictional UI111 fixed scope'))
                inventory_action('check_item', dict(session_id=fixed['id'], item_id=cable['id'], item_version=cable['version'], check_version=0, result='found', counted_quantity=7, note='Fictional before append'))
                prior_items, prior_count = copy.deepcopy(book['items']), copy.deepcopy(store.inventory.count(fixed['id'], actor))
                open_builder(fixtures[1], book['id'])
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                edit(2, 'Fictional corrected cable APPEND', '00000111-EDIT-APPEND', '000-PN-111-APPEND')
                relationship(2, 'container_ref', 'BOX-111-APPEND')
                append_checked = check()
                append_review_count = browse_checked(append_checked)
                p.evaluate('()=>{window.ui111CapturedSheet=document.querySelector("#di-sheet").onchange;window.ui111CapturedMap=document.querySelector("#di-map").onclick;}')
                delayed['path'], delayed['held'] = '/api/builders/document/action', None
                p.locator('#sb-import-save').click()
                for _ in range(300):
                    if delayed['held'] is not None:
                        break
                    p.wait_for_timeout(100)
                assert delayed['held'] is not None, 'The genuine save response was not held within 30 seconds'
                assert p.locator('#di-sheet').is_disabled() and p.locator('#di-map').is_disabled() and p.locator('#sb-close').is_disabled()
                busy_payload = copy.deepcopy(latest('/document/action')['request'])
                busy_model = model()
                confirmation_count = len(dialogs['messages'])
                p.evaluate('()=>{ui111CapturedSheet();ui111CapturedMap();}')
                assert model() == busy_model and len(dialogs['messages']) == confirmation_count
                held_route, _ = delayed['held']
                held_route.abort('failed')
                expect(p.locator('#sb-import-save')).to_have_text('Retry unchanged request')
                assert p.locator('#di-sheet').is_disabled() and p.locator('#di-map').is_disabled()
                p.evaluate('()=>{ui111CapturedSheet();ui111CapturedMap();}')
                assert model() == busy_model and len(dialogs['messages']) == confirmation_count
                assert p.evaluate('ui111Form.request.op_id') == busy_payload['op_id']
                screenshot('uncertain_append_lock', p.locator('#sb-result'), '#di-sheet,#di-map,#sb-import-save')
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                retried = latest('/document/action')
                assert retried['request'] == busy_payload and busy_payload['draft'] == append_checked['request']['draft'] and busy_payload['review_token'] == append_checked['response']['review_token']
                assert retried['response']['id'] == book['id'] and reviews() == append_review_count
                report['append_retry'] = dict(reviewed_draft_sha256=fingerprint(append_checked['request']['draft']), first_action_draft_sha256=fingerprint(busy_payload['draft']), retry_action_draft_sha256=fingerprint(retried['request']['draft']), reviewed_sheet=append_checked['request']['draft']['sheet'], inspected_sheet_at_save=WORKSHOP, first_op_id=busy_payload['op_id'], retry_op_id=retried['request']['op_id'], additional_reviews=reviews()-append_review_count, saved_receipt_id=retried['response']['id'], exact_request_match=retried['request']==busy_payload)
                appended = store.inventory.get(book['id'], actor)
                assert len(appended['items']) == 6
                assert {x['id']: x for x in appended['items'] if x['id'] in {y['id'] for y in prior_items}} == {y['id']: y for y in prior_items}
                after_count = store.inventory.count(fixed['id'], actor)
                assert after_count['checks'] == prior_count['checks'] and after_count['total'] == 3 and after_count['new_items'] == 3
                assert [r['expected'] for r in after_count['rows']] == [r['expected'] for r in prior_count['rows']]
                p.locator('#sb-done').click()
                ok('Busy and uncertain native append lock sheet/remap navigation and captured callbacks; retry uses identical signed payload/op_id and server receipt, adds exactly three rows once and preserves old SQLite items/fixed verification results')

                # Ordinary mutations still invalidate the signed review. A
                # stale callback cannot mutate a replaced or stale session.
                open_builder(fixtures[3])
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                check()
                p.evaluate('()=>{window.ui111StaleSheet=document.querySelector("#di-sheet").onchange;window.ui111StaleMap=document.querySelector("#di-map").onclick;window.ui111StaleForm=ui111Form;}')
                before_session = model()
                confirmation_count = len(dialogs['messages'])
                p.evaluate('()=>{window.ui111OriginalToken=state.auth.token;state.auth.token="fictional-replaced-session";ui111StaleSheet();ui111StaleMap();state.auth.token=ui111OriginalToken;}')
                assert model() == before_session and len(dialogs['messages']) == confirmation_count and p.locator('#di-confirm').is_checked()
                edit(2, part='000-PN-AFTER-CHECK')
                assert p.locator('#di-confirm').is_disabled() and not p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_disabled()
                check()
                p.locator('#di-description').fill('Fictional changed description after check')
                assert p.locator('#di-confirm').is_disabled() and not p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_disabled()
                check()
                p.locator('[data-di-row-select="3"]').check()
                assert p.locator('#di-confirm').is_disabled() and not p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_disabled()
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('#sb-close').click()
                open_builder(fixtures[2])
                replacement_before = model()
                confirmation_count = len(dialogs['messages'])
                p.evaluate('()=>{ui111StaleSheet();ui111StaleMap();}')
                assert model() == replacement_before and len(dialogs['messages']) == confirmation_count
                ok('Session-stale and replaced-form sheet/remap callbacks cannot mutate current proposals; actual item, description and inclusion edits still clear confirmation and disable Save pending another Check')

                assert not report['errors'], report['errors']
                assert all(value == report['source_hashes'][name] for name, value in report['served_asset_hashes'].items())
                assert all(sha(SOURCE / name) == value for name, value in report['source_hashes'].items())
                assert sha(SOURCE / 'RELEASE_FILES.json') == report['runtime_manifest_sha256']
                assert sha(Path(__file__)) == report['harness_sha256'] and sha(chrome) == report['chromium_executable_sha256']
                assert all(sha(path) == report['fictional_fixture_hashes'][path.name] for path in fixtures)
                ok('Served tracked assets match pinned source; runtime/manifest/harness/Chromium/fictional XLSX remain unchanged; no unhandled JavaScript errors occur')
                report['passed'] = True
            except Exception:
                report['passed'] = False
                p.screenshot(path=str(OUT / 'FAILURE.png'))
                print(json.dumps(dict(status=p.locator('#sb-result').inner_text() if p.locator('#sb-result').count() else '', recent_api=[dict(path=x['path'], status=x['status']) for x in exchanges[-4:]])))
                raise
            finally:
                report['summary'] = dict(checks_passed=len(report['checks']), unexpected_errors=len(report['errors']))
                (OUT / 'UI111_IMPORT_SAFEGUARDS_BROWSER_RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
