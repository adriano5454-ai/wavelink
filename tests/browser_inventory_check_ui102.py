"""Actual C01 verification acceptance, using fictional stock and real IndexedDB.

No production requests or storage resets. WebSockets and service-worker
registration are suppressed; ordinary app APIs, QR lookup and local drafts run.
The optional shipping example is read only from WAVELINK_IMPORT_SHIPPING_EXAMPLE.
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
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
from test_company_c01 import PASS, activate, client, instance

OUT = Path(os.environ.get('WAVELINK_UI102_EVIDENCE_DIR', '/tmp/wavelink-ui102/evidence/inventory'))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'checks': [], 'errors': [], 'widths': [1440, 390, 320],
              'method': 'Actual fictional C01 HostedBoundary/CompanyAccess/core APIs, Chromium and real IndexedDB. WebSockets and service-worker registration are suppressed.',
              'shipping_example': 'Pending source analysis and import contract; no supplied document is bundled.'}
    source = Path(os.environ['WAVELINK_TEST_SOURCE'])
    tracked = ('app/static/verification.js', 'app/static/inventory_workspace.js', 'app/static/operations.js', 'app/static/task_workspace.js', 'app/static/fieldwork.js', 'app/static/browser_workspace.js', 'app/static/equipment_workspace_ui79.css', 'app/static/work_execution_ui80.css', 'app/static/document_import.js', 'app/static/document_import.css', 'app/document_import.py', 'app/inventory.py', 'app/verification_tools.py', 'app/work_tasks.py')
    report['source_hashes'] = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in tracked}
    report['served_asset_hashes'] = {}
    previous_path = OUT / 'UI102_INVENTORY_BROWSER_REVIEW.json'
    previous = json.loads(previous_path.read_text()) if previous_path.is_file() else {}
    reuse_visuals = os.environ.get('WAVELINK_UI102_REUSE_SCREENSHOTS') == '1'
    if reuse_visuals:
        assert previous.get('source_hashes') == report['source_hashes'], 'Retake visual evidence after any app source change.'
        report['reused_visual_evidence'] = []

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui102-verification-') as td:
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
            p.add_init_script("class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();")
            exchanges = []
            lose_next = {'action': None}

            def route(r):
                req = r.request
                u = urlsplit(req.url)
                path = u.path + ('?' + u.query if u.query else '')
                response = c.request(req.method, path, headers=req.headers, content=req.post_data_buffer)
                if 'app' + u.path in tracked and response.status_code == 200:
                    report['served_asset_hashes']['app' + u.path] = hashlib.sha256(response.content).hexdigest()
                if u.path.startswith(('/api/inventory/', '/api/verification/', '/api/tasks/', '/api/builders/')):
                    exchanges.append({'path': u.path, 'status': response.status_code, 'request': json.loads(req.post_data or '{}'), 'response': response.json() if 'application/json' in response.headers.get('content-type', '') else None})
                if lose_next['action'] is not None and req.method == 'POST' and u.path.endswith('/action') and lose_next['action'] == json.loads(req.post_data or '{}').get('action'):
                    lose_next['action'] = None
                    r.abort('failed')
                    return
                r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

            p.route(origin + '/**', route)

            def api_action(area, action, payload, expected=200, auth_override=None):
                a = auth_override or p.evaluate('({token:state.auth.token,hub:state.hub_id})')
                h = {'Authorization': 'Bearer ' + a['token'], 'x-aj-hub-id': a['hub']}
                r = c.post('/api/' + area + '/action', json={'action': action, 'payload': payload, 'op_id': str(uuid.uuid4())}, headers=h)
                assert r.status_code == expected, r.text
                return r.json()

            def navigate(fragment, selector):
                p.evaluate('(hash)=>{location.hash=hash;render();}', fragment)
                expect(p.locator(selector)).to_be_visible()

            def screenshot(name, locator):
                if reuse_visuals:
                    for width in report['widths']:
                        filename = name + '_' + str(width) + '.png'
                        assert (OUT / filename).is_file(), filename
                        report['reused_visual_evidence'].append(filename)
                        ok(name.replace('_', ' ') + ' aligns at ' + str(width) + 'px without horizontal page overflow (retained screenshot from the identical frozen app)')
                    return
                p.wait_for_function('()=>!document.querySelector("#toast")?.classList.contains("visible")')
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    locator.evaluate('node=>node.scrollIntoView({block:"start"})')
                    p.evaluate('()=>scrollBy(0,-80)')
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name, width)
                    p.screenshot(path=str(OUT / (name + '_' + str(width) + '.png')))
                    ok(name.replace('_', ' ') + ' aligns at ' + str(width) + 'px without horizontal page overflow')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                auth = p.evaluate('({token:state.auth.token,user:state.auth.person.user_id,hub:state.hub_id})')
                actor = store.session(auth['token'])
                book = api_action('inventory', 'create_list', {'name': 'Fictional UI102 verification stock', 'description': 'Disposable interface tests only.', 'locations': ['Training Deck', 'Training Workshop']})
                items = {}

                def item(key, **values):
                    values = {'name': 'Fictional item', 'location': 'Training Deck', 'quantity': None, 'notes': 'Fictional stock for UI review only.', **values}
                    items[key] = api_action('inventory', 'save_item', {'list_id': book['id'], 'values': values})
                    return items[key]

                box = item('box', name='Fictional amber transport case', asset='TRAIN-BOX-AMBER', is_container=True)
                item('zero', name='Fictional duplicate sensor', serial='TRAIN-SERIAL-ZERO', asset='TRAIN-ASSET-ZERO', model='TRAIN-MODEL-AZURE', notes='Unique sapphire inspection note', quantity=0, container_id=box['id'])
                item('unknown', name='Fictional duplicate sensor', serial='TRAIN-SERIAL-UNKNOWN', asset='TRAIN-ASSET-UNKNOWN', model='TRAIN-MODEL-CORAL', notes='Unique coral inspection note', container_id=box['id'])
                item('known', name='Fictional spare cable', serial='TRAIN-SERIAL-CABLE', quantity=2, location='Training Workshop')
                item('stale', name='Fictional retained form item', serial='TRAIN-SERIAL-STALE', notes='Original retained form evidence')
                assert items['zero']['id'] != items['unknown']['id']
                ok('Fictional inventory uses duplicate names with distinct IDs, exact zero and unknown quantities, and an explicit containing box')
                if os.environ.get('WAVELINK_IMPORT_SHIPPING_EXAMPLE'):
                    shipping_checks(p, store, actor, navigate, screenshot, exchanges, ok, report)

                navigate('#inventory/' + book['id'], '#inv-start')
                p.locator('#inv-start').click()
                expect(p.locator('#fw-count-form')).to_be_visible()
                p.locator('#fw-count-form [name=name]').fill('Fictional UI102 stock verification')
                assert '5' in p.locator('#stock-scope-preview').inner_text()
                box_values = {key: value for key, value in box.items() if key in {'name','type','sub_type','model','serial','asset','paired_with','paired_serial','date_onboard','date_offloaded','notes','quantity','unit','location','department_id','extra','is_container','container_id'}}
                items['box'] = api_action('inventory', 'save_item', {'list_id': book['id'], 'id': box['id'], 'version': box['version'], 'values': {**box_values, 'notes': 'Fictional scope changed after preview'}, 'reason': 'Test reviewed-scope guard'})
                p.locator('#stock-create').click()
                expect(p.locator('#fw-error')).to_contain_text('changed')
                assert not store.inventory.get(book['id'], actor)['counts']
                p.locator('#stock-refresh-scope').click()
                expect(p.locator('#stock-create')).to_be_enabled()
                ok('A stale start preview is refused without creating a session and requires an explicit refreshed scope')
                p.locator('#stock-create').click()
                expect(p.locator('#stock-heading')).to_have_text('Fictional UI102 stock verification')
                sid = p.evaluate('location.hash.split("/")[2]')
                count = lambda: store.inventory.count(sid, actor)
                assert count()['total'] == 5 and count()['checked'] == 0
                assert p.locator('#stock-rows [data-stock-row]').count() == 5
                ok('Starting through the actual UI creates one fixed five-record unchecked scope')
                item('later', name='Fictional later addition', serial='TRAIN-LATER-SCOPE')
                p.locator('#fw-refresh').click()
                expect(p.locator('#stock-filter-total')).to_contain_text('1 later')
                assert count()['total'] == 5 and count()['new_items'] == 1
                p.locator('[name=stock_query]').fill('later addition')
                assert not p.locator('#stock-rows [data-stock-row]').count()
                p.locator('#stock-clear-search').click()
                ok('Later stock is explicitly outside the frozen session, cannot be found as scoped work, and never expands completion requirements')
                screenshot('verification_queue', p.locator('#stock-heading'))
                screenshot('verification_results', p.locator('#stock-filter-total'))

                query = p.locator('[name=stock_query]')
                probes = [('duplicate sen', {'zero', 'unknown'}), ('serial-zero', {'zero'}), ('asset-unknown', {'unknown'}), ('model-azure', {'zero'}), ('training workshop', {'known'}), ('sapphire inspection', {'zero'}), ('amber transport case', {'box', 'zero', 'unknown'}), (items['zero']['id'][8:24], {'zero'})]
                for text, keys in probes:
                    query.fill(text)
                    actual = set(p.locator('#stock-rows [data-stock-row]').evaluate_all('nodes=>nodes.map(n=>n.dataset.stockRow)'))
                    assert actual == {items[key]['id'] for key in keys}, (text, actual, keys)
                ok('Manual partial search finds name, serial, asset, model, location, notes, containing box and item ID without merging duplicate names')
                query.fill('fictional-no-match-9bda')
                assert not p.locator('#stock-rows [data-stock-row]').count()
                expect(p.locator('#stock-rows')).to_contain_text('No items match')
                assert count()['checked'] == 0
                ok('An unmatched search shows a clear empty view and changes no result or completion count')
                p.locator('#stock-clear-search').click()
                assert query.input_value() == ''

                zero = p.locator('[data-stock-row="' + items['zero']['id'] + '"]')
                unknown = p.locator('[data-stock-row="' + items['unknown']['id'] + '"]')
                quantity_text = '(node)=>[...node.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join("").trim()'
                assert zero.locator('td').nth(2).evaluate(quantity_text) == '0'
                assert unknown.locator('td').nth(2).evaluate(quantity_text) == 'Unknown'
                zero.locator('[data-check]').click()
                expect(p.locator('#fw-form')).to_be_visible()
                expect(p.locator('#fw-form')).to_contain_text('Expected quantity: 0')
                p.locator('#fw-form [name=counted_quantity]').fill('0')
                p.locator('#fw-save').click()
                expect(p.locator('#fw-form')).not_to_be_visible()
                expect(p.locator('#stock-status')).to_contain_text('1 / 5')
                assert count()['checks'][items['zero']['id']]['counted_quantity'] == 0
                assert not p.locator('[data-stock-row="' + items['zero']['id'] + '"]').count()
                ok('An explicit Found result preserves zero and leaves the default queue showing only four records still to record')

                query.fill('asset-zero')
                expect(p.locator('[data-stock-row="' + items['zero']['id'] + '"]')).to_be_visible()
                p.locator('[data-stock-row="' + items['zero']['id'] + '"] [data-check]').click()
                expect(p.locator('#verify-saved-result')).to_be_visible()
                assert p.locator('#fw-form').count() == 0
                expect(p.locator('#verify-saved-result')).to_contain_text('0')
                assert count()['checked'] == 1
                screenshot('already_recorded', p.locator('#verify-saved-result'))
                p.locator('#verify-result-back').click()
                p.locator('#stock-clear-search').click()
                assert p.locator('#stock-rows [data-stock-row]').count() == 4
                ok('Searching from the pending queue finds a saved result, shows a read-only summary, and clearing search restores the pending queue')

                query.fill('serial-unknown')
                p.locator('[data-count-tab=checked]').click()
                assert not p.locator('#stock-rows [data-stock-row]').count()
                query.fill('serial-zero')
                assert p.locator('#stock-rows [data-stock-row]').count() == 1
                p.locator('#stock-clear-search').click()
                p.locator('[data-count-tab=remaining]').click()
                ok('Choosing Recorded explicitly narrows later searches and never silently returns unrecorded items')

                p.locator('#count-scan').click()
                p.locator('#verify-code-form [name=code]').fill(items['zero']['id'])
                before_lookup = len([x for x in exchanges if x['path'] == '/api/inventory/action'])
                p.locator('#verify-code-open').click()
                expect(p.locator('#verify-saved-result')).to_be_visible()
                assert count()['checked'] == 1 and count()['checks'][items['zero']['id']]['version'] == 1
                assert len([x for x in exchanges if x['path'] == '/api/inventory/action']) == before_lookup
                p.locator('#verify-correct-result').click()
                expect(p.locator('#fw-form')).to_be_visible()
                assert p.locator('#fw-form [name=counted_quantity]').input_value() == '0'
                assert count()['checks'][items['zero']['id']]['version'] == 1
                p.locator('#fw-discard').click()
                expect(p.locator('#fw-form')).not_to_be_visible()
                ok('Repeated QR lookup reassures with the saved result; only explicit correction opens a fresh versioned form and lookup never writes')

                query.fill('serial-unknown')
                p.locator('[data-stock-row="' + items['unknown']['id'] + '"] [data-check]').click()
                expect(p.locator('#fw-form')).to_contain_text('Not recorded')
                assert p.locator('#fw-form [name=counted_quantity]').input_value() == ''
                p.locator('#fw-form [name=note]').fill('Fictional paused inspection notes')
                p.locator('#fw-keep').click()
                expect(p.locator('#fw-form')).not_to_be_visible()
                assert count()['checked'] == 1
                retained = p.evaluate('Object.values(state.fieldworkDrafts).find(d=>d.kind==="Stock verification check")')
                assert retained['values']['note'] == 'Fictional paused inspection notes'
                report['reload_workspace'] = {'before': p.evaluate('({window_id:browserWorkspace.id(),state_key:browserWorkspace.stateKey(),draft_ids:Object.keys(state.fieldworkDrafts||{})})')}
                p.reload()
                expect(p.locator('#stock-heading')).to_have_text('Fictional UI102 stock verification')
                report['reload_workspace']['after'] = p.evaluate('({window_id:browserWorkspace.id(),state_key:browserWorkspace.stateKey(),draft_ids:Object.keys(state.fieldworkDrafts||{})})')
                assert report['reload_workspace']['before'] == report['reload_workspace']['after'], report['reload_workspace']
                navigate('#inventory/' + book['id'], '#fw-drafts')
                p.locator('#fw-drafts').click()
                p.locator('[data-fw-resume="' + retained['id'] + '"]').click()
                expect(p.locator('#fw-form [name=note]')).to_have_value('Fictional paused inspection notes')
                assert p.locator('#fw-form [name=counted_quantity]').input_value() == ''
                lose_next['action'] = 'check_item'
                p.locator('#fw-save').click()
                expect(p.locator('#fw-local-state')).to_contain_text('uncertain')
                assert count()['checked'] == 2
                first = next(x for x in reversed(exchanges) if x['request'].get('action') == 'check_item')['request']
                p.locator('#fw-save').click()
                expect(p.locator('#fw-form')).not_to_be_visible()
                assert count()['checked'] == 2 and count()['checks'][items['unknown']['id']]['counted_quantity'] is None
                second = next(x for x in reversed(exchanges) if x['request'].get('action') == 'check_item')['request']
                assert first == second and count()['checks'][items['unknown']['id']]['version'] == 1
                ok('Keep draft and close pauses an unsaved unknown-quantity form; real IndexedDB restores it after reload, and only Save submits the resumed result')
                ok('A lost response retains the submitted draft and an unchanged retry uses the identical operation and payload without duplicate results')

                navigate('#inventory/count/' + sid, '#stock-heading')
                zero_values = {key: value for key, value in items['zero'].items() if key in {'name','type','sub_type','model','serial','asset','paired_with','paired_serial','date_onboard','date_offloaded','notes','quantity','unit','location','department_id','extra','is_container','container_id'}}
                items['zero'] = api_action('inventory', 'save_item', {'list_id': book['id'], 'id': items['zero']['id'], 'version': items['zero']['version'], 'values': {**zero_values, 'notes': 'Unique sapphire inspection note; fictional newer revision'}, 'reason': 'Test required recheck'})
                p.locator('#fw-refresh').click()
                expect(p.locator('#stock-status')).to_contain_text('1 / 5')
                query.fill('serial-zero')
                expect(p.locator('[data-stock-row="' + items['zero']['id'] + '"]')).to_contain_text('Recheck needed')
                p.locator('[data-stock-row="' + items['zero']['id'] + '"] [data-check]').click()
                expect(p.locator('#verify-saved-result')).to_contain_text('Recheck needed')
                assert count()['checked'] == 1
                p.locator('#verify-correct-result').click()
                expect(p.locator('#fw-form [name=counted_quantity]')).to_have_value('0')
                p.locator('#fw-save').click()
                expect(p.locator('#fw-form')).not_to_be_visible()
                assert count()['checked'] == 2 and count()['checks'][items['zero']['id']]['version'] == 2
                p.locator('#stock-clear-search').click()
                ok('An edited previously Found item returns to the pending queue as Recheck needed, preserves the previous result, and needs a fresh explicit correction')
                p.locator('[data-stock-row="' + items['stale']['id'] + '"] [data-check]').click()
                p.locator('#fw-form [name=note]').fill('Fictional retained old-version notes')
                p.locator('#fw-keep').click()
                expect(p.locator('#fw-form')).not_to_be_visible()
                stale_draft = p.evaluate('Object.values(state.fieldworkDrafts).find(d=>d.kind==="Stock verification check")')
                values = {key: value for key, value in items['stale'].items() if key in {'name','type','sub_type','model','serial','asset','paired_with','paired_serial','date_onboard','date_offloaded','notes','quantity','unit','location','department_id','extra','is_container','container_id'}}
                api_action('inventory', 'save_item', {'list_id': book['id'], 'id': items['stale']['id'], 'version': items['stale']['version'], 'values': {**values, 'notes': 'A newer fictional item edit'}, 'reason': 'Test stale draft conflict'})
                p.evaluate('(id)=>AJFieldwork.resume(state.fieldworkDrafts[id])', stale_draft['id'])
                expect(p.locator('#fw-form [name=note]')).to_have_value('Fictional retained old-version notes')
                p.locator('#fw-save').click()
                expect(p.locator('#fw-error')).to_contain_text('changed')
                assert items['stale']['id'] not in count()['checks'] and count()['checked'] == 2
                assert p.evaluate('(id)=>!!state.fieldworkDrafts[id]', stale_draft['id'])
                p.locator('#fw-discard').click()
                expect(p.locator('#fw-form')).not_to_be_visible()
                ok('A retained form with an old item version is refused by the actual API, keeps its notes and cannot overwrite the newer inventory record')

                assert p.evaluate('({token:state.auth.token,user:state.auth.person.user_id,hub:state.hub_id})') == auth
                assert not report['errors'], report['errors']
                ok('Verification preserves the current named account, company scope and authenticated session without JavaScript errors')
                task_checks(p, c, store, auth, actor, book, items, api_action, navigate, screenshot, exchanges, ok, report)
                assert all(hashlib.sha256((source / name).read_bytes()).hexdigest() == digest for name, digest in report['source_hashes'].items()), 'Source changed during acceptance; run against one frozen version.'
                assert all(digest == report['source_hashes'][name] for name, digest in report['served_asset_hashes'].items())
                assert not report['errors'], report['errors']
            except Exception:
                p.screenshot(path=str(OUT / 'failure.png'), full_page=True)
                print(json.dumps({'errors': report['errors'], 'recent_api': [{'path': x['path'], 'status': x['status'], 'action': x['request'].get('action'), 'error': (x['response'] or {}).get('error') if isinstance(x['response'], dict) else None} for x in exchanges[-5:]]}))
                raise
            finally:
                report['summary'] = {'checks_passed': len(report['checks']), 'unexpected_errors': len(report['errors']), 'widths': report['widths']}
                (OUT / 'UI102_INVENTORY_BROWSER_REVIEW.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


def shipping_checks(p, store, actor, navigate, screenshot, exchanges, ok, report):
    value = os.environ.get('WAVELINK_IMPORT_SHIPPING_EXAMPLE', '')
    path = Path(value) if value else None
    if path is None or not path.is_file():
        raise SystemExit('Set WAVELINK_IMPORT_SHIPPING_EXAMPLE to the supplied shipping workbook; source files are not bundled.')
    report['shipping_example'] = {'source_filename': path.name, 'source_bytes': path.stat().st_size, 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'destination': 'Disposable fictional C01 company only', 'sheets': {}}
    expected = {'Vehicle MR 07': (56, 63, 1), 'Pallet 1': (58, 179, 7), 'Pallet 2': (4, 4, 0), 'Pallet 3,4': (102, 219, 3)}
    cover = 'Commercial Invoice and PL '

    def builder():
        navigate('#builders', '#sb-document')
        p.locator('#sb-document').click()
        p.locator('#sb-file').set_input_files(str(path))
        expect(p.locator('#di-sheet')).to_be_visible(timeout=90000)

    def latest(suffix):
        return next(x for x in reversed(exchanges) if x['path'].endswith(suffix))

    def rows():
        return list(csv.DictReader(io.StringIO(p.locator('#di-inventory_rows').input_value()), delimiter='\t'))

    def review():
        p.locator('#sb-review').click()
        expect(p.locator('#di-confirm')).to_be_enabled()
        assert latest('/document/review')['status'] == 200
        p.locator('#di-confirm').check()
        expect(p.locator('#sb-import-save')).to_be_enabled()

    builder()
    scan = latest('/document/scan')['response']
    sheets = {s['name']: s for s in scan['sheets']}
    assert set(sheets) == {cover, *expected}
    assert sheets[cover]['role'] == 'summary' and not sheets[cover]['recommended']
    assert p.locator('#di-sheet').input_value() == 'Pallet 3,4'
    assert len(rows()) == 102
    ok('The actual five-sheet shipping workbook recommends a detailed stock worksheet and identifies the invoice/packing cover as a separate summary')
    screenshot('shipping_worksheets', p.locator('#di-sheet-role'))
    p.locator('#di-sheet').select_option(cover)
    assert len(rows()) == 18
    expect(p.locator('#di-sheet-role')).to_contain_text('excluded')
    p.locator('#di-sheet').select_option('Vehicle MR 07')
    expect(p.locator('#di-mapping-quality')).to_contain_text('Excel row 6')
    screenshot('shipping_quantity_review', p.locator('#di-mapping-quality'))
    review()
    p.locator('[data-di-column="6"]').select_option('4')
    assert p.locator('#sb-import-save').is_disabled() and not p.locator('#di-confirm').is_checked()
    p.locator('#sb-review').click()
    expect(p.locator('#sb-result')).to_contain_text('Apply')
    p.locator('#di-map').click()
    p.locator('[data-di-column="6"]').select_option('3')
    p.locator('#di-map').click()
    ok('Changing the shipping quantity mapping invalidates confirmation and requires Apply and a new server review')

    total = 0
    for index, (sheet, (n, quantity_sum, unknown)) in enumerate(expected.items()):
        if index:
            builder()
            p.locator('#di-sheet').select_option(sheet)
        data = rows()
        assert len(data) == n
        assert p.locator('[data-di-column="6"]').input_value() == '3'
        assert p.locator('[data-di-column="1"]').input_value() == '-1'
        assert sum(float(r['quantity']) for r in data if r['quantity']) == quantity_sum
        assert sum(not r['quantity'] for r in data) == unknown
        assert all(not r['asset'] and not r['is_container'] and not r['container_ref'] for r in data)
        assert all('Source selected worksheet: ' + sheet in r['notes'] and 'Source selected Excel row:' in r['notes'] for r in data)
        assert all('source qty counted:' in ' '.join(r['notes'].split()).lower() for r in data)
        if sheet == 'Vehicle MR 07':
            row = next(r for r in data if 'Source selected Excel row: 6\n' in r['notes'])
            assert not row['quantity'] and 'source qty shall: x' in ' '.join(row['notes'].split()).lower()
        if sheet == 'Pallet 3,4':
            row82 = next(r for r in data if 'Source selected Excel row: 82\n' in r['notes'])
            row83 = next(r for r in data if 'Source selected Excel row: 83\n' in r['notes'])
            assert 'source qty counted: 14+9' in ' '.join(row82['notes'].split()).lower()
            assert 'source qty counted: 4+2' in ' '.join(row83['notes'].split()).lower()
        review()
        p.locator('#sb-import-save').click()
        expect(p.locator('#sb-success')).to_be_visible()
        saved = latest('/document/action')['response']
        inventory = store.inventory.get(saved['id'], actor)
        assert len(inventory['items']) == n and not inventory['counts']
        assert sum(x['quantity'] is None for x in inventory['items']) == unknown
        assert sum(x['quantity'] or 0 for x in inventory['items']) == quantity_sum
        assert all(not x['is_container'] and not x['container_id'] and not x['asset'] for x in inventory['items'])
        assert all('Source selected worksheet: ' + sheet in x['notes'] for x in inventory['items'])
        total += n
        report['shipping_example']['sheets'][sheet] = {'records': n, 'expected_quantity_sum': quantity_sum, 'unknown_quantities': unknown, 'history_copied': False, 'containers_inferred': False}
        ok('Shipping worksheet ' + sheet + ' persists ' + str(n) + ' separate records with expected quantities, literal prior-count notes and no invented containers or verification')
        p.locator('#sb-done').click()
    assert total == 220
    ok('All four detailed shipping sheets preserve exactly 220 records through separate explicit imports; the 18-row commercial summary is never appended')


def task_checks(p, c, store, auth, admin, book, items, action, navigate, screenshot, exchanges, ok, report):
    accounts = c.app.state.core.state.accounts
    worker = accounts.create('fictional.ui102.worker', 'Fictional UI102 named checker', PASS, 'technician', admin)
    other = accounts.create('fictional.ui102.other', 'Fictional UI102 other checker', PASS, 'technician', admin)
    administrative_login = c.post('/api/login', json={'login_id': 'admin', 'password': PASS, 'device_id': 'fictional-ui102-administrative-test'})
    assert administrative_login.status_code == 200, administrative_login.text
    administrative = {'token': administrative_login.json()['token'], 'hub': auth['hub']}
    task = action('tasks', 'create', {'title': 'Fictional UI102 assigned stock check', 'instructions': 'Test each fictional scoped record; no equipment release.', 'list_id': book['id'], 'item_ids': [items[key]['id'] for key in ('zero', 'unknown', 'known')], 'assignee_ids': [worker['id']]}, auth_override=administrative)
    p.locator('#menu-button').click()
    p.locator('[data-signout]').click()
    expect(p.locator('#login-form')).to_be_visible()
    p.locator('[name=login_id]').fill('fictional.ui102.worker')
    p.locator('[name=password]').fill(PASS)
    p.locator('#login-form button[type=submit]').click()
    expect(p.locator('#workspace-nav')).to_be_visible()
    assert p.evaluate('state.auth.person.user_id') == worker['id']
    worker_actor = store.session(p.evaluate('state.auth.token'))
    current = lambda: store.tasks.get(task['id'], worker_actor)
    navigate('#tasks/' + task['id'], '[name=task-item-query]')
    assert current()['verification']['checked'] == 0
    query = p.locator('[name=task-item-query]')
    probes = [('duplicate sen', {'zero', 'unknown'}), ('serial-zero', {'zero'}), ('asset-unknown', {'unknown'}), ('model-azure', {'zero'}), ('training workshop', {'known'}), ('sapphire inspection', {'zero'}), ('amber transport case', {'zero', 'unknown'}), (items['unknown']['id'][8:24], {'unknown'})]
    for text, keys in probes:
        query.fill(text)
        actual = set(p.locator('#task-stock-results [data-stock-item]').evaluate_all('nodes=>nodes.map(n=>n.dataset.stockItem)'))
        assert actual == {items[key]['id'] for key in keys}, (text, actual, keys)
    query.fill('fictional-no-match-b42a')
    expect(p.locator('#task-item-count')).to_contain_text('0 of 3')
    assert current()['verification']['checked'] == 0
    p.locator('#task-item-reset').click()
    assert p.locator('[name=task-tab]').input_value() == 'remaining'
    ok('A named task assignee uses the same full partial search and empty-result behavior within only the private three-record scope')
    screenshot('assigned_task_queue', p.locator('.tw47-heading h1'))
    screenshot('assigned_task_results', p.locator('#task-item-count'))

    def open_item(key):
        p.locator('#task-stock-results [data-task-check="' + items[key]['id'] + '"]:visible').first.click()
        expect(p.locator('#fw-form')).to_be_visible()

    open_item('zero')
    p.locator('#fw-form [name=counted_quantity]').fill('0')
    p.locator('#fw-save').click()
    expect(p.locator('#fw-form')).not_to_be_visible()
    assert current()['verification']['checked'] == 1
    expect(p.locator('#task-item-count')).to_contain_text('2 of 3')
    query.fill('asset-zero')
    p.locator('#task-stock-results [data-task-check="' + items['zero']['id'] + '"]:visible').first.click()
    expect(p.locator('#verify-saved-result')).to_be_visible()
    assert p.locator('#fw-form').count() == 0 and current()['verification']['checked'] == 1
    p.locator('#verify-result-back').click()
    p.locator('#task-item-reset').click()
    expect(p.locator('#task-item-count')).to_contain_text('2 of 3')
    ok('The private task starts pending, preserves a zero result and finds its already checked item through a read-only summary without creating another result')

    p.locator('#task-scan').click()
    p.locator('#verify-code-form [name=code]').fill(items['zero']['id'])
    mutations = len([x for x in exchanges if x['path'] == '/api/tasks/action' and x['request'].get('action') == 'check'])
    p.locator('#verify-code-open').click()
    expect(p.locator('#verify-saved-result')).to_be_visible()
    assert current()['verification']['checked'] == 1
    assert len([x for x in exchanges if x['path'] == '/api/tasks/action' and x['request'].get('action') == 'check']) == mutations
    p.locator('#verify-correct-result').click()
    expect(p.locator('#fw-form [name=counted_quantity]')).to_have_value('0')
    assert current()['verification']['checked'] == 1
    p.locator('#fw-discard').click()
    expect(p.locator('#fw-form')).not_to_be_visible()
    ok('The task QR uses the same duplicate-result reassurance and a deliberate fresh-version correction without writing during lookup')

    open_item('unknown')
    p.locator('#fw-form [name=note]').fill('Fictional retained task note')
    p.locator('#fw-keep').click()
    expect(p.locator('#fw-form')).not_to_be_visible()
    draft = p.evaluate('Object.values(state.fieldworkDrafts).find(d=>d.kind==="Task item verification")')
    assert current()['verification']['checked'] == 1
    report['task_reload_workspace'] = {'before': p.evaluate('({window_id:browserWorkspace.id(),state_key:browserWorkspace.stateKey(),draft_ids:Object.keys(state.fieldworkDrafts||{})})')}
    p.reload()
    expect(p.locator('[name=task-item-query]')).to_be_visible()
    report['task_reload_workspace']['after'] = p.evaluate('({window_id:browserWorkspace.id(),state_key:browserWorkspace.stateKey(),draft_ids:Object.keys(state.fieldworkDrafts||{})})')
    assert report['task_reload_workspace']['before'] == report['task_reload_workspace']['after'], report['task_reload_workspace']
    p.locator('#op-drafts').click()
    p.locator('[data-task-resume="' + draft['id'] + '"]').click()
    expect(p.locator('#fw-form [name=note]')).to_have_value('Fictional retained task note')
    assert p.locator('#fw-form [name=counted_quantity]').input_value() == ''
    p.locator('#fw-save').click()
    expect(p.locator('#fw-form')).not_to_be_visible()
    assert current()['verification']['checked'] == 2
    ok('Private task work pauses in a scoped local draft, restores after reload and submits unknown quantity only through the explicit Save action')

    open_item('known')
    p.locator('#fw-form [name=counted_quantity]').fill('2')
    p.locator('#fw-form [name=note]').fill('Fictional pending assignment conflict')
    changed = action('tasks', 'reassign', {'id': task['id'], 'version': current()['version'], 'assignee_ids': [other['id']], 'due_at': '', 'reason': 'Fictional reassignment to test stale access'}, auth_override=administrative)
    p.locator('#fw-save').click()
    expect(p.locator('#fw-error')).to_contain_text('not available')
    assert store.tasks.get(task['id'], admin)['verification']['checked'] == 2
    retained = p.evaluate('Object.values(state.fieldworkDrafts).find(d=>d.kind==="Task item verification")')
    assert retained['values']['note'] == 'Fictional pending assignment conflict'
    p.locator('#fw-discard').click()
    expect(p.locator('#fw-form')).not_to_be_visible()
    worker_headers = {'Authorization': 'Bearer ' + p.evaluate('state.auth.token'), 'x-aj-hub-id': auth['hub']}
    assert c.get('/api/tasks/' + task['id'], headers=worker_headers).status_code == 404
    assert c.post('/api/verification/lookup', headers=worker_headers, json={'kind': 'task', 'context_id': task['id'], 'value': items['known']['id']}).status_code == 404
    ok('Reassigning private work while a form is open removes access at save and QR lookup; the old form cannot write and keeps the assignee\'s notes')

    readonly = action('tasks', 'create', {'title': 'Fictional UI102 reviewed stock check', 'instructions': 'Fictional read-only report checks.', 'list_id': book['id'], 'item_ids': [items['known']['id']], 'assignee_ids': [worker['id']]}, auth_override=administrative)
    row = readonly['verification']['rows'][0]
    readonly = action('tasks', 'check', {'id': readonly['id'], 'item_id': row['item']['id'], 'item_version': row['item']['version'], 'check_version': 0, 'result': 'found', 'counted_quantity': '2', 'note': 'Fictional report evidence', 'reason': ''}, auth_override=administrative)
    readonly = action('tasks', 'submit', {'id': readonly['id'], 'version': readonly['version'], 'note': 'Fictional submission'}, auth_override=administrative)
    navigate('#tasks/' + readonly['id'], '[name=task-item-query]')
    expect(p.locator('.tw47-heading h1')).to_have_text('Fictional UI102 reviewed stock check')
    p.locator('[name=task-tab]').select_option('all')
    assert not p.locator('#task-scan').count() and not p.locator('#task-submit').count()
    assert store.tasks.get(readonly['id'], worker_actor)['status'] == 'submitted'
    screenshot('submitted_task_readonly', p.locator('.tw47-heading h1'))
    p.locator('#task-stock-results [data-task-check]:visible').first.click()
    expect(p.locator('#verify-saved-result')).to_be_visible()
    assert not p.locator('#verify-correct-result').count() and not p.locator('#fw-form').count()
    p.locator('#verify-result-back').click()
    readonly = action('tasks', 'review', {'id': readonly['id'], 'version': readonly['version'], 'decision': 'complete', 'reason': 'Fictional report review', 'accept_discrepancies': False}, auth_override=administrative)
    p.locator('#op-refresh').click()
    expect(p.locator('.tw47-status')).to_contain_text('Completed')
    assert store.tasks.get(readonly['id'], worker_actor)['verification']['checked'] == 1
    assert not p.locator('#task-scan').count() and not p.locator('#task-submit').count()
    p.locator('#task-stock-results [data-task-check]:visible').first.click()
    expect(p.locator('#verify-saved-result')).to_be_visible()
    assert not p.locator('#verify-correct-result').count() and not p.locator('#fw-form').count()
    p.locator('#verify-result-back').click()
    ok('Submitted and completed task reports remain readable to the assignee and expose no scanning or submission actions')


if __name__ == '__main__':
    main()
