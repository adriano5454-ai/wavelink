"""Bound the daily check-in list and page the maintenance order browser."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

PARENT = '31e2b6e9b460d7ced603843391e501be643aaef11548d730854c43befab5ccf8'
STATIC = 'app/static/'


def replace(source, old, new, expected=1):
    if source.count(old) != expected:
        raise ValueError('Unexpected crew list source near ' + old[:80])
    return source.replace(old, new)


def moods(source):
    source = replace(source, '<h3>Shared today</h3><ul></ul>',
                     '<div class="wl-mood-roster-heading"><h3 id="wl-mood-shared-title">Shared today '
                     '<span id="wl-mood-total"></span></h3><small id="wl-mood-scroll-hint" hidden></small></div>'
                     '<ul aria-labelledby="wl-mood-shared-title"></ul>')
    source = replace(source, '  const share=editor.querySelector', """  const hint=shared.querySelector('#wl-mood-scroll-hint');
  hint.textContent=window.WavelinkUX.text('Role para ver toda a equipe','Scroll to see everyone');
  function updateOverflow(){
   const overflows=list.scrollHeight>list.clientHeight+1;
   hint.hidden=!overflows;
   list.tabIndex=overflows?0:-1;
  }
  const rosterObserver=typeof ResizeObserver==='function' ? new ResizeObserver(updateOverflow) : null;
  rosterObserver?.observe(list);
  const share=editor.querySelector""")
    source = replace(source, '   controls();\n   clearTimeout(expiryTimer);',
                     '   controls();\n   updateOverflow();\n   clearTimeout(expiryTimer);')
    source = replace(source, '   disposed=true;\n   clearDay();',
                     '   disposed=true;\n   rosterObserver?.disconnect();\n   clearDay();')
    source = replace(source, '   snapshot=data;',
                     '   const previousTop=snapshot?.day===data.day ? list.scrollTop : 0;\n   snapshot=data;')
    return replace(source, '   list.replaceChildren(...people);',
                   """   list.replaceChildren(...people);
   list.scrollTop=previousTop;
   shared.querySelector('#wl-mood-total').textContent=people.length ? '('+people.length+')' : '';""")


MOOD_STYLE = """
/* Keep the roster scrollable while the check-in controls remain in place. */
#wl-mood-shared ul {
 max-height: min(11rem, 34vh);
 overflow-y: auto;
 overscroll-behavior-y: contain;
 scrollbar-gutter: stable;
 align-content: start;
 padding-inline-end: .4rem;
}
#wl-mood-shared ul:focus-visible { outline: 2px solid var(--accent, #087e83); outline-offset: 2px; }
#wl-mood-total { color: var(--muted, #526873); font-weight: 500; font-variant-numeric: tabular-nums; }
.wl-mood-roster-heading { display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: .3rem 1rem; }
.wl-mood-roster-heading small { color: var(--muted, #526873); font-size: .82rem; }
"""


def maintenance(source):
    source = replace(source, "    const initial = () => ({query:", "    const ordersPerPage=10;\n    const initial = () => ({orderPage:0,query:")
    source = replace(source, '<div class="mw-list-detail"><div id="mw-results"',
                     '''<div class="mw-list-detail"><div class="mw-order-browser">
          <nav id="mw-pages" aria-label="${E(window.WavelinkUX.text('Páginas de ordens de serviço','Work order pages'))}" hidden>
            ${button('mw-previous',window.WavelinkUX.text('Anterior','Previous'))}
            <span id="mw-range" role="status"></span>
            ${button('mw-next',window.WavelinkUX.text('Próxima','Next'))}
          </nav><div id="mw-results"''')
    source = replace(source, 'aria-label="Saved work orders"></div><section id="mw-selected"',
                     'aria-label="Saved work orders"></div></div><section id="mw-selected"')
    source = replace(source, 'prefs.scroll=0;drawRows();', 'prefs.orderPage=0;prefs.scroll=0;drawRows();', expected=4)
    source = replace(source, '      guardLinks();drawRows();', """      click('mw-previous',()=>changePage(-1));
      click('mw-next',()=>changePage(1));
      el('mw-results').onclick=event=>{
        const card=event.target.closest('[data-mw-order]');
        if(!card || event.target.closest('button, a, input, select, textarea, label, summary'))return;
        const selection=window.getSelection();
        if(selection && !selection.isCollapsed && card.contains(selection.anchorNode))return;
        card.querySelector('[data-mw-select]')?.click();
      };
      guardLinks();drawRows();""")
    source = replace(source, '    function drawRows() {', """    function changePage(step) {
      prefs.orderPage+=step;
      prefs.scroll=0;
      prefs.selected=null;
      prefs.mobileDetail=false;
      drawRows();
      el('mw-results').querySelector('[data-mw-select]')?.focus({preventScroll:true});
    }
    function drawRows() {""")
    source = replace(source, '      if(lost){prefs.selected=null;prefs.mobileDetail=false;}', """      prefs.orderPage=Math.max(0,Math.min(prefs.orderPage,Math.ceil(rows.length/ordersPerPage)-1));
      const start=prefs.orderPage*ordersPerPage;
      const pageRows=rows.slice(start,start+ordersPerPage);
      el('mw-results').classList.toggle('mw-many-orders',rows.length>ordersPerPage);
      if(prefs.selected && !pageRows.some(j=>j.id===prefs.selected)){prefs.selected=null;prefs.mobileDetail=false;}
      el('mw-pages').hidden=rows.length<=ordersPerPage;
      el('mw-previous').disabled=start===0;
      el('mw-next').disabled=start+pageRows.length>=rows.length;
      el('mw-range').textContent=rows.length ? (start+1)+'–'+(start+pageRows.length)+window.WavelinkUX.text(' de ',' of ')+rows.length : '';""")
    return replace(source, "keyed(el('mw-results'),rows.map(", "keyed(el('mw-results'),pageRows.map(")


ORDER_STYLE = """
#maintenance-workspace .mw-order-browser { min-width: 0; }
#maintenance-workspace #mw-results {
 max-height: 65vh;
 max-height: min(65dvh, 44rem);
 overflow-y: auto;
 scrollbar-gutter: stable;
}
#maintenance-workspace [data-mw-order] { cursor: pointer; }
#maintenance-workspace [data-mw-order]:has(.mw-order-title:focus-visible) {
 outline: 2px solid var(--mw-accent, #087e86);
 outline-offset: -3px;
}
#mw-results.mw-many-orders .mw-order {
 display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: center; gap: .25rem .6rem;
 padding: .75rem .85rem !important;
}
#mw-results.mw-many-orders .mw-order-top,
#mw-results.mw-many-orders .mw-order-title,
#mw-results.mw-many-orders .mw-order > p,
#mw-results.mw-many-orders .mw-order > small { grid-column: 1 / -1; margin: 0; }
#mw-results.mw-many-orders .mw-order-title { min-height: 0; padding: .2rem 0; }
#mw-results.mw-many-orders .mw-order-meta { grid-column: 1; grid-row: 5; display: grid; gap: .2rem; margin: .25rem 0; }
#mw-results.mw-many-orders .mw-open-direct { grid-column: 2; grid-row: 5; min-height: 44px; margin: 0; }
#mw-results.mw-many-orders .mw-followup { grid-row: 6; }
#mw-pages {
 display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;
 gap: .35rem; padding-block-end: .55rem;
}
#mw-pages[hidden] { display: none; }
#mw-pages .btn { min-height: 44px; padding: .4rem .65rem; }
#mw-range { font-size: .875rem; font-variant-numeric: tabular-nums; }
@media (max-width: 850px) {
 #maintenance-workspace.mw-phone-detail .mw-order-browser { display: none; }
}
"""


def apply(root):
    receipt = root / 'RELEASE_FILES.json'
    raw = receipt.read_bytes()
    if sha256(raw).hexdigest() != PARENT:
        raise ValueError('Unexpected release before crew list update')
    manifest = json.loads(raw)
    changed = {}

    def edit(name, transform):
        before = (root / name).read_bytes()
        if sha256(before).hexdigest() != manifest['files'][name]:
            raise ValueError('Unexpected parent resource ' + name)
        after = transform(before.decode().replace('\r\n', '\n'))
        changed[name] = (after.replace('\n', '\r\n') if b'\r\n' in before else after).encode()

    for filename, transform in [('recognition_workspace.js', moods), ('maintenance_workspace.js', maintenance),
                                ('recognition_workspace.css', lambda s: s + MOOD_STYLE),
                                ('work_execution_ui80.css', lambda s: s + ORDER_STYLE)]:
        edit(STATIC + filename, transform)

    hashes = {name[len(STATIC):]: sha256(data).hexdigest()[:12] for name, data in changed.items()}

    def update_refs(source):
        for filename, digest in hashes.items():
            pattern = r'(/static/' + re.escape(filename) + r'\?v=[\d.]+-)[0-9a-f]{12}'
            source, count = re.subn(pattern, lambda m: m[1] + digest, source)
            if count != 1:
                raise ValueError('Unexpected reference count for ' + filename)
        return source

    for page in ('index.html', 'pt-BR/index.html'):
        edit(STATIC + page, update_refs)
    edit(STATIC + 'sw.js', lambda s: replace(update_refs(s), "ui162-20261121-workspace-file-library';",
                                             "ui162-20261122-crew-lists';"))
    variant = manifest['variant'] + '-crew-lists'
    info = json.loads((root / 'UI_PATCH.json').read_bytes())
    info.update(patch_id=variant, parent_patch_id=manifest['variant'], parent_manifest_sha256=PARENT,
                scope='Scrollable daily check-ins and paginated, fully clickable work-order cards.')
    info['boundaries']['data_schema_changed'] = False
    changed['UI_PATCH.json'] = (json.dumps(info, indent=2) + '\n').encode()
    for name, data in changed.items():
        (root / name).write_bytes(data)
        manifest['files'][name] = sha256(data).hexdigest()
    manifest['variant'] = variant
    receipt.write_bytes((json.dumps(manifest, indent=2) + '\n').encode())
    print(variant, sha256(receipt.read_bytes()).hexdigest())


if __name__ == '__main__':
    apply(Path(sys.argv[1]))
