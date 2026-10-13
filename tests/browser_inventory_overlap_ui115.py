"""UI115 overlap advice against real APIs in a disposable fictional C01 company.

Run with WAVELINK_TEST_SOURCE and WAVELINK_CHROMIUM_EXECUTABLE set. This creates
literal fictional XLSX and a temporary SQLite company through the existing C01
wrappers. It never contacts GitHub, Render or a production service. Service
worker registration and WebSockets are suppressed, as in the UI114 harness.
"""
import copy
import hashlib
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
sys.path[:0] = [str(SOURCE), str(ROOT), str(ROOT / 'tests')]
from test_company_c01 import PASS, activate, client, instance
from browser_import_row_selection_ui105 import selection_workbook

OUT = Path(os.environ.get('WAVELINK_UI115_OVERLAP_EVIDENCE_DIR', str(ROOT.parent / 'evidence-ui115/browser-overlap')))
TRACKED = ('app/document_import.py', 'app/document_extract.py', 'app/inventory.py',
           'app/static/document_import.js', 'app/static/document_import.css',
           'app/static/setup_builders.js', 'app/static/index.html', 'app/static/sw.js')
DECK, WORKSHOP, SUMMARY, ARCHIVE = 'Fictional deck & stock', 'Fictional workshop stock', 'Summary', 'Fictional excluded archive'
UNSAFE = '<tag & "serial">'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    chrome = Path(os.environ['WAVELINK_CHROMIUM_EXECUTABLE']).resolve()
    report = dict(checks=[], errors=[], widths=[1440, 1024, 390, 320], screenshots=[],
                  method='Real Chromium/IndexedDB, disposable fictional C01 HostedBoundary/CompanyAccess/core APIs and native SQLite; literal fictional XLSX.',
                  source_hashes={name: sha(SOURCE / name) for name in TRACKED}, served_asset_hashes={},
                  harness_sha256=sha(Path(__file__)), chromium_executable_sha256=sha(chrome),
                  limitations=['Service-worker registration and WebSockets are suppressed.',
                               'No production, Render, email, physical camera or Windows desktop acceptance.',
                               'Manual/missing-source and session ownership states use explicit controlled fixtures.',
                               'Busy/uncertain retry uses a genuine temporary-company save with its response held and lost, then retries its identical signed request.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui115-overlap-') as td:
        td = Path(td)
        header = ['Name', 'Asset reference', 'SN', 'PN', 'Qty expected', 'Qty counted', 'Remarks', 'Location']

        def item(name, asset='', serial='', location=''):
            return [name, asset, serial, 'PN-SHARED', 1, 99, 'Fictional retained note', location]

        fixtures = []
        for suffix in ('REVIEW', 'RETRY'):
            path = td / ('Fictional_UI115_' + suffix + '.xlsx')
            selection_workbook(path, [
                (DECK, [(5, header),
                        (9, item('Deck sensor ' + suffix, 'DECK-TAG-' + suffix, ' 000115 ', 'Deck shelf')),
                        (13, item('Deck asset ' + suffix, ' TAG-115 ', 'DECK-ASSET-SN-' + suffix, 'Deck crate')),
                        (17, item('Case-sensitive spare', serial='Case-A')),
                        (21, item('Leading-zero spare', serial='001')),
                        (25, item('PN and name repeat')),
                        (29, item('Same worksheet one', serial='SAME-SHEET')),
                        (33, item('Same worksheet two', serial='SAME-SHEET')),
                        (37, item('<img src=x onerror=alert(1)>', serial=UNSAFE, location='Deck & <unsafe>'))]),
                (SUMMARY, [(1, ['Department', 'Count']), (2, ['Summary only', 14])]),
                (WORKSHOP, [(7, header),
                            (35, item('Workshop sensor ' + suffix, 'WORK-TAG-' + suffix, '000115', 'Workshop shelf')),
                            (39, item('Workshop asset ' + suffix, 'TAG-115', 'WORK-ASSET-SN-' + suffix, 'Workshop bench')),
                            (43, item('Case-sensitive spare', serial='case-a')),
                            (47, item('Leading-zero spare', serial='1')),
                            (51, item('PN and name repeat')),
                            (55, item('Unsafe workshop spare', serial=UNSAFE, location='Workshop & <unsafe>'))]),
                (ARCHIVE, [(5, header), (9, item('Excluded source', serial='000115', location='Archive'))])])
            fixtures.append(path)
        large = td / 'Fictional_UI115_GROUP_BOUNDS.xlsx'
        selection_workbook(large, [
            (DECK, [(5,header)] + [(9+4*i,item('Deck member '+str(i),serial='MANY' if i<15 else 'GROUP-'+str(i-15).zfill(2))) for i in range(41)]),
            (SUMMARY, [(1,['Department','Count']),(2,['Summary only',82])]),
            (WORKSHOP, [(7,header)] + [(35+4*i,item('Workshop member '+str(i),serial='MANY' if i<15 else 'GROUP-'+str(i-15).zfill(2))) for i in range(41)]),
            (ARCHIVE, [(5,header),(9,item('Excluded source',serial='NO-GROUP'))])])
        fixtures.append(large)
        report['fictional_fixture_hashes'] = {path.name: sha(path) for path in fixtures}
        installation = instance.__wrapped__(td)
        with client(installation) as c, sync_playwright() as pw:
            activate(c)
            origin = installation[2].external_origin
            store = c.app.state.core.state.store
            browser = pw.chromium.launch(headless=True, args=['--no-sandbox','--no-zygote','--single-process'], executable_path=str(chrome))
            report['chromium_version'] = browser.version
            p = browser.new_page(viewport={'width': 1440, 'height': 1000})
            p.set_default_timeout(30000)
            p.on('pageerror', lambda error: report['errors'].append(str(error)))
            p.on('dialog', lambda dialog: dialog.accept())
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

            def calls():
                return len(exchanges)

            def navigate(fragment, selector):
                p.evaluate('(hash)=>{location.hash=hash;render();}', fragment)
                expect(p.locator(selector)).to_be_visible()

            def model():
                return p.evaluate('()=>JSON.parse(JSON.stringify(ui115Form.document.inventory_import))')

            def active():
                return next(s for s in model()['sheets'] if s['sheet'] == p.locator('#di-sheet').input_value())

            def material():
                return p.evaluate('''()=>JSON.stringify({kind:ui115Form.resource,dirty:ui115Form.dirty,source:ui115Form.document.source,source_token:ui115Form.document.source_token,sheets:ui115Form.document.inventory_import.sheets.map(s=>({sheet:s.sheet,selected:s.selected,location:s.location,rows:s.rows,data:s.data,mapping:s.mapping,source_rows:s.source_rows,source_review:s.source_review,manual:s.manual,selected_rows:s.selected_rows})),target:ui115Form.document.inventory_import.target,title:ui115Form.document.inventory_import.title,description:ui115Form.document.inventory_import.description,summary:document.querySelector('#di-summary').innerHTML,confirmed:document.querySelector('#di-confirm').checked})''')

            def signed():
                return p.evaluate('()=>JSON.stringify({review:ui115Form.review,request:ui115Form.request})')

            def snapshot():
                with store.connection() as con:
                    tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
                    return {name: [tuple(r) for r in con.execute('SELECT * FROM "' + name + '" ORDER BY rowid')] for name in tables}

            def immutable():
                return material(), signed(), snapshot(), calls()

            def panel():
                return p.locator('#di-inventory-overlaps').inner_text()

            def source(sheet, position):
                return p.locator('[data-di-overlap-source="' + str(sheet) + '"][data-di-overlap-row="' + str(position) + '"]').first

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
                for index, sheet in enumerate(model()['sheets']):
                    control = p.locator('[data-di-sheet-location="' + str(index) + '"]')
                    if control.is_enabled():
                        control.fill('' if sheet['sheet'] in (DECK, WORKSHOP) else 'Fictional archive')
                p.locator('[data-di-sheet-select="3"]').uncheck()
                p.locator('#di-sheet').select_option(DECK)
                assert [i for i,s in enumerate(model()['sheets']) if s['selected']] == [0,2]
                p.locator('#di-row-picker').evaluate('n=>n.open=true')
                p.locator('#di-inventory-overlaps').evaluate('n=>n.open=true')

            def check():
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                response = latest('/document/review')
                assert response['status'] == 200 and response['response']['summary']['inventory_review']['can_save']
                p.locator('#di-confirm').check()
                expect(p.locator('#sb-import-save')).to_be_enabled()
                return copy.deepcopy(response)

            def edit(position, serial):
                p.locator('#di-row-picker').evaluate('n=>n.open=true')
                p.locator('[data-di-item-edit="' + str(position) + '"]').click()
                p.locator('#di-item-serial').fill(serial)
                p.locator('#di-item-apply').click()
                expect(p.locator('#di-item-editor')).not_to_be_visible()

            def capture():
                source(2, 1).evaluate('n=>{window.ui115CapturedOverlap=n.onclick;}')

            def invoke():
                p.evaluate('()=>ui115CapturedOverlap()')

            def jump(sheet, row):
                before = immutable()
                source(sheet, row).click()
                assert p.locator('#di-sheet').input_value() == model()['sheets'][sheet]['sheet']
                assert immutable() == before
                expect(p.locator('#di-inspected-source-row')).to_be_focused()
                assert ('Excel row '+str(model()['sheets'][sheet]['source_rows'][row-1])) in p.locator('#di-inspected-source-row').inner_text()

            def item_jump(sheet,row):
                before = immutable()
                p.locator('[data-di-overlap-items="'+str(sheet)+'"][data-di-overlap-row="'+str(row)+'"]').first.click()
                expect(p.locator('#di-inspected-overlap-item')).to_be_focused()
                assert p.locator('#di-sheet').input_value() == model()['sheets'][sheet]['sheet']
                assert p.locator('#di-row-search').input_value() == '' and p.locator('#di-row-filter').input_value() == 'all'
                assert immutable() == before

            def inventory_action(action, payload):
                auth = p.evaluate('({token:state.auth.token,hub:state.hub_id})')
                response = c.post('/api/inventory/action', json=dict(action=action,payload=payload,op_id=str(uuid.uuid4())), headers={'Authorization':'Bearer '+auth['token'],'x-aj-hub-id':auth['hub']})
                assert response.status_code == 200, response.text
                return response.json()

            def layout(case, confirmed, summary):
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    before = immutable()
                    p.locator('#di-inventory-overlaps').evaluate('n=>n.scrollIntoView({block:"start"})')
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (case,width)
                    bounds = p.locator('#di-inventory-overlaps button').evaluate_all('ns=>ns.map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom};})')
                    assert bounds and all(b['left'] >= -1 and b['right'] <= width+1 for b in bounds), (case,width,bounds)
                    assert all(not(min(a['right'],b['right'])>max(a['left'],b['left'])+1 and min(a['bottom'],b['bottom'])>max(a['top'],b['top'])+1) for i,a in enumerate(bounds) for b in bounds[i+1:]), (case,width,bounds)
                    jump(2,1)
                    item_jump(2,1)
                    jump(0,1)
                    item_jump(0,1)
                    assert immutable() == before
                    assert p.locator('#di-confirm').is_checked() == confirmed and p.locator('#sb-import-save').is_enabled() == confirmed
                    assert p.locator('#di-inventory-review').inner_text() == summary
                    filename = case + '_' + str(width) + '.png'
                    p.locator('#di-inventory-overlaps').evaluate('n=>n.scrollIntoView({block:"start"})')
                    p.screenshot(path=str(OUT/filename))
                    report['screenshots'].append(filename)
                    ok(case + ': overlap controls fit at ' + str(width) + 'px; cross-sheet source jumps preserve confirmation, signed request, summary, every SQLite table and API count')
                p.set_viewport_size({'width':1440,'height':1000})

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                p.evaluate('''()=>{const n=window.AJDocumentImport;window.AJDocumentImport={...n,scan(f,h){window.ui115Form=f;window.ui115Hooks=h;return n.scan(f,h);},lock(f){window.ui115Form=f;return n.lock(f);}};}''')
                open_builder(fixtures[0])
                text = panel()
                assert '000115' in text and 'TAG-115' in text and UNSAFE in text
                assert 'Case-A' not in text and 'case-a' not in text and 'SAME-SHEET' not in text
                assert 'PN-SHARED' in text
                assert 'Deck shelf' in text and 'Workshop shelf' in text and 'Excel row 9' in text and 'Excel row 35' in text
                assert p.locator('#di-inventory-overlaps img,#di-inventory-overlaps tag').count() == 0
                assert p.locator('[data-di-overlap-source]').count() == 6
                ok('Real fictional XLSX produces three literal cross-sheet groups; same PN/name, case variants, leading-zero variants, same-sheet-only repeats and excluded archive are omitted; locations/source rows and escaped unsafe text remain visible')

                baseline = snapshot(),calls()
                p.locator('#di-sheet').select_option(WORKSHOP)
                p.locator('#di-row-picker').evaluate('n=>n.open=true')
                p.locator('[data-di-row-select="1"]').uncheck()
                assert '000115' not in panel() and p.locator('[data-di-overlap-source]').count() == 4
                p.locator('[data-di-row-select="1"]').check()
                assert '000115' in panel() and p.locator('[data-di-overlap-source]').count() == 6
                edit(1,'000116')
                assert '000115' not in panel()
                edit(1,'000115')
                p.locator('[data-di-column="2"]').select_option('3')
                assert 'Pending mapping' in panel() and '000115' in panel()
                p.locator('#di-restore-mapping').click()
                assert 'Pending mapping' not in panel()
                assert (snapshot(),calls()) == baseline
                ok('Row exclusion/reinclusion, current item serial edits and pending/Restore mapping refresh advice without any API call or SQLite write')

                p.locator('[data-di-sheet-location="2"]').fill('Fictional reviewed workshop')
                assert 'Fictional reviewed workshop' in panel() and 'Deck shelf' in panel()
                accepted = check()
                assert accepted['response']['summary']['inventory_review']['total_items'] == 14
                accepted_summary = p.locator('#di-inventory-review').inner_text()
                layout('accepted_overlap_review',True,accepted_summary)

                # Source navigation cannot bypass ownership, active modal or a stale callback.
                capture()
                before = immutable()
                p.evaluate('''()=>{const d=document.createElement('dialog');d.id='fictional-ui115-modal';d.innerHTML='<input id="fictional-ui115-modal-focus">';document.body.append(d);d.showModal();document.querySelector('#fictional-ui115-modal-focus').focus();}''')
                invoke()
                assert immutable() == before and p.evaluate('document.activeElement.id') == 'fictional-ui115-modal-focus'
                p.evaluate('()=>{const d=document.querySelector("#fictional-ui115-modal");d.close();d.remove();}')
                before = immutable(),p.locator('#di-sheet').input_value()
                p.evaluate('()=>{const token=state.auth.token;state.auth.token="fictional-stale-session";ui115CapturedOverlap();state.auth.token=token;}')
                assert (immutable(),p.locator('#di-sheet').input_value()) == before
                ok('Captured overlap source callback respects modal/session ownership and leaves the checked source, signed receipt, current worksheet and SQLite unchanged')

                # Original row-unavailability is explicit for manual edited text.
                p.locator('#di-sheet').select_option(DECK)
                p.locator('#di-inventory_rows').evaluate('n=>{let d=n.closest("details");while(d){d.open=true;d=d.parentElement?.closest("details");}}')
                raw = p.locator('#di-inventory_rows').input_value()
                p.locator('#di-inventory_rows').fill(raw+'\n')
                assert active()['manual'] and 'Manual' in panel() and 'unavailable' in panel().lower()
                assert p.locator('[data-di-overlap-source="0"]').evaluate_all('ns=>ns.every(n=>n.disabled)')
                item_jump(0,1)
                assert active()['manual'] and 'source_rows' not in active()
                manual_before = immutable()
                p.locator('[data-di-overlap-source="0"]').first.evaluate('n=>{n.disabled=false;n.onclick();}')
                assert immutable() == manual_before
                p.locator('#di-map').click()
                assert not active()['manual'] and p.locator('[data-di-overlap-source="0"]').evaluate_all('ns=>ns.every(n=>!n.disabled)')
                ok('Manual full-row editing retains current overlap advice with original-source unavailable labels; forced disabled source jump does nothing; explicit Apply restores confirmed source references')

                # A real source-proven seed drives a genuinely blocked append.
                original_source = latest('/document/scan')['response']['source']
                seeded = inventory_action('import_list', {'package': {'format':'ajinventory-3','classification':{'schema':1,'categories':[],'assignments':{}},'list':{'name':'Fictional UI115 duplicate-source destination','locations':['Deck shelf']},'items':[{'id':'fictional-ui115-seed','values':{'name':'Fictional original-source seed','serial':'000115','quantity':1,'location':'Deck shelf'},'source':{'document_import':original_source,'sheet':DECK,'source_row':9}}]}})
                open_builder(fixtures[0],seeded['id'])
                detached_before = immutable(),p.locator('#di-sheet').input_value()
                invoke()
                assert (immutable(),p.locator('#di-sheet').input_value()) == detached_before
                p.locator('#sb-review').click()
                expect(p.locator('#di-review-conflicts')).to_be_visible()
                blocked = latest('/document/review')['response']['summary']['inventory_review']
                assert not blocked['can_save'] and blocked['conflicts']['duplicate_count'] == 1
                assert p.evaluate('ui115Form.review===null') and p.locator('#di-confirm').is_disabled()
                layout('blocked_overlap_review',False,p.locator('#di-inventory-review').inner_text())
                ok('Native duplicate-source append remains blocked after all overlap source jumps; detached callbacks cannot alter a replacement builder')

                # Bound groups and repeated occurrences through genuine focused buttons.
                open_builder(fixtures[2])
                assert '27 exact identifier groups' in p.locator('#di-overlap-counts').inner_text()
                assert p.locator('#di-overlap-results .di-overlap-group').count() == 10
                assert p.locator('#di-overlap-results .di-overlap-group').first.locator('li').count() == 10
                bounded_before = immutable()
                for _ in range(2):
                    p.locator('[data-di-overlap-members="0"][data-di-overlap-direction="1"]').click()
                    assert p.locator('#di-overlap-results .di-overlap-group').first.locator('li').count() == 10
                    assert immutable() == bounded_before
                assert p.locator('[data-di-overlap-members="0"][data-di-overlap-direction="1"]').is_disabled()
                for expected in (10,7):
                    p.locator('#di-overlaps-next').click()
                    assert p.locator('#di-overlap-results .di-overlap-group').count() == expected
                    assert immutable() == bounded_before
                assert p.locator('#di-overlaps-next').is_disabled()
                assert not report['errors'],report['errors']
                ok('Real focused member/group pagination bounds rendering to ten groups and ten occurrences, preserves all 30 repeated members and 27 groups, and changes no material, signed state, API or SQLite data')

                # A genuine lost save response proves frozen requests and identical retry.
                open_builder(fixtures[1])
                reviewed = check()
                jump(2,1)
                capture()
                before_saved_items = len(snapshot()['inventory_items'])
                delayed['path'],delayed['held'] = '/api/builders/document/action',None
                p.locator('#sb-import-save').click()
                for _ in range(300):
                    if delayed['held'] is not None:
                        break
                    p.wait_for_timeout(100)
                assert delayed['held'] is not None
                expect(p.locator('#sb-close')).to_be_disabled()
                assert p.locator('[data-di-overlap-source],[data-di-overlap-items]').evaluate_all('ns=>ns.every(n=>n.disabled)')
                assert len(snapshot()['inventory_items']) == before_saved_items + 14
                busy_payload = copy.deepcopy(latest('/document/action')['request'])
                busy_before = immutable(),p.locator('#di-sheet').input_value()
                invoke()
                assert (immutable(),p.locator('#di-sheet').input_value()) == busy_before
                held_route,_ = delayed['held']
                held_route.abort('failed')
                expect(p.locator('#sb-import-save')).to_have_text('Retry unchanged request')
                assert p.locator('[data-di-overlap-source],[data-di-overlap-items]').evaluate_all('ns=>ns.every(n=>n.disabled)')
                uncertain_before = immutable(),p.locator('#di-sheet').input_value()
                invoke()
                assert (immutable(),p.locator('#di-sheet').input_value()) == uncertain_before
                assert p.evaluate('ui115Form.request.op_id') == busy_payload['op_id']
                before_reviews = sum(x['path'].endswith('/document/review') for x in exchanges)
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                retried = latest('/document/action')
                assert retried['request'] == busy_payload
                assert len(snapshot()['inventory_items']) == before_saved_items + 14
                assert busy_payload['draft'] == reviewed['request']['draft'] and busy_payload['review_token'] == reviewed['response']['review_token']
                assert sum(x['path'].endswith('/document/review') for x in exchanges) == before_reviews
                report['retry'] = dict(exact_request_match=True,operation_id=busy_payload['op_id'],receipt_id=retried['response']['id'],saved_items=retried['response'].get('imported_items'))
                assert len([x for x in exchanges if x['path'].endswith('/document/action')]) == 2
                ok('Real busy/lost-response uncertain states disable overlap jumps; captured handlers cannot change material or signed state, and unchanged retry sends the exact original draft/token/op_id once more without a new review')

                p.wait_for_load_state('networkidle')
                assert not report['errors'],report['errors']
                assert all(value==report['source_hashes'][name] for name,value in report['served_asset_hashes'].items())
                assert all(sha(SOURCE/name)==value for name,value in report['source_hashes'].items())
                assert sha(Path(__file__))==report['harness_sha256'] and sha(chrome)==report['chromium_executable_sha256']
                assert all(sha(path)==report['fictional_fixture_hashes'][path.name] for path in fixtures)
                report['passed']=True
            except Exception:
                report['passed']=False
                p.screenshot(path=str(OUT/'FAILURE.png'))
                print(json.dumps(dict(status=p.locator('#sb-result').inner_text() if p.locator('#sb-result').count() else '',recent_api=[dict(path=x['path'],status=x['status']) for x in exchanges[-4:]])))
                raise
            finally:
                report['summary']=dict(checks_passed=len(report['checks']),unexpected_errors=len(report['errors']))
                (OUT/'UI115_OVERLAP_BROWSER_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__=='__main__':
    main()
