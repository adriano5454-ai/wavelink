"""Install the public-demo navigation revision on the verified UI162 shell."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


PARENT = '81e795b55642b3cb3c84f901952f860614b273ed3bfe7655081986db6b9f1d40'
VARIANT = 'workspace-ui162-2026-11-19-demo4'
STATIC = 'app/static/'


def replace(source, before, after):
    if source.count(before) != 1:
        raise ValueError('Unexpected UI162 source at ' + before[:76])
    return source.replace(before, after)


def bootstrap(source):
    module = Path(__file__).with_name('demo_workspaces.js').read_text(encoding='utf-8')
    source = replace(source, "    if (!state.publicDemoUserId ||", "    if (person?.fleet_mode === 'vessel_only' || !state.publicDemoUserId ||")
    source = replace(source, 'available.join(\',\')', "available.filter(key => key !== 'hr' && key !== 'it').join(',')")
    source = replace(source, "    return {href: '/__demo/management?'",
                     "    return {destinations: PublicDemoWorkspaces.destinations(available, portuguese),\n            href: '/__demo/management?'")
    source = replace(source, "        const target=(hash.startsWith('#access-requests')",
                     "        const demo = publicDemoManagement();\n        const target = demo && hash.startsWith('#demo/') ? PublicDemoWorkspaces.activeKey(hash) : (hash.startsWith('#access-requests')")
    source = replace(source, "            if(a.dataset.workspace===target)",
                     "            PublicDemoWorkspaces.navLink(a, demo);\n            if(a.dataset.workspace===target)")
    for key in ('hr', 'it'):
        # The UI's final permission pass runs after the sidebar is painted. Only
        # the native destinations need the corresponding company permission.
        selector = f"""'{key}.view_own':'[data-workspace="{key}"]'"""
        native = f"""'{key}.view_own':'[data-workspace="{key}"][href="#{key}"]'"""
        source = replace(source, selector, native)
    marker = "if(AJWorkspaceShell.handles(location.hash)){AJLogs.cleanup();"
    source = replace(source, marker,
                     "if(['#hr','#it'].includes(location.hash)&&publicDemoManagement()){location.replace('#demo/'+location.hash.slice(1));return;}"
                     "if(location.hash.startsWith('#demo/')){const demo=publicDemoManagement();if(demo){AJLogs.cleanup();PublicDemoWorkspaces.open(root,demo);return;}}" + marker)
    # Keep the existing directive prologue and the module available before initial rendering.
    marker = "function publicDemoManagement() {"
    return replace(source, marker, module.rstrip() + '\n\n' + marker)


def workspaces(source):
    source = replace(source, "const priority=['handovers'", "const priority=[...(management ? ['hr','it'] : []),'handovers'")
    source = replace(source, 'const rows=catalogue.available(H.can,p).sort(',
                     'const rows=PublicDemoWorkspaces.directory(catalogue.available(H.can,p),management).sort(')
    source = replace(source, "a=catalogue.actions(r.key,H.can,w),fleet=r.permission==='@fleet',d=short[r.key]||[r.title,r.description]",
                     "a=!r.sample&&catalogue.actions(r.key,H.can,w),fleet=!r.sample&&r.permission==='@fleet',d=(!r.sample&&short[r.key])||[r.title,r.description]")
    return source


def home(source):
    source = replace(source, 'function shortcuts(){', 'function shortcuts(management){')
    source = replace(source, "   return '<nav class=\"ux-workspace-shortcuts\"",
                     "   if (management) items.splice(1,0,['it.view_own','#it','Solicitações de TI','IT requests','Chamados, prioridades e respostas','Tickets, priorities and replies']);\n"
                     "   const sample = item => management?.destinations[item[1].slice(1)];\n"
                     "   return '<nav class=\"ux-workspace-shortcuts\"")
    source = replace(source, "items.filter(i=>H.can(i[0])).map(i=>'<a href=\"'+i[1]+'\">",
                     "items.filter(i=>H.can(i[0])||sample(i)).map(i=>'<a href=\"'+(sample(i)?.href||i[1])+'\">")
    source = replace(source, '${shortcuts()}', '${shortcuts(management)}')
    source = replace(source, "function icon(name){const paths={hr:",
                     "function icon(name){const paths={it:'<rect x=\"3\" y=\"4\" width=\"18\" height=\"12\" rx=\"2\"/><path d=\"M8 21h8M12 16v5\"/>',hr:")
    return source


def apply(root):
    manifest_file = root / 'RELEASE_FILES.json'
    raw = manifest_file.read_bytes()
    if sha256(raw).hexdigest() != PARENT:
        raise ValueError('Expected the released UI162 runtime manifest.')
    manifest = json.loads(raw)
    outputs = {}

    def source(name):
        data = (root / name).read_bytes()
        if sha256(data).hexdigest() != manifest['files'][name]:
            raise ValueError('Modified UI162 resource: ' + name)
        return data.decode('utf-8')

    keys = {}
    for name, edit in [('app.js', bootstrap), ('home_workspace.js', workspaces), ('personal_home.js', home)]:
        data = edit(source(STATIC + name)).encode()
        outputs[STATIC + name] = data
        keys[name] = sha256(data).hexdigest()[:12]
    for name in ('index.html', 'pt-BR/index.html', 'sw.js'):
        text = source(STATIC + name)
        for asset, digest in keys.items():
            pattern = re.escape('/static/' + asset + '?v=1.34.61-') + r'[0-9a-f]{12}'
            text, count = re.subn(pattern, '/static/' + asset + '?v=1.34.61-' + digest, text)
            if count != 1:
                raise ValueError('Unexpected asset references in ' + name + ': ' + asset)
        if name == 'sw.js':
            text = replace(text, 'ui162-20261119', 'ui162-20261119-demo4')
        outputs[STATIC + name] = text.encode()
    patch = json.loads(source('UI_PATCH.json'))
    patch.update(patch_id=VARIANT, parent_patch_id=manifest['variant'], parent_manifest_sha256=PARENT,
                 scope='Expose read-only public demo workspaces in Home, navigation and the workspace directory.')
    outputs['UI_PATCH.json'] = (json.dumps(patch, indent=2) + '\n').encode()
    manifest['variant'] = VARIANT
    for name, data in outputs.items():
        (root / name).write_bytes(data)
        manifest['files'][name] = sha256(data).hexdigest()
    final = (json.dumps(manifest, indent=2) + '\n').encode()
    manifest_file.write_bytes(final)
    print(VARIANT, sha256(final).hexdigest())


if __name__ == '__main__':
    apply(Path(sys.argv[1]))
