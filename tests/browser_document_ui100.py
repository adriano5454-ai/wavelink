"""Reviewed imports against actual C01/core APIs in a disposable fictional company.

The supplied example stays outside the repository. Set WAVELINK_IMPORT_EXAMPLE
to that PDF to run its acceptance checks. Browser storage is genuine IndexedDB;
service-worker registration and WebSockets are suppressed in this harness.
"""
import copy
import json
import os
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
from test_company_c01 import PASS, activate, client, instance
from tests.test_document_import_ui95 import workbook

OUT = Path(os.environ.get('WAVELINK_UI100_EVIDENCE_DIR', '/tmp/wavelink-ui100/evidence/import'))
EXAMPLE_PATH = os.environ.get('WAVELINK_IMPORT_EXAMPLE', '')
EXAMPLE = Path(EXAMPLE_PATH) if EXAMPLE_PATH else None


def main():
    if EXAMPLE is None or not EXAMPLE.is_file():
        raise SystemExit('Set WAVELINK_IMPORT_EXAMPLE to the supplied checklist PDF; it is not bundled in this test.')
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'checks': [], 'errors': [], 'widths': [1440, 390, 320], 'method': 'Chromium with real IndexedDB and actual fictional C01 HostedBoundary/CompanyAccess/core API responses. WebSockets and service-worker registration suppressed.'}

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui100-import-') as td:
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
                if u.path.startswith('/api/builders/document/'):
                    exchanges.append({'path': u.path, 'status': response.status_code, 'request': json.loads(req.post_data or '{}'), 'response': response.json()})
                r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

            p.route(origin + '/**', route)

            def latest(suffix):
                return next(row for row in reversed(exchanges) if row['path'].endswith('/' + suffix))

            def counts():
                with store.connection() as con:
                    return {table: con.execute('SELECT count(*) FROM ' + table).fetchone()[0] for table in ['checklist_library_drafts', 'records', 'inventory_items', 'toolbox_talks', 'operations']}

            def builder():
                p.evaluate("()=>{location.hash='#builders';render();}")
                expect(p.locator('#sb-document')).to_be_visible()
                p.locator('#sb-document').click()

            def scan_pdf():
                builder()
                p.locator('#sb-file').set_input_files(str(EXAMPLE))
                expect(p.locator('#di-structure')).to_be_visible(timeout=90000)
                expect(p.locator('#sb-review')).to_be_enabled()
                assert latest('scan')['status'] == 200, latest('scan')['response']
                return latest('scan')['response']

            def review_and_confirm():
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                assert latest('review')['status'] == 200, latest('review')['response']
                assert p.locator('#sb-import-save').is_disabled()
                p.locator('#di-confirm').check()
                expect(p.locator('#sb-import-save')).to_be_enabled()

            def invalidated(name):
                assert p.locator('#sb-import-save').is_disabled()
                assert not p.locator('#di-confirm').is_checked()
                assert p.locator('#di-confirm').is_disabled()
                ok(name + ' invalidates the checked draft and explicit confirmation')

            def open_item(si, ii):
                p.locator('.di-section').nth(si).locator('.di-check').nth(ii).locator('.di-item-details summary').click()

            def fits(name, width):
                assert p.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (name, width)
                boxes = p.locator('#di-structure input:visible, #di-structure textarea:visible, #di-structure select:visible').evaluate_all('(nodes)=>nodes.map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right,width:b.width};})')
                assert not [b for b in boxes if b['left'] < -1 or b['right'] > width + 1], (name, width, boxes)
                ok(name + ' fits ' + str(width) + 'px without page overflow or clipped controls')

            def show_top(locator):
                locator.evaluate('node=>node.scrollIntoView({block:"start"})')
                p.evaluate('()=>scrollBy(0,-80)')

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                before = counts()
                scanned = scan_pdf()
                st = scanned['draft']['structure']
                assert scanned['kind'] == 'checklist'
                assert len(st['sections']) == 3
                assert [len(s['items']) for s in st['sections']] == [22, 27, 7]
                assert len(st['tools']) == 6
                assert st['workflow']['mode'] == 'prepost'
                assert {phase for s in st['sections'] for item in s['items'] for phase in item['phases']} == {'pre', 'post'}
                assert any(item.get('group') for s in st['sections'] for item in s['items'])
                assert counts() == before
                ok('Example PDF proposes one whole checklist with 3 sections, 56 checks, 6 tools and before/after stages without writing records')
                assert p.locator('#di-kind').input_value() == 'checklist'
                assert not scanned['draft']['sheet']
                assert p.locator('#di-sheet').count() == 0
                assert len(p.locator('#di-tools').input_value().splitlines()) == 6
                assert p.locator('#di-workflow-mode').input_value() == 'prepost'
                assert p.locator('.di-section').count() == 3
                assert p.locator('.di-check').count() == 56
                assert 'Source marks never complete a check' in p.locator('#di-structure').inner_text()
                ok('Preview keeps grouped checks, required tools and editable stages together with purpose and instruction controls')

                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    show_top(p.locator('.di-structure-block h3').first)
                    fits('Structured PDF editor', width)
                    p.wait_for_function("()=>[...document.querySelectorAll('#di-tools,.di-check-heading textarea')].every(node=>node.scrollHeight<=node.clientHeight+2)")
                    ok('All 56 source checks and six wrapped tool names remain readable at ' + str(width) + 'px without inner textarea scrolling')
                    p.screenshot(path=str(OUT / ('pdf_structure_' + str(width) + '.png')))
                    show_top(p.locator('.di-section-heading').first)
                    fits('Grouped checks', width)
                    p.screenshot(path=str(OUT / ('pdf_checks_' + str(width) + '.png')))
                p.set_viewport_size({'width': 1440, 'height': 1000})

                review_and_confirm()
                if not st['introduction']:
                    p.locator('[data-di-action="add-intro"]').click()
                    p.locator('[data-di-path="introduction.0.title"]').fill('Fictional reviewer instruction')
                p.locator('[data-di-path="introduction.0.text"]').fill((st['introduction'][0]['text'] if st['introduction'] else '') + '\nFictional reviewer instruction.')
                invalidated('Instruction edit')
                p.locator('#di-description').fill('Fictional reviewer purpose for acceptance testing.')
                review_and_confirm()
                p.locator('#di-tools').fill('\n'.join(st['tools']) + '\nFictional test tool')
                invalidated('Required-tool edit')
                review_and_confirm()
                first_stage = st['sections'][0]['items'][0]['phases'][0]
                p.locator('[data-di-phases="0:0"]').select_option('post' if first_stage == 'pre' else 'pre')
                invalidated('Check stage edit')
                review_and_confirm()
                open_item(0, 0)
                field_count = len(st['sections'][0]['items'][0]['fields'])
                if not field_count:
                    p.locator('[data-di-answer-style][data-di-field-index="0:0:-1"]').select_option('yesno')
                else:
                    p.locator('[data-di-answer-style][data-di-field-index="0:0:0"]').select_option('yesno')
                invalidated('Yes / No answer format edit')
                assert p.locator('[data-di-answer-style][data-di-field-index="0:0:0"]').input_value() == 'yesno'
                p.locator('[data-di-path="sections.0.items.0.fields.0.label"]').fill('Fictional reviewer answer')
                p.locator('[data-di-path="sections.0.items.0.fields.0.required"]').check()
                review_and_confirm()
                assert latest('review')['request']['draft']['structure']['sections'][0]['items'][0]['fields'][0]['choices'] == ['Yes', 'No']
                p.locator('[data-di-answer-style][data-di-field-index="0:0:0"]').select_option('custom')
                p.locator('[data-di-reading="0:0:0"] [data-di-choices]').fill('Ready\nNeeds review\nNot applicable')
                invalidated('Custom answer choices edit')
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    show_top(p.locator('[data-di-reading="0:0:0"]'))
                    fits('Expanded answer editor', width)
                    p.screenshot(path=str(OUT / ('pdf_answers_' + str(width) + '.png')))
                p.set_viewport_size({'width': 1440, 'height': 1000})
                review_and_confirm()
                p.locator('[data-di-action="add-field"][data-di-index="0:0"]').click()
                second_field = field_count if field_count else 1
                second_path = 'sections.0.items.0.fields.' + str(second_field)
                second_index = '0:0:' + str(second_field)
                p.locator('[data-di-answer-style][data-di-field-index="' + second_index + '"]').select_option('number')
                p.locator('[data-di-path="' + second_path + '.label"]').fill('Fictional test pressure')
                p.locator('[data-di-path="' + second_path + '.unit"]').fill('bar')
                p.locator('[data-di-reading="' + second_index + '"] [data-di-bound="min"]').fill('1')
                p.locator('[data-di-reading="' + second_index + '"] [data-di-bound="max"]').fill('10')
                invalidated('Numeric reading and bounds edit')
                review_and_confirm()
                reviewed = copy.deepcopy(latest('review')['request']['draft'])
                numeric = reviewed['structure']['sections'][0]['items'][0]['fields'][second_field]
                assert numeric['type'] == 'number' and numeric['unit'] == 'bar' and numeric['min'] == 1 and numeric['max'] == 10
                ok('Numeric reading labels, units and optional bounds reach the actual API as typed fields')
                assert counts() == before
                ok('All semantic edits are checked by the actual current-company API without creating an operational record')

                # Lose the first response after the server commits. Retrying must
                # send the exact operation, not create another definition.
                p.evaluate("""()=>{window.realImportFetch=fetch;window.lostImportResponse=false;window.importSaveBodies=[];window.fetch=async(path,opt={})=>{if(path==='/api/builders/document/action'){importSaveBodies.push(JSON.parse(opt.body));const response=await realImportFetch(path,opt);if(!lostImportResponse){lostImportResponse=true;throw new TypeError('Fictional lost response');}return response;}return realImportFetch(path,opt);};}""")
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-import-save')).to_have_text('Retry unchanged request')
                assert p.locator('#di-tools').is_disabled()
                assert p.locator('[data-di-path="introduction.0.text"]').is_disabled()
                assert p.locator('#di-kind').is_disabled()
                assert p.locator('#sb-file').is_disabled()
                assert counts()['checklist_library_drafts'] == before['checklist_library_drafts'] + 1
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                assert p.evaluate('JSON.stringify(importSaveBodies[0])===JSON.stringify(importSaveBodies[1])')
                result = latest('action')['response']
                state = store.checklists.editor_state(result['id'])
                saved = state['draft']['template']
                assert state['revision'] == '0'
                assert saved['tools'] == reviewed['structure']['tools']
                assert saved['sections'] == reviewed['structure']['sections']
                assert saved['introduction'] == reviewed['structure']['introduction']
                assert saved['workflow'] == reviewed['structure']['workflow']
                assert saved['document']['purpose'] == reviewed['description']
                assert scanned['source']['sha256'] in saved['source']
                assert counts()['checklist_library_drafts'] == before['checklist_library_drafts'] + 1
                assert counts()['records'] == before['records']
                assert latest('action')['request']['draft'] == reviewed
                ok('Lost response freezes semantic controls; identical retry returns one unpublished draft with tools, instructions, fields, stages, groups and source SHA preserved')
                p.locator('#sb-open-saved').click()
                expect(p.locator('#app')).to_contain_text(result['title'])
                ok('Saved unpublished definition opens in the current-company editor')

                # The exact review proof remains bound to every structured edit.
                proof = latest('action')['request']
                changed = copy.deepcopy(proof)
                changed['draft']['structure']['tools'].append('Unreviewed tool')
                response = c.post('/api/builders/document/action', json=changed, headers={'Authorization': 'Bearer ' + p.evaluate('state.auth.token'), 'X-AJ-Hub-ID': p.evaluate('state.hub_id')})
                assert response.status_code in (409, 422), response.text
                assert counts()['checklist_library_drafts'] == before['checklist_library_drafts'] + 1
                ok('Tampered structured draft cannot reuse its earlier review proof or duplicate the definition')

                builder()
                p.locator('#sb-file').set_input_files({'name': 'fictional-inventory.xlsx', 'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'buffer': workbook()})
                expect(p.locator('#di-sheet')).to_be_visible(timeout=90000)
                expect(p.locator('#di-kind')).to_have_value('inventory')
                assert p.locator('#di-sheet option').count() == 3
                assert 'Private hidden' not in p.locator('#di-sheet').inner_text()
                assert 'Spare cable' in p.locator('#di-inventory_rows').input_value()
                p.locator('#di-sheet').select_option('Engine room')
                assert 'Pump' in p.locator('#di-inventory_rows').input_value()
                assert 'Spare cable' not in p.locator('#di-inventory_rows').input_value()
                assert p.locator('#di-header').input_value() == '1'
                ok('Workbook retains distinct visible worksheets, skips hidden sheets and maps the selected sheet after its title row')
                raw = p.locator('#di-inventory_rows').input_value().splitlines()
                cols = raw[0].split('\t')
                row = raw[1].split('\t')
                row[cols.index('quantity')] = ''
                p.locator('summary').filter(has_text='Edit mapped rows').click()
                p.locator('#di-inventory_rows').fill(raw[0] + '\n' + '\t'.join(row) + '\n')
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    show_top(p.locator('.di-mapping h3'))
                    assert p.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                    p.screenshot(path=str(OUT / ('inventory_sheet_' + str(width) + '.png')))
                    ok('Workbook sheet and mapping preview fits ' + str(width) + 'px')
                p.set_viewport_size({'width': 1440, 'height': 1000})
                review_and_confirm()
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                inventory_result = latest('action')['response']
                person = store.session(p.evaluate('state.auth.token'))
                inventory = store.inventory.get(inventory_result['id'], person)
                assert len(inventory['items']) == 1 and inventory['items'][0]['name'] == 'Pump'
                assert inventory['items'][0]['quantity'] is None
                assert not inventory['counts']
                ok('Selected worksheet creates one separate inventory with unknown blank quantity and no verification history')
                p.locator('#sb-done').click()

                for away in ['home', 'profile', 'tasks', 'logs']:
                    p.evaluate("()=>{location.hash='#toolbox';render();}")
                    expect(p.locator('.tb-workspace')).to_be_visible()
                    p.evaluate("r=>{location.hash='#'+r;render();}", away)
                    expect(p.locator('.tb-workspace')).to_have_count(0)
                    p.evaluate("()=>{location.hash='#toolbox';render();}")
                    expect(p.locator('.tb-workspace')).to_be_visible()
                    ok('Toolbox screen reopens after ' + away + ' using actual current-company API')
                assert not report['errors'], report['errors']
            except Exception:
                p.screenshot(path=str(OUT / 'failure.png'), full_page=True)
                print(json.dumps({'status': p.locator('#sb-result').inner_text() if p.locator('#sb-result').count() else '', 'latest_api': [{k: v for k, v in row.items() if k in ('path', 'status')} for row in exchanges[-6:]], 'errors': report['errors']}))
                raise
            finally:
                report['summary'] = {'checks_passed': len(report['checks']), 'unexpected_errors': len(report['errors']), 'widths': report['widths']}
                (OUT / 'UI100_IMPORT_BROWSER_REVIEW.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
