"""UI108 interrupted Toolbox read/retry in a disposable fictional C01.

Real Chromium, IndexedDB and CompanyAccess/core endpoints. Delayed genuine API
responses reproduce dialog and route races; all captured text is fictional.
Service workers and WebSockets are suppressed. No operational talk is saved.
"""
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
sys.path.insert(0, str(SOURCE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))
from test_company_c01 import PASS, activate, client, instance
from app import access
from app.accounts import Accounts

OUT = Path(os.environ.get('WAVELINK_UI108_TOOLBOX_EVIDENCE_DIR', str(ROOT.parent / 'evidence' / 'browser-toolbox')))
TRACKED = ('app/static/fieldwork.js', 'app/static/toolbox_ui.js', 'app/static/toolbox_form.js',
           'app/static/app.js', 'app/static/browser_workspace.js', 'app/static/experience_shell.js',
           'app/static/index.html', 'app/static/sw.js', 'app/toolbox.py', 'app/fieldwork_common.py')


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
    report = dict(checks=[], errors=[], widths=[1440, 390, 320], screenshots=[],
                  method='Real Chromium, genuine IndexedDB, disposable fictional C01 HostedBoundary/CompanyAccess/core APIs and native SQLite. Genuine Toolbox reads are deliberately delayed to reproduce ownership races.',
                  source_hashes={name: sha(SOURCE / name) for name in TRACKED}, served_asset_hashes={},
                  harness_sha256=sha(Path(__file__)), runtime_manifest_sha256=sha(SOURCE / 'RELEASE_FILES.json'),
                  limitations=['Service-worker registration and WebSockets are suppressed.',
                               'No production, Render, live mail, physical camera, Windows display or worker-upgrade acceptance.',
                               'A newly fictional form is published only inside the disposable test company. No performed talk, acknowledgement or signature is saved.',
                               'API response delays and captured live node identity are test instrumentation, not product behavior.',
                               'One fictional permission table is changed without revoking authentication, then the browser permission snapshot is refreshed from native effective flags, to isolate response/form ordering from sign-out.'])

    def ok(name):
        report['checks'].append(name)
        (OUT / 'PROGRESS.json').write_text(json.dumps(report, indent=2) + '\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui108-toolbox-') as td:
        installation = instance.__wrapped__(Path(td))
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
            delays = {'enabled': False, 'held': [], 'remaining': None}

            def route(r):
                req = r.request
                u = urlsplit(req.url)
                response = c.request(req.method, u.path + ('?' + u.query if u.query else ''), headers=req.headers, content=req.post_data_buffer)
                name = 'app' + u.path
                if name in TRACKED and response.status_code == 200:
                    report['served_asset_hashes'][name] = hashlib.sha256(response.content).hexdigest()
                if u.path.startswith('/api/toolbox'):
                    exchanges.append(dict(path=u.path, method=req.method, status=response.status_code))
                if delays['enabled'] and req.method == 'GET' and u.path == '/api/toolbox':
                    delays['held'].append((r, response))
                    if delays['remaining'] is not None:
                        delays['remaining'] -= 1
                        if delays['remaining'] == 0:
                            delays['enabled'] = False
                    return
                r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

            p.route(origin + '/**', route)

            def release():
                delays['enabled'] = False
                held = delays['held'][:]
                delays['held'].clear()
                assert held
                for r, response in held:
                    r.fulfill(status=response.status_code, body=response.content, headers=dict(response.headers))

            def read_count():
                return sum(x['method'] == 'GET' and x['path'] == '/api/toolbox' for x in exchanges)

            def talk_count():
                with store.connection() as con:
                    return con.execute('SELECT count(*) FROM toolbox_talks').fetchone()[0]

            def home():
                p.evaluate("()=>location.hash='#home'")
                expect(p.locator('.ph-hero')).to_be_visible()
                assert not p.locator('.tb-workspace').count()

            def toolbox():
                p.evaluate("()=>location.hash='#toolbox'")
                expect(p.locator('.tb-workspace')).to_be_visible()

            def screenshot(name, width, selector):
                p.wait_for_function('()=>!document.querySelector("#toast")?.classList.contains("visible")')
                p.locator(selector).evaluate('n=>n.scrollIntoView({block:"start"})')
                assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), (name, width)
                controls = p.locator(selector + ' input:visible,' + selector + ' button:visible,' + selector + ' textarea:visible,' + selector + ' select:visible').evaluate_all('(ns)=>ns.map(n=>{const b=n.getBoundingClientRect();return {id:n.id,left:b.left,right:b.right};})')
                assert not [x for x in controls if x['left'] < -1 or x['right'] > width + 1], (name, width, controls)
                filename = name + '_' + str(width) + '.png'
                p.screenshot(path=str(OUT / filename))
                report['screenshots'].append(filename)
                ok(name.replace('_', ' ') + ' fits ' + str(width) + 'px without page overflow or clipped controls')

            try:
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('admin')
                p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('.ph-hero')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
                token = p.evaluate('state.auth.token')
                native = c.post('/api/toolbox/action', headers={'Authorization': 'Bearer ' + token, 'X-AJ-Hub-ID': p.evaluate('state.hub_id')}, json={
                    'action': 'save_template', 'op_id': str(uuid.uuid4()), 'payload': {
                        'definition': {'name': 'Fictional UI108 read test briefing', 'code': 'FICT-108',
                                       'description': 'Disposable fictional read acceptance only.',
                                       'prompts': [{'group': 'Discussion', 'text': 'Discuss fictional energy isolation.'}],
                                       'questions': [{'text': 'Can you identify the fictional isolation point?'}],
                                       'declaration': 'I understand this fictional briefing.',
                                       'supervisor_instruction': 'Ask the fictional question.'},
                        'publish': True, 'reviewed': True}})
                assert native.status_code == 200, native.text
                template_id = native.json()['id']
                admin_actor = store.session(token)
                assert talk_count() == 0
                ok('A newly fictional published template exists only in the disposable native company; no talk, acknowledgement or signature is performed')

                for width in report['widths']:
                    p.set_viewport_size({'width': width, 'height': 1000})
                    home()
                    delays['enabled'] = True
                    delays['remaining'] = None
                    toolbox()
                    p.wait_for_function('()=>document.querySelector("#tb-read-state")?.textContent.includes("Loading")')
                    assert p.locator('#fw-retry').is_disabled()
                    p.evaluate('()=>window.ui108ToolboxHost=root.firstElementChild')
                    assert p.locator('#app h1').inner_text() == 'Toolbox Talks'
                    ok('First read mounts an honest Toolbox loading shell with disabled retry at ' + str(width) + 'px')
                    p.locator('#wl-action-trigger').click()
                    expect(p.locator('#wl-action-dialog[open]')).to_be_visible()
                    p.evaluate('()=>window.ui108ActionDialog=document.querySelector("#wl-action-dialog")')
                    release()
                    expect(p.locator('#tb-read-state')).to_contain_text('Retry loading')
                    expect(p.locator('#fw-retry')).to_be_enabled()
                    assert p.evaluate('ui108ToolboxHost===root.firstElementChild&&ui108ActionDialog===document.querySelector("#wl-action-dialog")&&ui108ActionDialog.open')
                    assert not p.locator('#tb-new').count()
                    ok('My actions interrupts the first read without replacing its open dialog or Toolbox host, and exposes an honest fresh-retry control at ' + str(width) + 'px')
                    before_reads = read_count()
                    p.locator('#fw-retry').evaluate('n=>n.click()')
                    p.wait_for_timeout(100)
                    assert read_count() == before_reads
                    assert p.evaluate('ui108ActionDialog.open&&ui108ToolboxHost===root.firstElementChild')
                    ok('Forced retry while My actions remains open sends no read and keeps the current dialog at ' + str(width) + 'px')
                    p.keyboard.press('Escape')
                    expect(p.locator('#wl-action-dialog')).not_to_be_visible()
                    screenshot('interrupted_toolbox_retry', width, '.tb-workspace')
                    p.locator('#fw-retry').click()
                    expect(p.locator('#fw-refresh')).to_be_visible()
                    expect(p.locator('#tb-new')).to_be_visible()
                    assert not p.locator('#tb-read-state').count()
                    assert read_count() == before_reads + 1
                    ok('Closing My actions then choosing Retry loading makes one fresh read and opens the genuine saved Toolbox view at ' + str(width) + 'px')
                    screenshot('toolbox_after_fresh_retry', width, '.tb-workspace')

                    p.locator('#tb-new').click()
                    expect(p.locator('[data-tb-template="' + template_id + '"]')).to_be_visible()
                    p.locator('[data-tb-template="' + template_id + '"]').click()
                    expect(p.locator('#fw-form')).to_be_visible()
                    p.locator('#fw-form [name=site]').fill('Fictional unsent location ' + str(width))
                    text = 'Fictional unsent work description ' + str(width)
                    p.locator('#fw-form [name=work_description]').fill(text)
                    p.evaluate('()=>{window.ui108UnsentForm=document.querySelector("#fw-form");window.ui108LoadedHost=root.firstElementChild;}')
                    before_reads = read_count()
                    p.evaluate('()=>AJFieldwork.open()')
                    p.locator('#fw-refresh').evaluate('n=>n.click()')
                    p.wait_for_timeout(100)
                    assert read_count() == before_reads
                    assert p.evaluate('ui108UnsentForm===document.querySelector("#fw-form")&&ui108LoadedHost===root.firstElementChild&&dlg.open')
                    assert p.locator('#fw-form [name=work_description]').input_value() == text
                    assert p.evaluate('ui108UnsentForm.ajToolboxOwner()')
                    assert talk_count() == 0
                    ok('Foreground open and forced Refresh while an edited genuine Toolbox form is unsent send no GET, retain the same form/view/owner/text and create no talk at ' + str(width) + 'px')
                    screenshot('unsent_toolbox_form_preserved', width, '#dialog')
                    p.locator('#fw-keep').click()
                    expect(p.locator('#dialog')).not_to_be_visible()
                    assert p.evaluate('text=>Object.values(state.fieldworkDrafts).some(d=>d.kind==="Toolbox talk"&&d.values.work_description===text)', text)
                    assert talk_count() == 0
                    ok('Keep draft and close preserves the edited unsent Toolbox description locally without creating an operational record at ' + str(width) + 'px')

                    home()
                    delays['enabled'] = True
                    delays['remaining'] = None
                    toolbox()
                    expect(p.locator('#tb-read-state')).to_be_visible()
                    home()
                    p.evaluate('()=>window.ui108HomeHost=root.firstElementChild')
                    release()
                    p.wait_for_timeout(100)
                    assert p.evaluate('location.hash==="#home"&&ui108HomeHost===root.firstElementChild')
                    assert not p.locator('.tb-workspace,#fw-retry').count()
                    ok('A delayed obsolete Toolbox response cannot replace the current Home route or inject a retry after navigation at ' + str(width) + 'px')

                supervisor = Accounts(store).create('fictional.supervisor108', 'Fictional UI108 Supervisor', 'Fictional-supervisor-passphrase-108', 'supervisor', admin_actor)
                p.close()
                p = browser.new_page(viewport={'width': 390, 'height': 1000})
                p.set_default_timeout(30000)
                p.on('pageerror', lambda error: report['errors'].append(str(error)))
                p.on('dialog', lambda dialog: dialog.accept())
                p.add_init_script('class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();')
                p.route(origin + '/**', route)
                p.goto(origin + '/')
                p.locator('[name=login_id]').fill('fictional.supervisor108')
                p.locator('[name=password]').fill('Fictional-supervisor-passphrase-108')
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('.ph-hero')).to_be_visible()
                toolbox()
                expect(p.locator('#fw-refresh')).to_be_visible()
                supervisor_token = p.evaluate('state.auth.token')
                delays['enabled'] = True
                delays['remaining'] = 1
                p.locator('#fw-refresh').click()
                p.locator('#tb-new').click()
                p.locator('[data-tb-template="' + template_id + '"]').click()
                expect(p.locator('#fw-form')).to_be_visible()
                p.locator('#fw-form [name=site]').fill('Fictional retained permission-race site')
                p.locator('#fw-form [name=work_description]').fill('Fictional work retained across access change')
                p.evaluate('()=>{window.ui108PermissionForm=document.querySelector("#fw-form");window.ui108PermissionHost=root.firstElementChild;}')
                flags = access.defaults('supervisor')
                flags.update({'toolbox.view': False, 'toolbox.conduct': False, 'toolbox.acknowledge': False, 'toolbox.export': False})
                with store.connection(True) as con:
                    con.execute('INSERT OR REPLACE INTO account_permissions(user_id,permissions,version,updated_at,updated_by) VALUES(?,?,1,?,?)', (supervisor['id'], json.dumps(flags), '2026-10-10T00:00:00Z', admin_actor['user_id']))
                    effective = access.effective(con, supervisor['id'], 'supervisor')
                p.evaluate('flags=>state.auth.person.permissions=flags', effective)
                release()
                expect(p.locator('#tb-refresh-state')).to_contain_text('interrupted')
                assert p.evaluate('ui108PermissionForm===document.querySelector("#fw-form")&&ui108PermissionHost===root.firstElementChild&&ui108PermissionForm.ajToolboxOwner()&&dlg.open')
                ok('A genuine pending saved-view read followed by an unsent form and refreshed revoked Toolbox permission flags keeps the same form host and owner, checking interruption before denial')
                retained_text = 'Fictional further edits retained after access change'
                p.locator('#fw-form [name=work_description]').fill(retained_text)
                screenshot('permission_race_unsent_form', 390, '#dialog')
                p.locator('#fw-keep').click()
                expect(p.locator('#dialog')).not_to_be_visible()
                assert p.evaluate('text=>Object.values(state.fieldworkDrafts).some(d=>d.kind==="Toolbox talk"&&d.values.work_description===text)', retained_text)
                ok('After the permission-race read, further typed wording still persists through the genuine Keep draft and close handler without creating an operational talk')
                p.evaluate('()=>AJFieldwork.open()')
                expect(p.locator('#app h1')).to_have_text('Toolbox Talks access unavailable')
                assert not p.locator('#tb-new').count()
                forbidden = c.get('/api/toolbox', headers={'Authorization': 'Bearer ' + supervisor_token, 'X-AJ-Hub-ID': p.evaluate('state.hub_id')})
                assert forbidden.status_code == 403, forbidden.text
                screenshot('fresh_toolbox_access_denied', 390, '.tb-workspace')
                assert talk_count() == 0
                ok('A fresh open applies current Toolbox denial and hides saved actions; the native authenticated endpoint also rejects the revoked permission with 403 while the local draft remains')

                assert talk_count() == 0
                assert not report['errors'], report['errors']
                for name, value in report['served_asset_hashes'].items():
                    assert value == report['source_hashes'][name], name
                assert all(sha(SOURCE / name) == value for name, value in report['source_hashes'].items())
                assert sha(SOURCE / 'RELEASE_FILES.json') == report['runtime_manifest_sha256']
                assert sha(Path(__file__)) == report['harness_sha256']
                ok('All served tracked assets match active source pins, no unhandled JavaScript errors occur and no operational Toolbox talk is saved')
                report['passed'] = True
            except Exception:
                report['passed'] = False
                p.screenshot(path=str(OUT / 'FAILURE.png'))
                raise
            finally:
                report['summary'] = dict(checks_passed=len(report['checks']), unexpected_errors=len(report['errors']))
                (OUT / 'UI108_TOOLBOX_BROWSER_RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
                browser.close()
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
