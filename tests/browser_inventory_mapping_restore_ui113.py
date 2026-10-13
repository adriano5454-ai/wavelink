"""UI113 inventory mapping restoration in a disposable fictional C01 company.

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

OUT = Path(os.environ.get('WAVELINK_UI113_RESTORE_EVIDENCE_DIR', str(ROOT.parent / 'evidence-ui113/browser-restore')))
TRACKED = ('app/document_import.py', 'app/document_structure.py', 'app/document_extract.py',
           'app/inventory.py', 'app/inventory_boxes.py', 'app/builder_hub.py',
           'app/static/document_import.js', 'app/static/document_import.css',
           'app/static/setup_builders.js', 'app/static/fieldwork.js',
           'app/static/inventory_workspace.js', 'app/static/verification.js',
           'app/static/browser_workspace.js', 'app/static/index.html', 'app/static/sw.js')
DECK, WORKSHOP, SUMMARY = 'Fictional deck stock', 'Fictional workshop stock', 'Summary'


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
                               'Controlled busy/uncertain flags and captured event callbacks verify navigation ownership locks; retained UI111 safeguards harness separately verifies genuine save/retry.',
                               'One empty fictional destination is created through the real API before the read-only restore cases; browser never sends write actions. Legacy-sidecar and ownership states are controlled fixtures, not user reload workflows.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui113-import-safeguards-') as td:
        td = Path(td)
        header = ['Name', 'Asset reference', 'SN', 'PN', 'Qty expected', 'Qty counted', 'Remarks', 'Is box', 'Parent box reference', 'Location']
        fixtures = []
        for suffix in ('NEW', 'APPEND', 'MANUAL', 'STALE'):
            path = td / ('Fictional_UI113_' + suffix + '.xlsx')
            local_header = header.copy()
            if suffix == 'MANUAL':
                local_header[2:4] = ['Serial', 'Serial']
            selection_workbook(path, [
                (DECK, [(5, local_header),
                 (9, ['Fictional deck crate ' + suffix, 'BOX-111-' + suffix, '000BOX111-' + suffix, '000-PN-BOX111', 1, 88, 'Fictional intact crate note', 'yes', '', 'Fictional deck']),
                 (13, ['Fictional cable ' + suffix, 'CABLE-111-' + suffix, '00000111-' + suffix, '000-PN-OLD', 0, 88, 'Fictional intact cable note', 'no', '', 'Fictional shelf']),
                 (17, ['Fictional excluded valve ' + suffix, 'VALVE-111-' + suffix, '00000117-' + suffix, '000-PN-VALVE', 2, 88, 'Fictional intact excluded note', 'no', '', 'Fictional deck']),
                 (21, local_header)]),
                (WORKSHOP, [(7, local_header),
                 (35, ['Fictional workshop spare ' + suffix, 'SPARE-111-' + suffix, '00000135-' + suffix, '000-PN-SPARE', 3, 88, 'Fictional intact workshop note', 'no', '', 'Fictional workshop'])]),
                (SUMMARY, [(1, ['Department', 'Count']), (2, ['Fictional summary only', 3])])])
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
                    field = p.locator('[data-di-sheet-location="' + str(index) + '"]').first
                    if field.is_enabled():
                        field.fill('Fictional deck' if sheet['name'] == DECK else 'Fictional workshop')
                switch(DECK)

            def switch(name):
                p.locator('#di-sheet').select_option(name)
                p.locator('#di-row-picker').evaluate('n=>n.open=true')

            def rows():
                return list(csv.DictReader(io.StringIO(p.locator('#di-inventory_rows').input_value()), delimiter='\t'))

            def model():
                return p.evaluate('()=>JSON.parse(JSON.stringify(ui113Form.document.inventory_import))')

            def active():
                return next(s for s in model()['sheets'] if s['sheet'] == p.locator('#di-sheet').input_value())

            def signed():
                return p.evaluate('()=>JSON.stringify({review:ui113Form.review,request:ui113Form.request})')

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

            def snapshot():
                with store.connection() as con:
                    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
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

            TARGETS = {'worksheets': 'di-inventory-plan', 'mapping': 'di-inventory-mapping',
                       'items': 'di-row-search', 'boxes': 'di-relationship-search',
                       'source': 'di-source-text', 'overview': 'di-review-heading'}

            def material():
                """Strip view preferences only; retain every selected source/data field."""
                value = model()
                value.pop('active_sheet', None)
                for sheet in value['sheets']:
                    sheet.pop('mapping_restore_notice', None)
                    for name in list(sheet):
                        if name.endswith('_view'):
                            del sheet[name]
                return value

            def calls():
                return len(exchanges), reviews(), sum(x['path'].endswith('/action') for x in exchanges)

            def inspect(name):
                index = next(i for i, sheet in enumerate(model()['sheets']) if sheet['sheet'] == name)
                p.locator('[data-di-sheet-inspect="' + str(index) + '"]').click()
                expect(p.locator('#di-sheet')).to_have_value(name)
                expect(p.locator('#di-inspected-worksheet-heading')).to_have_text('Inspecting: ' + name)
                assert p.locator('#di-inventory-mapping').evaluate('n=>document.activeElement===n')
                inclusion = next(s['selected'] for s in model()['sheets'] if s['sheet'] == name)
                expect(p.locator('.di-inventory-inclusion-state')).to_have_text('Included in this import' if inclusion else 'Excluded from this import')

            def jump(key, width=None):
                p.locator('[data-di-inventory-jump="' + key + '"]').click()
                target = p.locator('#' + TARGETS[key])
                expect(target).to_be_visible()
                assert target.evaluate('n=>document.activeElement===n'), (key, p.evaluate('document.activeElement.id'))
                rect = target.evaluate('n=>{const b=n.getBoundingClientRect();return {top:b.top,bottom:b.bottom,left:b.left,right:b.right};}')
                shell_bottom = p.locator('#wl-topbar').evaluate('n=>n.getBoundingClientRect().bottom')
                assert shell_bottom + 4 <= rect['top'] < 940, (key, width, rect, shell_bottom)
                assert rect['left'] >= -1 and rect['right'] <= (width or p.viewport_size['width']) + 1, (key, width, rect)
                if key in ('items', 'boxes', 'source'):
                    assert target.evaluate('n=>{const b=n.getBoundingClientRect();const x=Math.min(innerWidth-1,Math.max(1,b.left+b.width/2)),y=Math.min(innerHeight-1,Math.max(1,b.top+Math.min(12,b.height/2)));const t=document.elementFromPoint(x,y);return t===n||n.contains(t);}'), (key, rect)

            def mapping_rows_material():
                """All material source state except the intentionally changed mapping."""
                value = material()
                for sheet in value['sheets']:
                    sheet.pop('mapping', None)
                return value

            def mapping_snapshot():
                return copy.deepcopy(active()['mapping'])

            def baseline():
                return copy.deepcopy(active().get('last_applied_mapping'))

            def capture_restore():
                p.evaluate('()=>{window.ui113CapturedRestore=document.querySelector("#di-restore-mapping").onclick;}')

            def invoke_restore():
                p.evaluate('()=>ui113CapturedRestore()')

            def restore():
                p.locator('#di-restore-mapping').click()
                expect(p.locator('#di-inventory-mapping')).to_be_focused()
                expect(p.locator('#di-confirm')).to_be_disabled()
                assert not p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_disabled()
                assert 'restored' in p.locator('#di-mapping-restore-status').inner_text().lower()
                assert p.locator('[data-di-inventory-jump="overview"]').is_disabled()

            def pending_header_columns():
                p.locator('#di-header').select_option('4')  # Confirmed Excel row 21.
                p.locator('#di-name-column').select_option('1')
                p.locator('[data-di-column="12"]').select_option('2' if baseline()['columns'][12] != 2 else '3')
                assert active()['mapping']['dirty']
                assert p.locator('#di-restore-mapping').is_enabled()
                changes = p.locator('#di-mapping-changes').inner_text()
                assert 'header' in changes.lower() and '5' in changes and '21' in changes, changes
                assert 'Name' in changes and 'Column 1' in changes and 'Column 2' in changes, changes
                assert 'Part' in changes or 'PN' in changes, changes
                return changes

            def mapping_layout(case, selector):
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    node = p.locator(selector)
                    node.evaluate('n=>n.scrollIntoView({block:"center"})')
                    rect = node.bounding_box()
                    shell_bottom = p.locator('#wl-topbar').evaluate('n=>n.getBoundingClientRect().bottom')
                    assert rect and rect['x'] >= -1 and rect['x'] + rect['width'] <= width + 1 and shell_bottom + 4 <= rect['y'] < 940, (case, width, rect)
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (case, width)
                    bounds = p.locator('.di-mapping-actions button').evaluate_all('ns=>ns.map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom};})')
                    assert len(bounds) == 2, bounds
                    assert all(b['left'] >= -1 and b['right'] <= width + 1 for b in bounds), (case, width, bounds)
                    a, b = bounds
                    assert not (min(a['right'], b['right']) > max(a['left'], b['left']) + 1 and min(a['bottom'], b['bottom']) > max(a['top'], b['top']) + 1), (case, width, bounds)
                    filename = case + '_' + str(width) + '.png'
                    p.screenshot(path=str(OUT / filename))
                    report['screenshots'].append(filename)
                    ok(case.replace('_', ' ') + ': restore/change guidance is visible below the shell; Apply/Restore fit without overlap or page overflow at ' + str(width) + 'px')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            def restore_focus_layout(expected_material, expected_mapping, expected_db, expected_calls):
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    if not active()['mapping']['dirty']:
                        p.locator('[data-di-column="12"]').select_option('2' if expected_mapping['columns'][12] != 2 else '3')
                    restore()
                    rect = p.locator('#di-inventory-mapping').bounding_box()
                    shell_bottom = p.locator('#wl-topbar').evaluate('n=>n.getBoundingClientRect().bottom')
                    assert rect and shell_bottom + 4 <= rect['y'] < 940 and rect['x'] >= -1 and rect['x'] + rect['width'] <= width + 1, (width, rect)
                    assert material() == expected_material and mapping_snapshot() == expected_mapping
                    assert snapshot() == expected_db and calls() == expected_calls
                    filename = 'restored_mapping_focus_' + str(width) + '.png'
                    p.screenshot(path=str(OUT / filename))
                    report['screenshots'].append(filename)
                    ok('Restore receives actual visible mapping focus below the shell at ' + str(width) + 'px, preserving complete source draft/corrections/row choices and every native SQLite table without API calls')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                p.evaluate('''()=>{const n=window.AJDocumentImport;window.AJDocumentImport={...n,
                 scan(f,h){window.ui113Form=f;window.ui113Hooks=h;return n.scan(f,h);},
                 lock(f){window.ui113Form=f;return n.lock(f);}};}''')
                seeded = inventory_action('create_list', {'name': 'Fictional UI113 destination', 'locations': ['Fictional deck', 'Fictional workshop']})
                report['fixture_setup'] = {'method': 'One empty inventory create_list through disposable TestClient; no imported items', 'id': seeded['id']}

                open_builder(fixtures[0], seeded['id'])
                assert model()['target']['mode'] == 'existing' and model()['target']['list_id'] == seeded['id']
                assert [s['sheet'] for s in model()['sheets'] if s['selected']] == [DECK, WORKSHOP]
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                edit(2, 'Fictional corrected UI113 cable', '000-113-EDIT', '000-PN-113-EDIT')
                relationship(2, 'container_ref', 'BOX-111-NEW')
                relationship(2, 'quantity', '7')
                inspect(WORKSHOP)
                jump('items')
                edit(1, 'Fictional corrected UI113 workshop spare', '000-113-WORKSHOP', '000-PN-113-WORKSHOP')
                inspect(DECK)
                p.locator('#di-description').fill('Fictional UI113 reviewed destination description')
                initial_check = check()
                assert p.locator('#di-restore-mapping').is_disabled()
                assert isinstance(baseline(), dict) and baseline()['version'] == 1 and baseline()['sheet'] == DECK
                initial_material, initial_mapping, initial_baseline = material(), mapping_snapshot(), baseline()
                initial_rows, initial_db, initial_calls = rows(), snapshot(), calls()
                report['initial_material_sha256'] = fingerprint(initial_material)
                report['initial_source_baseline_sha256'] = fingerprint(initial_baseline)
                report['initial_sqlite_sha256'] = fingerprint(initial_db)
                pending_header_columns()
                assert rows() == initial_rows and mapping_rows_material() == {**initial_material, 'sheets': [{k:v for k,v in t.items() if k != 'mapping'} for t in initial_material['sheets']]}
                assert baseline() == initial_baseline
                assert p.locator('#di-confirm').is_disabled() and not p.locator('#di-confirm').is_checked()
                mapping_layout('pending_header_and_column_changes', '#di-mapping-changes')
                restore_focus_layout(initial_material, initial_mapping, initial_db, initial_calls)
                assert rows() == initial_rows and baseline() == initial_baseline
                assert p.evaluate('ui113Form.review===null&&ui113Form.request===null')
                assert 'again' in p.locator('#di-mapping-restore-status').inner_text().lower()
                fresh = check()
                assert reviews() == initial_calls[1] + 1
                assert fresh['request']['draft'] == initial_check['request']['draft']
                ok('Restore of pending header and source-column choices preserves edited identity/SN/PN, Notes, exact Excel provenance, row exclusions, boxes/quantity, locations, other worksheet edits and existing destination; approval is cleared and real fresh Check is required')

                # Navigation remains read-only, including inspection of an excluded
                # worksheet after a restored draft has been checked again.
                nav_before = material(), signed(), snapshot(), calls()
                overview = p.locator('#di-inventory-review').inner_text()
                inspect(SUMMARY)
                assert not active()['selected']
                jump('source')
                jump('overview')
                inspect(WORKSHOP)
                jump('items')
                inspect(DECK)
                assert (material(), signed(), snapshot(), calls()) == nav_before
                assert p.locator('#di-inventory-review').inner_text() == overview and p.locator('#di-confirm').is_checked()
                ok('Concise UI112 regression: excluded/included inspection and Source/Overview/Items shortcuts retain selected drafts, the new signed approval, overview, API calls and all native SQLite tables')

                # A successful explicit remap records a new baseline. Subsequent
                # row corrections are not replaced by Restore or a cancelled Apply.
                p.locator('[data-di-column="12"]').select_option('2')
                before_success = baseline()
                remap(True)
                assert baseline() != before_success and baseline()['columns'][12] == 2
                assert rows()[1]['part_number'] == rows()[1]['serial'] == '00000111-NEW'
                assert p.locator('#di-confirm').is_disabled()
                edit(2, 'Fictional latest UI113 cable correction', '000-113-LATEST-SN', '000-113-LATEST-PN')
                relationship(2, 'container_ref', 'BOX-111-NEW')
                relationship(2, 'quantity', '11')
                latest_material, latest_mapping, latest_baseline, latest_rows = material(), mapping_snapshot(), baseline(), rows()
                latest_db, latest_calls = snapshot(), calls()
                report['latest_applied_baseline_sha256'] = fingerprint(latest_baseline)
                report['latest_corrected_material_sha256'] = fingerprint(latest_material)
                pending_header_columns()
                pending_material = material()
                remap(False)
                assert material() == pending_material and baseline() == latest_baseline and rows() == latest_rows
                restore()
                assert material() == latest_material and mapping_snapshot() == latest_mapping and baseline() == latest_baseline and rows() == latest_rows
                assert snapshot() == latest_db and calls() == latest_calls
                assert p.locator('[data-di-column="12"]').input_value() == '2'
                check()
                ok('Last successful Apply updates the proven baseline; native Cancel does not overwrite it; subsequent Restore returns to the newest header/column choices while preserving later item/box/quantity corrections and requires genuine fresh Check')

                # The new callback follows busy/uncertain, modal and session guards.
                p.locator('[data-di-column="12"]').select_option('3')
                capture_restore()
                for flag in ('busy', 'uncertain'):
                    p.evaluate('(flag)=>{ui113Form[flag]=true;ui113Hooks.lock();}', flag)
                    assert p.locator('#di-restore-mapping').is_disabled()
                    before = material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')
                    invoke_restore()
                    assert (material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')) == before
                    p.evaluate('(flag)=>{ui113Form[flag]=false;ui113Hooks.lock();}', flag)
                before = material(), signed(), snapshot(), calls()
                p.evaluate('''()=>{const d=document.createElement('dialog');d.id='fictional-owner-modal';d.innerHTML='<input id="fictional-owner-focus">';document.body.append(d);d.showModal();document.querySelector('#fictional-owner-focus').focus();}''')
                invoke_restore()
                assert (material(), signed(), snapshot(), calls()) == before
                assert p.evaluate('document.activeElement.id') == 'fictional-owner-focus'
                p.evaluate('()=>{const d=document.querySelector("#fictional-owner-modal");d.close();d.remove();}')
                before = material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')
                p.evaluate('()=>{const t=state.auth.token;state.auth.token="fictional-stale-owner";ui113CapturedRestore();state.auth.token=t;}')
                assert (material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')) == before
                ok('Restore is disabled during controlled busy/uncertain states; captured callbacks under busy/uncertain, another open modal or a replaced session cannot change mapping/rows, reviews, API calls, native SQLite or modal focus')

                # A legacy pending draft has no proven baseline. Never infer one
                # from its current, unapplied choices or destroy its corrected rows.
                p.evaluate('()=>{delete ui113Form.document.inventory_import.sheets.find(t=>t.sheet===ui113Form.document.draft.sheet).last_applied_mapping;}')
                inspect(WORKSHOP)
                inspect(DECK)
                expect(p.locator('#di-restore-mapping')).to_be_disabled()
                assert active()['mapping']['dirty'] and baseline() is None
                unavailable = p.locator('#di-mapping-restore-status').inner_text().lower()
                assert 'unavailable' in unavailable or 'no' in unavailable and ('baseline' in unavailable or 'last applied' in unavailable), unavailable
                legacy_before = material(), signed(), snapshot(), calls()
                capture_restore()
                invoke_restore()
                assert (material(), signed(), snapshot(), calls()) == legacy_before
                assert rows() == latest_rows
                mapping_layout('legacy_pending_restore_unavailable', '#di-mapping-restore-status')
                ok('Legacy pending mapping without the proven sidecar leaves Restore unavailable; direct callbacks neither infer a baseline nor change corrected rows, source proof, API calls or native SQLite')
                p.locator('#sb-close').click()
                open_builder(fixtures[1])
                replacement_before = material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')
                invoke_restore()
                assert (material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')) == replacement_before
                assert model()['target']['mode'] == 'new'
                ok('A captured Restore callback from a closed/replaced builder cannot mutate the fresh new-inventory proposal or its source baseline, API, SQLite or focus')
                new_before = material(), mapping_snapshot(), snapshot(), calls()
                p.locator('[data-di-column="12"]').select_option('2')
                restore()
                assert (material(), mapping_snapshot(), snapshot(), calls()) == new_before
                assert model()['target']['mode'] == 'new'
                ok('Fresh new-inventory Restore also retains its destination, worksheet choices, source baseline/rows and every native SQLite table without API writes')

                assert not report['errors'], report['errors']
                assert not [x for x in exchanges if x['path'].endswith('/action')], exchanges
                assert all(value == report['source_hashes'][name] for name, value in report['served_asset_hashes'].items())
                assert all(sha(SOURCE / name) == value for name, value in report['source_hashes'].items())
                assert sha(SOURCE / 'RELEASE_FILES.json') == report['runtime_manifest_sha256']
                assert sha(Path(__file__)) == report['harness_sha256'] and sha(chrome) == report['chromium_executable_sha256']
                assert all(sha(path) == report['fictional_fixture_hashes'][path.name] for path in fixtures)
                ok('Browser sends no action writes or unhandled JS errors; served assets equal pinned source and source/manifest/harness/Chromium/fictional XLSX hashes remain unchanged')
                report['passed'] = True
            except Exception:
                report['passed'] = False
                p.screenshot(path=str(OUT / 'FAILURE.png'))
                print(json.dumps(dict(status=p.locator('#sb-result').inner_text() if p.locator('#sb-result').count() else '', recent_api=[dict(path=x['path'], status=x['status']) for x in exchanges[-4:]])))
                raise
            finally:
                report['summary'] = dict(checks_passed=len(report['checks']), unexpected_errors=len(report['errors']))
                (OUT / 'UI113_MAPPING_RESTORE_BROWSER_RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
