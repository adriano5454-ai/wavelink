"""Use the saved checklist inspector and standard record card sizing."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
PARENT = '451802ae4d11c782e8a6b9bb6fe05b16cc12ff68eb8336c4926a00d3c7036a66'
STATIC = 'app/static/'


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f'Unexpected checklist panel source near {old[:70]}')
    return source.replace(old, new)


def checklist_workspace(source):
    old_title = ('class="cw-record-name" data-cw-open="${esc(r.id)}" data-cw-phase="${nextPhase(r)}" '
                 'aria-label="${closed(r)?__wl118.t(\'View finalised checklist\'):__wl118.t(\'Continue checklist\')}: ${esc(reference(r))}"')
    new_title = ('class="cw-record-name" data-cw-select="${esc(r.id)}" aria-controls="checklist-inspector" '
                 'aria-expanded="${prefs.selected===r.id&&prefs.detail}"')
    source = replace_once(source, old_title, new_title)
    context_start = source.index('<p class="cw-record-context small">')
    context_end = source.index('<p class="small cw-totals">', context_start)
    source = source[:context_start] + source[context_end:]
    count_start = source.index('<span class="small">${phases(r).filter(p=>r.phases[p].final).length}')
    count_end = source.index('<div class="cw-card-actions">', count_start)
    source = (source[:count_start] + '${ctx.recordLocal(r.id)?\'<span class="small">\'+panelText("Local work waiting","Alterações locais pendentes")+\'</span>\':\'\'}'
              + source[count_end:])
    source = replace_once(source, '<button type="button" class="btn ghost" data-cw-select="${esc(r.id)}" aria-controls="checklist-inspector" aria-expanded="${prefs.selected===r.id&&prefs.detail}">Summary</button>', '')
    source = replace_once(source, "session = now; prefs = initial();", "session = now; prefs = initial(); savedChecks = null;")
    source = replace_once(source, "button.disabled=true;\n        try{await ctx.refresh();}", "button.disabled=true;savedChecks=null;\n        try{await ctx.refresh();}")
    source = replace_once(source, "root.querySelector('#cw-detail-title')?.focus({preventScroll:false});", """const panel = root.querySelector('#checklist-inspector');
      panel.scrollTop = 0;
      root.querySelector('#cw-detail-title')?.focus({preventScroll:true});
      if (matchMedia('(max-width:850px)').matches) panel.scrollIntoView({block:'start'});""")
    start = source.index('    function detail(r) {')
    end = source.index('    function bind() {', start)
    return source[:start] + (BASE / 'checklist_panel.js').read_text('utf-8').rstrip() + '\n' + source[end:]


def maintenance_workspace(source):
    # The register shows equipment, location, due date and progress. The inspector
    # already presents the external reference and the routine revision.
    extra_start = source.index('<small>${E(j.reference || __wl118.t(\'No external reference\'))}')
    extra_end = source.index('<div class="mw-order-meta">', extra_start)
    source = source[:extra_start] + source[extra_end:]
    source = replace_once(source, "card.querySelector('[data-mw-open]')?.click();",
                          "card.querySelector('[data-mw-select]')?.click();")
    source = replace_once(source, "click('mw-back-orders',()=>ctx.navigate('#maintenance'))",
                          "click('mw-back-orders',()=>{prefs.mobileDetail=false;ctx.navigate('#maintenance');})")
    source = replace_once(source, 'class="mw-order-title" data-mw-open="${E(j.id)}"',
                          'class="mw-order-title" data-mw-select="${E(j.id)}" aria-controls="mw-selected" aria-pressed="${j.id===prefs.selected}"')
    return replace_once(source, '<button type="button" class="btn secondary" data-mw-select="${E(j.id)}" aria-controls="mw-selected" aria-pressed="${j.id===prefs.selected}">${E(WLWorkSites.words("Resumo","Summary"))}</button>', '')


def apply(root):
    receipt = root / 'RELEASE_FILES.json'
    if sha256(receipt.read_bytes()).hexdigest() != PARENT:
        raise ValueError('Unexpected release before checklist panel update')
    manifest = json.loads(receipt.read_bytes())
    changed = {}

    def edit(path, transform):
        raw = (root / path).read_bytes()
        if sha256(raw).hexdigest() != manifest['files'][path]:
            raise ValueError('Unexpected resource: ' + path)
        output = transform(raw.decode('utf-8')).encode('utf-8')
        if output != raw:
            changed[path] = output

    edit(STATIC + 'checklist_workspace.js', checklist_workspace)
    edit(STATIC + 'maintenance_workspace.js', maintenance_workspace)
    edit(STATIC + 'action_center_ui82.js', lambda s: replace_once(s,
         "['article[data-cw-card]', ['[data-cw-open]']]", "['article[data-cw-card]', ['[data-cw-select]']]"))
    edit(STATIC + 'app.js', lambda s: replace_once(s,
         "    records:()=>state.records,can:canUse,admin:", """    readSaved: (id, beforeSend) => api('/api/records/'+encodeURIComponent(id), {beforeSend}),
    stageItems: usableItems, statusText: status => labels[status] || __wl118.t('Unknown'),
    records:()=>state.records,can:canUse,admin:"""))
    edit(STATIC + 'ui132_visual.css', lambda s: s + '\n' + (BASE / 'record_card_sizes.css').read_text('utf-8'))
    hashes = {k[len(STATIC):]: sha256(v).hexdigest()[:12] for k, v in changed.items()}
    pattern = re.compile(r'(/static/(' + '|'.join(re.escape(k) for k in hashes) + r')\?v=[\d.]+-)[0-9a-f]{12}')

    def refs(source):
        return pattern.sub(lambda m: m[1] + hashes[m[2]], source)

    for path in manifest['files']:
        if path.startswith(STATIC) and path.endswith('.html'):
            edit(path, refs)
    edit(STATIC + 'sw.js', lambda s: replace_once(refs(s), 'ui162-20261122-work-locations-1', 'ui162-20261122-checklist-panel'))
    variant = manifest['variant'] + '-checklist-panel'
    info = json.loads((root / 'UI_PATCH.json').read_bytes())
    info.update(patch_id=variant, parent_patch_id=manifest['variant'], parent_manifest_sha256=PARENT,
                scope='Checklist item previews and consistent card sizing across workspaces.')
    info['boundaries']['data_schema_changed'] = False
    changed['UI_PATCH.json'] = (json.dumps(info, indent=2) + '\n').encode()
    for name, raw in changed.items():
        (root / name).write_bytes(raw)
        manifest['files'][name] = sha256(raw).hexdigest()
    manifest['variant'] = variant
    receipt.write_bytes((json.dumps(manifest, indent=2) + '\n').encode())
    print(variant, sha256(receipt.read_bytes()).hexdigest())


if __name__ == '__main__':
    apply(Path(sys.argv[1]))
