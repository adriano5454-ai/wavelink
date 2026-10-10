"""UI108 table/source-row acceptance in a disposable fictional C01.

Real Chromium, IndexedDB, scan/review/save APIs and native SQLite persistence.
All Office fixtures are created here and contain only literal fictional data.
The test does not contact production, send mail or modify original documents.
"""
import copy
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
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
from browser_document_recognition_ui106 import docx

OUT = Path(os.environ.get('WAVELINK_UI108_EVIDENCE_DIR', str(ROOT.parent / 'evidence' / 'browser')))
TRACKED = ('app/document_import.py', 'app/document_structure.py', 'app/document_extract.py',
           'app/inventory.py', 'app/inventory_boxes.py', 'app/builder_hub.py',
           'app/static/document_import.js', 'app/static/document_import.css',
           'app/static/setup_builders.js', 'app/static/index.html', 'app/static/sw.js',
           'app/static/help.css', 'app/static/help_topics/documentimport.html',
           'app/static/help_topics/inventorybuilder.html', 'app/static/help_topics/toolbox.html',
           'app/static/help_topics/toolboxbuilder.html',
           'docs/user/topics/documentimport.html', 'docs/user/topics/inventorybuilder.html',
           'docs/user/topics/toolbox.html', 'docs/user/topics/toolboxbuilder.html')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    report = dict(checks=[], errors=[], widths=[1440, 390, 320], screenshots=[],
                  method='Real Chromium, genuine IndexedDB, disposable fictional C01 HostedBoundary/CompanyAccess/core APIs and native SQLite. Newly generated literal fictional DOCX/XLSX fixtures only.',
                  source_hashes={name: sha(SOURCE / name) for name in TRACKED}, served_asset_hashes={},
                  harness_sha256=sha(Path(__file__)), runtime_manifest_sha256=sha(SOURCE / 'RELEASE_FILES.json'),
                  limitations=['Service-worker registration and WebSockets are suppressed.',
                               'No production, Render, live mail, physical camera, Windows display or worker-upgrade acceptance.',
                               'A captured live form is used only to prove read-only receipt retention and guarded event behavior, not an end-user reload workflow.',
                               'Inventory source-row labels are advisory. Every mapped row remains until an explicit user choice; heterogeneous table blocks are not normalized automatically.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui108-tables-') as td:
        td = Path(td)
        labelvalue = td / 'Fictional_UI108_LabelValue.docx'
        docx(labelvalue, ['Lifting toolbox talk', [
            ['Description', 'Review the fictional deck lift.'],
            ['Instructions', 'Isolate fictional energy before work.'],
            ['Tools required', 'Fictional radio; Fictional gloves'],
            ['Supervisor instructions', 'Discuss the fictional exclusion zone.'],
            ['Declaration', 'I understand the fictional lift plan.']],
            [['Task', 'Yes', 'No'], ['Is the fictional area isolated?', 'HISTORICAL-ANSWER', '']]])
        changed = td / 'Fictional_UI108_ChangedHeaders.xlsx'
        selection_workbook(changed, [('Fictional maintenance', [
            (2, ['Pump maintenance checklist']), (5, ['Task', 'Yes', 'No']),
            (9, ['Check fictional guard', 'HISTORICAL-ANSWER', '']),
            (14, ['Task', 'Before', 'After', 'Pressure (bar)']),
            (19, ['Measure fictional discharge', 'HISTORICAL-PRE', 'HISTORICAL-POST', 'HISTORICAL-PRESSURE'])])])
        sequential = td / 'Fictional_UI108_SequentialStages.xlsx'
        selection_workbook(sequential, [('Fictional staged maintenance', [
            (2, ['Maintenance checklist']), (5, ['Task', 'Yes', 'No']),
            (9, ['Before operation']), (13, ['Check fictional cable', 'HISTORICAL-YES', '']),
            (17, ['After operation']), (21, ['Inspect fictional guard', '', 'HISTORICAL-NO'])])])
        inline = td / 'Fictional_UI108_InlineInstructions.docx'
        docx(inline, ['Deck maintenance checklist', [['Task', 'Yes', 'No'],
            ['Instructions', 'Isolate fictional energy before work.', ''],
            ['Check fictional lock', 'HISTORICAL-YES', '']]])
        header = ['Description', 'Asset reference', 'SN', 'PN', 'Qty expected', 'Qty counted', 'Remarks']
        mixed = td / 'Fictional_UI108_MixedRows.xlsx'
        selection_workbook(mixed, [('Fictional mixed stock', [
            (5, header), (9, ['Fictional genuine pump', 'A-00108', '000108', 'PN-000108', 0, 88, 'Fictional first note']),
            (12, header), (15, ['Section: SPARES']),
            (19, ['Fictional genuine cable', 'A-00109', '000109', 'PN-000109', 2, 88, 'Fictional second note']),
            (23, ['Total', '', '', '', 2]),
            (27, ['Instructions: verify the fictional labels']),
            (31, ['Prepared by: Fictional reviewer'])])])
        ambiguous = td / 'Fictional_UI108_RealNames.xlsx'
        selection_workbook(ambiguous, [('Fictional real item names', [
            (4, header), (8, ['Total', 'A-TOTAL-108', '000TOTAL', 'PN-TOTAL', 0]),
            (13, ['Instructions', 'A-INSTRUCTIONS-108', '000INSTRUCTIONS', 'PN-INSTRUCTIONS', 1]),
            (21, ['Unidentified spare'])])])
        late = td / 'Fictional_UI108_LateHeader.xlsx'
        selection_workbook(late, [('Fictional late stock',
            [(i * 3 + 1, ['Fictional instruction ' + str(i)]) for i in range(1, 32)] +
            [(100, header), (109, ['Fictional late item', 'A-LATE-108', '000LATE', 'PN-LATE', 0, 88])])])
        deep = td / 'Fictional_UI108_DeepHeader.xlsx'
        selection_workbook(deep, [('Fictional deep stock',
            [(i * 3 + 1, ['Fictional preface ' + str(i)]) for i in range(1, 262)] +
            [(800, header), (809, ['Fictional deep item', 'A-DEEP-108', '000DEEP', 'PN-DEEP', 0, 88])])])
        stronger = td / 'Fictional_UI108_StrongerLater.xlsx'
        selection_workbook(stronger, [('Fictional two tables', [
            (3, ['Description', 'Quantity']), (8, ['Fictional early pump', 0]),
            (13, ['Fictional early cable', 2]), (21, header),
            (29, ['Fictional later item', 'A-LATER-108', '000LATER', 'PN-LATER', 1, 88])])])
        report['fictional_fixture_hashes'] = {p.name: sha(p) for p in td.glob('Fictional_*')}
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
            delayed = {'path': None, 'held': None}
            lose_next = {'save': False}

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
                    return {table: con.execute('SELECT count(*) FROM ' + table).fetchone()[0] for table in ['checklist_library_drafts', 'records', 'maintenance_routines', 'maintenance_jobs', 'toolbox_templates', 'toolbox_talks', 'inventory_items', 'inventory_counts']}

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

            def review(confirm=True):
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                assert latest('review')['status'] == 200, latest('review')['response']
                if confirm:
                    p.locator('#di-confirm').check()
                    expect(p.locator('#sb-import-save')).to_be_enabled()
                return copy.deepcopy(latest('review')['request']['draft'])

            def save():
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                assert latest('action')['response']['saved'] is True
                return copy.deepcopy(latest('action')['response'])

            def snapshot():
                return p.evaluate('JSON.stringify({resource:ui108Form.resource,draft:ui108Form.document.draft,inventory:ui108Form.document.inventory_import,review:ui108Form.review,request:ui108Form.request})')

            def mapped():
                return list(csv.DictReader(io.StringIO(p.locator('#di-inventory_rows').input_value()), delimiter='\t'))

            def screenshot(name, locator, controls='#di-edit input:visible,#di-edit select:visible,#di-edit button:visible,#di-edit textarea:visible'):
                p.wait_for_function('()=>!document.querySelector("#toast")?.classList.contains("visible")')
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    locator.evaluate('n=>n.scrollIntoView({block:"start"})')
                    p.evaluate('()=>scrollBy(0,-80)')
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name, width)
                    bounds = p.locator(controls).evaluate_all('(nodes)=>nodes.map(n=>{const b=n.getBoundingClientRect();return {id:n.id,left:b.left,right:b.right};})')
                    assert not [b for b in bounds if b['left'] < -1 or b['right'] > width + 1], (name, width, bounds)
                    filename = name + '_' + str(width) + '.png'
                    p.screenshot(path=str(OUT / filename))
                    report['screenshots'].append(filename)
                    ok(name.replace('_', ' ') + ' fits ' + str(width) + 'px without page overflow or clipped controls')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            def blank_history(draft):
                assert 'HISTORICAL-' not in json.dumps(draft)

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                p.evaluate('''()=>{const n=window.AJDocumentImport;window.AJDocumentImport={...n,scan(f,h){window.ui108Form=f;window.ui108Hooks=h;return n.scan(f,h);},lock(f){window.ui108Form=f;return n.lock(f);}};}''')
                before = counts()
                scan = builder(labelvalue)
                d = scan['draft']
                assert scan['kind'] == 'toolbox'
                assert d['description'] == 'Review the fictional deck lift.'
                assert d['structure']['tools'] == ['Fictional radio', 'Fictional gloves']
                assert 'Isolate fictional energy before work.' in json.dumps(d['structure']['introduction'])
                assert d['supervisor_instruction'] == 'Discuss the fictional exclusion zone.'
                assert d['declaration'] == 'I understand the fictional lift plan.'
                blank_history(d)
                assert counts() == before
                ok('Exact two-column source roles preserve description, instructions, tools, supervisor guidance and declaration without native writes or imported historical answers')
                expect(p.locator('#di-supervisor_instruction')).to_have_value(d['supervisor_instruction'])
                expect(p.locator('#di-declaration')).to_have_value(d['declaration'])
                p.locator('#di-toolbox-copy-notes').click()
                p.locator('#di-questions').fill('Can everyone identify the fictional isolation point?')
                edited = review()
                assert all(v in edited['outline'] for v in ['Isolate fictional energy', 'Fictional radio', 'Fictional gloves'])
                screenshot('label_value_toolbox', p.locator('#di-supervisor_instruction'))
                result = save()
                with store.connection() as con:
                    native = json.loads(con.execute('SELECT body FROM toolbox_templates WHERE id=?', (result['id'],)).fetchone()[0])
                assert native['revision'] == 0 and native['published'] is False
                assert native['definition']['supervisor_instruction'] == d['supervisor_instruction']
                assert native['definition']['declaration'] == d['declaration']
                assert all(v in json.dumps(native['definition']['prompts']) for v in ['Isolate fictional energy', 'Fictional radio', 'Fictional gloves'])
                blank_history(native)
                assert counts()['toolbox_talks'] == before['toolbox_talks']
                ok('Explicit include-source-notes and reviewed native save produce one unpublished toolbox form with preserved role text and no performed talk or copied historical responses')

                scan = builder(changed)
                items = [i for s in scan['draft']['structure']['sections'] for i in s['items']]
                assert [i['text'] for i in items] == ['Check fictional guard', 'Measure fictional discharge']
                assert items[0]['fields'][0]['choices'] == ['Yes', 'No']
                assert items[1]['phases'] == ['pre', 'post']
                assert any(f['unit'] == 'bar' for f in items[1]['fields'])
                assert not any(f.get('choices') == ['Yes', 'No'] for f in items[1]['fields'])
                blank_history(scan['draft'])
                ok('A changed repeated Task/Before/After/Pressure header changes subsequent column roles while earlier printed Yes/No fields remain local to earlier checks')
                screenshot('changed_table_header', p.locator('#di-structure'))
                review()
                assert counts()['records'] == before['records'] and counts()['maintenance_jobs'] == before['maintenance_jobs']
                ok('Changed-header proposal can be reviewed as a maintenance definition without creating completed check records or maintenance jobs')

                scan = builder(sequential)
                st = scan['draft']['structure']
                items = [i for s in st['sections'] for i in s['items']]
                assert [i['text'] for i in items] == ['Check fictional cable', 'Inspect fictional guard']
                assert [i['phases'] for i in items] == [['pre'], ['post']]
                assert st['workflow']['mode'] == 'prepost'
                blank_history(scan['draft'])
                ok('Exact standalone Before operation and After operation table rows supply check stages rather than becoming false checks')
                screenshot('sequential_table_stages', p.locator('#di-structure'))

                scan = builder(inline)
                st = scan['draft']['structure']
                assert [i['text'] for s in st['sections'] for i in s['items']] == ['Check fictional lock']
                assert 'Isolate fictional energy before work.' in json.dumps(st['introduction'])
                blank_history(scan['draft'])
                ok('An exact Instructions label/value row inside the response table becomes retained instruction text, leaving one genuine check and no historical answer')

                scan = builder(mixed)
                assert scan['kind'] == 'inventory'
                assert len(mapped()) == 7
                p.locator('#di-row-picker').evaluate('n=>n.open=true')
                p.locator('#di-row-filter').select_option('source-review')
                assert p.locator('[data-di-source-review]').count() == 5
                assert {int(x) for x in p.locator('[data-di-source-review]').evaluate_all('(ns)=>ns.map(n=>n.dataset.diSourceReview)')} == {2, 3, 5, 6, 7}
                assert all(p.locator('[data-di-row-select="' + str(i) + '"]').is_checked() for i in [2, 3, 5, 6, 7])
                expect(p.locator('#di-source-review-note')).to_contain_text('original')
                ok('Repeated header, section, numeric Total, instruction and footer are five located advisories while all seven mapped rows remain included')
                review()
                receipt = p.evaluate('JSON.stringify({review:ui108Form.review,request:ui108Form.request,draft:ui108Form.document.draft})')
                p.locator('#di-row-search').fill('Total')
                assert p.locator('[data-di-source-review]').count() == 1
                p.locator('#di-row-search').fill('')
                p.locator('#di-header-chooser').evaluate('n=>n.open=true')
                p.locator('#di-header-search').fill('Description')
                assert p.locator('[data-di-header-choice]').count() <= 50
                assert p.evaluate('JSON.stringify({review:ui108Form.review,request:ui108Form.request,draft:ui108Form.document.draft})') == receipt
                assert p.locator('#di-confirm').is_checked()
                ok('Source-review filtering, item searching and header-source searching are read-only and keep the checked receipt and strict draft unchanged')
                p.locator('#di-header-chooser').evaluate('n=>n.open=false')
                screenshot('located_inventory_source_review', p.locator('#di-row-picker'))
                p.locator('#di-rows-exclude-shown').click()
                assert len(mapped()) == 7
                assert p.locator('#di-confirm').is_disabled() and p.locator('#sb-import-save').is_disabled()
                reviewed = review()
                batch = reviewed['inventory_sheets'][0]
                assert batch['selected_rows'] == [1, 4]
                assert batch['source_rows'] == [9, 12, 15, 19, 23, 27, 31]
                ok('Explicit exclusion of the five shown advisories invalidates approval but retains every mapped row and exact Excel row proof, selecting only genuine positions 1 and 4')
                lost_before = counts()
                lose_next['save'] = True
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-import-save')).to_have_text('Retry unchanged request')
                assert p.locator('#di-header-search').is_disabled() and p.locator('#di-header-next').is_disabled()
                request = copy.deepcopy(latest('action')['request'])
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                assert latest('action')['request'] == request
                result = latest('action')['response']
                assert counts()['inventory_items'] == lost_before['inventory_items'] + 2
                assert counts()['inventory_counts'] == lost_before['inventory_counts']
                with store.connection() as con:
                    saved_items = [json.loads(x[0]) for x in con.execute('SELECT body FROM inventory_items WHERE parent_id=? ORDER BY id', (result['id'],))]
                assert sorted(x['name'] for x in saved_items) == ['Fictional genuine cable', 'Fictional genuine pump']
                assert next(x for x in saved_items if x['name'].endswith('pump'))['quantity'] == 0
                assert all('88' in x['notes'] for x in saved_items)
                assert {x['serial'] for x in saved_items} == {'000108', '000109'}
                ok('Lost-response identical retry creates exactly two distinct unverified native inventory items, preserving leading-zero SN, expected zero and Counted only in Notes')

                scan = builder(ambiguous)
                assert len(mapped()) == 3
                p.locator('#di-row-picker').evaluate('n=>n.open=true')
                p.locator('#di-row-filter').select_option('source-review')
                assert p.locator('[data-di-source-review]').count() == 0
                assert mapped()[0]['quantity'] == '0' and mapped()[2]['quantity'] == ''
                ok('Items named Total or Instructions with identifiers and a name-only Unknown spare remain included and unflagged; expected zero is valid')

                scan = builder(late)
                assert p.locator('#di-header').input_value() == '31'
                assert len(mapped()) == 1 and mapped()[0]['name'] == 'Fictional late item'
                expect(p.locator('#di-header-boundary')).to_contain_text('31')
                expect(p.locator('#di-header-boundary')).to_contain_text('Excel row')
                ok('Qualified extracted header row 32 is automatically mapped within the expanded 250-row bound and its 31 preceding nonempty source rows are visible for review')
                screenshot('late_header_boundary', p.locator('#di-header-boundary'))

                scan = builder(stronger)
                assert p.locator('#di-header').input_value() == '3'
                assert len(mapped()) == 1
                expect(p.locator('#di-header-boundary')).to_contain_text('Excel row 3')
                expect(p.locator('#di-header-boundary')).to_contain_text('Excel row 8')
                expect(p.locator('#di-header-boundary')).to_contain_text('Excel row 13')
                review()
                p.locator('#di-header').select_option('0')
                assert p.locator('#di-confirm').is_disabled()
                p.locator('#di-map').click()
                assert [x['name'] for x in mapped()][:2] == ['Fictional early pump', 'Fictional early cable']
                ok('A stronger later header exposes omitted source rows 3/8/13; choosing the earlier header invalidates approval and explicitly remaps earlier genuine items')

                scan = builder(deep)
                p.locator('#di-kind').select_option('inventory')
                expect(p.locator('#di-header-chooser')).to_be_visible()
                p.locator('#di-header-chooser').evaluate('n=>n.open=true')
                assert p.locator('[data-di-header-choice]').count() <= 50
                p.locator('#di-header-next').click()
                assert p.locator('[data-di-header-choice]').count() <= 50
                p.locator('#di-header-search').fill('Asset reference')
                expect(p.locator('[data-di-header-choice="261"]')).to_be_visible()
                expect(p.locator('[data-di-header-choice="261"]')).to_contain_text('Excel row 800')
                screenshot('deep_header_source_search', p.locator('#di-header-chooser'))
                p.locator('[data-di-header-choice="261"]').click()
                expect(p.locator('#di-header')).to_have_value('261')
                p.locator('#di-map').click()
                assert len(mapped()) == 1 and mapped()[0]['name'] == 'Fictional deep item'
                p.locator('[data-di-sheet-select="0"]').check()
                reviewed = review()
                assert reviewed['inventory_sheets'][0]['source_rows'] == [809]
                ok('Paged source-row chooser renders at most 50 rows, searches beyond automatic row250 and, after explicit worksheet selection, maps chosen extracted row262 to genuine Excel row809')

                p.locator('#di-inventory_rows').evaluate('n=>n.closest("details").open=true')
                p.locator('#di-inventory_rows').fill(p.locator('#di-inventory_rows').input_value() + '\n')
                expect(p.locator('#di-source-review-note')).to_contain_text('unavailable')
                p.locator('#di-row-picker').evaluate('n=>n.open=true')
                p.locator('#di-row-filter').select_option('source-review')
                assert p.locator('[data-di-source-review]').count() == 0
                assert p.locator('#di-confirm').is_disabled()
                ok('Manual full-TSV editing visibly clears extraction-dependent advisory facts and approval rather than attributing stale original proof to edited rows')

                guide = browser.new_page()
                guide_errors = []
                guide.on('pageerror', lambda error: guide_errors.append(str(error)))
                guide.route(origin + '/**', route)
                topics = [('documentimport', ['ui108-table-source-review', 'ui108-inventory-source-review']),
                          ('inventorybuilder', ['ui108-inventory-source-review']),
                          ('toolbox', ['ui108-table-source-review', 'ui108-toolbox-read-recovery']),
                          ('toolboxbuilder', ['ui108-table-source-review', 'ui108-toolbox-read-recovery'])]
                for mode in ['offline', 'served']:
                    for topic, sections in topics:
                        guide.goto((SOURCE / 'docs/user/topics' / (topic + '.html')).as_uri() if mode == 'offline' else origin + '/help/topics/' + topic)
                        guide.evaluate('document.documentElement.style.scrollBehavior="auto"')
                        for width in [1440, 320]:
                            guide.set_viewport_size({'width': width, 'height': 1000})
                            for section in sections:
                                node = guide.locator('#' + section)
                                expect(node).to_be_visible()
                                if mode == 'offline':
                                    assert node.evaluate('n=>n.classList.contains("chapter")&&!!n.closest("main.wrap.layout > .content")')
                                node.evaluate('n=>n.scrollIntoView({block:"start",behavior:"instant"})')
                                expect(node).to_be_in_viewport()
                                b = node.bounding_box()
                                assert b['width'] > (600 if width == 1440 else 200), (mode, topic, section, width, b)
                                assert b['x'] >= -1 and b['x'] + b['width'] <= width + 1
                                assert guide.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (mode, topic, width)
                                name = 'help_' + mode + '_' + topic + '_' + section + '_' + str(width) + '.png'
                                guide.screenshot(path=str(OUT / name))
                                report['screenshots'].append(name)
                            ok(mode.capitalize() + ' ' + topic + ' Help shows the current UI108 guidance inside the content column at ' + str(width) + 'px without horizontal overflow')
                assert not guide_errors, guide_errors
                guide.close()
                assert not report['errors'], report['errors']
                for name, value in report['served_asset_hashes'].items():
                    assert value == report['source_hashes'][name], (name, value)
                assert all(sha(SOURCE / name) == value for name, value in report['source_hashes'].items())
                assert sha(SOURCE / 'RELEASE_FILES.json') == report['runtime_manifest_sha256']
                assert sha(Path(__file__)) == report['harness_sha256']
                ok('Every served tracked asset matches the source pin and the exercised genuine-browser workflows raise no unhandled JavaScript errors')
                report['passed'] = True
            except Exception:
                report['passed'] = False
                p.screenshot(path=str(OUT / 'FAILURE.png'))
                raise
            finally:
                report['summary'] = dict(checks_passed=len(report['checks']), unexpected_errors=len(report['errors']))
                (OUT / 'UI108_TABLE_BROWSER_RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
