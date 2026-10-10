"""UI109 per-item proposal acceptance in a disposable fictional company.

Real Chromium, IndexedDB, company/core API receipts and native SQLite. Literal
XLSX fixtures are generated here; original or production data are never read.
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

OUT = Path(os.environ.get('WAVELINK_UI109_INVENTORY_EVIDENCE_DIR', str(ROOT.parent / 'evidence/browser-inventory')))
TRACKED = ('app/document_import.py', 'app/document_structure.py', 'app/document_extract.py',
           'app/inventory.py', 'app/inventory_boxes.py', 'app/builder_hub.py',
           'app/static/document_import.js', 'app/static/document_import.css',
           'app/static/setup_builders.js', 'app/static/fieldwork.js',
           'app/static/inventory_workspace.js', 'app/static/verification.js',
           'app/static/browser_workspace.js', 'app/static/index.html', 'app/static/sw.js')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    chrome = Path(os.environ['WAVELINK_CHROMIUM_EXECUTABLE']).resolve()
    report = dict(checks=[], errors=[], widths=[1440, 390, 320], screenshots=[],
                  method='Real Chromium, genuine IndexedDB, disposable fictional C01 HostedBoundary/CompanyAccess/core APIs and native SQLite; generated literal fictional XLSX only.',
                  source_hashes={name: sha(SOURCE / name) for name in TRACKED}, served_asset_hashes={},
                  harness_sha256=sha(Path(__file__)), runtime_manifest_sha256=sha(SOURCE / 'RELEASE_FILES.json'),
                  chromium_executable_sha256=sha(chrome),
                  repository_helper_hashes={name: sha(ROOT / 'tests' / name) for name in ['test_company_c01.py', 'browser_import_row_selection_ui105.py']},
                  limitations=['Service-worker registration and WebSockets are suppressed.',
                               'No production, Render, live email, physical camera, Windows display or worker-upgrade acceptance.',
                               'Captured local event handlers are invoked only to exercise stale/busy ownership guards; these are not user reload workflows.',
                               'Per-item changes edit this proposal only; original source-row advice is not reclassified.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui109-item-review-') as td:
        td = Path(td)
        inventory = td / 'Fictional_UI109_ItemReview.xlsx'
        header = ['Name', 'Asset reference', 'SN', 'PN', 'Qty expected', 'Qty counted', 'Remarks', 'Is box', 'Parent box reference', 'Location']
        selection_workbook(inventory, [
            ('Fictional deck stock', [(5, header),
             (9, ['Fictional deck crate', 'BOX-109', '000BOX109', '000-PN-BOX109', 1, 88, 'Fictional intact crate note', 'yes', '', 'Fictional deck']),
             (13, ['Fictional cable needing correction', 'CABLE-109', '00000109', '000-PN-OLD', 0, 88, 'Fictional intact cable note', 'no', 'BOX-109', 'Fictional shelf']),
             (17, ['Fictional excluded valve', 'VALVE-109', '00000117', '000-PN-VALVE', 2, 88, 'Fictional intact excluded note', 'no', '', 'Fictional deck']),
             (21, header)]),
            ('Fictional workshop stock', [(7, header),
             (35, ['Fictional workshop spare', 'SPARE-109', '00000135', '000-PN-SPARE', 1, 88, 'Fictional intact workshop note', 'no', '', 'Fictional workshop'])])])
        append_source = td / 'Fictional_UI109_ItemAppend.xlsx'
        selection_workbook(append_source, [
            ('Fictional deck stock', [(5, header),
             (9, ['Fictional appended deck crate', 'BOX-109-APPEND', '000BOX109-APPEND', '000-PN-BOX109', 1, 88, 'Fictional intact crate note', 'yes', '', 'Fictional deck']),
             (13, ['Fictional appended cable', 'CABLE-109-APPEND', '00000109-APPEND', '000-PN-OLD', 0, 88, 'Fictional intact cable note', 'no', 'BOX-109-APPEND', 'Fictional shelf']),
             (17, ['Fictional excluded appended valve', 'VALVE-109-APPEND', '00000117-APPEND', '000-PN-VALVE', 2, 88, 'Fictional intact excluded note', 'no', '', 'Fictional deck']),
             (21, header)]),
            ('Fictional workshop stock', [(7, header),
             (35, ['Fictional appended workshop spare', 'SPARE-109-APPEND', '00000135-APPEND', '000-PN-SPARE', 1, 88, 'Fictional intact workshop note', 'no', '', 'Fictional workshop'])])])
        report['fictional_fixture_hashes'] = {path.name: sha(path) for path in [inventory, append_source]}
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
            p.on('dialog', lambda dialog: dialog.accept())
            p.add_init_script('class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();')
            exchanges = []
            lose_next = {'save': False}

            def route(r):
                req = r.request
                u = urlsplit(req.url)
                response = c.request(req.method, u.path + ('?' + u.query if u.query else ''), headers=req.headers, content=req.post_data_buffer)
                source_name = 'app' + u.path
                if source_name in TRACKED and response.status_code == 200:
                    report['served_asset_hashes'][source_name] = hashlib.sha256(response.content).hexdigest()
                if u.path.startswith(('/api/builders/document/', '/api/inventory/', '/api/verification/')):
                    exchanges.append(dict(path=u.path, status=response.status_code, request=json.loads(req.post_data or '{}'), response=response.json()))
                if lose_next['save'] and u.path == '/api/builders/document/action':
                    lose_next['save'] = False
                    r.abort('failed')
                    return
                r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

            p.route(origin + '/**', route)

            def latest(suffix):
                return next(x for x in reversed(exchanges) if x['path'].endswith(suffix))

            def navigate(fragment, selector):
                p.evaluate('(hash)=>{location.hash=hash;render();}', fragment)
                expect(p.locator(selector)).to_be_visible()

            def builder(existing=None):
                if p.locator('#sb-close').count():
                    p.locator('#sb-close').click()
                if existing:
                    navigate('#inventory/' + existing, '#inv-import-items')
                    p.locator('#inv-import-items').click()
                else:
                    navigate('#builders', '#sb-document')
                    p.locator('#sb-document').click()
                p.locator('#sb-file').set_input_files(str(append_source if existing else inventory))
                expect(p.locator('#di-sheet')).to_be_visible(timeout=90000)
                assert latest('/document/scan')['status'] == 200, latest('/document/scan')['response']
                p.locator('#di-select-data').click()
                for index, sheet in enumerate(latest('/document/scan')['response']['sheets']):
                    p.locator('[data-di-sheet-location="' + str(index) + '"]').fill('Fictional deck' if sheet['name'] == 'Fictional deck stock' else 'Fictional workshop')
                p.locator('#di-sheet').select_option('Fictional deck stock')
                p.locator('#di-row-picker').evaluate('n=>n.open=true')

            def rows():
                return list(csv.DictReader(io.StringIO(p.locator('#di-inventory_rows').input_value()), delimiter='\t'))

            def state():
                return p.evaluate('()=>{const s=ui109Form.document.inventory_import.sheets.find(s=>s.sheet===ui109Form.document.draft.sheet);return JSON.parse(JSON.stringify(s));}')

            def receipt():
                return p.evaluate('JSON.stringify({review:ui109Form.review,request:ui109Form.request,draft:ui109Form.document.draft,inventory:ui109Form.document.inventory_import})')

            def check():
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                result = latest('/document/review')
                assert result['status'] == 200 and result['response']['summary']['inventory_review']['can_save'], result
                p.locator('#di-confirm').check()
                expect(p.locator('#sb-import-save')).to_be_enabled()
                return copy.deepcopy(result['request']['draft'])

            def editor(position):
                p.locator('[data-di-item-edit="' + str(position) + '"]').click()
                expect(p.locator('#di-item-editor[open]')).to_be_visible()
                assert p.locator('#di-item-name').evaluate('n=>document.activeElement===n')

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

            def action(name, payload):
                auth = p.evaluate('({token:state.auth.token,hub:state.hub_id})')
                response = c.post('/api/inventory/action', json=dict(action=name, payload=payload, op_id=str(uuid.uuid4())), headers={'Authorization': 'Bearer ' + auth['token'], 'x-aj-hub-id': auth['hub']})
                assert response.status_code == 200, response.text
                return response.json()

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                actor = store.session(p.evaluate('state.auth.token'))
                p.evaluate('''()=>{const n=window.AJDocumentImport;window.AJDocumentImport={...n,scan(f,h){window.ui109Form=f;window.ui109Hooks=h;return n.scan(f,h);},lock(f){window.ui109Form=f;return n.lock(f);}};}''')
                builder()
                assert len(rows()) == 4
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                original_rows, original_state = rows(), state()
                check()
                accepted = receipt()
                p.locator('#di-row-search').fill('00000109')
                assert p.locator('[data-di-item-edit]').count() == 1
                p.locator('#di-row-search').fill('')
                editor(2)
                expect(p.locator('#di-item-editor')).to_contain_text('Excel row 13')
                expect(p.locator('#di-item-editor')).to_contain_text('Included')
                assert len(p.locator('#di-item-editor input').all()) == 3
                assert p.locator('#di-item-serial').input_value() == '00000109'
                assert p.locator('#di-item-part-number').input_value() == '000-PN-OLD'
                screenshot('item_editor', p.locator('#di-item-editor'), '#di-item-editor input,#di-item-editor button')
                p.locator('#di-item-apply').click()
                expect(p.locator('#di-item-editor')).not_to_be_visible()
                assert receipt() == accepted and p.locator('#di-confirm').is_checked()
                assert p.locator('[data-di-item-edit="2"]').evaluate('n=>document.activeElement===n')
                ok('Opening/searching and no-op Apply retain the exact checked receipt, leading-zero identity, source row and keyboard focus')
                editor(2)
                p.locator('#di-item-name').fill('Fictional cancelled name')
                p.keyboard.press('Escape')
                expect(p.locator('#di-item-editor')).not_to_be_visible()
                assert rows() == original_rows and receipt() == accepted
                ok('Escape discards temporary item edits without changing rows, inclusion, source notes or approval')
                editor(2)
                p.locator('#di-item-name').fill('')
                p.locator('#di-item-apply').click()
                expect(p.locator('#di-item-editor[open]')).to_be_visible()
                assert not p.locator('#di-item-name').evaluate('n=>n.checkValidity()')
                assert rows() == original_rows and receipt() == accepted
                p.locator('#di-item-name').fill('Fictional corrected cable')
                p.locator('#di-item-serial').fill('00000109-EDIT')
                p.locator('#di-item-part-number').fill('000-PN-109-EDIT')
                p.locator('#di-item-apply').click()
                expect(p.locator('#di-item-editor')).not_to_be_visible()
                changed_rows = rows()
                expected = copy.deepcopy(original_rows)
                expected[1].update(name='Fictional corrected cable', serial='00000109-EDIT', part_number='000-PN-109-EDIT')
                assert changed_rows == expected
                current_state = state()
                for key in ['source_rows', 'selected_rows', 'source_review', 'manual', 'mapping', 'location', 'selected']:
                    if key in original_state:
                        assert current_state[key] == original_state[key], key
                assert p.locator('#di-confirm').is_disabled() and p.locator('#sb-import-save').is_disabled()
                ok('Required Name validation blocks empty edits; a real three-field correction retains every other TSV value, original Notes, row proof, exclusion and box relationships and requires a fresh Check')
                editor(3)
                expect(p.locator('#di-item-editor')).to_contain_text('Excluded')
                expect(p.locator('#di-item-editor')).to_contain_text('Excel row 17')
                p.locator('#di-item-name').fill('Fictional corrected excluded valve')
                p.locator('#di-item-apply').click()
                assert not p.locator('[data-di-row-select="3"]').is_checked()
                assert rows()[2]['name'] == 'Fictional corrected excluded valve' and len(rows()) == 4
                assert state()['source_rows'] == [9, 13, 17, 21] and state()['selected_rows'] == [1, 2]
                expect(p.locator('#di-source-review-note')).to_contain_text('original')
                ok('Excluded rows remain editable and available with their exact source coordinates, stay excluded and do not acquire current-data source advice')
                checked = check()
                sheet = next(s for s in checked['inventory_sheets'] if s['sheet'] == 'Fictional deck stock')
                assert sheet['selected_rows'] == [1, 2] and sheet['source_rows'] == [9, 13, 17, 21]
                assert len(list(csv.DictReader(io.StringIO(sheet['inventory_rows']), delimiter='\t'))) == 4
                screenshot('edited_item_proposal', p.locator('#di-row-picker'), '#di-row-picker input:visible,#di-row-picker button:visible,#di-row-picker select:visible')
                ok('The real server review contains all four mapped source rows and explicit positions 1/2 only; the second selected worksheet stays separate in the same inventory')

                # Invoke the captured original submit only to prove its guard;
                # no event fixture substitutes for the service-backed workflow.
                guarded_before = receipt()
                editor(2)
                p.locator('#di-item-name').fill('Fictional stale busy edit')
                p.evaluate('()=>{window.ui109CapturedSubmit=document.querySelector("#di-item-editor-form").onsubmit;ui109Form.busy=true;ui109CapturedSubmit({preventDefault(){}});ui109Form.busy=false;}')
                assert receipt() == guarded_before
                p.locator('#di-item-cancel').click()
                editor(2)
                p.locator('#di-item-name').fill('Fictional revoked-access edit')
                p.evaluate('''()=>{window.ui109PermissionBackup=structuredClone(state.auth.person);window.ui109CapturedSubmit=document.querySelector('#di-item-editor-form').onsubmit;state.auth.person.role='technician';state.auth.person.permissions={...(state.auth.person.permissions||{}),'builders.inventory':false,'builders.checklists':true};AJDocumentImport.lock(ui109Form);}''')
                assert p.evaluate('ui109Hooks.own(ui109Form)')
                assert p.locator('#di-item-apply').is_disabled() and p.locator('#di-item-name').is_disabled()
                expect(p.locator('#di-item-cancel')).to_be_enabled()
                p.evaluate('()=>ui109CapturedSubmit({preventDefault(){}})')
                assert receipt() == guarded_before
                screenshot('revoked_item_edit_cancel', p.locator('#di-item-editor'), '#di-item-editor input,#di-item-editor button')
                p.locator('#di-item-cancel').click()
                expect(p.locator('#di-item-editor')).not_to_be_visible()
                p.evaluate('()=>{state.auth.person=ui109PermissionBackup;AJDocumentImport.lock(ui109Form);}')
                assert receipt() == guarded_before
                ok('Specific local inventory-builder access revocation blocks a captured editor submit while another builder retains form ownership; actual Cancel remains usable and preserves the checked proposal')
                editor(2)
                p.locator('#di-item-name').fill('Fictional stale sheet edit')
                p.evaluate('()=>{window.ui109CapturedSubmit=document.querySelector("#di-item-editor-form").onsubmit;window.ui109CapturedDialog=document.querySelector("#di-item-editor");ui109CapturedDialog.close();}')
                expect(p.locator('#di-item-editor')).not_to_be_visible()
                p.locator('#di-sheet').select_option('Fictional workshop stock')
                other_before = receipt()
                p.evaluate('()=>ui109CapturedSubmit({preventDefault(){}})')
                assert receipt() == other_before
                p.locator('#di-sheet').select_option('Fictional deck stock')
                assert rows()[1]['name'] == 'Fictional corrected cable'
                ok('Captured editor submits cannot change a busy form or a departed active worksheet; retained original and other-sheet rows remain intact')
                check()
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                saved = latest('/document/action')['response']
                assert saved['saved']
                book = store.inventory.get(saved['id'], actor)
                assert len(book['items']) == 3 and not book['counts']
                cable = next(x for x in book['items'] if x['name'] == 'Fictional corrected cable')
                box = next(x for x in book['items'] if x['name'] == 'Fictional deck crate')
                assert cable['quantity'] == 0 and cable['serial'] == '00000109-EDIT' and cable['part_number'] == '000-PN-109-EDIT'
                assert cable['container_id'] == box['id'] and cable['location'] == 'Fictional deck'
                assert '88' in cable['notes'] and 'Fictional intact cable note' in cable['notes']
                assert 'Fictional shelf' in cable['notes']
                assert cable['source']['source_row'] == 13
                assert not any('excluded' in x['name'] for x in book['items'])
                p.locator('#sb-done').click()
                ok('Native Save creates three unverified items from two locations, preserving edited SN/PN, expected zero, full source Notes and explicit box containment while omitted rows remain absent')

                fixed = action('start_count', dict(list_id=book['id'], name='Fictional UI109 fixed scope'))
                action('check_item', dict(session_id=fixed['id'], item_id=cable['id'], item_version=cable['version'], check_version=0, result='found', counted_quantity=0, note='Fictional pre-append checked result'))
                prior_items = copy.deepcopy(book['items'])
                prior_count = copy.deepcopy(store.inventory.count(fixed['id'], actor))
                builder(book['id'])
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                editor(2)
                p.locator('#di-item-part-number').fill('000-PN-109-APPEND')
                p.locator('#di-item-apply').click()
                checked = check()
                assert checked['inventory_target']['mode'] == 'existing' and checked['inventory_target']['list_id'] == book['id']
                assert all(set(s) <= {'sheet', 'location', 'inventory_rows', 'source_rows', 'selected_rows'} for s in checked['inventory_sheets'])
                assert 'source_review' not in checked and 'item_editor' not in checked
                screenshot('append_item_review', p.locator('#di-inventory-review'), '#di-edit input:visible,#di-edit select:visible,#di-edit button:visible')
                lose_next['save'] = True
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-import-save')).to_have_text('Retry unchanged request')
                request = copy.deepcopy(latest('/document/action')['request'])
                assert p.locator('[data-di-item-edit]').evaluate_all('ns=>ns.every(n=>n.disabled)')
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                assert latest('/document/action')['request'] == request
                appended = store.inventory.get(book['id'], actor)
                assert len(appended['items']) == 6
                assert {x['id']: x for x in appended['items'] if x['id'] in {y['id'] for y in prior_items}} == {y['id']: y for y in prior_items}
                after_count = store.inventory.count(fixed['id'], actor)
                assert after_count['checks'] == prior_count['checks'] and after_count['total'] == 3 and after_count['new_items'] == 3
                assert [r['expected'] for r in after_count['rows']] == [r['expected'] for r in prior_count['rows']]
                p.locator('#sb-done').click()
                ok('A corrected append uses the unchanged strict native request shape, locks item editors during uncertain delivery and retries the identical receipt without changing prior items or fixed verification results')
                navigate('#inventory/count/' + fixed['id'], '[name=stock_query]')
                p.locator('[name=stock_query]').fill('000 pn 109 edit')
                expect(p.locator('#stock-rows')).to_contain_text('Already checked: Found')
                expect(p.locator('#stock-rows')).to_contain_text('000-PN-109-EDIT')
                assert p.locator('#stock-rows [data-stock-row]').count() == 1
                screenshot('already_checked_edited_part', p.locator('#stock-rows'), '#stock-rows button:visible,[name=stock_query]')
                assert store.inventory.count(fixed['id'], actor)['checked'] == 1
                ok('Searching the corrected PN in fixed verification returns the already checked Found-zero original and does not verify newly appended stock')
                assert not report['errors'], report['errors']
                assert all(value == report['source_hashes'][name] for name, value in report['served_asset_hashes'].items())
                assert all(sha(SOURCE / name) == value for name, value in report['source_hashes'].items())
                assert sha(SOURCE / 'RELEASE_FILES.json') == report['runtime_manifest_sha256']
                assert sha(Path(__file__)) == report['harness_sha256']
                assert sha(chrome) == report['chromium_executable_sha256']
                ok('Served tracked assets equal their source pins, source/harness/Chrome/manifest remain unchanged and no unhandled JavaScript errors occur')
                report['passed'] = True
            except Exception:
                report['passed'] = False
                p.screenshot(path=str(OUT / 'FAILURE.png'))
                print(json.dumps(dict(status=p.locator('#sb-result').inner_text() if p.locator('#sb-result').count() else '', recent_api=[dict(path=x['path'], status=x['status']) for x in exchanges[-4:]])))
                raise
            finally:
                report['summary'] = dict(checks_passed=len(report['checks']), unexpected_errors=len(report['errors']))
                (OUT / 'UI109_INVENTORY_ITEM_BROWSER_RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
