"""UI104 inventory document acceptance against a disposable fictional C01.

Real Chromium, real company boundary/core APIs, real IndexedDB. No production
requests, resets, email, or source workbook writes. WebSocket and service-worker
registration are suppressed. Set WAVELINK_TEST_SOURCE to the derived runtime;
optionally set WAVELINK_IMPORT_SHIPPING_EXAMPLE to the original shipping XLSX.
"""
import base64
import copy
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
import uuid
from collections import Counter
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
from app import access

OUT = Path(os.environ.get('WAVELINK_UI104_EVIDENCE_DIR', str(ROOT.parent / 'evidence' / 'browser')))
TRACKED = ('app/document_import.py', 'app/inventory.py', 'app/builder_hub.py',
           'app/static/document_import.js', 'app/static/document_import.css',
           'app/static/setup_builders.js',
           'app/static/fieldwork.js', 'app/static/inventory_workspace.js',
           'app/static/verification.js', 'app/static/task_workspace.js',
           'app/static/browser_workspace.js', 'app/static/equipment_workspace_ui79.css',
           'app/static/work_execution_ui80.css', 'app/static/index.html', 'app/static/sw.js')


def workbook(path, serial_suffix='', quantity_values=None, serial_values=None, part_values=None):
    """Small literal XLSX fixture using only the standard library."""
    labels = [('Fictional Deck', 'SN', 'PN'), ('Fictional Workshop', 'S/N', 'Part No.'),
              ('Fictional Store', 'Serial Number', 'Part Number'), ('Fictional Locker', 'Serial no.', 'P/N')]
    ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
    rel = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    with ZipFile(path, 'w', ZIP_DEFLATED) as book:
        book.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>' + ''.join('<Override PartName="/xl/worksheets/sheet' + str(i+1) + '.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(4)) + '</Types>')
        book.writestr('_rels/.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="' + rel + '/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        book.writestr('xl/workbook.xml', '<workbook xmlns="' + ns + '" xmlns:r="' + rel + '"><sheets>' + ''.join('<sheet name="' + escape(name) + '" sheetId="' + str(i+1) + '" r:id="rId' + str(i+1) + '"/>' for i, (name, _, _) in enumerate(labels)) + '</sheets></workbook>')
        book.writestr('xl/_rels/workbook.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join('<Relationship Id="rId' + str(i+1) + '" Type="' + rel + '/worksheet" Target="worksheets/sheet' + str(i+1) + '.xml"/>' for i in range(4)) + '</Relationships>')
        for index, (_, serial, part) in enumerate(labels):
            rows = [['Item name', serial, part, 'QTY Shall', 'Qty Counted', 'Remarks'],
                    ['Fictional UI104 item ' + str(index), serial_values[index] if serial_values is not None else 'TRAIN-SN-104-' + str(index) + serial_suffix,
                     part_values[index] if part_values is not None else 'TRAIN-PN-104-' + str(index), quantity_values[index] if quantity_values is not None else index, '99+99' if index == 2 else 99,
                     'Disposable example only']]
            body = ''
            for row_index, values in enumerate(rows, 1):
                cells = ''
                for column, value in enumerate(values):
                    address = chr(65 + column) + str(row_index)
                    cells += '<c r="' + address + '"' + ('><v>' + str(value) + '</v></c>' if type(value) is int else ' t="inlineStr"><is><t>' + escape(str(value)) + '</t></is></c>')
                body += '<row r="' + str(row_index) + '">' + cells + '</row>'
            book.writestr('xl/worksheets/sheet' + str(index+1) + '.xml', '<worksheet xmlns="' + ns + '"><sheetData>' + body + '</sheetData></worksheet>')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {'checks': [], 'errors': [], 'widths': [1440, 390, 320],
              'method': 'Real Chromium, fictional disposable C01 HostedBoundary/CompanyAccess/core APIs and IndexedDB; no production requests. WebSocket and service-worker registration are suppressed.',
              'source_hashes': {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() for name in TRACKED},
              'served_asset_hashes': {},
              'harness_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'limitations': ['Service-worker registration and WebSockets are suppressed.', 'No production, Render, live email, physical camera, Windows display or worker-upgrade acceptance.', 'The shipping workbook is exercised only when WAVELINK_IMPORT_SHIPPING_EXAMPLE is provided; otherwise only disposable literal XLSX fixtures are used.']}

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui104-import-') as td:
        synthetic = Path(td) / 'Fictional_UI104_Inventory.xlsx'
        workbook(synthetic)
        installation = instance.__wrapped__(Path(td))
        with client(installation) as c, sync_playwright() as pw:
            activate(c)
            origin = installation[2].external_origin
            store = c.app.state.core.state.store
            browser = pw.chromium.launch(headless=True, args=['--no-sandbox'], executable_path=os.environ.get('WAVELINK_CHROMIUM_EXECUTABLE') or None)
            p = browser.new_page(viewport={'width': 1440, 'height': 1000})
            p.set_default_timeout(30000)
            p.on('pageerror', lambda error: report['errors'].append(str(error)))
            p.on('dialog', lambda dialog: dialog.accept())
            p.add_init_script("class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();")
            exchanges = []
            lose_next = {'document': False}
            delayed = {'path': None, 'held': None}

            def route(r):
                req = r.request
                u = urlsplit(req.url)
                path = u.path + ('?' + u.query if u.query else '')
                response = c.request(req.method, path, headers=req.headers, content=req.post_data_buffer)
                source_name = 'app' + u.path
                if source_name in TRACKED and response.status_code == 200:
                    report['served_asset_hashes'][source_name] = hashlib.sha256(response.content).hexdigest()
                if u.path.startswith(('/api/inventory/', '/api/verification/', '/api/builders/')):
                    exchanges.append({'path': u.path, 'status': response.status_code,
                                      'request': json.loads(req.post_data or '{}'),
                                      'response': response.json() if 'application/json' in response.headers.get('content-type', '') else None})
                if delayed['path'] == u.path:
                    delayed['path'] = None
                    delayed['held'] = (r, response)
                    return
                if lose_next['document'] and u.path == '/api/builders/document/action':
                    lose_next['document'] = False
                    r.abort('failed')
                    return
                r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

            p.route(origin + '/**', route)

            def latest(suffix):
                return next(x for x in reversed(exchanges) if x['path'].endswith(suffix))

            def auth():
                return p.evaluate('({token:state.auth.token,hub:state.hub_id})')

            def action(name, payload, expected=200):
                a = auth()
                response = c.post('/api/inventory/action', json={'action': name, 'payload': payload, 'op_id': str(uuid.uuid4())},
                                  headers={'Authorization': 'Bearer ' + a['token'], 'x-aj-hub-id': a['hub']})
                assert response.status_code == expected, response.text
                return response.json()

            def navigate(fragment, selector):
                p.evaluate('(hash)=>{location.hash=hash;render();}', fragment)
                expect(p.locator(selector)).to_be_visible()

            def builder(path, wait=True):
                if p.locator('#sb-close').count():
                    p.locator('#sb-close').click()
                navigate('#builders', '#sb-document')
                p.locator('#sb-document').click()
                p.locator('#sb-file').set_input_files(str(path))
                if wait:
                    expect(p.locator('#di-sheet')).to_be_visible(timeout=90000)

            def existing_builder(path, book_id):
                if p.locator('#sb-close').count():
                    p.locator('#sb-close').click()
                navigate('#inventory/' + book_id, '#inv-import-items')
                p.locator('#inv-import-items').click()
                expect(p.locator('#sb-file')).to_be_visible()
                p.locator('#sb-file').set_input_files(str(path))
                expect(p.locator('#di-sheet')).to_be_visible(timeout=90000)
                expect(p.locator('#di-target-mode')).to_have_value('existing')
                expect(p.locator('#di-target-id')).to_have_value(book_id)

            def data_rows():
                return list(csv.DictReader(io.StringIO(p.locator('#di-inventory_rows').input_value()), delimiter='\t'))

            def write_rows(rows):
                columns = list(rows[0])
                out = io.StringIO()
                writer = csv.DictWriter(out, fieldnames=columns, delimiter='\t', lineterminator='\n')
                writer.writeheader()
                writer.writerows(rows)
                p.locator('#di-inventory_rows').evaluate('node=>node.closest("details").open=true')
                p.locator('#di-inventory_rows').fill(out.getvalue())

            def check():
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                assert latest('/document/review')['status'] == 200
                overview = latest('/document/review')['response']['summary']['inventory_review']
                assert overview['can_save'] is True and not overview['conflicts']['duplicate_count'] and not overview['conflicts']['unproven_sheets'], overview
                expect(p.locator('#di-inventory-review')).to_be_visible()
                expect(p.locator('#di-inventory-review')).to_contain_text('Ready for your confirmation')
                assert p.locator('#di-review-block-reason').count() == 0
                p.locator('#di-confirm').check()
                expect(p.locator('#sb-import-save')).to_be_enabled()

            def save():
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                saved = latest('/document/action')['response']
                assert saved['saved'] is True
                book = store.inventory.get(saved['id'], actor)
                p.locator('#sb-done').click()
                return book

            def screenshot(name, locator):
                p.wait_for_function('()=>!document.querySelector("#toast")?.classList.contains("visible")')
                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    locator.evaluate('node=>node.scrollIntoView({block:"start"})')
                    locator.evaluate('node=>{const modal=node.closest(".modal");if(modal){modal.scrollTop=0;const dialog=node.closest("dialog");if(dialog)dialog.scrollTop=0;const host=document.querySelector("#dialog-content");if(host)host.scrollTop=0;}}')
                    p.evaluate('()=>scrollBy(0,-80)')
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name, width)
                    p.screenshot(path=str(OUT / (name + '_' + str(width) + '.png')))
                    ok(name.replace('_', ' ') + ' fits ' + str(width) + 'px without horizontal page overflow')
                p.set_viewport_size({'width': 1440, 'height': 1000})

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                original_auth = auth()
                actor = store.session(original_auth['token'])

                # A reviewed draft for one sheet survives active-sheet changes and
                # temporary deselection; combining sheets needs no source edits.
                builder(synthetic)
                scan = latest('/document/scan')['response']
                indexes = {s['name']: index for index, s in enumerate(scan['sheets'])}
                assert len(indexes) == 4
                p.locator('#di-select-data').click()
                assert p.locator('[data-di-sheet-select]:checked').count() == 4
                p.locator('#di-sheet').select_option('Fictional Deck')
                rows = data_rows()
                assert rows[0]['serial'] == 'TRAIN-SN-104-0' and rows[0]['part_number'] == 'TRAIN-PN-104-0'
                assert rows[0]['quantity'] == '0' and not rows[0]['asset']
                rows[0]['name'] = 'Fictional reviewed Deck wording'
                write_rows(rows)
                p.locator('#di-sheet').select_option('Fictional Workshop')
                p.locator('#di-sheet').select_option('Fictional Deck')
                assert data_rows()[0]['name'] == 'Fictional reviewed Deck wording'
                deck_index = indexes['Fictional Deck']
                p.locator('[data-di-sheet-select="' + str(deck_index) + '"]').uncheck()
                p.locator('[data-di-sheet-select="' + str(deck_index) + '"]').check()
                p.locator('#di-sheet').select_option('Fictional Deck')
                assert data_rows()[0]['name'] == 'Fictional reviewed Deck wording'
                ok('Switching and deselecting/reselecting a worksheet preserves its explicitly edited mapped row')
                for name, index in indexes.items():
                    p.locator('[data-di-sheet-location="' + str(index) + '"]').fill('Reviewed ' + name)
                    p.locator('#di-sheet').select_option(name)
                    row = data_rows()[0]
                    assert row['serial'] == 'TRAIN-SN-104-' + str(index) and row['part_number'] == 'TRAIN-PN-104-' + str(index), {'sheet': name, 'serial': row['serial'], 'part_number': row['part_number']}
                    assert not row['asset']
                ok('SN, S/N, Serial Number and Serial no. map to serial; PN, Part No., Part Number and P/N map separately to native part number')
                p.locator('#di-title').fill('Fictional combined UI104 inventory')
                screenshot('multi_sheet_selection', p.locator('#di-sheet-checks'))
                screenshot('identity_mapping', p.locator('.di-map-grid'))
                check()
                overview = latest('/document/review')['response']['summary']['inventory_review']
                assert overview['total_items'] == 4 and len(overview['sheets']) == 4
                assert all(x['items'] == 1 and x['serials'] == 1 and x['part_numbers'] == 1 and x['unknown_quantities'] == 0 for x in overview['sheets'])
                assert overview['destination']['mode'] == 'new' and overview['destination']['existing_items'] == 0 and overview['destination']['proposed_items'] == 4
                expect(p.locator('#di-review-total')).to_contain_text('4')
                expect(p.locator('#di-review-total')).to_contain_text('items in this import')
                assert p.locator('#di-review-sheets .di-review-sheet').count() == 4
                assert set(p.locator('#di-review-sheets h4').all_text_contents()) == set(indexes)
                assert set(p.locator('#di-review-sheets .di-review-location strong').all_text_contents()) == {'Reviewed ' + n for n in indexes}
                screenshot('readable_combined_overview', p.locator('#di-inventory-review'))
                ok('Review shows one readable destination/record total and four individual worksheet/location cards, with record counts separate from quantities and identity coverage')
                reviewed = latest('/document/review')['request']['draft']
                assert len(reviewed['inventory_sheets']) == 4
                assert {s['location'] for s in reviewed['inventory_sheets']} == {'Reviewed ' + n for n in indexes}
                # Mapped-row changes invalidate the reviewed exact draft.
                p.locator('#di-sheet').select_option('Fictional Deck')
                edited_rows = data_rows()
                edited_rows[0]['notes'] += ' Reviewed overview edit'
                write_rows(edited_rows)
                assert p.locator('#sb-import-save').is_disabled() and not p.locator('#di-confirm').is_checked()
                check()
                ok('Editing an inventory row after reviewing clears exact-draft confirmation and requires a fresh review')
                # Destination changes invalidate the reviewed exact draft.
                p.locator('[data-di-sheet-location="' + str(deck_index) + '"]').fill('Reviewed Fictional Deck corrected')
                assert p.locator('#sb-import-save').is_disabled() and not p.locator('#di-confirm').is_checked()
                check()
                combined = save()
                assert len(combined['items']) == 4 and not combined['counts']
                assert len({x['location'] for x in combined['items']}) == 4
                assert next(x for x in combined['items'] if x['serial'] == 'TRAIN-SN-104-0')['quantity'] == 0
                assert all(x['part_number'].startswith('TRAIN-PN-104-') and not x['asset'] for x in combined['items'])
                assert all('Source Qty Counted:' in x['notes'] for x in combined['items'])
                ok('One confirmed import creates one inventory containing all four sheets in four reviewed locations, with zero preserved and prior Excel counts kept solely as source notes')

                # Actual source workbook acceptance is optional, never bundled.
                path_value = os.environ.get('WAVELINK_IMPORT_SHIPPING_EXAMPLE', '')
                if path_value:
                    path = Path(path_value)
                    digest = hashlib.sha256(path.read_bytes()).hexdigest()
                    builder(path)
                    source_scan = latest('/document/scan')['response']
                    expected = {'Vehicle MR 07': (56, 63, 1), 'Pallet 1': (58, 179, 7), 'Pallet 2': (4, 4, 0), 'Pallet 3,4': (102, 219, 3)}
                    p.locator('#di-select-data').click()
                    chosen = p.locator('[data-di-sheet-select]:checked').evaluate_all('nodes=>nodes.map(n=>Number(n.dataset.diSheetSelect))')
                    assert {source_scan['sheets'][i]['name'] for i in chosen} == set(expected)
                    assert len(chosen) == 4
                    for name, (n, quantity_sum, unknown) in expected.items():
                        p.locator('#di-sheet').select_option(name)
                        values = data_rows()
                        assert len(values) == n, {'sheet': name, 'actual_rows': len(values), 'expected_rows': n, 'active_sheet': p.locator('#di-sheet').input_value(), 'header': p.locator('#di-header').input_value()}
                        assert sum(float(r['quantity']) for r in values if r['quantity']) == quantity_sum
                        assert sum(not r['quantity'] for r in values) == unknown
                        assert all(not r['asset'] and not r['is_container'] and not r['container_ref'] for r in values)
                        assert p.locator('[data-di-column="12"] option:checked').inner_text() == 'PN'
                    p.locator('#di-title').fill('Fictional reviewed shipping source')
                    check()
                    shipping_overview = latest('/document/review')['response']['summary']['inventory_review']
                    assert shipping_overview['total_items'] == 220 and shipping_overview['serials'] == 66 and shipping_overview['part_numbers'] == 220 and shipping_overview['unknown_quantities'] == 11
                    assert {s['sheet']: (s['items'], s['unknown_quantities']) for s in shipping_overview['sheets']} == {name: (n, unknown) for name, (n, quantity_sum, unknown) in expected.items()}
                    expect(p.locator('#di-review-total')).to_contain_text('220')
                    screenshot('shipping_workbook_overview', p.locator('#di-inventory-review'))
                    shipping = save()
                    assert len(shipping['items']) == 220 and not shipping['counts']
                    assert all(x['part_number'] for x in shipping['items']) and sum(bool(x['serial']) for x in shipping['items']) == 66
                    assert Counter(x['location'] for x in shipping['items']) == Counter({name: values[0] for name, values in expected.items()})
                    assert sum(x['quantity'] or 0 for x in shipping['items']) == 465
                    assert sum(x['quantity'] is None for x in shipping['items']) == 11
                    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
                    report['shipping_example'] = {'source_sha256': digest, 'source_bytes': path.stat().st_size, 'records': 220, 'locations': 4, 'expected_quantity_sum': 465, 'unknown_expected_quantities': 11, 'summary_included': False, 'verification_created': False}
                    ok('The supplied shipping workbook combines all 220 detail records into one inventory with four sheet locations; its commercial summary stays excluded and the original source remains unchanged')

                # Native PN lives alongside serial and asset in ordinary inventory.
                navigate('#inventory/' + combined['id'], '#inv-add')
                for query in ('TRAIN-PN-104-0', 'trainpn1040'):
                    p.locator('[name=search]').fill(query)
                    expect(p.locator('#inv-rows')).to_contain_text('TRAIN-PN-104-0')
                    assert p.locator('#inv-rows [data-select-row]').count() == 1
                ok('A full punctuated PN and its compact spelling both find only the matching item despite similar source filenames and numeric notes in other rows')
                current_item = next(x for x in combined['items'] if x['serial'] == 'TRAIN-SN-104-0')
                p.locator('[data-inv-item="' + current_item['id'] + '"]').click()
                expect(p.locator('#dialog-content')).to_contain_text('TRAIN-PN-104-0')
                p.locator('#inv-edit').click()
                expect(p.locator('#fw-form [name=part_number]')).to_have_value('TRAIN-PN-104-0')
                long_part = 'TRAIN-PN-104-EDITED-' + 'LONGSEGMENT' * 28
                p.locator('#fw-form [name=part_number]').fill(long_part)
                screenshot('native_part_number_editor', p.locator('#fw-form'))
                p.locator('#fw-keep').click()
                expect(p.locator('#fw-form')).not_to_be_visible()
                p.reload()
                expect(p.locator('#inv-add')).to_be_visible()
                p.locator('#fw-drafts').click()
                p.locator('[data-fw-resume]').first.click()
                expect(p.locator('#fw-form [name=part_number]')).to_have_value(long_part)
                p.locator('#fw-save').click()
                expect(p.locator('#fw-form')).not_to_be_visible()
                combined = store.inventory.get(combined['id'], actor)
                current_item = next(x for x in combined['items'] if x['id'] == current_item['id'])
                assert current_item['part_number'] == long_part and current_item['serial'] == 'TRAIN-SN-104-0' and not current_item['asset']
                p.locator('[name=search]').fill('train pn 104 edited')
                expect(p.locator('#inv-rows')).to_contain_text('TRAIN-PN-104-EDITED')
                screenshot('inventory_part_number', p.locator('#inv-rows'))
                ok('Part number is visible and searchable in the inventory, has its own native editor field, and survives a kept local draft plus primary-window reload without changing serial or asset')

                # Appending reviewed rows preserves every prior item and frozen count.
                prior_items = copy.deepcopy(combined['items'])
                count = action('start_count', {'list_id': combined['id'], 'name': 'Fictional UI104 pre-append fixed scope'})
                action('check_item', {'session_id': count['id'], 'item_id': current_item['id'], 'item_version': current_item['version'], 'check_version': 0, 'result': 'found', 'counted_quantity': 0, 'note': 'Fictional checked prior to append'})
                before_count = copy.deepcopy(store.inventory.count(count['id'], actor))
                append_path = Path(td) / 'Fictional_UI104_Append.xlsx'
                # Distinct serials: PN may repeat between legitimate spare items.
                workbook(append_path, serial_suffix='-APPEND')
                existing_builder(append_path, combined['id'])
                p.locator('#di-select-data').click()
                expect(p.locator('#di-target-id')).to_have_value(combined['id'])
                ok('The inventory\'s visible Import items action opens document import with that existing inventory already selected')
                screenshot('append_destination', p.locator('#di-target-mode'))
                check()
                p.locator('#di-target-mode').select_option('new')
                assert p.locator('#sb-import-save').is_disabled() and not p.locator('#di-confirm').is_checked()
                p.locator('#di-target-mode').select_option('existing')
                p.locator('#di-target-id').select_option(combined['id'])
                check()
                ok('Changing the destination mode after checking an append clears confirmation and Save until that exact destination is reviewed again')
                append_overview = latest('/document/review')['response']['summary']['inventory_review']
                assert append_overview['destination']['mode'] == 'existing' and append_overview['destination']['name'] == combined['name']
                assert append_overview['destination']['existing_items'] == 4 and append_overview['destination']['proposed_items'] == 8
                expect(p.locator('#di-review-destination')).to_contain_text(combined['name'])
                screenshot('readable_append_overview', p.locator('#di-inventory-review'))
                ok('Existing-inventory review names its destination and separates four incoming records from the four prior records and proposed total of eight')
                lose_next['document'] = True
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-import-save')).to_contain_text('Retry')
                first_request = copy.deepcopy(latest('/document/action')['request'])
                assert len(store.inventory.get(combined['id'], actor)['items']) == 8
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-success')).to_be_visible()
                second_request = latest('/document/action')['request']
                assert first_request == second_request
                appended = store.inventory.get(combined['id'], actor)
                assert len(appended['items']) == 8
                assert {x['id']: x for x in appended['items'] if x['id'] in {y['id'] for y in prior_items}} == {y['id']: y for y in prior_items}
                after_count = store.inventory.count(count['id'], actor)
                assert [x['expected'] for x in after_count['rows']] == [x['expected'] for x in before_count['rows']] and after_count['checks'] == before_count['checks']
                assert after_count['total'] == 4 and after_count['checked'] == 1 and after_count['new_items'] == 4
                p.locator('#sb-done').click()
                ok('Appending four reviewed rows keeps all prior item bytes, exact existing verification scope and saved result; a lost-response retry reuses the identical receipt and creates no duplicate rows')

                navigate('#inventory/count/' + count['id'], '[name=stock_query]')
                for query in ('TRAIN-PN-104-EDITED', 'trainpn104edited', 'train pn 104 edited'):
                    p.locator('[name=stock_query]').fill(query)
                    expect(p.locator('#stock-rows')).to_contain_text('TRAIN-PN-104-EDITED')
                    assert p.locator('#stock-rows [data-stock-row]').count() == 1
                    expect(p.locator('#stock-rows')).to_contain_text('Already checked: Found')
                    assert store.inventory.count(count['id'], actor)['checked'] == 1
                p.locator('[data-check="' + current_item['id'] + '"]').click()
                expect(p.locator('#verify-saved-result')).to_contain_text('TRAIN-PN-104-EDITED')
                screenshot('checked_part_number', p.locator('#verify-saved-result'))
                p.locator('#verify-result-back').click()
                assert store.inventory.count(count['id'], actor)['checked'] == 1
                ok('Punctuated, compact and worded part-number searches in a fixed verification all find the same previously checked Found-zero item and open its read-only saved result without verifying appended stock')

                # UI104 catches whole-batch duplicate source conflicts before Save.
                duplicate_before = copy.deepcopy(store.inventory.get(combined['id'], actor))
                duplicate_count_before = copy.deepcopy(store.inventory.count(count['id'], actor))
                builder(append_path)
                p.locator('#di-select-data').click()
                p.locator('#di-target-mode').select_option('existing')
                p.locator('#di-target-id').select_option(combined['id'])
                document_actions_before = sum(x['path'].endswith('/document/action') for x in exchanges)
                p.locator('#sb-review').click()
                expect(p.locator('#di-review-conflicts')).to_be_visible()
                expect(p.locator('#di-inventory-review')).to_contain_text('Import blocked')
                expect(p.locator('#di-review-conflicts')).to_contain_text('This entire import is blocked.')
                expect(p.locator('#di-review-block-reason')).to_be_visible()
                expect(p.locator('#di-review-block-reason')).to_contain_text('4 source rows are already in this inventory.')
                assert p.locator('#di-review-block-reason').evaluate('node=>Boolean(node.compareDocumentPosition(document.querySelector("#di-review-destination")) & Node.DOCUMENT_POSITION_FOLLOWING)')
                ok('A short blocking reason appears immediately below the overview heading and before the destination, with complete source-row diagnostics available below')
                reviewed = latest('/document/review')['response']
                assert latest('/document/review')['status'] == 200
                overview = reviewed['summary']['inventory_review']
                assert overview['can_save'] is False and overview['conflicts']['duplicate_count'] == 4, overview
                assert {r['sheet'] for r in overview['conflicts']['rows']} == set(indexes)
                assert all(r['source_row'] == 2 and r['name'] and r['reason'] for r in overview['conflicts']['rows'])
                expect(p.locator('#di-confirm')).to_be_disabled()
                expect(p.locator('#sb-import-save')).to_be_disabled()
                assert not p.locator('#di-confirm').is_checked()
                assert sum(x['path'].endswith('/document/action') for x in exchanges) == document_actions_before
                assert store.inventory.get(combined['id'], actor) == duplicate_before
                assert store.inventory.count(count['id'], actor) == duplicate_count_before
                screenshot('duplicate_source_preflight', p.locator('#di-inventory-review'))
                screenshot('duplicate_source_rows', p.locator('#di-review-conflicts'))
                ok('An already imported source is diagnosed during review with all four worksheet and original row conflicts, disabled confirmation/Save, no action request and no inventory or verification change')

                # Editing a mapped row clears its explicit source_rows metadata;
                # removing the compatible source-row Notes line too makes original
                # provenance unavailable rather than inventing a row match.
                p.locator('#di-sheet').select_option('Fictional Deck')
                unproven_rows = data_rows()
                unproven_rows[0]['name'] = 'Fictional wording with unavailable original row provenance'
                assert 'Source selected Excel row:' in unproven_rows[0]['notes']
                unproven_rows[0]['notes'] = '\n'.join(line for line in unproven_rows[0]['notes'].splitlines() if not line.startswith('Source selected Excel row:'))
                write_rows(unproven_rows)
                assert p.locator('#sb-import-save').is_disabled() and not p.locator('#di-confirm').is_checked()
                p.locator('#sb-review').click()
                expect(p.locator('#di-review-conflicts')).to_be_visible()
                unproven = latest('/document/review')['response']['summary']['inventory_review']
                assert unproven['can_save'] is False and 'Fictional Deck' in unproven['conflicts']['unproven_sheets'], unproven
                expect(p.locator('#di-review-block-reason')).to_contain_text('Original row references are missing or could not be confirmed')
                expect(p.locator('#di-confirm')).to_be_disabled()
                expect(p.locator('#sb-import-save')).to_be_disabled()
                assert store.inventory.get(combined['id'], actor) == duplicate_before
                assert store.inventory.count(count['id'], actor) == duplicate_count_before
                ok('Editing rows on an already imported source sheet displays missing-provenance diagnostics and keeps the entire batch blocked without modifying saved stock or counts')

                # A destination changed after exact review requires new review.
                stale_path = Path(td) / 'Fictional_UI104_Stale.xlsx'
                workbook(stale_path, serial_suffix='-STALE')
                builder(stale_path)
                p.locator('#di-select-data').click()
                p.locator('#di-target-mode').select_option('existing')
                p.locator('#di-target-id').select_option(combined['id'])
                p.locator('#di-sheet').select_option('Fictional Deck')
                stale_rows = data_rows()
                stale_rows[0]['name'] = 'Fictional retained stale-import wording'
                write_rows(stale_rows)
                p.locator('[data-di-sheet-location="0"]').fill('Fictional retained stale-import location')
                check()
                action('add_location', {'list_id': combined['id'], 'version': store.inventory.get(combined['id'], actor)['version'], 'name': 'Fictional location added after review'})
                p.locator('#sb-import-save').click()
                expect(p.locator('#sb-result')).to_contain_text('before importing')
                assert latest('/document/action')['status'] == 409
                assert len(store.inventory.get(combined['id'], actor)['items']) == 8
                ok('Changing an existing inventory after review rejects the stale import with no extra records')
                p.locator('#di-refresh-inventories').click()
                expect(p.locator('#sb-result')).to_contain_text('Inventories refreshed')
                assert not p.locator('#di-confirm').is_checked()
                assert data_rows()[0]['name'] == 'Fictional retained stale-import wording'
                assert p.locator('[data-di-sheet-location="0"]').input_value() == 'Fictional retained stale-import location'
                expect(p.locator('#di-target-id')).to_have_value(combined['id'])
                check()
                refreshed = save()
                assert refreshed['id'] == combined['id'] and len(refreshed['items']) == 12
                assert store.inventory.count(count['id'], actor)['checks'] == before_count['checks']
                ok('Explicit Refresh inventories keeps the chosen destination, edited mapped row and location, then a fresh review adds each of four rows exactly once')

                # Delayed source reading cannot replace a different module view.
                delayed['path'] = '/api/builders/document/scan'
                builder(synthetic, wait=False)
                p.wait_for_function('()=>document.querySelector("#sb-result")?.textContent.includes("Reading")')
                while delayed['held'] is None:
                    p.wait_for_timeout(100)
                p.locator('#workspace-nav a[href="#inventory"]').click()
                assert p.evaluate('location.hash') == '#builders'
                ok('Ordinary navigation while a source scan is open keeps the current builder until the form is saved or closed')
                replacement = c.post('/api/login', json={'login_id': 'admin', 'password': PASS, 'device_id': 'fictional-ui104-stale-read-session'})
                assert replacement.status_code == 200, replacement.text
                # Deliberately simulate an independently authenticated replacement
                # session while the old response is outstanding. No storage reset.
                p.evaluate('(token)=>{state.auth.token=token;location.hash="#inventory/' + combined['id'] + '";render();}', replacement.json()['token'])
                navigate('#inventory/' + combined['id'], '#inv-add')
                held_route, held_response = delayed['held']
                held_route.fulfill(status=held_response.status_code, body=held_response.content, headers=dict(held_response.headers))
                p.wait_for_timeout(300)
                assert p.locator('#di-sheet').count() == 0 and p.locator('#inv-add').is_visible()
                assert len(store.inventory.get(combined['id'], actor)['items']) == 12
                p.evaluate('(token)=>{state.auth.token=token;render();}', original_auth['token'])
                expect(p.locator('#inv-add')).to_be_visible()
                ok('A source scan delayed across an authenticated session and route change cannot inject an old proposal into the current inventory page or save any rows')

                assert auth() == original_auth
                assert not report['errors'], report['errors']
                ok('All import and verification workflows preserve the current named account and company scope')

                worker = c.app.state.core.state.accounts.create('fictional.ui104.viewer', 'Fictional UI104 ordinary technician', PASS, 'technician', actor)
                p.locator('#menu-button').click()
                p.locator('[data-signout]').click()
                expect(p.locator('#login-form')).to_be_visible()
                p.locator('[name=login_id]').fill('fictional.ui104.viewer')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('state.auth.person.user_id') == worker['id']
                navigate('#inventory/' + combined['id'], '#inv-folder-title')
                assert p.locator('#inv-import-items').count() == 0 and p.locator('#di-target-id').count() == 0
                a = auth()
                denied = c.post('/api/builders/document/scan', json={'kind': 'inventory', 'file': {'name': synthetic.name, 'data': base64.b64encode(synthetic.read_bytes()).decode()}, 'language': 'eng'},
                                headers={'Authorization': 'Bearer ' + a['token'], 'x-aj-hub-id': a['hub']})
                assert denied.status_code == 403, denied.text
                assert len(store.inventory.get(combined['id'], actor)['items']) == 12
                ok('An authenticated ordinary technician sees no append/import destination control and cannot obtain inventory destinations or scan through the protected import API')

                permissions = access.defaults('technician')
                permissions.update({'inventory.view': True, 'inventory.edit': True, 'builders.inventory': True})
                access.save(store, actor, worker['id'], permissions, 0, 'Fictional delegated inventory import acceptance')
                p.locator('#menu-button').click()
                p.locator('[data-signout]').click()
                expect(p.locator('#login-form')).to_be_visible()
                p.locator('[name=login_id]').fill('fictional.ui104.viewer')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('state.auth.person.role') == 'technician'
                delegated_path = Path(td) / 'Fictional_UI104_Delegated.xlsx'
                workbook(delegated_path, serial_suffix='-DELEGATED')
                existing_builder(delegated_path, combined['id'])
                p.locator('#di-select-data').click()
                check()
                delegated = save()
                assert delegated['id'] == combined['id'] and len(delegated['items']) == 16
                assert store.inventory.count(count['id'], actor)['checks'] == before_count['checks']
                ok('A named technician explicitly granted inventory view, edit and builder permissions can append through the same visible UI without becoming an administrator')

                # Missing expected quantity is explicitly Unknown; zero is known.
                unknown_path = Path(td) / 'Fictional_UI104_Unknown.xlsx'
                workbook(unknown_path, quantity_values=(0, '', 'X', 3),
                         serial_values=('TRAIN-SN-104-UNKNOWN-0', 'TRAIN-SN-104-UNKNOWN-1', '', 'TRAIN-SN-104-UNKNOWN-3'),
                         part_values=('TRAIN-PN-104-UNKNOWN-0', 'TRAIN-PN-104-UNKNOWN-1', 'TRAIN-PN-104-UNKNOWN-2', ''))
                builder(unknown_path)
                p.locator('#di-select-data').click()
                malicious_label = '<img src=x onerror=window.ui104Injected=1>'
                p.locator('#di-title').fill('Fictional literal label ' + malicious_label)
                p.locator('[data-di-sheet-location="0"]').fill(malicious_label)
                check()
                unknown_overview = latest('/document/review')['response']['summary']['inventory_review']
                assert unknown_overview['total_items'] == 4
                assert sum(x['unknown_quantities'] for x in unknown_overview['sheets']) == 2
                assert sum(x['serials'] for x in unknown_overview['sheets']) == 3
                assert sum(x['part_numbers'] for x in unknown_overview['sheets']) == 3
                expect(p.locator('#di-review-sheets')).to_contain_text(malicious_label)
                assert p.locator('#di-inventory-review img').count() == 0
                assert not p.evaluate('Boolean(window.ui104Injected)')
                p.locator('#di-review-details').evaluate('node=>node.open=true')
                expect(p.locator('#di-review-details')).to_contain_text('Unknown expected quantities')
                expect(p.locator('#di-review-details')).to_contain_text('Items without a serial number')
                expect(p.locator('#di-review-details')).to_contain_text('Items without a part number')
                screenshot('identity_quantity_review', p.locator('#di-inventory-review'))
                screenshot('unknown_quantity_details', p.locator('#di-review-details'))
                unknown_book = save()
                assert len(unknown_book['items']) == 4 and not unknown_book['counts']
                assert Counter(x['quantity'] for x in unknown_book['items']) == Counter({0: 1, None: 2, 3: 1})
                assert all('Source Qty Counted:' in x['notes'] for x in unknown_book['items'])
                ok('Review distinguishes two Unknown expected quantities from explicit zero and reports missing SN/PN; HTML-like user labels remain literal text, and Excel Counted values create no verification results')

                # Legitimate repeated identifiers are never source-row duplicates.
                repeat_path = Path(td) / 'Fictional_UI104_Repeated_Identifiers.xlsx'
                workbook(repeat_path, serial_values=('TRAIN-SN-104-REPEATED',) * 4,
                         part_values=('TRAIN-PN-104-REPEATED',) * 4)
                repeated_before = copy.deepcopy(store.inventory.get(combined['id'], actor))
                existing_builder(repeat_path, combined['id'])
                p.locator('#di-select-data').click()
                check()
                repeat_overview = latest('/document/review')['response']['summary']['inventory_review']
                assert repeat_overview['can_save'] is True and repeat_overview['conflicts']['duplicate_count'] == 0
                assert not repeat_overview['conflicts']['unproven_sheets']
                repeated = save()
                assert len(repeated['items']) == 20
                added = [x for x in repeated['items'] if x['id'] not in {y['id'] for y in repeated_before['items']}]
                assert len(added) == 4 and len({x['id'] for x in added}) == 4
                assert all(x['serial'] == 'TRAIN-SN-104-REPEATED' and x['part_number'] == 'TRAIN-PN-104-REPEATED' for x in added)
                assert {x['id']: x for x in repeated['items'] if x['id'] in {y['id'] for y in repeated_before['items']}} == {x['id']: x for x in repeated_before['items']}
                assert store.inventory.count(count['id'], actor)['checks'] == before_count['checks']
                ok('Four distinct source rows sharing the same serial and part number remain four fresh items; preflight permits them and append preserves all prior stock and verification results')

                assert all(hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() == digest for name, digest in report['source_hashes'].items()), 'Source changed during acceptance; rerun with frozen assets.'
                assert all(digest == report['source_hashes'][name] for name, digest in report['served_asset_hashes'].items())
                assert not report['errors'], report['errors']
                ok('All served tracked assets match the frozen source and Chromium reports no unexpected JavaScript errors')
            except Exception:
                p.screenshot(path=str(OUT / 'failure.png'), full_page=True)
                print(json.dumps({'errors': report['errors'], 'recent_api': [{'path': x['path'], 'status': x['status'], 'error': (x['response'] or {}).get('error') if isinstance(x['response'], dict) else None} for x in exchanges[-6:]]}))
                raise
            finally:
                report['summary'] = {'checks_passed': len(report['checks']), 'unexpected_errors': len(report['errors']), 'widths': report['widths']}
                (OUT / 'UI104_IMPORT_INVENTORY_BROWSER_REVIEW.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
