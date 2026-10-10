"""UI106 located document recognition against a real disposable fictional C01.

Screenshots contain only literal fictional fixtures. Optional authorized PDF
acceptance records hashes and aggregate counts only, never private source text.
No production requests, email, source writes, SW registration or WebSockets.
"""
import copy
import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import urlsplit
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
from test_company_c01 import PASS, activate, client, instance
from browser_import_row_selection_ui105 import selection_workbook

OUT = Path(os.environ.get('WAVELINK_UI106_EVIDENCE_DIR', str(ROOT.parent / 'evidence' / 'browser')))
TRACKED = ('app/document_import.py', 'app/document_structure.py', 'app/document_extract.py',
           'app/inventory.py', 'app/builder_hub.py', 'app/static/document_import.js',
           'app/static/document_import.css', 'app/static/setup_builders.js',
           'app/static/index.html', 'app/static/sw.js')


def docx(path, blocks):
    """Passive literal Word XML fixture, preserving paragraph/table order."""
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    paragraph = lambda text: '<w:p><w:r><w:t xml:space="preserve">' + escape(text) + '</w:t></w:r></w:p>'
    body = ''
    for block in blocks:
        if isinstance(block, str):
            body += paragraph(block)
        else:
            body += '<w:tbl>' + ''.join('<w:tr>' + ''.join('<w:tc>' + paragraph(cell) + '</w:tc>' for cell in row) + '</w:tr>' for row in block) + '</w:tbl>'
    with ZipFile(path, 'w', ZIP_DEFLATED) as book:
        book.writestr('word/document.xml', '<w:document xmlns:w="' + ns + '"><w:body>' + body + '</w:body></w:document>')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    report = dict(checks=[], errors=[], widths=[1440, 390, 320],
                  method='Real Chromium with genuine IndexedDB and disposable fictional C01 HostedBoundary/company/core APIs. Screenshots contain only literal fictional fixtures.',
                  source_hashes={name: sha(SOURCE / name) for name in TRACKED}, served_asset_hashes={},
                  harness_sha256=sha(Path(__file__)), runtime_manifest_sha256=sha(SOURCE / 'RELEASE_FILES.json'), authorized_examples=[],
                  limitations=['Service-worker registration and WebSockets are suppressed.',
                               'No production, Render, live email, physical camera, Windows display or worker-upgrade acceptance.',
                               'Serialized draft rehydration is exercised through a transparently captured live form and a real Import-as repaint; the product has no end-user builder reload/restore workflow.',
                               'Recognition is a bounded advisory from original extraction, not a guarantee that every document can be converted.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui106-recognition-') as td:
        td = Path(td)
        narrative = td / 'Fictional_UI106_Maintenance.txt'
        narrative.write_text('Maintenance checklist\nFerramentas necessárias: Chave; Luvas\nInstruções: Isolar a energia.\nKeep this form for records.\nBefore opening, isolate fictional energy.\n# Checks\nCheck guard\nSignature: Fictional historical signature\nDate: 2026-01-01\n', encoding='utf-8')
        english = td / 'Fictional_UI106_English.docx'
        docx(english, ['Fictional English checklist', 'Tools required', [['Spanner', 'Gloves']],
                      'Instructions: Isolate the energy before starting.',
                      [['Task', 'Yes', 'No', 'N/A', 'Signature'], ['Check safety guard', 'X', '', '', 'Fictional historical signer'], ['Check cable', '', 'X', '', 'Fictional historical signer']]])
        portuguese = td / 'Fictional_UI106_Portuguese.csv'
        portuguese.write_text('Task,Sim,Não,N/A\nVerificar guarda,X,,\nInspecionar cabo,,X,\n', encoding='utf-8')
        passfail = td / 'Fictional_UI106_PassFail.csv'
        passfail.write_text('Task,Pass,Fail\nCheck fictional seal,X,\nCheck fictional hose,,X\n', encoding='utf-8')
        status = td / 'Fictional_UI106_Status.csv'
        status.write_text('Task,Status\nCheck fictional fixture,Completed\n', encoding='utf-8')
        bounded = td / 'Fictional_UI106_BoundedStatus.csv'
        bounded.write_text('Task,Status\n' + '\n'.join('Check fictional bounded fixture ' + str(i) + ',Completed' for i in range(125)) + '\n', encoding='utf-8')
        beforeafter = td / 'Fictional_UI106_BeforeAfter.docx'
        docx(beforeafter, ['Maintenance checklist', [['Task', 'Before', 'After', 'Date', 'Time'], ['Check fictional seal', 'X', '', '2026-01-01', '09:00'], ['Check fictional hose', '', 'X', '2026-01-01', '09:05']]])
        datemeta = td / 'Fictional_UI106_DateTime.csv'
        datemeta.write_text('Check,Date,Time\nFictional historical check,2026-01-01,09:00\n', encoding='utf-8')
        toolbox = td / 'Fictional_UI106_Toolbox.docx'
        docx(toolbox, ['Toolbox talk', 'Instructions: Isolate fictional energy before briefing.',
                      'Tools required', [['Fictional spanner', 'Fictional gloves']],
                      'Discussion', 'Check fictional work area', 'Understanding questions',
                      'Can everyone identify the isolation point?', 'Acknowledgement declaration: I understand the fictional briefing.',
                      'Signature: Fictional historical signer'])
        longtoolbox = td / 'Fictional_UI106_LongToolbox.txt'
        longtoolbox.write_text('Toolbox talk\nInstructions: # Fictional source heading\n' + 'Fictional instruction retained verbatim. ' * 40 + '\nCheck fictional work area\nCan you identify the isolation point?\n', encoding='utf-8')
        repeatedtoolbox = td / 'Fictional_UI106_RepeatedChunks.txt'
        repeatedtoolbox.write_text('Toolbox talk\nInstructions: ' + 'Z' * 1200 + '\nCheck fictional work area\nCan you identify the isolation point?\n', encoding='utf-8')
        malicious = td / 'Fictional_UI106_LiteralLabels.txt'
        malicious.write_text('Fictional checklist\nInstructions: <img src=x onerror=window.ui106Injected=1>\nCheck fictional cable\nKeep <script>window.ui106Injected=2</script> as literal source text.\n', encoding='utf-8')
        sheets = td / 'Fictional_UI106_LocatedSheets.xlsx'
        selection_workbook(sheets, [('Fictional English checks', [(3, ['Task', 'Status']), (8, ['Check first worksheet guard', 'Completed'])]),
                                   ('Fictional Portuguese checks', [(5, ['Task', 'Status']), (17, ['Verificar segunda guarda', 'Completed'])])])
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

            def counts():
                with store.connection() as con:
                    return {table: con.execute('SELECT count(*) FROM ' + table).fetchone()[0] for table in ['checklist_library_drafts', 'records', 'maintenance_routines', 'maintenance_jobs', 'toolbox_templates', 'toolbox_talks', 'inventory_items']}

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

            def recognition(scan):
                review = scan['recognition_review']
                assert set(review) == {'version', 'total_points', 'points', 'truncated'}
                assert review['version'] == 1 and review['total_points'] >= len(review['points']) and len(review['points']) <= 50
                assert len({x['id'] for x in review['points']}) == len(review['points'])
                for point in review['points']:
                    assert set(point) == {'id', 'category', 'reason', 'excerpt', 'source', 'target'}
                    assert point['source']['label'] and len(point['reason']) <= 500 and len(point['excerpt']) <= 600
                    assert point['category'] in ('classification', 'answer_format', 'stage', 'tools', 'unmapped', 'limit')
                assert 'recognition_review' not in scan['draft']
                return review

            def current_draft():
                return p.locator('#di-edit input,#di-edit select,#di-edit textarea').evaluate_all('(nodes)=>JSON.stringify(nodes.map(n=>({id:n.id,path:n.dataset.diPath||"",value:n.value,checked:n.type==="checkbox"?n.checked:undefined})))')

            def native_keys(value):
                if isinstance(value, dict):
                    return set(value).union(*(native_keys(v) for v in value.values()))
                if isinstance(value, list):
                    return set().union(*(native_keys(v) for v in value))
                return set()

            def assert_blank_native(value):
                assert not {'answers', 'completed', 'checked', 'signature', 'attendees', 'acknowledgements', 'discussed', 'history'}.intersection(native_keys(value))
                encoded = json.dumps(value)
                assert 'Fictional historical signer' not in encoded
                assert 'Fictional historical signature' not in encoded

            def save():
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                response = copy.deepcopy(latest('action')['response'])
                assert response['saved'] is True
                return response

            def review_and_confirm():
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                assert latest('review')['status'] == 200, latest('review')['response']
                assert set(latest('review')['request']) == {'kind', 'source', 'source_token', 'draft'}
                p.locator('#di-confirm').check()
                expect(p.locator('#sb-import-save')).to_be_enabled()
                return copy.deepcopy(latest('review')['request']['draft'])

            def screenshot(name, locator):
                p.wait_for_function('()=>!document.querySelector("#toast")?.classList.contains("visible")')
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    locator.evaluate('node=>node.scrollIntoView({block:"start"})')
                    p.evaluate('()=>scrollBy(0,-80)')
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name, width)
                    bounds = p.locator('#di-recognition-review button:visible,#di-edit input:visible,#di-edit select:visible,#di-edit textarea:visible').evaluate_all('(nodes)=>nodes.map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right};})')
                    assert not [b for b in bounds if b['left'] < -1 or b['right'] > width + 1], (name, width, bounds)
                    p.screenshot(path=str(OUT / (name + '_' + str(width) + '.png')))
                    ok(name.replace('_', ' ') + ' fits ' + str(width) + 'px without horizontal page overflow or clipped editor controls')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                p.evaluate('''()=>{const native=window.AJDocumentImport;window.AJDocumentImport={...native,scan(f,h){window.ui106LiveForm=f;window.ui106LiveHooks=h;return native.scan(f,h);},lock(f){window.ui106LiveForm=f;return native.lock(f);}};}''')
                before = counts()
                scan = builder(narrative)
                points = recognition(scan)
                st = scan['draft']['structure']
                items = [i for s in st['sections'] for i in s['items']]
                assert scan['kind'] == 'maintenance'
                assert st['tools'] == ['Chave', 'Luvas']
                assert [i['text'] for i in items] == ['Check guard']
                assert any('Isolar a energia.' in b['text'] for b in st['introduction'])
                assert any('Keep this form for records.' in b['text'] for b in st['introduction'])
                assert st['workflow']['mode'] == 'single'
                assert any(x['category'] == 'classification' and 'Keep this form' in x['excerpt'] for x in points['points'])
                assert counts() == before
                expect(p.locator('#di-recognition-review')).to_be_visible()
                assert not p.locator('#di-recognition-review').evaluate('n=>n.open')
                assert p.locator('#di-recognition-review').evaluate('n=>!!(n.compareDocumentPosition(document.querySelector("#di-edit"))&Node.DOCUMENT_POSITION_FOLLOWING)')
                ok('Narrative English and accented Portuguese roles preserve instructions/tools, keep ambiguous prose out of checks, and expose advisory evidence outside the strict draft without database writes')
                screenshot('recognition_panel_closed', p.locator('#di-recognition-review'))
                p.locator('#di-recognition-review > summary').click()
                expect(p.locator('#di-recognition-review')).to_contain_text('original extraction')
                screenshot('recognition_panel_open', p.locator('#di-recognition-points'))
                original_panel = p.locator('#di-recognition-points').inner_text()
                reviewed = review_and_confirm()
                state_before_jump = current_draft()
                request_count = len(exchanges)
                point = next(x for x in points['points'] if x['target']['role'] == 'tools')
                p.locator('[data-di-recognition-jump="' + point['id'] + '"]').click()
                expect(p.locator('#di-tools')).to_be_focused()
                assert current_draft() == state_before_jump
                assert len(exchanges) == request_count
                expect(p.locator('#sb-import-save')).to_be_enabled()
                assert p.locator('#di-confirm').is_checked()
                ok('Source navigation opens/focuses an existing editor without changing draft controls, sending a request or invalidating a checked confirmation')
                p.locator('[data-di-path="sections.0.items.0.text"]').fill('Check fictional reviewer-adjusted guard')
                expect(p.locator('#sb-import-save')).to_be_disabled()
                assert not p.locator('#di-confirm').is_checked()
                assert p.locator('#di-recognition-points').inner_text() == original_panel
                expect(p.locator('#di-recognition-review')).to_contain_text('Your edits are not reclassified')
                ok('Manual check edits invalidate the actual review while retaining the original source interpretation and its explicit advisory wording')
                screenshot('structured_edit', p.locator('[data-di-path="sections.0.items.0.text"]'))
                review_and_confirm()
                original_sidecar = p.evaluate('JSON.stringify(ui106LiveForm.document.recognition_review)')
                p.evaluate('()=>{ui106LiveForm.document=JSON.parse(JSON.stringify(ui106LiveForm.document));}')
                p.locator('#di-kind').select_option('checklist')
                p.locator('#di-kind').select_option('maintenance')
                assert p.locator('[data-di-path="sections.0.items.0.text"]').input_value() == 'Check fictional reviewer-adjusted guard'
                assert p.evaluate('JSON.stringify(ui106LiveForm.document.recognition_review)') == original_sidecar
                assert p.locator('#di-recognition-points').inner_text() == original_panel
                assert counts() == before
                ok('In-memory JSON rehydration of the captured live document followed by a real Import-as repaint preserves edited draft text and original sidecar; this does not claim an end-user reload/restore feature')

                scan = builder(english)
                recognition(scan)
                st = scan['draft']['structure']
                items = [i for s in st['sections'] for i in s['items']]
                assert st['tools'] == ['Spanner', 'Gloves']
                assert [i['text'] for i in items] == ['Check safety guard', 'Check cable']
                assert all(i['fields'][0]['choices'] == ['Yes', 'No', 'N/A'] for i in items)
                p.locator('#di-kind').select_option('checklist')
                p.locator('[data-di-path="sections.0.items.0.text"]').fill('Check fictional guard after reviewer correction')
                reviewed = review_and_confirm()
                result = save()
                editor = store.checklists.editor_state(result['id'])
                template = editor['draft']['template']
                assert editor['revision'] == '0'
                assert template['sections'] == reviewed['structure']['sections']
                assert template['tools'] == reviewed['structure']['tools']
                assert template['introduction'] == reviewed['structure']['introduction']
                assert scan['source']['sha256'] in template['source']
                assert_blank_native(template)
                assert counts()['records'] == before['records']
                assert counts()['maintenance_jobs'] == before['maintenance_jobs']
                assert counts()['toolbox_talks'] == before['toolbox_talks']
                ok('A labeled Word tools table and explicit English Yes/No/N/A columns save the actual edited unpublished checklist with blank answers/signatures and original source SHA')

                for path, choices in [(portuguese, ['Sim', 'Não', 'N/A']), (passfail, ['Pass', 'Fail'])]:
                    scan = builder(path)
                    recognition(scan)
                    assert scan['suggested_kind'] == 'checklist'
                    p.locator('#di-kind').select_option('checklist')
                    all_items = [i for s in scan['draft']['structure']['sections'] for i in s['items']]
                    assert len(all_items) == 2 and all(i['fields'][0]['choices'] == choices for i in all_items)
                    reviewed = review_and_confirm()
                    assert all(i['fields'][0]['choices'] == choices for s in reviewed['structure']['sections'] for i in s['items'])
                    ok('Strong ' + '/'.join(choices) + ' labels propose answer definitions from source columns while source selected answers remain unfilled')

                scan = builder(status)
                points = recognition(scan)
                st = scan['draft']['structure']
                items = [i for s in st['sections'] for i in s['items']]
                assert len(items) == 1 and not items[0]['fields']
                answer_point = next(x for x in points['points'] if x['target']['role'] == 'answer' and x['target'].get('item_id') == items[0]['id'])
                assert answer_point['target']['item_id'] == items[0]['id']
                review_and_confirm()
                p.locator('#di-recognition-review').evaluate('n=>n.open=true')
                snapshot = current_draft()
                p.locator('[data-di-recognition-jump="' + answer_point['id'] + '"]').click()
                expect(p.locator('[data-di-answer-style]')).to_be_focused()
                assert current_draft() == snapshot and p.locator('#sb-import-save').is_enabled()
                p.locator('[data-di-action="remove-item"][data-di-index="0:0"]').click()
                p.locator('#di-recognition-review').evaluate('n=>n.open=true')
                p.locator('[data-di-recognition-jump="' + answer_point['id'] + '"]').click()
                expect(p.locator('#di-recognition-status')).to_contain_text('moved or removed')
                expect(p.locator('#di-structure .di-section input').first).to_be_focused()
                assert p.locator('#di-recognition-points').inner_text().find(answer_point['reason']) >= 0
                ok('Status without printed choices remains an unspecified answer with a stable item target; deleting the item falls back to its current section without resolving the original point')
                screenshot('removed_target_fallback', p.locator('#di-recognition-review'))

                scan = builder(bounded)
                points = recognition(scan)
                assert points['total_points'] >= 125 and len(points['points']) == 50 and points['truncated'] is True
                p.locator('#di-recognition-review').evaluate('n=>n.open=true')
                assert p.locator('#di-recognition-points > li').count() == 50
                expect(p.locator('#di-recognition-review')).to_contain_text('Showing 50 of ' + str(points['total_points']))
                assert p.locator('.di-check').count() == 125
                ok('The source panel renders at most 50 located advisory points, discloses the larger original total and retains all 125 editable proposed checks')

                scan = builder(beforeafter)
                recognition(scan)
                st = scan['draft']['structure']
                assert scan['kind'] == 'maintenance'
                assert st['workflow']['mode'] == 'prepost'
                assert all(i['phases'] == ['pre', 'post'] for s in st['sections'] for i in s['items'])
                assert '2026-01-01' not in json.dumps(st) and '09:00' not in json.dumps(st)
                p.locator('[data-di-path="sections.0.items.0.text"]').fill('Check fictional seal after maintenance review')
                reviewed = review_and_confirm()
                result = save()
                with store.connection() as con:
                    saved = json.loads(con.execute('SELECT body FROM maintenance_routines WHERE id=?', (result['id'],)).fetchone()[0])
                assert saved['published'] is None and saved['revision'] == 0
                assert saved['draft']['sections'] == reviewed['structure']['sections']
                assert saved['draft']['workflow'] == reviewed['structure']['workflow']
                assert_blank_native(saved['draft'])
                assert counts()['maintenance_jobs'] == before['maintenance_jobs']
                ok('Before/after stages save an actual edited unpublished maintenance routine while historical Date/Time values and operational work remain absent')

                scan = builder(datemeta)
                recognition(scan)
                assert scan['suggested_kind'] == 'checklist'
                expect(p.locator('#di-kind')).to_have_value('checklist')
                expect(p.locator('#di-recognition-review')).to_be_visible()
                assert not [i for s in scan['draft']['structure']['sections'] for i in s['items']]
                assert any(x['category'] == 'unmapped' for x in scan['recognition_review']['points'])
                ok('Check/Date/Time historical metadata is omitted rather than inventing a reusable checklist task or silently promoting it to a logbook')

                scan = builder(sheets)
                recognition(scan)
                for sheet, row in [('Fictional English checks', 8), ('Fictional Portuguese checks', 17)]:
                    p.locator('#di-sheet').select_option(sheet)
                    candidate = next(x for x in scan['sheets'] if x['name'] == sheet)
                    points = recognition(dict(candidate, draft=candidate['draft']))
                    assert points['points']
                    assert candidate['row_numbers'] == [3 if row == 8 else 5, row]
                    assert all(x['source'].get('sheet') in (None, sheet) for x in points['points'])
                    assert all(x['source'].get('row') in (None, 3 if row == 8 else 5, row) for x in points['points'])
                    assert any(x['source'].get('row') == row and x['source'].get('sheet') == sheet for x in points['points'])
                    p.locator('#di-recognition-review').evaluate('n=>n.open=true')
                    for point in points['points']:
                        expect(p.locator('#di-recognition-points')).to_contain_text(point['source']['label'])
                    assert p.locator('.di-check').count() == 1
                    item = next(i for s in candidate['draft']['structure']['sections'] for i in s['items'])
                    assert p.locator('.di-check-heading textarea').input_value() == item['text']
                    assert sheet in item['guidance']['source_ref'] and str(row) in item['guidance']['source_ref']
                ok('Worksheet switching shows only the selected source candidate and honest non-contiguous original worksheet row diagnostics')

                scan = builder(toolbox)
                recognition(scan)
                assert scan['kind'] == 'toolbox'
                initial_outline = p.locator('#di-outline').input_value()
                tools = scan['draft']['structure']['tools']
                blocks = [x['text'] for x in scan['draft']['structure']['introduction'] if x['text'].strip()]
                assert tools == ['Fictional spanner', 'Fictional gloves']
                assert blocks and not all(text in initial_outline for text in tools + blocks)
                p.locator('#di-declaration').fill('I understand this fictional briefing.')
                p.locator('#di-questions').fill('Can everyone identify the isolation point?')
                p.locator('#di-outline').fill(initial_outline + '\nReviewer current discussion prompt')
                review_and_confirm()
                before_copy = p.locator('#di-outline').input_value()
                p.locator('#di-toolbox-copy-notes').click()
                copied = p.locator('#di-outline').input_value()
                assert copied.startswith(before_copy)
                assert all(x in copied for x in tools + blocks)
                assert p.locator('#sb-import-save').is_disabled()
                assert not p.locator('#di-confirm').is_checked()
                p.locator('#di-toolbox-copy-notes').click()
                assert p.locator('#di-outline').input_value() == copied
                expect(p.locator('#sb-result')).to_contain_text('already included')
                ok('Explicit toolbox copy appends full source instructions/tools to the current discussion without replacing edits, truncating text or duplicating repeated clicks; actual changes invalidate review')
                screenshot('toolbox_source_add', p.locator('#di-toolbox-notes-summary'))
                delayed['path'] = '/api/builders/document/review'
                p.locator('#sb-review').click()
                p.wait_for_function('document.querySelector("#di-toolbox-copy-notes")?.disabled===true')
                deadline = time.monotonic() + 30
                while delayed['held'] is None and time.monotonic() < deadline:
                    p.wait_for_timeout(25)
                assert delayed['held'] is not None
                assert all(p.locator('[data-di-recognition-jump]').nth(i).is_disabled() for i in range(p.locator('[data-di-recognition-jump]').count()))
                assert p.locator('#di-outline').input_value() == copied
                guarded = p.evaluate('JSON.stringify({resource:ui106LiveForm.resource,draft:ui106LiveForm.document.draft,request:ui106LiveForm.request})')
                p.locator('#di-kind').evaluate('n=>{const current=n.value;n.value="checklist";n.onchange();n.value=current;}')
                assert p.evaluate('JSON.stringify({resource:ui106LiveForm.resource,draft:ui106LiveForm.document.draft,request:ui106LiveForm.request})') == guarded
                route_held, response_held = delayed['held']
                delayed['held'] = None
                route_held.fulfill(status=response_held.status_code, body=response_held.content, headers=dict(response_held.headers))
                expect(p.locator('#di-confirm')).to_be_enabled()
                p.locator('#di-confirm').check()
                reviewed = copy.deepcopy(latest('review')['request']['draft'])
                lose_next['save'] = True
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-import-save')).to_have_text('Retry unchanged request')
                assert p.locator('#di-toolbox-copy-notes').is_disabled()
                assert all(p.locator('[data-di-recognition-jump]').nth(i).is_disabled() for i in range(p.locator('[data-di-recognition-jump]').count()))
                first_save = copy.deepcopy(latest('action')['request'])
                guarded = p.evaluate('JSON.stringify({resource:ui106LiveForm.resource,draft:ui106LiveForm.document.draft,request:ui106LiveForm.request})')
                p.locator('#di-kind').evaluate('n=>{const current=n.value;n.value="checklist";n.onchange();n.value=current;}')
                assert p.evaluate('JSON.stringify({resource:ui106LiveForm.resource,draft:ui106LiveForm.document.draft,request:ui106LiveForm.request})') == guarded
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                assert latest('action')['request'] == first_save
                result = latest('action')['response']
                with store.connection() as con:
                    saved = json.loads(con.execute('SELECT body FROM toolbox_templates WHERE id=?', (result['id'],)).fetchone()[0])
                assert saved['revision'] == 0 and saved['published'] is False
                native_prompt_text = '\n'.join(prompt['text'] for prompt in saved['definition']['prompts'])
                assert all(x in native_prompt_text for x in tools + blocks)
                assert any(prompt['text'] == 'Reviewer current discussion prompt' for prompt in saved['definition']['prompts'])
                assert_blank_native(saved['definition'])
                assert counts()['toolbox_talks'] == before['toolbox_talks']
                assert counts()['toolbox_templates'] == before['toolbox_templates'] + 1
                ok('Busy and uncertain review/save freeze source navigation/copy; identical real lost-response retry saves one unpublished toolbox definition with edited prompts and blank operational answers/acknowledgements')

                scan = builder(longtoolbox)
                recognition(scan)
                outline = p.locator('#di-outline').input_value()
                assert any(len(x['text']) > 600 for x in scan['draft']['structure']['introduction'])
                p.locator('#di-toolbox-copy-notes').click()
                copied = p.locator('#di-outline').input_value()
                assert copied.startswith(outline)
                assert 'Source: # Fictional source heading' in copied
                prompts = [line for line in copied.splitlines() if line.strip() and not line.startswith('#')]
                assert all(len(x) <= 600 for x in prompts)
                normalized = ' '.join(' '.join(prompts).split())
                assert normalized.count('Fictional instruction retained verbatim.') == 40
                p.locator('#di-toolbox-copy-notes').click()
                assert p.locator('#di-outline').input_value() == copied
                p.locator('#di-source-text-details').evaluate('n=>n.open=true')
                assert 'Fictional instruction retained verbatim. ' * 24 in p.locator('#di-source-text').inner_text()
                ok('A long retained source instruction is divided into native prompts at most 600 characters without dropping repeated text; literal hash prefixes remain prompt content and repeated copy adds nothing')
                p.locator('#di-recognition-review').evaluate('n=>n.open=true')
                screenshot('long_located_point', p.locator('#di-recognition-review'))

                scan = builder(repeatedtoolbox)
                p.locator('#di-toolbox-copy-notes').click()
                copied = p.locator('#di-outline').input_value()
                assert copied.splitlines().count('Z' * 600) == 2
                p.locator('#di-toolbox-copy-notes').click()
                assert p.locator('#di-outline').input_value() == copied
                p.locator('#di-declaration').fill('I understand this fictional briefing.')
                assert not p.locator('#di-questions').input_value().strip()
                repeated_before = counts()
                p.locator('#sb-review').click()
                expect(p.locator('#sb-result')).to_contain_text('Add one to 20 understanding questions')
                assert p.locator('#sb-import-save').is_disabled() and counts() == repeated_before
                ok('Source instructions containing a question do not silently supply a toolbox understanding question; native review blocks missing questions without saving anything')
                p.locator('#di-questions').fill('Can everyone identify the fictional isolation point?')
                reviewed = review_and_confirm()
                prompts = [line for line in reviewed['outline'].splitlines() if line.strip() and not line.startswith('#')]
                assert prompts.count('Z' * 600) == 2
                ok('Two identical full-length source chunks are retained as two native discussion prompts; repeating the add action uses occurrence counts and does not discard or duplicate them')

                scan = builder(toolbox)
                existing = '\n'.join('Fictional existing prompt ' + str(i) for i in range(100))
                p.locator('#di-outline').fill(existing)
                p.locator('#di-toolbox-copy-notes').click()
                assert p.locator('#di-outline').input_value() == existing
                expect(p.locator('#sb-result')).to_contain_text('100')
                ok('The explicit source-add action respects the native 100-prompt maximum atomically and keeps all current discussion text unchanged')
                p.evaluate('()=>{window.ui106DepartedCopy=document.querySelector("#di-toolbox-copy-notes");window.ui106DepartedJump=document.querySelector("[data-di-recognition-jump]");}')

                scan = builder(malicious)
                recognition(scan)
                snapshot = current_draft()
                request_count = len(exchanges)
                p.evaluate('()=>{ui106DepartedCopy.click();ui106DepartedJump?.click();}')
                assert current_draft() == snapshot and len(exchanges) == request_count
                ok('Detached copy/navigation controls from a departed builder cannot mutate the next draft or send a stale request')
                p.locator('#di-recognition-review').evaluate('n=>n.open=true')
                p.locator('#di-source-text-details').evaluate('n=>n.open=true')
                assert p.evaluate('window.ui106Injected===undefined')
                assert not p.locator('#di-recognition-review img,#di-recognition-review script,#di-source-text img,#di-source-text script').count()
                expect(p.locator('#di-source-text')).to_contain_text('<img src=x onerror=window.ui106Injected=1>')
                ok('HTML-like original excerpts and source labels are literal escaped text with no executable images or scripts')
                screenshot('literal_source_excerpt', p.locator('#di-recognition-points'))

                # Private source acceptance stays outside the browser DOM and
                # screenshot path: only its hash, aggregate counts and flags are
                # written to the public evidence report.
                example_path = os.environ.get('WAVELINK_DOCUMENT_EXAMPLE', '')
                if example_path:
                    import base64
                    example = Path(example_path)
                    raw = example.read_bytes()
                    expected_sha = '14a19fa9e545f5880bf42d327c1a01ee4607bbabf68ac458340e40800140a9ad'
                    assert hashlib.sha256(raw).hexdigest() == expected_sha
                    headers = {'Authorization': 'Bearer ' + p.evaluate('state.auth.token'), 'x-aj-hub-id': p.evaluate('state.hub_id')}
                    private_before = counts()
                    response = c.post('/api/builders/document/scan', json={'kind': 'checklist', 'language': 'eng', 'file': {'name': example.name, 'data': base64.b64encode(raw).decode()}}, headers=headers)
                    assert response.status_code == 200
                    source = response.json()
                    st = source['draft']['structure']
                    items = [i for s in st['sections'] for i in s['items']]
                    assert len(items) == 56 and len(st['tools']) == 6
                    fields = sum(len(i['fields']) for i in items)
                    assert fields == 7
                    assert sum('pre' in i['phases'] for i in items) == 55 and sum('post' in i['phases'] for i in items) == 56
                    assert example.read_bytes() == raw
                    assert counts() == private_before
                    report['authorized_examples'].append(dict(source_sha256=expected_sha, checks=56, tools=6, reading_fields=7, pre_checks=55, post_checks=56, source_unchanged=True, source_rendered=False, database_unchanged=True, saved=False))
                    ok('Authorized original PDF retains aggregate 56 checks, 6 tools, 7 reading fields and pre55/post56 without rendering, saving or exposing private excerpts')
                assert not report['errors'], report['errors']
                for name, hash in report['served_asset_hashes'].items():
                    assert report['source_hashes'][name] == hash, name
                for name, hash in report['source_hashes'].items():
                    assert sha(SOURCE / name) == hash, name
                assert sha(SOURCE / 'RELEASE_FILES.json') == report['runtime_manifest_sha256']
                ok('All served tracked assets match the frozen source and Chromium reports no unexpected JavaScript errors')
                report['summary'] = dict(checks_passed=len(report['checks']), unexpected_errors=len(report['errors']), widths=report['widths'])
                (OUT / 'UI106_DOCUMENT_RECOGNITION_BROWSER_REVIEW.json').write_text(json.dumps(report, indent=2) + '\n')
                print(json.dumps(report, indent=2))
            except Exception:
                # The active source here is always fictional; private acceptance
                # is performed through aggregate-only API calls below.
                p.screenshot(path=str(OUT / 'failure.png'))
                (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')
                raise
            finally:
                browser.close()


if __name__ == '__main__':
    main()
