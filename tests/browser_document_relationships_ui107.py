"""UI107 boxes/contents acceptance against a disposable fictional C01.

Real Chromium, real IndexedDB and CompanyAccess/core APIs. All source fixtures
are literal fictional XLSX files; no original private document is shown or saved.
WebSockets and service-worker registration are suppressed. Captured form state
is used only for transparent guard/serialization acceptance, not a product reload.
"""
import copy
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
import time
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

OUT = Path(os.environ.get('WAVELINK_UI107_EVIDENCE_DIR', str(ROOT.parent / 'evidence' / 'browser')))
TRACKED = ('app/document_import.py', 'app/document_structure.py', 'app/document_extract.py',
           'app/inventory.py', 'app/inventory_boxes.py', 'app/builder_hub.py',
           'app/static/document_import.js', 'app/static/document_import.css',
           'app/static/setup_builders.js', 'app/static/index.html', 'app/static/sw.js',
           'app/static/help.css', 'docs/user/topics/documentimport.html',
           'docs/user/topics/inventorybuilder.html', 'docs/user/topics/toolboxbuilder.html')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    report = dict(checks=[], errors=[], widths=[1440, 390, 320],
                  method='Real Chromium, genuine IndexedDB, disposable fictional C01 HostedBoundary/CompanyAccess/core APIs, literal fictional XLSX sources.',
                  source_hashes={name: sha(SOURCE / name) for name in TRACKED}, served_asset_hashes={},
                  harness_sha256=sha(Path(__file__)), runtime_manifest_sha256=sha(SOURCE / 'RELEASE_FILES.json'),
                  limitations=['Service-worker registration and WebSockets are suppressed.',
                               'No production, Render, live email, physical camera, Windows display or worker-upgrade acceptance.',
                               'Captured live form state is used for event-guard and in-memory serialization acceptance, not an end-user reload/restore workflow.',
                               'Parentage is limited to explicit boxes in the same selected worksheet; asset references are not matched to serials, part numbers or existing inventory.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui107-boxes-') as td:
        td = Path(td)
        sheets = ('Fictional Deck', 'Fictional Shore')
        header = ['Item name', 'Asset reference', 'Is box', 'Parent container reference', 'QTY Shall', 'Physical location', 'SN', 'PN', 'Qty Counted', 'Remarks']
        source = td / 'Fictional_UI107_Relationships.xlsx'
        selection_workbook(source, [(sheets[0], [
            (3, header),
            (8, ['Fictional zero child', 'CHILD-107', 'no', 'INNER-107', 0, 'Fictional workshop source', 'SAME-SN-107', 'SAME-PN-107', 88, 'Literal child note']),
            (13, ['Fictional nested box', 'INNER-107', 'yes', 'ROOT-107', 1, 'Fictional bench source', 'INNER-SN-107', 'SAME-PN-107', 88, 'Literal nested note']),
            (17, ['Fictional root box', 'ROOT-107', 'yes', '', 1, 'Fictional deck root', 'ROOT-SN-107', 'ROOT-PN-107', 88, 'Literal root note']),
            (22, ['Fictional repeated spare', 'SPARE-107', 'no', '', '', 'Fictional locker', 'SAME-SN-107', 'SAME-PN-107', 88, 'Literal Unknown note']),
            (27, ['Fictional excluded spare', 'EXCLUDED-107', 'no', '', 2, 'Fictional locker', '', 'SAME-PN-107', 88, 'Literal excluded note'])]),
            (sheets[1], [(5, header),
                (11, ['Fictional shore child', 'SHORE-CHILD-107', 'no', 'ROOT-107', 1, 'Fictional shore source', 'SHORE-SN-107', 'SAME-PN-107', 88, 'Literal shore child note']),
                (19, ['Fictional shore root', 'ROOT-107', 'yes', '', 1, 'Fictional shore root location', 'SHORE-ROOT-SN-107', 'ROOT-PN-107', 88, 'Literal shore root note']),
                (25, ['Fictional other-sheet-only box', 'SHORE-ONLY-107', 'yes', '', 1, 'Fictional shore only location', 'SHORE-ONLY-SN-107', 'ROOT-PN-107', 88, 'Literal other-sheet box note'])])])
        source_sha = sha(source)
        portuguese = td / 'Fictional_UI107_Portuguese.xlsx'
        selection_workbook(portuguese, [('Fictional Portuguese stock', [
            (2, ['Nome', 'Patrimônio', 'É caixa', 'Referência da caixa pai', 'Quantidade', 'Localização', 'SN', 'PN']),
            (7, ['Fictional instrumento', 'PT-CHILD-107', 'não', 'PT-ROOT-107', 0, 'Fictional local origem', 'PT-SN-107', 'PT-PN-107']),
            (16, ['Fictional caixa', 'PT-ROOT-107', 'sim', '', 1, 'Fictional local raiz', 'PT-BOX-SN-107', 'PT-BOX-PN-107'])])])
        containment = td / 'Fictional_UI107_ContainmentOnly.xlsx'
        selection_workbook(containment, [('Fictional minimal containment', [
            (1, ['Name', 'Is box', 'Parent box reference']),
            (6, ['Fictional minimal child', 'no', 'MINIMAL-ROOT-107'])])])
        generic = td / 'Fictional_UI107_AmbiguousContainer.xlsx'
        selection_workbook(generic, [('Fictional ambiguous refs', [
            (1, ['Item name', 'Asset reference', 'Is box', 'Container ID', 'Box reference', 'SN', 'PN', 'QTY Shall']),
            (7, ['Fictional generic child', 'GENERIC-CHILD-107', 'no', 'GENERIC-ROOT-107', 'KEEP-LITERAL-107', 'GENERIC-SN-107', 'GENERIC-PN-107', 0]),
            (15, ['Fictional generic root', 'GENERIC-ROOT-107', 'yes', '', '', 'GENERIC-BOX-SN-107', 'GENERIC-BOX-PN-107', 1])])])
        malicious = td / 'Fictional_UI107_LiteralReferences.xlsx'
        long_ref = 'FICTIONAL-LONG-BOX-107-' + 'LONGSEGMENT-' * 8
        selection_workbook(malicious, [('Fictional literal references', [
            (1, header),
            (5, ['Fictional literal child <img src=x onerror=window.ui107Injected=1>', 'LITERAL-CHILD-107', 'no', long_ref, 0, 'Fictional original literal location', 'LITERAL-SN-107', 'LITERAL-PN-107', 0, '<script>window.ui107Injected=2</script>']),
            (9, ['Fictional long reference box', long_ref, 'yes', '', 1, 'Fictional literal root', 'LONG-BOX-SN-107', 'LONG-BOX-PN-107', 0, 'Literal long box note'])])])
        paginated = td / 'Fictional_UI107_Paginated.xlsx'
        page_sheet = 'Fictional paginated relationships'
        page_rows = [(1, header)]
        for position in range(1, 126):
            page_rows.append((position * 3 + 2, ['Fictional page item ' + str(position), 'PAGE-ROOT-107' if position == 1 else 'PAGE-ASSET-107-' + str(position), 'yes' if position == 1 else 'no', 'PAGE-ROOT-107' if position == 125 else '', 1 if position == 1 else 0, 'Fictional page location', 'PAGE-SN-107-' + str(position), 'PAGE-PN-107-' + str(position), 99, 'Literal page note ' + str(position)]))
        selection_workbook(paginated, [(page_sheet, page_rows)])

        installation = instance.__wrapped__(td)
        with client(installation) as c, sync_playwright() as pw:
            activate(c)
            origin = installation[2].external_origin
            store = c.app.state.core.state.store
            browser = pw.chromium.launch(headless=True, args=['--no-sandbox'], executable_path=os.environ.get('WAVELINK_CHROMIUM_EXECUTABLE') or None)
            report['chromium_version'] = browser.version
            p = browser.new_page(viewport={'width': 1440, 'height': 1000})
            p.set_default_timeout(30000)
            p.on('pageerror', lambda error: report['errors'].append(str(error)))
            p.on('dialog', lambda dialog: dialog.accept())
            p.add_init_script('class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();')
            exchanges = []
            lose_next = {'save': False}
            delayed = {'path': None, 'held': None}

            def route(r):
                req = r.request
                u = urlsplit(req.url)
                response = c.request(req.method, u.path + ('?' + u.query if u.query else ''), headers=req.headers, content=req.post_data_buffer)
                source_name = 'app' + u.path
                if source_name in TRACKED and response.status_code == 200:
                    report['served_asset_hashes'][source_name] = hashlib.sha256(response.content).hexdigest()
                if u.path.startswith('/api/builders/document/'):
                    exchanges.append(dict(path=u.path, status=response.status_code, request=json.loads(req.post_data or '{}'), response=response.json()))
                if delayed['path'] == u.path:
                    delayed['path'] = None
                    delayed['held'] = (r, response)
                    return
                if lose_next['save'] and u.path == '/api/builders/document/action':
                    lose_next['save'] = False
                    r.abort('failed')
                    return
                r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

            p.route(origin + '/**', route)

            def latest(suffix):
                return next(x for x in reversed(exchanges) if x['path'].endswith('/' + suffix))

            def database_snapshot():
                with store.connection() as con:
                    names = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE 'inventory_%' OR name IN ('work_tasks','fieldwork_audit')) ORDER BY name")]
                    return {name: [tuple(r) for r in con.execute('SELECT * FROM "' + name + '" ORDER BY rowid')] for name in names}

            def builder(path):
                if p.locator('#sb-done').count():
                    p.locator('#sb-done').click()
                if p.locator('#sb-close').count():
                    p.locator('#sb-close').click()
                p.evaluate("()=>{location.hash='#builders';render();}")
                expect(p.locator('#sb-document')).to_be_visible()
                p.locator('#sb-document').click()
                p.locator('#sb-file').set_input_files(str(path))
                expect(p.locator('#di-kind')).to_be_visible(timeout=90000)
                assert latest('scan')['status'] == 200, latest('scan')['response']
                return copy.deepcopy(latest('scan')['response'])

            def data_rows():
                return list(csv.DictReader(io.StringIO(p.locator('#di-inventory_rows').input_value()), delimiter='\t'))

            def review(confirm=True):
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                assert latest('review')['status'] == 200, latest('review')['response']
                assert latest('review')['response']['summary']['inventory_review']['can_save'] is True
                if confirm:
                    p.locator('#di-confirm').check()
                    expect(p.locator('#sb-import-save')).to_be_enabled()
                return copy.deepcopy(latest('review')['request']['draft'])

            def reviewed_sheet(name):
                return next(x for x in latest('review')['request']['draft']['inventory_sheets'] if x['sheet'] == name)

            def draft_snapshot():
                return p.evaluate('JSON.stringify({resource:ui107LiveForm.resource,document:ui107LiveForm.document,review:ui107LiveForm.review,request:ui107LiveForm.request,dirty:ui107LiveForm.dirty})')

            def choose(position, included):
                p.locator('#di-row-picker').evaluate('n=>n.open=true')
                p.locator('[data-di-row-select="' + str(position) + '"]').set_checked(included)

            def screenshot(name, locator):
                p.wait_for_function('()=>!document.querySelector("#toast")?.classList.contains("visible")')
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    locator.evaluate('node=>node.scrollIntoView({block:"start"})')
                    p.evaluate('()=>scrollBy(0,-80)')
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name, width)
                    bounds = p.locator('#di-relationships input:visible,#di-relationships select:visible,#di-relationships button:visible').evaluate_all('(nodes)=>nodes.map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right};})')
                    assert not [b for b in bounds if b['left'] < -1 or b['right'] > width + 1], (name, width, bounds)
                    p.screenshot(path=str(OUT / (name + '_' + str(width) + '.png')))
                    ok(name.replace('_', ' ') + ' fits ' + str(width) + 'px without page overflow or clipped relationship controls')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                actor = store.session(p.evaluate('state.auth.token'))
                p.evaluate('''()=>{const native=window.AJDocumentImport;window.AJDocumentImport={...native,scan(f,h){window.ui107LiveForm=f;window.ui107LiveHooks=h;return native.scan(f,h);},lock(f){window.ui107LiveForm=f;return native.lock(f);}};}''')

                def panel_open():
                    p.locator('#di-relationships').evaluate('n=>n.open=true')
                    expect(p.locator('#di-relationship-search')).to_be_visible()

                def field(position, name):
                    return p.locator('[data-di-relationship-row="' + str(position) + '"][data-di-relationship-field="' + name + '"]')

                def edit(position, name, value):
                    panel_open()
                    node = field(position, name)
                    if name == 'is_container':
                        node.select_option(value)
                    else:
                        node.fill(value)

                def card(position):
                    return p.locator('[data-di-relationship-card="' + str(position) + '"]')

                def bad_review(message):
                    before = database_snapshot()
                    p.locator('#sb-review').click()
                    expect(p.locator('#sb-result')).to_contain_text(message)
                    assert latest('review')['status'] == 422, latest('review')['response']
                    assert p.locator('#di-confirm').is_disabled() and p.locator('#sb-import-save').is_disabled()
                    assert database_snapshot() == before

                def guard_events():
                    p.locator('#di-relationship-search').evaluate('n=>{const previous=n.value;n.value="GUARDED";n.oninput();n.value=previous;}')
                    p.locator('#di-relationship-filter').evaluate('n=>{const previous=n.value;n.value="boxes";n.onchange();n.value=previous;}')
                    field(1, 'asset').evaluate('n=>{const previous=n.value;n.value="GUARDED-ASSET";n.oninput();n.value=previous;}')
                    field(1, 'is_container').evaluate('n=>{const previous=n.value;n.value="yes";n.onchange();n.value=previous;}')
                    field(1, 'container_ref').evaluate('n=>{const previous=n.value;n.value="GUARDED-PARENT";n.oninput();n.value=previous;}')
                    field(1, 'quantity').evaluate('n=>{const previous=n.value;n.value="42";n.oninput();n.value=previous;}')
                    p.locator('[data-di-relationship-clear="1"]').evaluate('n=>n.onclick()')
                    p.locator('#di-relationships-next').evaluate('n=>n.onclick()')
                    p.locator('#di-relationships-prev').evaluate('n=>n.onclick()')

                initial_db = database_snapshot()
                scan = builder(source)
                assert scan['kind'] == 'inventory'
                assert all(s['suggested_kind'] == 'inventory' for s in scan['sheets'])
                indexes = {s['name']: i for i, s in enumerate(scan['sheets'])}
                p.locator('#di-select-data').click()
                for name, index in indexes.items():
                    p.locator('[data-di-sheet-location="' + str(index) + '"]').fill('')
                p.locator('#di-sheet').select_option(sheets[0])
                p.locator('#di-title').fill('Fictional UI107 boxes and contents')
                assert p.locator('[data-di-column="10"]').input_value() == '2'
                assert p.locator('[data-di-column="11"]').input_value() == '3'
                original_rows = data_rows()
                assert len(original_rows) == 5 and original_rows[0]['quantity'] == '0' and original_rows[3]['quantity'] == ''
                assert original_rows[0]['container_ref'] == 'INNER-107' and original_rows[1]['container_ref'] == 'ROOT-107'
                expect(p.locator('#di-relationships')).to_be_visible()
                assert not p.locator('#di-relationships').evaluate('n=>n.open')
                assert p.locator('#di-relationships-summary').inner_text() == 'Boxes and contents · 2 boxes · 2 contained rows'
                assert database_snapshot() == initial_db
                ok('Qualified English box and parent headers classify both sparse worksheets as inventory; the child-first nested hierarchy appears in a collapsed same-sheet inspector without writes')
                screenshot('boxes_panel_closed', p.locator('#di-relationships'))
                panel_open()
                expect(card(1)).to_contain_text('Excel row 8')
                expect(card(2)).to_contain_text('Excel row 13')
                expect(card(3)).to_contain_text('Excel row 17')
                expect(card(1).locator('.di-relationship-location strong')).to_have_text('Fictional deck root')
                expect(card(2).locator('.di-relationship-location strong')).to_have_text('Fictional deck root')
                expect(card(1)).to_contain_text('Fictional workshop source')
                assert p.locator('#di-box-options option').evaluate_all('nodes=>nodes.map(n=>n.value)') == ['INNER-107', 'ROOT-107']
                screenshot('boxes_panel_open', p.locator('#di-relationships'))
                screenshot('contained_row_location', card(1))
                ok('Located rows retain original Excel coordinates and only unique included explicit boxes are parent suggestions; contained rows preview the root box location and their differing source location')

                choose(5, False)
                draft = review()
                token = latest('review')['response']['review_token']
                reviewed = reviewed_sheet(sheets[0])
                assert reviewed['source_rows'] == [8, 13, 17, 22, 27] and reviewed['selected_rows'] == [1, 2, 3, 4]
                assert len(list(csv.DictReader(io.StringIO(reviewed['inventory_rows']), delimiter='\t'))) == 5
                rows_before_view = p.locator('#di-inventory_rows').input_value()
                panel_open()
                p.locator('#di-relationship-search').fill('SAME-PN-107')
                assert p.locator('[data-di-relationship-card]').count() == 4
                p.locator('#di-relationship-filter').select_option('boxes')
                assert p.locator('[data-di-relationship-card]').count() == 1
                p.locator('#di-relationship-filter').select_option('all')
                p.locator('#di-relationship-search').fill('')
                field(1, 'asset').focus()
                field(1, 'asset').evaluate('n=>n.oninput()')
                field(1, 'is_container').evaluate('n=>n.onchange()')
                p.locator('[data-di-relationship-clear="4"]').evaluate('n=>n.onclick()')
                p.locator('#di-relationships').evaluate('n=>n.open=false')
                panel_open()
                assert p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_enabled()
                assert p.evaluate('ui107LiveForm.review.review_token') == token
                assert p.locator('#di-inventory_rows').input_value() == rows_before_view
                ok('Opening, searching by repeated PN, filtering, focusing and unchanged field events preserve exact review approval, all five mapped rows, original row coordinates and the excluded item choice')

                edit(1, 'asset', 'CHILD-107-REVIEWED')
                assert p.locator('#sb-import-save').is_disabled() and not p.locator('#di-confirm').is_checked()
                assert p.evaluate('ui107LiveForm.review===null&&ui107LiveForm.request===null&&ui107LiveForm.dirty')
                changed = data_rows()
                assert [r['name'] for r in changed] == [r['name'] for r in original_rows]
                assert changed[0]['asset'] == 'CHILD-107-REVIEWED'
                for before, after in zip(original_rows, changed):
                    assert {k: v for k, v in before.items() if k != 'asset'} == {k: v for k, v in after.items() if k != 'asset'}
                draft = review()
                assert latest('review')['response']['review_token'] != token
                assert reviewed_sheet(sheets[0])['source_rows'] == [8, 13, 17, 22, 27]
                assert reviewed_sheet(sheets[0])['selected_rows'] == [1, 2, 3, 4]
                ok('An actual asset-reference field edit invalidates approval and changes only that TSV cell while preserving row order, original coordinates, excluded choices, SN/PN, source notes and zero/Unknown quantities')
                serialized = p.evaluate('JSON.stringify(ui107LiveForm.document)')
                p.evaluate('(value)=>{ui107LiveForm.document=JSON.parse(value);}', serialized)
                p.locator('#di-kind').select_option('logbook')
                p.locator('#di-kind').select_option('inventory')
                assert data_rows() == changed
                review()
                assert reviewed_sheet(sheets[0])['source_rows'] == [8, 13, 17, 22, 27]
                assert reviewed_sheet(sheets[0])['selected_rows'] == [1, 2, 3, 4]
                ok('Transparent in-memory JSON serialization and a real Import-as repaint retain the current edited relationship cells, row choices and original source coordinates; this is not a product reload workflow')

                p.locator('[data-di-relationship-clear="1"]').click()
                assert data_rows()[0]['container_ref'] == ''
                expect(card(1).locator('.di-relationship-location strong')).to_have_text('Fictional workshop source')
                assert p.locator('#sb-import-save').is_disabled()
                edit(1, 'container_ref', 'INNER-107')
                expect(card(1).locator('.di-relationship-location strong')).to_have_text('Fictional deck root')
                ok('No container explicitly clears one parent; entering its included same-sheet box reference restores the nested hierarchy and inherited root location without replacing source evidence')
                choose(3, False)
                panel_open()
                expect(card(1)).to_contain_text('matching parent box is excluded')
                assert p.locator('#di-box-options option').evaluate_all('nodes=>nodes.map(n=>n.value)') == ['INNER-107']
                bad_review('parent must be an explicitly marked box')
                expect(p.locator('#sb-result')).to_contain_text('source row 13')
                screenshot('excluded_parent_relationship', p.locator('#di-relationships'))
                screenshot('excluded_parent_card', card(1))
                screenshot('excluded_parent_error', p.locator('#sb-result'))
                choose(3, True)
                review()
                assert reviewed_sheet(sheets[0])['selected_rows'] == [1, 2, 3, 4]
                assert database_snapshot() == initial_db
                ok('Excluding the root box removes its parent suggestion and exposes the located parent-chain error; review makes no writes, and explicitly restoring that box permits a fresh check without automatic inclusion')

                edit(2, 'is_container', 'no')
                expect(card(1)).to_contain_text('not explicitly marked as a box')
                bad_review('parent must be an explicitly marked box')
                edit(2, 'is_container', 'yes')
                edit(2, 'quantity', '2')
                expect(card(2)).to_contain_text('must represent one container')
                bad_review('must represent one container')
                edit(2, 'quantity', '1')
                edit(2, 'container_ref', 'INNER-107')
                expect(card(2)).to_contain_text('own parent box')
                bad_review('cannot be its own parent')
                edit(2, 'container_ref', 'ROOT-107')
                edit(3, 'container_ref', 'INNER-107')
                expect(card(2)).to_contain_text('cycle')
                bad_review('cycle')
                edit(3, 'container_ref', '')
                edit(2, 'asset', 'ROOT-107')
                expect(card(3)).to_contain_text('unique reference')
                bad_review('Box references must be unique')
                edit(2, 'asset', 'INNER-107')
                edit(1, 'container_ref', 'SHORE-ONLY-107')
                expect(card(1)).to_contain_text('References do not link across worksheets')
                bad_review('parent must be an explicitly marked box')
                edit(1, 'container_ref', 'INNER-107')
                review()
                ok('Explicit box flags, one-container quantities, cycles, duplicate same-sheet box references and unresolved parents remain visible correction points and authoritative no-write review failures')

                delayed['path'] = '/api/builders/document/review'
                p.locator('#sb-review').click()
                p.wait_for_function('ui107LiveForm.busy===true')
                deadline = time.monotonic() + 30
                while delayed['held'] is None and time.monotonic() < deadline:
                    p.wait_for_timeout(25)
                assert delayed['held'] is not None
                assert p.locator('#di-relationships input,#di-relationships select,#di-relationships button').evaluate_all('nodes=>nodes.every(n=>n.matches(":disabled"))')
                guarded = draft_snapshot()
                guard_events()
                assert draft_snapshot() == guarded
                held_route, held_response = delayed['held']
                delayed['held'] = None
                held_route.fulfill(status=held_response.status_code, body=held_response.content, headers=dict(held_response.headers))
                expect(p.locator('#di-confirm')).to_be_enabled()
                p.locator('#di-confirm').check()
                ok('A genuine delayed review disables all relationship inputs/actions; direct stale event-handler calls cannot change the busy draft or its pending request')

                lose_next['save'] = True
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-import-save')).to_have_text('Retry unchanged request')
                first_save = copy.deepcopy(latest('action')['request'])
                assert p.locator('#di-relationships input,#di-relationships select,#di-relationships button').evaluate_all('nodes=>nodes.every(n=>n.matches(":disabled"))')
                guarded = draft_snapshot()
                guard_events()
                assert draft_snapshot() == guarded
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                assert latest('action')['request'] == first_save
                result = latest('action')['response']
                saved = store.inventory.get(result['id'], actor)
                assert len(saved['items']) == 7 and not saved['counts']
                by_asset_sheet = {(x['asset'], x['source']['sheet']): x for x in saved['items']}
                child = by_asset_sheet[('CHILD-107-REVIEWED', sheets[0])]
                inner = by_asset_sheet[('INNER-107', sheets[0])]
                root = by_asset_sheet[('ROOT-107', sheets[0])]
                shore_child = by_asset_sheet[('SHORE-CHILD-107', sheets[1])]
                shore_root = by_asset_sheet[('ROOT-107', sheets[1])]
                spare = by_asset_sheet[('SPARE-107', sheets[0])]
                assert child['container_id'] == inner['id'] and inner['container_id'] == root['id']
                assert shore_child['container_id'] == shore_root['id'] and shore_root['id'] != root['id']
                assert child['location'] == inner['location'] == root['location'] == 'Fictional deck root'
                assert shore_child['location'] == shore_root['location'] == 'Fictional shore root location'
                assert child['quantity'] == 0 and spare['quantity'] is None
                assert child['serial'] == spare['serial'] == 'SAME-SN-107' and child['part_number'] == spare['part_number'] == 'SAME-PN-107'
                assert child['source']['source_row'] == 8 and child['source']['reviewed_row'] == 1
                assert inner['source']['source_row'] == 13 and root['source']['source_row'] == 17
                assert all('Source Qty Counted: 88' in x['notes'] for x in saved['items'])
                assert 'Mapped location before containment: Fictional workshop source' in child['notes']
                assert 'Mapped location before containment: Fictional bench source' in inner['notes']
                assert 'Mapped location before containment: Fictional shore source' in shore_child['notes']
                assert 'Literal child note' in child['notes'] and 'Literal nested note' in inner['notes']
                assert sha(source) == source_sha
                ok('An uncertain genuine Save freezes relationship edits and retries an identical receipt once; one native inventory retains two independent same-reference sheet roots, nested IDs/root locations, repeated SN/PN, zero/Unknown and original differing-location evidence')

                scan = builder(portuguese)
                assert scan['kind'] == 'inventory' and scan['sheets'][0]['suggested_kind'] == 'inventory'
                assert p.locator('[data-di-column="10"]').input_value() == '2'
                assert p.locator('[data-di-column="11"]').input_value() == '3'
                assert p.locator('[data-di-column="1"]').input_value() == '1'
                panel_open()
                expect(field(1, 'is_container')).to_have_value('no')
                expect(field(2, 'is_container')).to_have_value('yes')
                expect(card(1)).to_contain_text('Excel row 7')
                review()
                ok('Accented Portuguese explicit box/parent headers and não/sim flags align backend inventory classification with the editable native mapping without inferring relationships from names')

                scan = builder(containment)
                assert scan['kind'] == 'inventory' and scan['sheets'][0]['suggested_kind'] == 'inventory'
                panel_open()
                assert data_rows()[0]['container_ref'] == 'MINIMAL-ROOT-107'
                expect(card(1)).to_contain_text('parent box was not found')
                bad_review('parent must be an explicitly marked box')
                ok('A containment-only Name/Is box/Parent box reference table is offered as inventory but a missing explicit parent remains a visible no-write correction point')

                scan = builder(generic)
                assert scan['kind'] == 'inventory'
                assert p.locator('[data-di-column="11"]').input_value() == '-1'
                generic_rows = data_rows()
                assert all(not row['container_ref'] for row in generic_rows)
                assert 'Source Container ID: GENERIC-ROOT-107' in generic_rows[0]['notes']
                assert 'Source Box reference: KEEP-LITERAL-107' in generic_rows[0]['notes']
                p.locator('#di-all-quality').evaluate('n=>n.open=true')
                expect(p.locator('#di-all-quality')).to_contain_text('deliberately map them')
                screenshot('ambiguous_mapping_advisory', p.locator('#di-all-quality'))
                p.locator('[data-di-column="11"]').select_option('3')
                p.locator('#di-map').click()
                assert data_rows()[0]['container_ref'] == 'GENERIC-ROOT-107'
                panel_open()
                expect(card(1)).to_contain_text('Parent reference resolves')
                review()
                ok('Generic Container ID and Box reference remain source notes with a manual-mapping advisory; choosing and applying the confirmed parent column explicitly creates the relationship')
                edit(1, 'asset', 'GENERIC-EDITED-107')
                p.locator('#di-map').click()
                panel_open()
                expect(p.locator('#di-relationship-edit-notice')).to_contain_text('replaced by mapped source values')
                assert data_rows()[0]['asset'] == 'GENERIC-CHILD-107'
                review()
                assert reviewed_sheet('Fictional ambiguous refs')['source_rows'] == [7, 15]
                ok('Explicitly applying the source mapping again replaces field edits with source values and shows that replacement while retaining confirmed original Excel coordinates')

                builder(paginated)
                panel_open()
                assert p.locator('[data-di-relationship-card]').count() == 50
                review()
                page_token = latest('review')['response']['review_token']
                p.locator('#di-relationships-next').click()
                assert p.locator('[data-di-relationship-card]').count() == 50
                expect(card(76)).to_contain_text('Excel row 230')
                assert p.locator('#di-confirm').is_checked()
                edit(76, 'asset', 'PAGE-EDITED-76')
                assert p.locator('#sb-import-save').is_disabled()
                p.locator('#di-relationship-search').fill('PAGE-PN-107-125')
                assert p.locator('[data-di-relationship-card]').count() == 1
                expect(card(125)).to_contain_text('Excel row 377')
                expect(field(125, 'container_ref')).to_have_value('PAGE-ROOT-107')
                review()
                assert latest('review')['response']['review_token'] != page_token
                payload = reviewed_sheet(page_sheet)
                assert len(list(csv.DictReader(io.StringIO(payload['inventory_rows']), delimiter='\t'))) == 125
                assert payload['source_rows'] == [position * 3 + 2 for position in range(1, 126)]
                rows = list(csv.DictReader(io.StringIO(payload['inventory_rows']), delimiter='\t'))
                assert rows[75]['asset'] == 'PAGE-EDITED-76' and rows[124]['container_ref'] == 'PAGE-ROOT-107'
                p.locator('#di-relationship-search').fill('')
                p.locator('#di-relationships-next').click()
                p.locator('#di-relationships-next').click()
                assert p.locator('[data-di-relationship-card]').count() == 25
                assert p.locator('#di-confirm').is_checked() and p.locator('#sb-import-save').is_enabled()
                p.locator('#di-relationship-filter').select_option('contents')
                assert p.locator('[data-di-relationship-card]').count() == 1
                screenshot('paginated_last_contained_row', card(125))
                ok('Relationship paging bounds the DOM to 50 rows, edits mapped position 76 without shifting any original coordinate, finds the final row by PN and preserves all 125 reviewed TSV records while view-only paging/filtering retain approval')

                scan = builder(malicious)
                panel_open()
                expect(field(1, 'container_ref')).to_have_value(long_ref)
                expect(card(1)).to_contain_text('<img src=x onerror=window.ui107Injected=1>')
                assert p.evaluate('window.ui107Injected===undefined')
                assert p.locator('#di-relationships img,#di-relationships script').count() == 0
                screenshot('long_literal_box_reference', p.locator('#di-relationships'))
                review()
                p.evaluate("""()=>{window.ui107DepartedNodes=[document.querySelector('[data-di-relationship-row="1"][data-di-relationship-field="asset"]'),document.querySelector('#di-relationship-search'),document.querySelector('[data-di-relationship-clear="1"]')];window.ui107DepartedForm=ui107LiveForm;window.ui107DepartedDocument=ui107LiveForm.document;}""")
                ok('Long parent/asset references remain editable at desktop and phone widths, and source HTML-like names/notes are escaped as literal text without executing markup')

                builder(source)
                snapshot = draft_snapshot()
                api_count = len(exchanges)
                p.evaluate('()=>{const [asset,search,clear]=ui107DepartedNodes;asset.value="DEPARTED-ASSET";asset.oninput();search.value="DEPARTED-SEARCH";search.oninput();clear.onclick();}')
                assert draft_snapshot() == snapshot and len(exchanges) == api_count
                assert p.evaluate('ui107DepartedDocument.inventory_import.sheets[0].rows.includes("DEPARTED-ASSET")===false')
                ok('Detached inspector handlers from a departed form cannot modify either the new live form or the earlier captured document and issue no API request')

                guide = browser.new_page()
                guide_errors = []
                guide.on('pageerror', lambda error: guide_errors.append(str(error)))
                for topic, sections in [('documentimport', ['ui106-source-interpretation', 'ui107-boxes-and-contents']),
                                        ('inventorybuilder', ['ui107-boxes-and-contents']),
                                        ('toolboxbuilder', ['ui106-source-interpretation'])]:
                    guide.goto((SOURCE / 'docs/user/topics' / (topic + '.html')).as_uri())
                    guide.evaluate('document.documentElement.style.scrollBehavior="auto"')
                    for width in [1440, 320]:
                        guide.set_viewport_size({'width': width, 'height': 1000})
                        for section in sections:
                            node = guide.locator('#' + section)
                            assert node.evaluate('n=>n.classList.contains("chapter")&&!!n.closest("main.wrap.layout > .content")')
                            node.evaluate('n=>n.scrollIntoView({block:"start",behavior:"instant"})')
                            expect(node).to_be_in_viewport()
                            bounds = node.evaluate('n=>{const b=n.getBoundingClientRect(),c=n.closest(".content").getBoundingClientRect();return {left:b.left,right:b.right,width:b.width,contentLeft:c.left,contentRight:c.right,contentWidth:c.width};}')
                            assert bounds['width'] > (600 if width == 1440 else 200), (topic, section, width, bounds)
                            assert bounds['left'] >= bounds['contentLeft'] - 1 and bounds['right'] <= bounds['contentRight'] + 1
                            assert guide.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (topic, width)
                            guide.screenshot(path=str(OUT / ('help_' + topic + '_' + section + '_' + str(width) + '.png')))
                        ok('Local ' + topic + ' help renders retained/new guidance inside the normal content column at ' + str(width) + 'px without horizontal overflow')
                assert not guide_errors, guide_errors
                guide.close()

                assert not report['errors'], report['errors']
                for name, digest in report['served_asset_hashes'].items():
                    assert report['source_hashes'][name] == digest, name
                for name, digest in report['source_hashes'].items():
                    assert sha(SOURCE / name) == digest, name
                assert sha(SOURCE / 'RELEASE_FILES.json') == report['runtime_manifest_sha256']
                assert sha(Path(__file__)) == report['harness_sha256']
                ok('All served tracked assets and final runtime manifest match the source pins, source fixtures are unchanged and Chromium reports no unexpected JavaScript errors')
            except Exception:
                p.screenshot(path=str(OUT / 'failure.png'), full_page=True)
                print(json.dumps({'errors': report['errors'], 'recent_api': [{'path': x['path'], 'status': x['status'], 'error': x['response'].get('error') if isinstance(x['response'], dict) else None} for x in exchanges[-6:]]}))
                raise
            finally:
                report['summary'] = dict(checks_passed=len(report['checks']), unexpected_errors=len(report['errors']), widths=report['widths'])
                (OUT / 'UI107_DOCUMENT_RELATIONSHIPS_BROWSER_REVIEW.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
