"""Present public Inventory recovery after a confirmed native demo session expires."""
from pathlib import Path
import runpy
import sys


def script(source):
    def replace(old, new):
        nonlocal source
        if source.count(old) != 1:
            raise ValueError('Unexpected Inventory recovery anchor: ' + old)
        source = source.replace(old, new)

    # The hint is tied to the current in-memory visit. Nothing is stored.
    marker = "                if(resp.status===401&&state.auth){state.auth=null;"
    replace(marker, """                if (resp.status === 401 && state.auth) {
                    expiredInventoryVisit = WavelinkNativeDemo.active() ? browserWorkspace.id() : null;
                }
""" + marker)
    entry = 'function loginView(){'
    replace(entry, r"""let expiredInventoryVisit = null;
function isPublicInventoryRoute() {
    const query = new URLSearchParams(location.search);
    return query.get('public_demo') === '1' && query.get('browser_workspace') === browserWorkspace.id() &&
        /^#inventory(?:\/|$)/.test(location.hash);
}
function loginView(){
    if (!state.auth && expiredInventoryVisit && expiredInventoryVisit === browserWorkspace.id() && isPublicInventoryRoute()) {
        // Connection updates can render again. Keep the focused link mounted.
        if (root.querySelector('#reopen-inventory-demo')) return;
        const text = window.WavelinkUX.text;
        root.innerHTML = '<section class="card" aria-labelledby="demo-visit-title"><h1 id="demo-visit-title" tabindex="-1"></h1>' +
            '<p id="demo-visit-explanation"></p><a class="btn primary" id="reopen-inventory-demo" href="/__demo/public?area=inventory"></a></section>';
        const heading = root.querySelector('#demo-visit-title');
        heading.textContent = text('Sua visita à demo terminou', 'Your demo visit has ended');
        root.querySelector('#demo-visit-explanation').textContent = text(
            'Abra uma nova visita para consultar o Inventário.', 'Start a new visit to view Inventory.');
        root.querySelector('#reopen-inventory-demo').textContent = text('Reabrir a demo do Inventário', 'Reopen Inventory demo');
        heading.focus();
        return;
    }""")
    return source


def transforms():
    return {'app/static/app.js': script}


if __name__ == '__main__':
    build = Path(__file__).resolve()
    apply = runpy.run_path(str(build.with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]), parent='f40c6258c78c54e751e5841eadb7d5e7ae512c106f48f37626c754ed43f4c375',
          overlays=(build.name,), cache=None, suffix='demo-inventory-expiry',
          scope='Reopen public Inventory after a visitor session ends.')
