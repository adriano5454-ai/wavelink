"""Put the existing Team check-in on Corcovado's named-account Home."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


# The company deployment and the public demo currently ship different shells.
COMPANY = 'e34d89daa1892bcabc497aa75d43cb4d6df59d084de5462bbd9f95237ec76453'
SHOWCASE = 'c67eac929a0a8f4af935b58d5554a533bb459f19152ad23c26b81c8016aa64f7'
STATIC = 'app/static/'


def once(source, before, after):
    if source.count(before) != 1:
        raise ValueError('Unexpected Home check-in source at ' + before[:70])
    return source.replace(before, after)


def personal_home(source, showcase):
    company = "H.brand?.()?.id==='corcovado'"
    slot = """'<div id="ph-home-moods"></div>':''"""
    if showcase:
        return once(source, """window.WavelinkNativeDemo?.active()?'<div id="ph-demo-moods"></div>':''""",
                    '(' + company + ' || window.WavelinkNativeDemo?.active())?' + slot)
    return once(source, '${shortcuts()}<div id="ph-local">',
                '${shortcuts()}${' + company + '?' + slot + '}<div id="ph-local">')


def recognition(source, showcase):
    if showcase:
        source = once(source, "#ph-demo-moods", "#ph-home-moods")
        source = once(source, 'location.hash!==teamMoodPanel.route', "(location.hash||'#home')!==teamMoodPanel.route")
        source = once(source, 'const route=location.hash;', "const route=location.hash||'#home';")
        source = once(source, 'location.hash===route && panel.isConnected', "(location.hash||'#home')===route && panel.isConnected")
    else:
        source = once(source, "next!==owner || location.hash!=='#team'", "next!==owner || (location.hash||'#home')!==teamMoodPanel.route")
        source = once(source, 'function mountTeamMoods(content,ticket,session){',
                      "function mountTeamMoods(content,ticket,session){\n  const route=location.hash||'#home';")
        source = once(source, "location.hash==='#team' && panel.isConnected", "(location.hash||'#home')===route && panel.isConnected")
        source = once(source, 'teamMoodPanel={dispose,keepOpen:', 'teamMoodPanel={route,dispose,keepOpen:')
        mount = '  const ticket=++homeEpoch,session=owner;'
        source = once(source, mount, mount + """
  const moods=home.querySelector('#ph-home-moods');
  if(moods && !moods.firstElementChild){
   moods.innerHTML=moodPanel();
   mountTeamMoods(moods,epoch,session)();
  }""")
    # A member can change screens while a save is in flight. Refresh the new
    # panel only for the same signed-in member, after the server confirms it.
    source = once(source, 'teamMoodPanel={route,dispose,keepOpen:', 'teamMoodPanel={route,dispose,refresh,keepOpen:')
    newline = '\r\n' if 'return;\r\n    render(data);' in source else '\n'
    source = once(source, '    if(!active() || request!==sequence) return;' + newline + '    render(data);',
                  """    if(!active() || request!==sequence){
     if(session===owner && session===H.session()) teamMoodPanel?.refresh();
     return;
    }
    render(data);""".replace('\n', newline))
    return source


def apply(root):
    release = root / 'RELEASE_FILES.json'
    raw = release.read_bytes()
    parent = sha256(raw).hexdigest()
    if parent not in (COMPANY, SHOWCASE):
        raise ValueError('Unknown parent for the Corcovado Home check-in.')
    manifest = json.loads(raw)
    outputs = {}

    def original(path):
        data = (root / path).read_bytes()
        if sha256(data).hexdigest() != manifest['files'][path]:
            raise ValueError('Unexpected resource: ' + path)
        return data.decode('utf-8')

    keys = {}
    for name, edit in [('personal_home.js', personal_home), ('recognition_workspace.js', recognition)]:
        path = STATIC + name
        data = edit(original(path), parent == SHOWCASE).encode()
        outputs[path] = data
        keys[name] = sha256(data).hexdigest()[:12]
    for name in ('index.html', 'pt-BR/index.html', 'sw.js'):
        path = STATIC + name
        source = original(path)
        for asset, key in keys.items():
            pattern = r'(' + re.escape('/static/' + asset + '?v=') + r'1\.34\.\d+-)[0-9a-f]{12}'
            source, count = re.subn(pattern, lambda match: match[1] + key, source)
            if count != 1:
                raise ValueError('Unexpected cache reference to ' + asset + ' in ' + name)
        if name == 'sw.js':
            source, count = re.subn(r"^(const CACHE='[^']+)';", r"\1-corcovado-mood';", source, flags=re.M)
            if count != 1:
                raise ValueError('Unexpected service worker cache.')
        outputs[path] = source.encode()
    variant = manifest['variant'] + '-corcovado-home-mood'
    patch = json.loads(original('UI_PATCH.json'))
    patch.update(patch_id=variant, parent_patch_id=manifest['variant'], parent_manifest_sha256=parent,
                 scope='Show the existing optional Team mood check-in on Corcovado Home.')
    outputs['UI_PATCH.json'] = (json.dumps(patch, indent=2) + '\n').encode()
    for path, data in outputs.items():
        (root / path).write_bytes(data)
        manifest['files'][path] = sha256(data).hexdigest()
    manifest['variant'] = variant
    final = (json.dumps(manifest, indent=2) + '\n').encode()
    release.write_bytes(final)
    print(variant, sha256(final).hexdigest())


if __name__ == '__main__':
    apply(Path(sys.argv[1]))
