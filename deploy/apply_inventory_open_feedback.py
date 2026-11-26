"""Display immediate, account-scoped feedback when opening an inventory.

This optional entry script leaves the existing fieldwork bundle usable offline.
The native loader continues to own the request, permission checks, and result.
"""
from hashlib import sha256
import re


SCRIPT = r"""(() => {
  'use strict';
  const fieldwork = window.AJFieldwork;
  if (!fieldwork) return;

  const open = fieldwork.open;
  let catalogueOwner;
  let viewOwner;
  let pending;

  function authorizedTitle(host, scope, owner, hash) {
    if (catalogueOwner !== owner || host?.dataset.fwRoute !== scope + '|#inventory' ||
        host.dataset.equipmentWorkspace !== 'inventory-catalogue' || host.classList.contains('iw53-stale')) return '';
    for (const row of host.querySelectorAll('a[data-inventory-id]')) {
      if (row.hash === hash) return row.querySelector('h2')?.textContent.trim() || '';
    }
    return '';
  }

  function start(host, context, hash, owner) {
    const catalogue = hash === '#inventory';
    const title = catalogue ? '' : authorizedTitle(host, context, owner, hash);
    const text = (pt, en) => window.WavelinkUX.text(pt, en);
    const restoreFocus = host?.contains(document.activeElement);
    fieldwork.page('<header class="fw-heading" aria-busy="true"><div><h1 id="inventory-open-heading" tabindex="-1"></h1></div></header>' +
      '<p class="muted" id="inventory-open-status" role="status" aria-live="polite" aria-atomic="true"></p>');
    const heading = document.getElementById('inventory-open-heading');
    heading.textContent = title || (catalogue ? text('Inventários', 'Inventories') : text('Inventário', 'Inventory'));
    const status = document.getElementById('inventory-open-status');
    status.textContent = catalogue ? text('Carregando inventários…', 'Loading inventories…') :
      title ? text('Abrindo ' + title + '…', 'Opening ' + title + '…') :
      text('Carregando itens do inventário…', 'Loading inventory items…');
    if (restoreFocus) heading.focus({preventScroll: true});
    return {heading, hash, owner, restoreFocus};
  }

  fieldwork.open = async function(options) {
    const hash = location.hash;
    if (options?.background || !/^#inventory(?:\/[^/?#]+)?$/.test(hash) || hash === '#inventory/count' ||
        !state.auth || !canUse('inventory.view') || document.querySelector('dialog[open]')) return open.call(this, options);

    const root = document.getElementById('app');
    const host = root.firstElementChild;
    const scope = fieldwork.scope();
    const owner = AJInventoryWorkspace.key();
    const sameRoute = host?.dataset.fwRoute === scope + '|' + hash;
    const catalogue = hash === '#inventory';
    const ready = sameRoute && viewOwner === owner &&
      host.dataset.equipmentWorkspace === (catalogue ? 'inventory-catalogue' : 'inventory-record');
    if (ready) return open.call(this, options);

    if (!pending?.heading.isConnected || pending.hash !== hash || pending.owner !== owner) {
      pending = start(host, scope, hash, owner);
    }
    viewOwner = owner;
    if (catalogue) catalogueOwner = owner;
    const entry = pending;
    await open.call(this, options);
    if (pending !== entry || entry.heading.isConnected) return;
    pending = null;
    if (!entry.restoreFocus || document.activeElement !== document.body ||
        location.hash !== hash || AJInventoryWorkspace.key() !== owner) return;
    const target = root.querySelector('#inv-folder-title, .fw-heading h1');
    if (target) {
      target.tabIndex = -1;
      target.focus({preventScroll: true});
    }
  };
})();
"""

ASSET = 'inventory_open_feedback.js'


def additions():
    return {f'app/static/{ASSET}': SCRIPT}


def index(source):
    # Use the existing locale page's script convention and keep its fieldwork URL intact.
    pattern = r'(<script defer(?:="")? src="/static/fieldwork[.]js[?]v=[^"]+"></script>)'
    version = sha256(SCRIPT.encode('utf-8')).hexdigest()[:12]
    tag = f'<script defer src="/static/{ASSET}?v=1.34.61-{version}"></script>'
    updated, count = re.subn(pattern, lambda match: match[0] + '\n' + tag, source)
    if count != 1:
        raise ValueError('Expected one deferred fieldwork entry in the inventory shell')
    return updated


def transforms():
    return {f'app/static/{name}': index for name in ('index.html', 'pt-BR/index.html')}


if __name__ == '__main__':
    import runpy
    import sys
    from pathlib import Path

    build = Path(__file__).resolve()
    apply = runpy.run_path(str(build.with_name('apply_editor_exit.py')))['apply']
    apply(
        Path(sys.argv[1]),
        parent='eb92d8a33d75adb1abf8330519dee011ae2e303473706ba27091c4b31710887d',
        overlays=(build.name,),
        cache=None,
        suffix='inventory-open-feedback',
        scope='Announce the selected inventory while its authorised records load.',
    )
