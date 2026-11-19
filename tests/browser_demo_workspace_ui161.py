"""Verify the guest handoff with real Chromium and a local fictional fixture.

Run from the release checkout after materializing the application runtime:
python tests/browser_demo_workspace_ui161.py <runtime>/app/static/browser_workspace.js
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from deploy.gate import Gate


ORIGIN = 'https://guest-fixture.invalid'
GUEST = {
    'token': 'fixture-session', 'hub_id': 'training',
    'person': {'user_id': 'fixture-guest', 'login_id': 'guest', 'role': 'technician',
               'name': 'Guest', 'device_id': 'fictional'},
}
STAFF_AUTH = {'token': 'fixture-staff', 'person': {'user_id': 'staff'}}
STAFF = {
    'main': {'hub_id': 'training', 'auth': STAFF_AUTH, 'drafts': {'active': 'keep'}},
    'lease': {'owner': 'staff-tab', 'expires': 9999999999999},
    'browser-windows-1': {'version': 1, 'session': {'hub_id': 'training', 'auth': STAFF_AUTH}},
}
HELPERS = """
window.openFixture = () => new Promise((resolve, reject) => {
    const req = indexedDB.open('pxgeo-dive-check-1', 1);
    req.onupgradeneeded = () => req.result.createObjectStore('state');
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
});
window.runFixture = async (mode, perform) => {
    const db = await openFixture();
    try {
        return await new Promise((resolve, reject) => {
            const tx = db.transaction('state', mode);
            let value;
            perform(tx.objectStore('state'), v => { value = v; });
            tx.oncomplete = () => resolve(value);
            tx.onabort = () => reject(tx.error);
        });
    } finally { db.close(); }
};
"""
CLAIM = """
async fork => {
    const db = await openFixture();
    const ws = AJBrowserWorkspace.create({uuid: () => crypto.randomUUID()});
    try { await ws.init(db); } finally { db.close(); }
    if (fork) ws.fork();
    return runFixture('readwrite', (store, result) => {
        const req = store.get(ws.stateKey());
        req.onsuccess = () => ws.claim(store, req.result, () => result(req.result || ws.seed()));
    });
}
"""
READ = """key => runFixture('readonly', (store, done) => {
    const req = store.get(key);
    req.onsuccess = () => done(req.result);
})"""


def run(workspace_module):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        ctx = browser.new_context()
        ctx.add_init_script(script=HELPERS)

        def fixture(route):
            guest_entry = urlsplit(route.request.url).path == '/__demo/public'
            html = Gate.public_bootstrap_page(GUEST) if guest_entry else '<title>Fixture</title>'
            route.fulfill(content_type='text/html', body=html)

        ctx.route('**/*', fixture)
        staff = ctx.new_page()
        staff.goto(ORIGIN + '/fixture')
        staff.evaluate("""data => runFixture('readwrite', store => {
            for (const [key, value] of Object.entries(data)) store.put(value, key);
        })""", STAFF)

        def open_visitor():
            tab = ctx.new_page()
            tab.goto(ORIGIN + '/__demo/public')
            tab.wait_for_url(re.compile(r'browser_workspace=.+&public_demo=1#home$'))
            tab.add_script_tag(content=workspace_module)
            return tab

        first, second = open_visitor(), open_visitor()
        assert first.url != second.url
        for tab in (first, second):
            assert tab.evaluate(CLAIM, False)['auth']['person']['user_id'] == 'fixture-guest'
        assert first.evaluate(CLAIM, True)['auth']['person']['user_id'] == 'fixture-guest'
        for key, value in STAFF.items():
            assert staff.evaluate(READ, key) == value
        browser.close()


if __name__ == '__main__':
    run(Path(sys.argv[1]).read_text(encoding='utf-8'))
