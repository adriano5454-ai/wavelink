"""Install the public-demo navigation revision on the verified UI162 shell."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


PARENT = '81e795b55642b3cb3c84f901952f860614b273ed3bfe7655081986db6b9f1d40'
VARIANT = 'workspace-ui162-2026-11-19-native-demo'
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
    source = replace(source, marker, module.rstrip() + '\n\n' + marker)
    native = """window.WavelinkNativeDemo = {
    active: () => Boolean(state.publicDemoUserId && state.publicDemoUserId === state.auth?.person?.user_id
                          && state.auth?.token?.startsWith('wlshow.')),
    area: hash => {
        const key = hash.replace(/^#(?:demo\\/)?/, '').split(/[/?]/)[0];
        if (['personnel','schedule','travel','time','expenses','alerts'].includes(key)) return 'hr';
        if (key === 'access') return 'members';
        if (key === 'shipments') return 'fleet';
        return ['hr','it','team','profile','admin','workspaces','calendar','inventory','members','fleet','builders'].includes(key) ? key : 'home';
    }
};
"""
    source = replace(source, marker, native + marker)
    source = replace(source, "        if(saved)state={...state,...saved};", """        if(saved)state={...state,...saved};
        if(state.publicDemoUserId && state.publicDemoUserId===state.auth?.person?.user_id
            && new URLSearchParams(location.search).get('public_demo')==='1' && !WavelinkNativeDemo.active()){
            await releaseTab();
            location.replace('/__demo/public?area='+WavelinkNativeDemo.area(location.hash));return;
        }
        if(WavelinkNativeDemo.active() && location.hash.startsWith('#demo/'))
            history.replaceState(history.state,'','#'+WavelinkNativeDemo.area(location.hash));""")
    source = replace(source, "location.host+'/ws'", "location.host+(WavelinkNativeDemo.active()?'/__demo/native/ws':'/ws')")
    source = replace(source, "if(['#hr','#it'].includes(location.hash)", "if(WavelinkNativeDemo.active()&&location.hash.startsWith('#demo/')){location.replace('#'+WavelinkNativeDemo.area(location.hash));return;}if(['#hr','#it'].includes(location.hash)")
    return source


def workspaces(source):
    source = replace(source, "const priority=['handovers'", "const priority=[...((management||window.WavelinkNativeDemo?.active()) ? ['hr','it'] : []),'handovers'")
    source = replace(source, 'const rows=catalogue.available(H.can,p).sort(',
                     'const rows=PublicDemoWorkspaces.directory(catalogue.available(H.can,p),management).sort(')
    source = replace(source, "a=catalogue.actions(r.key,H.can,w),fleet=r.permission==='@fleet',d=short[r.key]||[r.title,r.description]",
                     "a=!r.sample&&catalogue.actions(r.key,H.can,w),fleet=!r.sample&&r.permission==='@fleet',d=(!r.sample&&short[r.key])||[r.title,r.description]")
    return source


def home(source):
    source = replace(source, 'function shortcuts(){', 'function shortcuts(management){')
    source = replace(source, "   return '<nav class=\"ux-workspace-shortcuts\"",
                     "   if (management || window.WavelinkNativeDemo?.active()) items.splice(1,0,['it.view_own','#it','Solicitações de TI','IT requests','Chamados, prioridades e respostas','Tickets, priorities and replies']);\n"
                     "   const sample = item => management?.destinations[item[1].slice(1)];\n"
                     "   return '<nav class=\"ux-workspace-shortcuts\"")
    source = replace(source, "items.filter(i=>H.can(i[0])).map(i=>'<a href=\"'+i[1]+'\">",
                     "items.filter(i=>H.can(i[0])||sample(i)).map(i=>'<a href=\"'+(sample(i)?.href||i[1])+'\">")
    source = replace(source, '${shortcuts()}', '${shortcuts(management)}')
    source = replace(source, "function icon(name){const paths={hr:",
                     "function icon(name){const paths={it:'<rect x=\"3\" y=\"4\" width=\"18\" height=\"12\" rx=\"2\"/><path d=\"M8 21h8M12 16v5\"/>',hr:")
    source = replace(source, '${shortcuts(management)}<div id="ph-local">',
        """${shortcuts(management)}${window.WavelinkNativeDemo?.active()?'<div id="ph-demo-moods"></div>':''}<div id="ph-local">""")
    source = replace(source, '<div class="ph-hero-actions"><a href="#workspaces"',
        """${window.WavelinkNativeDemo?.active()?'<p>'+E(window.WavelinkUX.text('Visão de gestão · Empresa fictícia · Somente leitura','Demo manager · Fictional company · Read-only records'))+'</p>':''}<div class="ph-hero-actions">${window.WavelinkNativeDemo?.active()?'<a class="btn secondary" href="#admin">'+E(window.WavelinkUX.text('Administração','Administration'))+'</a>':''}<a href="#workspaces" """.rstrip())
    source = replace(source, '<footer class="ph-footer"><a href="#workspaces">',
        """<footer class="ph-footer">${window.WavelinkNativeDemo?.active()?'<a hreflang="'+(location.pathname==='/__demo/native/pt'?'en':'pt-BR')+'" href="'+E((location.pathname==='/__demo/native/pt'?'/':'/__demo/native/pt')+location.search+'#home')+'">'+(location.pathname==='/__demo/native/pt'?'English':'Português')+'</a>':''}<a href="#workspaces">""")
    return source


def recognition(source):
    source = replace(source, "next!==owner || location.hash!=='#team'", "next!==owner || location.hash!==teamMoodPanel.route")
    source = replace(source, "function mountTeamMoods(content,ticket,session){",
                     "function mountTeamMoods(content,ticket,session){\n  const route=location.hash;")
    source = replace(source, "location.hash==='#team' && panel.isConnected", "location.hash===route && panel.isConnected")
    source = replace(source, 'teamMoodPanel={dispose,keepOpen:', 'teamMoodPanel={route,dispose,keepOpen:')
    marker = '  const ticket=++homeEpoch,session=owner;'
    source = replace(source, marker, marker+"""
  const moods=home.querySelector('#ph-demo-moods');
  if(moods && !moods.firstElementChild){
   moods.innerHTML=moodPanel();
   mountTeamMoods(moods,epoch,session)();
  }""")
    marker = "  const editor=panel.querySelector('#wl-mood-editor')"
    source = replace(source, marker, """  if(window.WavelinkNativeDemo?.active()){
   panel.querySelector('#wl-mood-audience').textContent=window.WavelinkUX.text(
     'Experimente uma carinha. Sua escolha fica visível apenas nesta visita.','Try a mood. Your choice is visible only during your own visit.');
  }
""" + marker)
    return source


def fleet_shell(source):
    return replace(source, "frame.src='/fleet?embedded=1'+hash;",
        "frame.src=(window.WavelinkNativeDemo?.active()&&location.pathname==='/__demo/native/pt'?'/__demo/native/pt/fleet':'/fleet')+'?embedded=1'+hash;")


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
    for name, edit in [('app.js', bootstrap), ('home_workspace.js', workspaces), ('personal_home.js', home),
                       ('recognition_workspace.js', recognition), ('workspace_continuity.js', fleet_shell)]:
        data = edit(source(STATIC + name)).encode()
        outputs[STATIC + name] = data
        keys[name] = sha256(data).hexdigest()[:12]
    for name in ('index.html', 'pt-BR/index.html', 'sw.js'):
        text = source(STATIC + name)
        for asset, digest in keys.items():
            pattern = re.escape('/static/' + asset + '?v=') + r'1\.34\.\d+-[0-9a-f]{12}'
            text, count = re.subn(pattern, '/static/' + asset + '?v=1.34.61-' + digest, text)
            if count != 1:
                raise ValueError('Unexpected asset references in ' + name + ': ' + asset)
        if name == 'sw.js':
            text = replace(text, 'ui162-20261119', 'ui162-20261119-native')
        outputs[STATIC + name] = text.encode()
    patch = json.loads(source('UI_PATCH.json'))
    patch.update(patch_id=VARIANT, parent_patch_id=manifest['variant'], parent_manifest_sha256=PARENT,
                 scope='Open the native application, administration and a private daily mood check-in in the fictional public company.')
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
