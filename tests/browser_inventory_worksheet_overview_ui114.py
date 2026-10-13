"""UI114 inventory worksheet overview in a disposable fictional C01 company.

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

OUT = Path(os.environ.get('WAVELINK_UI114_OVERVIEW_EVIDENCE_DIR', str(ROOT.parent / 'evidence-ui114/browser-overview')))
TRACKED = ('app/document_import.py', 'app/document_structure.py', 'app/document_extract.py',
           'app/inventory.py', 'app/inventory_boxes.py', 'app/builder_hub.py',
           'app/static/document_import.js', 'app/static/document_import.css',
           'app/static/setup_builders.js', 'app/static/fieldwork.js',
           'app/static/inventory_workspace.js', 'app/static/verification.js',
           'app/static/browser_workspace.js', 'app/static/index.html', 'app/static/sw.js')
DECK, WORKSHOP, SUMMARY, ARCHIVE = 'Fictional deck stock', 'Fictional workshop stock', 'Summary', 'Fictional excluded archive'


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
                               'One fictional native inventory row is seeded via disposable TestClient to exercise a genuinely blocked duplicate-source append; browser never sends write actions. Busy/uncertain/modal/session guards are controlled fixtures, not user reload workflows.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui114-import-safeguards-') as td:
        td = Path(td)
        header = ['Name', 'Asset reference', 'SN', 'PN', 'Qty expected', 'Qty counted', 'Remarks', 'Is box', 'Parent box reference', 'Location']
        fixtures = []
        for suffix in ('NEW', 'APPEND', 'MANUAL', 'STALE'):
            path = td / ('Fictional_UI114_' + suffix + '.xlsx')
            local_header = header.copy()
            if suffix == 'MANUAL':
                local_header[2:4] = ['Serial', 'Serial']
            selection_workbook(path, [
                (DECK, [(5, local_header),
                 (9, ['Fictional deck crate ' + suffix, 'BOX-111-' + suffix, '000BOX111-' + suffix, '000-PN-BOX111', 1, 88, 'Fictional intact crate note', 'yes', '', 'Fictional deck']),
                 (13, ['Fictional cable ' + suffix, 'CABLE-111-' + suffix, '00000111-' + suffix, '000-PN-OLD', 0, 88, 'Fictional intact cable note', 'no', '', 'Fictional shelf']),
                 (17, ['Fictional excluded valve ' + suffix, 'VALVE-111-' + suffix, '00000117-' + suffix, '000-PN-VALVE', 2, 88, 'Fictional intact excluded note', 'no', '', 'Fictional deck']),
                 (21, local_header)]),
                (SUMMARY, [(1, ['Department', 'Count']), (2, ['Fictional summary only', 3])]),
                (WORKSHOP, [(7, local_header),
                 (35, ['Fictional workshop spare ' + suffix, 'SPARE-111-' + suffix, '00000135-' + suffix, '000-PN-SPARE', 3, 88, 'Fictional intact workshop note', 'no', '', 'Fictional workshop'])]),
                (ARCHIVE, [(5, local_header), (9, ['Fictional archive spare ' + suffix, 'ARCHIVE-114-' + suffix, '000ARCHIVE114-' + suffix, '000-PN-ARCHIVE', 1, 88, 'Fictional excluded archive source note', 'no', '', 'Fictional archive'])])])
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
                archive_index = next(i for i,sheet in enumerate(model()['sheets']) if sheet['sheet'] == ARCHIVE)
                p.locator('[data-di-sheet-location="' + str(archive_index) + '"]').fill('Fictional archive')
                p.locator('[data-di-sheet-select="' + str(archive_index) + '"]').uncheck()
                switch(DECK)

            def switch(name):
                p.locator('#di-sheet').select_option(name)
                p.locator('#di-row-picker').evaluate('n=>n.open=true')

            def rows():
                return list(csv.DictReader(io.StringIO(p.locator('#di-inventory_rows').input_value()), delimiter='\t'))

            def model():
                return p.evaluate('()=>JSON.parse(JSON.stringify(ui114Form.document.inventory_import))')

            def active():
                return next(s for s in model()['sheets'] if s['sheet'] == p.locator('#di-sheet').input_value())

            def signed():
                return p.evaluate('()=>JSON.stringify({review:ui114Form.review,request:ui114Form.request})')

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

            def visible_indices():
                return p.locator('[data-di-sheet-card]').evaluate_all('ns=>ns.filter(n=>!n.hidden).map(n=>Number(n.dataset.diSheetCard))')

            def filter_view(key):
                p.locator('[data-di-worksheet-filter="' + key + '"]').click()
                expect(p.locator('[data-di-worksheet-filter="' + key + '"]')).to_have_attribute('aria-pressed', 'true')
                assert p.locator('[data-di-worksheet-filter]').evaluate_all('ns=>ns.filter(n=>n.getAttribute("aria-pressed")==="true").length') == 1
                assert p.locator('[data-di-worksheet-filter="' + key + '"]').evaluate('n=>document.activeElement===n')

            def mapping_state(index):
                return p.locator('[data-di-sheet-mapping-state="' + str(index) + '"]').inner_text().lower()

            def attention():
                return p.locator('#di-worksheet-attention').inner_text()

            def captured_view():
                return p.locator('[data-di-worksheet-filter][aria-pressed="true"]').get_attribute('data-di-worksheet-filter'), visible_indices()

            def capture_filter():
                p.evaluate('()=>{window.ui114CapturedFilter=document.querySelector("[data-di-worksheet-filter=mapping]").onclick;}')

            def invoke_filter():
                p.evaluate('()=>ui114CapturedFilter()')

            def apply_mapping(accept=True, dialog=True):
                current_sheet = p.locator('#di-sheet').input_value()
                before = len(dialogs['messages'])
                dialogs['accept_remap'] = accept
                p.locator('#di-map').click()
                if dialog:
                    assert len(dialogs['messages']) == before + 1 and current_sheet in dialogs['messages'][-1]
                else:
                    assert len(dialogs['messages']) == before
                dialogs['accept_remap'] = True

            def restore_mapping():
                p.locator('#di-restore-mapping').click()
                expect(p.locator('#di-inventory-mapping')).to_be_focused()

            def filter_layout(case, expected, confirmed, summary):
                before_material, before_signed, before_db, before_calls = material(), signed(), snapshot(), calls()
                active_sheet = p.locator('#di-sheet').input_value()
                p.evaluate('()=>{window.ui114Cards=[...document.querySelectorAll("[data-di-sheet-card]")];window.ui114CardControls=ui114Cards.map(n=>[n.querySelector("[data-di-sheet-select]"),n.querySelector("[data-di-sheet-location]"),n.querySelector("[data-di-sheet-inspect]")]);}')
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    jump('worksheets', width)
                    for key in ('all', 'included', 'mapping', 'all'):
                        filter_view(key)
                        assert visible_indices() == expected[key], (case, width, key, visible_indices(), expected[key])
                        assert p.evaluate('()=>{const cards=[...document.querySelectorAll("[data-di-sheet-card]")];return cards.length===ui114Cards.length&&cards.every((n,i)=>n===ui114Cards[i]&&[n.querySelector("[data-di-sheet-select]"),n.querySelector("[data-di-sheet-location]"),n.querySelector("[data-di-sheet-inspect]")].every((c,j)=>c===ui114CardControls[i][j]));}')
                        assert material() == before_material and signed() == before_signed and snapshot() == before_db and calls() == before_calls
                        assert p.locator('#di-sheet').input_value() == active_sheet
                        assert p.locator('#di-confirm').is_checked() == confirmed and p.locator('#sb-import-save').is_enabled() == confirmed
                        assert p.locator('#di-inventory-review').inner_text() == summary
                        assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (case, key, width)
                        p.locator('#di-worksheet-filters').evaluate('n=>n.scrollIntoView({block:"center"})')
                        bounds = p.locator('#di-worksheet-filters button').evaluate_all('ns=>ns.map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom};})')
                        assert len(bounds) == 3 and all(b['left'] >= -1 and b['right'] <= width + 1 for b in bounds), (case, width, bounds)
                        assert all(not (min(a['right'],b['right'])>max(a['left'],b['left'])+1 and min(a['bottom'],b['bottom'])>max(a['top'],b['top'])+1) for i,a in enumerate(bounds) for b in bounds[i+1:]), (case, width, bounds)
                    filename = case + '_' + str(width) + '.png'
                    p.screenshot(path=str(OUT / filename))
                    report['screenshots'].append(filename)
                    ok(case.replace('_', ' ') + ': all filters retain original card/control identities and source indices, active sheet, exact material/signed state, confirmation/summary/API/all-table SQLite with visible filter focus and no overflow/overlap at ' + str(width) + 'px')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            def status_layout(case, selector='#di-worksheet-attention'):
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    node = p.locator(selector)
                    node.evaluate('n=>n.scrollIntoView({block:"center"})')
                    rect = node.bounding_box()
                    shell = p.locator('#wl-topbar').evaluate('n=>n.getBoundingClientRect().bottom')
                    assert rect and rect['x'] >= -1 and rect['x'] + rect['width'] <= width + 1 and shell + 4 <= rect['y'] < 940, (case, width, rect)
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (case, width)
                    bounds = p.locator('[data-di-sheet-card]:not([hidden]) [data-di-sheet-select], [data-di-sheet-card]:not([hidden]) [data-di-sheet-location], [data-di-sheet-card]:not([hidden]) [data-di-sheet-inspect]').evaluate_all('ns=>ns.map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right};})')
                    assert all(b['left'] >= -1 and b['right'] <= width + 1 for b in bounds), (case, width, bounds)
                    filename = case + '_' + str(width) + '.png'
                    p.screenshot(path=str(OUT / filename))
                    report['screenshots'].append(filename)
                    ok(case.replace('_', ' ') + ': attention/status and original indexed controls fit without clipping or page overflow at ' + str(width) + 'px')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                p.evaluate('''()=>{const n=window.AJDocumentImport;window.AJDocumentImport={...n,
                 scan(f,h){window.ui114Form=f;window.ui114Hooks=h;return n.scan(f,h);},
                 lock(f){window.ui114Form=f;return n.lock(f);}};}''')
                open_builder(fixtures[0])
                assert [s['sheet'] for s in model()['sheets']] == [DECK, SUMMARY, WORKSHOP, ARCHIVE]
                assert [i for i,s in enumerate(model()['sheets']) if s['selected']] == [0,2]
                assert 'applied mapping recorded' in mapping_state(0) and 'applied mapping recorded' in mapping_state(2)
                assert 'item-name' in mapping_state(1) and 'not mapped' in mapping_state(1)
                assert 'applied mapping recorded' in mapping_state(3)
                assert p.locator('#di-worksheet-attention > strong').inner_text().startswith('0 included')
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                edit(2, 'Fictional UI114 corrected cable', '000-114-CABLE', '000-PN-114-CABLE')
                relationship(2, 'container_ref', 'BOX-111-NEW')
                relationship(2, 'quantity', '7')
                readonly_db, readonly_calls = snapshot(), calls()

                # Hidden cards preserve source indices and independent controls.
                filter_view('included')
                assert visible_indices() == [0,2]
                p.locator('[data-di-sheet-location="2"]').fill('Fictional filtered workshop')
                assert model()['sheets'][2]['location'] == 'Fictional filtered workshop' and model()['sheets'][0]['location'] == 'Fictional deck'
                inspect(WORKSHOP)
                jump('items')
                edit(1, 'Fictional UI114 corrected workshop spare', '000-114-WORKSHOP', '000-PN-114-WORKSHOP')
                filter_view('included')
                p.locator('[data-di-sheet-select="2"]').uncheck()
                assert [s['sheet'] for s in model()['sheets'] if s['selected']] == [DECK]
                assert visible_indices() == [0] and p.locator('#di-sheet').input_value() == WORKSHOP
                assert p.locator('[data-di-sheet-card="2"]').evaluate('n=>n.hidden')
                filter_view('all')
                p.locator('[data-di-sheet-select="2"]').check()
                filter_view('included')
                inspect(WORKSHOP)
                assert p.locator('#di-sheet').input_value() == WORKSHOP and model()['sheets'][2]['selected']
                assert snapshot() == readonly_db and calls() == readonly_calls
                ok('Included filtering preserves original noncontiguous indices0/2: location, checkbox and Inspect affect only worksheet2; excluding its visible card keeps it active, and restoring inclusion leaves all native SQLite/API unchanged')

                # Source choices, Restore and Apply update existing status cards.
                p.locator('[data-di-column="12"]').select_option('2')
                assert 'pending mapping' in mapping_state(2)
                assert p.locator('#di-worksheet-attention > strong').inner_text().startswith('1 included') and WORKSHOP in attention() and ARCHIVE not in attention()
                filter_view('mapping')
                assert visible_indices() == [1,2]
                inspect(WORKSHOP)
                assert p.locator('#di-sheet').input_value() == WORKSHOP
                filter_view('all')
                inspect(DECK)
                p.locator('#di-header').select_option('4')
                p.locator('#di-name-column').select_option('-1')
                assert 'pending mapping' in mapping_state(0) and 'item-name' in mapping_state(0)
                assert p.locator('#di-worksheet-attention > strong').inner_text().startswith('2 included') and DECK in attention() and WORKSHOP in attention()
                inspect(ARCHIVE)
                p.locator('[data-di-column="12"]').select_option('2')
                assert 'pending mapping' in mapping_state(3)
                assert p.locator('#di-worksheet-attention > strong').inner_text().startswith('2 included') and ARCHIVE not in attention()
                filter_view('mapping')
                assert visible_indices() == [0,1,2,3]
                status_layout('selected_attention_with_excluded_pending')
                inspect(DECK)
                restore_mapping()
                assert 'applied mapping recorded' in mapping_state(0)
                assert p.locator('#di-worksheet-attention > strong').inner_text().startswith('1 included') and DECK not in attention() and WORKSHOP in attention()
                inspect(WORKSHOP)
                apply_mapping(True, True)
                assert 'applied mapping recorded' in mapping_state(2)
                assert p.locator('#di-worksheet-attention > strong').inner_text().startswith('0 included')
                # Needs mapping membership changes live, without changing active sheet.
                assert visible_indices() == [1,3] and p.locator('#di-sheet').input_value() == WORKSHOP
                assert p.locator('[data-di-sheet-card="2"]').evaluate('n=>n.hidden')
                filter_view('all')
                jump('items')
                edit(1, 'Fictional UI114 corrected workshop spare', '000-114-WORKSHOP', '000-PN-114-WORKSHOP')
                inspect(ARCHIVE)
                assert active()['mapping']['dirty'] and not active()['selected']
                assert snapshot() == readonly_db and calls() == readonly_calls
                checked = check()
                assert latest('/document/review')['response']['summary']['inventory_review']['total_items'] == 3
                assert checked['request']['draft']['inventory_sheets'][1]['sheet'] == WORKSHOP
                assert all(s['sheet'] not in (SUMMARY,ARCHIVE) for s in checked['request']['draft']['inventory_sheets'])
                ok('Live pending/header/missing-Name/Restore/Apply status and Needs mapping membership follow each original worksheet; attention names/counts include only selected worksheets, and an active excluded pending mapping does not block real Check of the three selected records')
                accepted_summary = p.locator('#di-inventory-review').inner_text()
                filter_layout('accepted_review_filtering', {'all':[0,1,2,3],'included':[0,2],'mapping':[1,3]}, True, accepted_summary)
                assert active()['sheet'] == ARCHIVE and p.locator('#di-sheet').input_value() == ARCHIVE

                # Guards retain a genuine accepted review and an immutable controlled
                # pending request; real unchanged retries run in retained safeguards.
                filter_view('included')
                capture_filter()
                p.evaluate('()=>{ui114Form.request={op_id:"fictional-ui114-request",draft:JSON.parse(JSON.stringify(ui114Form.document.draft)),review_token:ui114Form.review.review_token,confirmed:true};}')
                for flag in ('busy','uncertain'):
                    p.evaluate('(flag)=>{ui114Form[flag]=true;ui114Hooks.lock();}', flag)
                    assert p.locator('[data-di-worksheet-filter]').evaluate_all('ns=>ns.every(n=>n.disabled)')
                    before = material(), signed(), snapshot(), calls(), captured_view(), p.evaluate('document.activeElement.id')
                    invoke_filter()
                    assert (material(), signed(), snapshot(), calls(), captured_view(), p.evaluate('document.activeElement.id')) == before
                    p.evaluate('(flag)=>{ui114Form[flag]=false;ui114Hooks.lock();}', flag)
                p.evaluate('()=>{ui114Form.request=null;ui114Hooks.lock();}')
                before = material(), signed(), snapshot(), calls(), captured_view()
                p.evaluate('''()=>{const d=document.createElement('dialog');d.id='fictional-ui114-modal';d.innerHTML='<input id="fictional-ui114-modal-focus">';document.body.append(d);d.showModal();document.querySelector('#fictional-ui114-modal-focus').focus();}''')
                invoke_filter()
                assert (material(), signed(), snapshot(), calls(), captured_view()) == before and p.evaluate('document.activeElement.id') == 'fictional-ui114-modal-focus'
                p.evaluate('()=>{const d=document.querySelector("#fictional-ui114-modal");d.close();d.remove();}')
                before = material(), signed(), snapshot(), calls(), captured_view(), p.evaluate('document.activeElement.id')
                p.evaluate('()=>{const token=state.auth.token;state.auth.token="fictional-stale-session";ui114CapturedFilter();state.auth.token=token;}')
                assert (material(), signed(), snapshot(), calls(), captured_view(), p.evaluate('document.activeElement.id')) == before
                ok('Busy/uncertain disable filters and captured callbacks retain mapping/rows, genuine review/confirmation and controlled immutable request; modal/session ownership guards retain view, focus, APIs and every native SQLite table')

                # A source-proven native seed produces actual blocked append diagnostics.
                source = latest('/document/scan')['response']['source']
                seeded = inventory_action('import_list', {'package': {'format':'ajinventory-3',
                  'classification':{'schema':1,'categories':[],'assignments':{}},
                  'list':{'name':'Fictional UI114 duplicate-source destination','locations':['Fictional deck']},
                  'items':[{'id':'fictional-ui114-seed','values':{'name':'Fictional UI114 seeded cable','serial':'00000111-NEW','quantity':0,'location':'Fictional deck'},
                    'source':{'document_import':source,'sheet':DECK,'source_row':13}}]}})
                report['fixture_setup'] = {'method':'One source-proven native import_list through disposable TestClient','id':seeded['id'],'items':seeded['imported_items']}
                p.locator('#sb-close').click()
                open_builder(fixtures[0],seeded['id'])
                stale_before = material(), signed(), snapshot(), calls(), captured_view(), p.evaluate('document.activeElement.id')
                invoke_filter()
                assert (material(), signed(), snapshot(), calls(), captured_view(), p.evaluate('document.activeElement.id')) == stale_before
                ok('A detached filter callback from the closed builder cannot change the replacement proposal, current filter membership, APIs, SQLite or focus')
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                p.locator('#sb-review').click()
                expect(p.locator('#di-review-conflicts')).to_be_visible()
                blocked = latest('/document/review')['response']['summary']['inventory_review']
                assert not blocked['can_save'] and blocked['conflicts']['duplicate_count'] == 1
                assert p.evaluate('ui114Form.review===null') and p.locator('#di-confirm').is_disabled()
                blocked_summary = p.locator('#di-inventory-review').inner_text()
                filter_layout('blocked_review_filtering', {'all':[0,1,2,3],'included':[0,2],'mapping':[1]}, False, blocked_summary)

                # Missing-Name is source-mapping attention, not a fabricated blanket
                # save blocker; Apply updates the excluded card and an empty filter.
                filter_view('all')
                inspect(SUMMARY)
                p.locator('#di-name-column').select_option('0')
                assert 'pending mapping' in mapping_state(1)
                assert p.locator('#di-worksheet-attention > strong').inner_text().startswith('0 included')
                apply_mapping(True, False)
                assert 'applied mapping recorded' in mapping_state(1)
                assert not active()['selected']
                filter_view('mapping')
                assert visible_indices() == []
                assert '0' in p.locator('#di-worksheet-filter-count').inner_text()
                assert p.locator('#di-sheet').input_value() == SUMMARY
                status_layout('empty_needs_mapping_filter', '#di-worksheet-filter-count')
                ok('Explicit Apply changes an excluded worksheet from missing Name to an applied mapping; Needs mapping can be empty while keeping that excluded worksheet active and selected attention at zero')

                # Drain static/API intercepts before shutdown, avoiding an in-flight
                # request cancellation after successful assertions.
                p.wait_for_load_state('networkidle')
                assert not report['errors'], report['errors']
                assert not [x for x in exchanges if x['path'].endswith('/action')], exchanges
                assert all(value == report['source_hashes'][name] for name,value in report['served_asset_hashes'].items())
                assert all(sha(SOURCE/name)==value for name,value in report['source_hashes'].items())
                assert sha(SOURCE/'RELEASE_FILES.json')==report['runtime_manifest_sha256']
                assert sha(Path(__file__))==report['harness_sha256'] and sha(chrome)==report['chromium_executable_sha256']
                assert all(sha(path)==report['fictional_fixture_hashes'][path.name] for path in fixtures)
                ok('Browser sends no action writes or unhandled JS errors; served assets match the frozen source and source/manifest/harness/Chromium/fictional XLSX hashes remain unchanged')
                report['passed']=True
            except Exception:
                report['passed']=False
                p.screenshot(path=str(OUT/'FAILURE.png'))
                print(json.dumps(dict(status=p.locator('#sb-result').inner_text() if p.locator('#sb-result').count() else '',recent_api=[dict(path=x['path'],status=x['status']) for x in exchanges[-4:]])))
                raise
            finally:
                report['summary']=dict(checks_passed=len(report['checks']),unexpected_errors=len(report['errors']))
                (OUT/'UI114_WORKSHEET_OVERVIEW_BROWSER_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__=='__main__':
    main()
