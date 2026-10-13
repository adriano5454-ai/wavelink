"""UI110 browsing acceptance with real Chromium, C01 APIs and fictional SQLite.

Only a disposable company is created. Selecting a summary must issue no write or
acknowledgement; full Task/Work Order screens retain their established behavior.
Service workers and WebSockets are suppressed by this local request bridge.
"""
import hashlib
import json
import os
import sys
import tempfile
import traceback
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
from app.checklist_wizard import new_draft

OUT = Path(os.environ.get('WAVELINK_UI110_EVIDENCE_DIR', str(ROOT.parent / 'evidence/ui110-browser')))
WIDTHS = [1440, 850, 768, 390, 320]
TRACKED = ('app/static/task_workspace.js', 'app/static/maintenance_workspace.js',
           'app/static/operations.js', 'app/static/general_tasks.js',
           'app/static/index.html', 'app/static/sw.js')
TABLES = ('work_tasks', 'task_alerts', 'inventory_items', 'inventory_counts',
          'maintenance_jobs', 'maintenance_routines', 'ops_photo_evidence',
          'fieldwork_audit', 'fieldwork_operations')


def snapshot(store):
    with store.connection() as con:
        return {table: sorted([tuple(row) for row in con.execute('SELECT * FROM ' + table)], key=repr)
                for table in TABLES}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    chrome = Path(os.environ['WAVELINK_CHROMIUM_EXECUTABLE']).resolve()
    report = dict(checks=[], errors=[], widths=WIDTHS, screenshots=[],
                  method='Real Chromium and IndexedDB, actual C01 HostedBoundary/CompanyAccess/core API responses, fictional native SQLite, genuine service-created records.',
                  source_hashes={name: sha(SOURCE / name) for name in TRACKED},
                  served_asset_hashes={}, harness_sha256=sha(Path(__file__)),
                  chromium_executable_sha256=sha(chrome),
                  limitations=['No live deployment, physical-device or real-user acceptance.',
                               'Service-worker registration and WebSockets are suppressed.',
                               'Evidence compares operational tables, not authentication/session refresh tables.'])
    exchanges = []

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')
        print('PASS', name, flush=True)

    try:
        with tempfile.TemporaryDirectory(prefix='fictional-ui110-browsing-') as td:
            installation = instance.__wrapped__(Path(td))
            with client(installation) as c, sync_playwright() as pw:
                activate(c)
                origin = installation[2].external_origin
                store = c.app.state.core.state.store
                browser = pw.chromium.launch(headless=True, executable_path=str(chrome),
                    args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--disable-software-rasterizer'])
                report['chromium_version'] = browser.version
                p = browser.new_page(viewport={'width': 1440, 'height': 1000})
                p.set_default_timeout(20000)
                p.on('pageerror', lambda error: report['errors'].append(str(error)))
                p.on('dialog', lambda dialog: dialog.accept())
                p.add_init_script('class LocalSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=LocalSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();')

                def route(r):
                    req = r.request
                    u = urlsplit(req.url)
                    response = c.request(req.method, u.path + ('?' + u.query if u.query else ''),
                                         headers=req.headers, content=req.post_data_buffer)
                    if u.path.startswith('/static/') and response.status_code == 200:
                        report['served_asset_hashes']['app' + u.path] = hashlib.sha256(response.content).hexdigest()
                    if u.path == '/' and response.status_code == 200:
                        report['served_asset_hashes']['app/static/index.html'] = hashlib.sha256(response.content).hexdigest()
                    if u.path.startswith(('/api/tasks', '/api/maintenance')):
                        exchanges.append(dict(path=u.path, method=req.method, status=response.status_code,
                                              request=json.loads(req.post_data or '{}')))
                    r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

                p.route(origin + '/**', route)

                def navigate(fragment, selector):
                    p.evaluate('(hash)=>{location.hash=hash;render();}', fragment)
                    expect(p.locator(selector)).to_be_visible()

                def unwritten(before, offset, label):
                    assert snapshot(store) == before, label + ': operational SQLite changed'
                    assert not [x for x in exchanges[offset:] if x['method'] != 'GET'], exchanges[offset:]
                    assert not p.locator('dialog[open]').count(), label + ': editor opened'
                    ok(label)

                def fit(name, selector, controls):
                    p.locator(selector).scroll_into_view_if_needed()
                    bounds = p.locator(controls).evaluate_all('(ns)=>ns.filter(n=>n.offsetWidth||n.offsetHeight).map(n=>{const b=n.getBoundingClientRect();return {id:n.id,left:b.left,right:b.right};})')
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name, p.viewport_size, bounds)
                    assert not [b for b in bounds if b['left'] < -1 or b['right'] > p.viewport_size['width'] + 1], (name, p.viewport_size, bounds)
                    filename = name + '_' + str(p.viewport_size['width']) + '.png'
                    p.screenshot(path=str(OUT / filename))
                    report['screenshots'].append(filename)
                    ok(name.replace('_', ' ') + ' fits ' + str(p.viewport_size['width']) + 'px without page overflow or clipped actions')

                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                actor = store.session(p.evaluate('state.auth.token'))

                def run(service, action, payload):
                    return service.run(action, payload, actor, str(uuid.uuid4()))

                draft = new_draft('outline', 'Inspect the fictional display only')
                draft['title'] = 'Fictional UI110 inspection routine'
                routine = run(store.maintenance, 'save_routine', dict(template=draft, publish=True, reviewed=True))
                orders = [run(store.maintenance, 'create_job', dict(routine_id=routine['id'], revision=routine['revision'],
                           name='Fictional UI110 ' + label + ' inspection', reference='TRAINING-110-' + label,
                           asset_name='Fictional unit ' + label, instructions='Saved fictional instructions; record no step while browsing.',
                           due_at='', assignee_ids=[actor['user_id']])) for label in ['ALPHA', 'BRAVO']]
                tasks = [run(store.tasks, 'create_general', dict(kind='general' if i == 0 else 'maintenance',
                         title='Fictional UI110 ' + label + ' assignment', instructions='Inspect <saved> notes & preserve identity.\nBrowsing records no work.',
                         assignee_ids=[actor['user_id']], department_id='', priority='normal', due_at='', confirmed=True,
                         context_link=None if i == 0 else dict(kind='maintenance', id=orders[1]['id'], version=orders[1]['version'])))
                         for i, label in enumerate(['ALPHA', 'BRAVO'])]
                report['fictional_record_ids'] = dict(tasks=[t['id'] for t in tasks], orders=[j['id'] for j in orders])
                before, offset = snapshot(store), len(exchanges)
                navigate('#tasks', '#tw110-list')
                expect(p.locator('#tw110-detail')).to_contain_text('Select a task')
                assert p.locator('[data-task-id]').count() == 2
                p.locator('[data-task-id="' + tasks[0]['id'] + '"]').click()
                expect(p.locator('#tw110-open')).to_be_visible()
                expect(p.locator('#tw110-detail')).to_contain_text(tasks[0]['instructions'])
                assert p.evaluate('location.hash') == '#tasks'
                assert not p.locator('#tw110-detail saved').count()
                p.locator('[data-task-id="' + tasks[1]['id'] + '"]').click()
                expect(p.locator('#tw110-detail h2')).to_have_text(tasks[1]['title'])
                expect(p.locator('#tw110-detail')).to_contain_text(orders[1]['name'])
                unwritten(before, offset, 'Task summaries use genuine authorised GET responses; selection preserves unread alerts, every operational table and the list route')

                p.locator('[name=task-query]').fill('ALPHA')
                expect(p.locator('#tw110-detail')).to_contain_text('Select a task')
                assert p.locator('[data-task-id]:visible').count() == 1
                p.locator('[name=task-query]').fill('')
                unwritten(before, offset, 'Filtering out the selected Task clears its private summary and returns all rows without acknowledgement or writes')
                p.locator('#task-new').click()
                expect(p.locator('#task-choice-grid')).to_be_visible()
                assert set(p.locator('[data-task-choice]').evaluate_all('(ns)=>ns.map(n=>n.dataset.taskChoice)')) == {'general', 'maintenance', 'certificate_review', 'stock_verification'}
                p.keyboard.press('Escape')
                expect(p.locator('#task-choice-grid')).not_to_be_visible()
                unwritten(before, offset, 'The visible four-card Task chooser retains Inventory verification; opening and closing it creates no work')

                for width in WIDTHS:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    if p.locator('#tw110-back').is_visible():
                        p.locator('#tw110-back').click()
                    p.locator('[data-task-id="' + tasks[0]['id'] + '"]').click()
                    expect(p.locator('#tw110-open')).to_be_visible()
                    fit('task_summary', '#tw110-detail', '#tw110-detail button:visible,#tw110-detail a:visible')
                    if width <= 760:
                        expect(p.locator('#tw110-back')).to_be_visible()
                        p.locator('#tw110-back').click()
                        expect(p.locator('[data-task-id="' + tasks[0]['id'] + '"]')).to_be_visible()
                        assert p.locator('[data-task-id="' + tasks[0]['id'] + '"]').evaluate('n=>document.activeElement===n')
                        ok('Task list Back restores the selected row and keyboard focus at ' + str(width) + 'px')
                unwritten(before, offset, 'Task desktop/tablet/mobile summary and Back navigation remain read only')
                p.set_viewport_size({'width': 1440, 'height': 1000})
                p.locator('[data-task-id="' + tasks[0]['id'] + '"]').click()
                expect(p.locator('#tw110-open')).to_be_visible()
                with p.expect_response(lambda response: response.url.split('?', 1)[0].endswith('/api/tasks/action') and response.request.method == 'POST'):
                    p.locator('#tw110-open').click()
                expect(p.locator('.tw47-detail[data-task-record="' + tasks[0]['id'] + '"]')).to_be_visible()
                p.wait_for_function('id=>location.hash==="#tasks/"+id', arg=tasks[0]['id'])
                assert any(x['request'].get('action') == 'ack_alert' and x['request']['payload']['id'] == tasks[0]['id'] for x in exchanges[offset:])
                after = snapshot(store)
                assert after['work_tasks'] == before['work_tasks']
                for table in TABLES:
                    if table not in ('task_alerts', 'fieldwork_operations'):
                        assert after[table] == before[table], table
                with store.connection() as con:
                    assert con.execute('SELECT read_at FROM task_alerts WHERE task_id=? AND user_id=?', (tasks[0]['id'], actor['user_id'])).fetchone()[0]
                    assert not con.execute('SELECT read_at FROM task_alerts WHERE task_id=? AND user_id=?', (tasks[1]['id'], actor['user_id'])).fetchone()[0]
                ok('Explicit Open task enters the established full record and acknowledges only that opened revision; task work, versions, evidence and the other unread Task remain unchanged')

                before, offset = snapshot(store), len(exchanges)
                navigate('#maintenance', '#mw-results')
                p.locator('[data-mw-select="' + orders[0]['id'] + '"]').click()
                expect(p.locator('#mw-selected h2')).to_have_text(orders[0]['name'])
                p.locator('[data-mw-select="' + orders[1]['id'] + '"]').click()
                expect(p.locator('#mw-selected h2')).to_have_text(orders[1]['name'])
                assert p.evaluate('location.hash') == '#maintenance'
                unwritten(before, offset, 'Selecting Maintenance titles changes only the summary; the saved order route, results, evidence and every operational table remain unchanged')
                p.locator('#mw-search').fill('ALPHA')
                expect(p.locator('#mw-selected')).to_contain_text('Choose a work order')
                p.locator('#mw-search').fill('')
                unwritten(before, offset, 'Maintenance search clears a filtered-out order summary without creating or editing an order')

                for width in WIDTHS:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    if p.locator('#mw-list-back').is_visible():
                        p.locator('#mw-list-back').click()
                    p.locator('[data-mw-select="' + orders[0]['id'] + '"]').click()
                    expect(p.locator('#mw-open-order')).to_be_visible()
                    fit('maintenance_summary', '#mw-selected', '#mw-selected button:visible')
                    if width <= 760:
                        expect(p.locator('#mw-list-back')).to_be_visible()
                        p.locator('#mw-list-back').click()
                        expect(p.locator('[data-mw-select="' + orders[0]['id'] + '"]')).to_be_visible()
                        assert p.locator('[data-mw-select="' + orders[0]['id'] + '"]').evaluate('n=>document.activeElement===n')
                        ok('Maintenance Back restores the selected order and keyboard focus at ' + str(width) + 'px')
                unwritten(before, offset, 'Maintenance desktop/tablet/mobile summary and Back navigation remain read only')
                p.set_viewport_size({'width': 1440, 'height': 1000})
                p.locator('[data-mw-open="' + orders[0]['id'] + '"]').click()
                expect(p.locator('#maintenance-workspace.mw-work-order')).to_be_visible()
                expect(p.locator('[data-maint-step]').first).to_be_visible()
                assert p.evaluate('location.hash') == '#maintenance/' + orders[0]['id']
                unwritten(before, offset, 'The direct Continue work button opens the existing exact order and step-entry controls without recording a step or completing maintenance')
                p.locator('#mw-back-orders').click()
                expect(p.locator('#mw-results')).to_be_visible()
                expect(p.locator('#mw-selected h2')).to_have_text(orders[0]['name'])
                p.locator('#mw-open-order').click()
                expect(p.locator('#maintenance-workspace.mw-work-order')).to_be_visible()
                unwritten(before, offset, 'Returning to the register retains selection; the summary Continue work button opens the same order without operational mutations')
                assert not report['errors'], report['errors']
                for name, expected in report['source_hashes'].items():
                    if name == 'app/static/sw.js':
                        continue  # Registration is intentionally suppressed; no worker lifecycle claim.
                    assert report['served_asset_hashes'].get(name) == expected, name
                ok('Loaded tracked scripts and the shell are served byte for byte from the prepared source; no unexpected JavaScript errors')
                report['task_and_maintenance_api_exchanges'] = exchanges
                browser.close()
    except Exception:
        report['failure'] = traceback.format_exc()
        print(report['failure'], flush=True)
        try:
            p.screenshot(path=str(OUT / 'failure.png'), full_page=True)
        except Exception:
            pass
    finally:
        (OUT / 'results.json').write_text(json.dumps(report, indent=2) + '\n')
    if report.get('failure') or report['errors']:
        raise SystemExit(1)
    print(json.dumps(dict(checks_passed=len(report['checks']), unexpected_javascript_errors=0,
                          widths=WIDTHS, evidence=str(OUT)), indent=2))


if __name__ == '__main__':
    main()
