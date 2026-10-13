"""UI112 inventory import navigation in a disposable fictional C01 company.

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

OUT = Path(os.environ.get('WAVELINK_UI112_IMPORT_EVIDENCE_DIR', str(ROOT.parent / 'evidence-ui112/browser-import')))
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
                               'One native inventory package is seeded through the real API to exercise genuine blocked append diagnostics; user navigation never sends a write action.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui112-import-safeguards-') as td:
        td = Path(td)
        header = ['Name', 'Asset reference', 'SN', 'PN', 'Qty expected', 'Qty counted', 'Remarks', 'Is box', 'Parent box reference', 'Location']
        fixtures = []
        for suffix in ('NEW', 'APPEND', 'MANUAL', 'STALE'):
            path = td / ('Fictional_UI112_' + suffix + '.xlsx')
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

            def write_rows(values):
                out = io.StringIO()
                writer = csv.DictWriter(out, fieldnames=list(values[0]), delimiter='\t', lineterminator='\n')
                writer.writeheader()
                writer.writerows(values)
                p.locator('#di-inventory_rows').evaluate('n=>n.closest("details").open=true')
                p.locator('#di-inventory_rows').fill(out.getvalue())

            def model():
                return p.evaluate('()=>JSON.parse(JSON.stringify(ui112Form.document.inventory_import))')

            def active():
                return next(s for s in model()['sheets'] if s['sheet'] == p.locator('#di-sheet').input_value())

            def signed():
                return p.evaluate('()=>JSON.stringify({review:ui112Form.review,request:ui112Form.request})')

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

            def validate_navigation_layout(case, overview=True):
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    for key in TARGETS:
                        if key == 'overview' and not overview:
                            assert p.locator('[data-di-inventory-jump="overview"]').is_disabled()
                            continue
                        jump(key, width)
                        assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (case, key, width)
                    p.locator('#di-inventory-view-nav').evaluate('n=>n.scrollIntoView({block:"center"})')
                    bounds = p.locator('#di-inventory-view-nav button').evaluate_all('ns=>ns.map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom};})')
                    assert all(b['left'] >= -1 and b['right'] <= width + 1 for b in bounds), (case, width, bounds)
                    assert all(not (min(a['right'], b['right']) > max(a['left'], b['left']) + 1 and min(a['bottom'], b['bottom']) > max(a['top'], b['top']) + 1) for i, a in enumerate(bounds) for b in bounds[i + 1:]), (case, width, bounds)
                    p.locator('#di-inventory-workspace-context').evaluate('n=>n.scrollIntoView({block:"center"})')
                    filename = case + '_' + str(width) + '.png'
                    p.screenshot(path=str(OUT / filename))
                    report['screenshots'].append(filename)
                    ok(case.replace('_', ' ') + ': all available shortcut targets receive actual focus, are visible, and fit without nav overlap/page overflow at ' + str(width) + 'px')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            def assert_readonly(before_material, before_signed, before_db, before_calls, confirmed):
                if material() != before_material:
                    (OUT / 'MATERIAL_DIFF.json').write_text(json.dumps({'before': before_material, 'after': material()}, indent=2) + '\n')
                assert material() == before_material
                assert signed() == before_signed
                assert snapshot() == before_db
                assert calls() == before_calls
                assert p.locator('#di-confirm').is_checked() == confirmed
                assert p.locator('#sb-import-save').is_enabled() == confirmed

            def capture_callbacks():
                p.evaluate('''()=>{window.ui112Captured={jump:document.querySelector('[data-di-inventory-jump="source"]').onclick,
                 inspect:document.querySelector('[data-di-sheet-inspect="1"]').onclick,
                 sheet:document.querySelector('#di-sheet').onchange};}''')

            def invoke_callbacks():
                p.evaluate('()=>{ui112Captured.jump();ui112Captured.inspect();ui112Captured.sheet();}')

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                p.evaluate('''()=>{const n=window.AJDocumentImport;window.AJDocumentImport={...n,
                 scan(f,h){window.ui112Form=f;window.ui112Hooks=h;return n.scan(f,h);},
                 lock(f){window.ui112Form=f;return n.lock(f);}};}''')

                # Real scan and review, with corrected fields/Notes, source coordinates,
                # box relationship, exclusions and another worksheet correction.
                open_builder(fixtures[0])
                assert [s['sheet'] for s in model()['sheets'] if s['selected']] == [DECK, WORKSHOP]
                assert p.locator('#di-sheet').locator('..').inner_text().startswith('Inspect worksheet')
                assert 'Worksheets to import' in p.locator('#di-inventory-plan').inner_text()
                assert p.locator('[data-di-inventory-jump="overview"]').is_disabled()
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                edit(2, 'Fictional corrected cable NEW', '00000111-EDIT-NEW', '000-PN-112-EDIT')
                relationship(2, 'container_ref', 'BOX-111-NEW')
                relationship(2, 'quantity', '7')
                inspect(WORKSHOP)
                jump('items')
                edit(1, 'Fictional corrected workshop spare NEW', '00000135-EDIT-NEW', '000-PN-WORKSHOP-EDIT')
                inspect(DECK)
                checked = check()
                before_material, before_signed, before_db, before_calls = material(), signed(), snapshot(), calls()
                overview_text = p.locator('#di-inventory-review').inner_text()
                inspect(SUMMARY)
                assert not active()['selected']
                assert p.locator('.di-inventory-inclusion-state').evaluate('n=>n.classList.contains("di-inventory-excluded")')
                validate_navigation_layout('accepted_excluded_sheet')
                assert_readonly(before_material, before_signed, before_db, before_calls, True)
                inspect(WORKSHOP)
                jump('items')
                p.locator('#di-row-search').fill('00000135-EDIT')
                assert p.locator('[data-di-item-edit]').count() == 1
                p.locator('#di-row-filter').select_option('included')
                jump('source')
                p.locator('#di-header-chooser').evaluate('n=>n.open=true')
                p.locator('#di-header-search').fill('Excel row 35')
                inspect(DECK)
                validate_navigation_layout('accepted_corrected_sheet')
                assert p.locator('#di-inventory-review').inner_text() == overview_text
                assert_readonly(before_material, before_signed, before_db, before_calls, True)
                report['accepted_navigation'] = dict(reviewed_draft_sha256=fingerprint(checked['request']['draft']),
                 signed_draft_sha256=fingerprint(json.loads(before_signed)), material_sha256=fingerprint(before_material),
                 sqlite_sha256=fingerprint(before_db), additional_review_or_action_calls=0,
                 original_review_sheet=checked['request']['draft']['sheet'], inspected_sheets=[SUMMARY, WORKSHOP, DECK])
                ok('Direct worksheet inspection plus all section shortcuts retain selected worksheets, material source drafts/corrections/relationships/exclusions, accepted check/token/confirmation and identical native SQLite; no API review or write is sent')

                # Controlled busy/uncertain states exercise the new controls without
                # sending a Save; genuine uncertain Save/retry is covered separately.
                capture_callbacks()
                for flag in ('busy', 'uncertain'):
                    p.evaluate('(flag)=>{ui112Form[flag]=true;ui112Hooks.lock();}', flag)
                    for locator in ['#di-sheet', '[data-di-sheet-inspect]', '[data-di-inventory-jump]']:
                        assert p.locator(locator).evaluate_all('ns=>ns.every(n=>n.disabled)')
                    before = material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')
                    invoke_callbacks()
                    assert (material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')) == before
                    p.evaluate('(flag)=>{ui112Form[flag]=false;ui112Hooks.lock();}', flag)
                capture_callbacks()
                stale_before = material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')
                p.evaluate('()=>{const token=state.auth.token;state.auth.token="fictional-replaced-session";ui112Captured.jump();ui112Captured.inspect();ui112Captured.sheet();state.auth.token=token;}')
                assert (material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')) == stale_before
                ok('Busy and uncertain navigation controls are disabled; captured inspect/jump/sheet callbacks and a stale login session cannot mutate material drafts, accepted confirmation, focus, API calls or SQLite')

                # One explicit real API fixture setup makes genuine duplicate-source
                # blocked append diagnostics; navigation remains write-free.
                source = latest('/document/scan')['response']['source']
                seeded = inventory_action('import_list', {'package': {'format': 'ajinventory-3',
                 'classification': {'schema': 1, 'categories': [], 'assignments': {}},
                 'list': {'name': 'Fictional UI112 existing inventory', 'locations': ['Fictional deck']},
                 'items': [{'id': 'fictional-seeded-cable', 'values': {'name': 'Fictional seeded cable',
                   'serial': '00000111-NEW', 'part_number': '000-PN-OLD', 'quantity': 0,
                   'location': 'Fictional deck'},
                   'source': {'document_import': source, 'sheet': DECK, 'source_row': 13}}]}})
                report['fixture_setup'] = {'method': 'One authorized /api/inventory/action import_list via disposable TestClient', 'id': seeded['id'], 'items': seeded['imported_items']}
                p.locator('#sb-close').click()
                open_builder(fixtures[0], seeded['id'])
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                p.locator('#sb-review').click()
                expect(p.locator('#di-review-conflicts')).to_be_visible()
                blocked = latest('/document/review')['response']['summary']['inventory_review']
                assert not blocked['can_save'] and blocked['conflicts']['duplicate_count'] == 1
                blocked_before = material(), signed(), snapshot(), calls()
                blocked_text = p.locator('#di-inventory-review').inner_text()
                inspect(SUMMARY)
                validate_navigation_layout('blocked_excluded_sheet')
                inspect(WORKSHOP)
                jump('overview')
                assert p.locator('#di-inventory-review').inner_text() == blocked_text
                assert (material(), signed(), snapshot(), calls()) == blocked_before
                assert p.locator('#di-confirm').is_disabled() and not p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_disabled()
                ok('Real duplicate-source blocked append retains exact conflict overview through excluded/included inspection and shortcuts, with confirmation/Save disabled, unchanged SQLite and no review/write calls')

                # Captured controls from this form cannot touch the replacement form.
                capture_callbacks()
                p.locator('#sb-close').click()
                open_builder(fixtures[2])
                replacement_before = material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')
                invoke_callbacks()
                assert (material(), signed(), snapshot(), calls(), p.evaluate('document.activeElement.id')) == replacement_before
                ok('Detached shortcuts, per-card inspection and sheet callbacks from a closed/replaced builder cannot alter the replacement proposal or API/SQLite/focus state')

                # Ambiguous source headings are distinguishable by physical column.
                choices = p.locator('#di-name-column option').all_text_contents()
                assert any('Serial' in value and 'Column 3' in value for value in choices), choices
                assert any('Serial' in value and 'Column 4' in value for value in choices), choices
                p.locator('[data-di-row-select="3"]').uncheck()
                p.locator('[data-di-row-select="4"]').uncheck()
                edit(2, name='Fictional pending corrected cable', serial='000-112-PENDING', part='000-PN-112-PENDING')
                before_rows, before_material, before_db, before_calls = rows(), material(), snapshot(), calls()
                p.locator('[data-di-column="12"]').select_option('2')
                assert active()['mapping']['dirty']
                pending_caption = p.locator('#di-inventory-mapping-status').inner_text()
                assert 'not been applied' in pending_caption.lower() and ('previous' in pending_caption.lower() or 'last applied' in pending_caption.lower()), pending_caption
                assert rows() == before_rows and p.locator('[data-di-item-edit="2"]').is_disabled()
                assert p.locator('#sb-import-save').is_disabled()
                p.locator('#sb-review').click()
                assert 'Apply the changed column mapping' in p.locator('#sb-result').inner_text()
                assert calls() == before_calls and snapshot() == before_db
                remap(False)
                assert rows() == before_rows and active()['mapping']['dirty']
                assert p.locator('[data-di-column="12"]').input_value() == '2'
                assert p.locator('#di-inventory-mapping-status').inner_text() == pending_caption
                assert calls() == before_calls and snapshot() == before_db
                validate_navigation_layout('pending_mapping', overview=False)
                ok('Repeated Serial headings display Column 3/Column 4; changing a source mapping reports pending choices with last-applied corrected rows intact, blocks Check/Save, and native Cancel keeps mapping choices and corrections without API/SQLite writes')
                remap(True)
                assert not active()['mapping']['dirty']
                assert p.locator('[data-di-column="12"]').input_value() == '2'
                assert rows()[1]['part_number'] == rows()[1]['serial'] == '00000111-MANUAL'
                assert p.locator('#di-inventory-mapping-status').inner_text() != pending_caption
                assert p.locator('#sb-import-save').is_disabled()
                advisory = p.locator('#di-inventory-mapping').inner_text()
                assert 'Serial' in advisory and ('more than one' in advisory.lower() or 'reused' in advisory.lower() or 'multiple' in advisory.lower() or 'same source' in advisory.lower() or 'shared source' in advisory.lower() or 'reuse' in advisory.lower()), advisory
                check()
                assert p.locator('#sb-import-save').is_enabled()
                ok('One source Serial column deliberately reused for SN and PN remains selected, receives an advisory, applies only after ordinary confirmation and passes genuine Check/confirmation without a forced remapping rule')

                # Applying a mapping without Name guides to the actual select.
                p.locator('#di-name-column').select_option('-1')
                before_calls, before_db = calls(), snapshot()
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    p.locator('#di-map').click()
                    expect(p.locator('#di-name-column')).to_be_focused()
                    rect = p.locator('#di-name-column').bounding_box()
                    assert rect and rect['x'] >= -1 and rect['x'] + rect['width'] <= width + 1 and 0 <= rect['y'] < 940, (width, rect)
                    assert 'item-name' in p.locator('#di-inventory-mapping-status').inner_text().lower()
                    assert calls() == before_calls and snapshot() == before_db
                    filename = 'missing_name_focus_' + str(width) + '.png'
                    p.screenshot(path=str(OUT / filename))
                    report['screenshots'].append(filename)
                    ok('Applying a missing Name mapping focuses the actual visible item-name source selector without API/SQLite mutation at ' + str(width) + 'px')
                p.set_viewport_size({'width': 1440, 'height': 1000})
                assert not report['errors'], report['errors']
                assert not [x for x in exchanges if x['path'].endswith('/action')], exchanges
                assert all(value == report['source_hashes'][name] for name, value in report['served_asset_hashes'].items())
                assert all(sha(SOURCE / name) == value for name, value in report['source_hashes'].items())
                assert sha(SOURCE / 'RELEASE_FILES.json') == report['runtime_manifest_sha256']
                assert sha(Path(__file__)) == report['harness_sha256'] and sha(chrome) == report['chromium_executable_sha256']
                assert all(sha(path) == report['fictional_fixture_hashes'][path.name] for path in fixtures)
                ok('No browser action writes or unhandled JavaScript errors; served assets match pinned source and source/manifest/harness/Chromium/fictional XLSX hashes remain unchanged throughout acceptance')
                report['passed'] = True
            except Exception:
                report['passed'] = False
                p.screenshot(path=str(OUT / 'FAILURE.png'))
                print(json.dumps(dict(status=p.locator('#sb-result').inner_text() if p.locator('#sb-result').count() else '', recent_api=[dict(path=x['path'], status=x['status']) for x in exchanges[-4:]])))
                raise
            finally:
                report['summary'] = dict(checks_passed=len(report['checks']), unexpected_errors=len(report['errors']))
                (OUT / 'UI112_IMPORT_NAVIGATION_BROWSER_RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
