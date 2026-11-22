"""Restore native record layouts and consistent feedback on actionable cards."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
PARENT = '693ee15c8ebc86c5202fb79699044596f03b823bcf357af2fb5e211daa667574'
STATIC = 'app/static/'


def apply(root):
    receipt = root/'RELEASE_FILES.json'
    if sha256(receipt.read_bytes()).hexdigest() != PARENT:
        raise ValueError('Unexpected runtime before card feedback')
    manifest = json.loads(receipt.read_bytes())
    changed = {}

    def edit(path, transform):
        raw = (root/path).read_bytes()
        if sha256(raw).hexdigest() != manifest['files'][path]:
            raise ValueError('Unexpected resource: '+path)
        out = transform(raw.decode('utf-8')).encode('utf-8')
        if out != raw:
            changed[path] = out

    def styles(source):
        start = source.index('/* The same browsing card is used')
        end = source.index(':is(#app, main) .cw-record-name[aria-expanded="true"]', start)
        return source[:start]+source[end:]+'\n'+(BASE/'card_interaction.css').read_text(encoding='utf-8')

    routes = (BASE/'card_routes.js').read_text(encoding='utf-8')
    marker = "/* Forward a record card's empty space to its normal navigation control. */"
    def main_routes(source):
        if source.count(marker) != 1 or not source.rstrip().endswith('})();'):
            raise ValueError('Unexpected card route installer')
        return source[:source.index(marker)]+routes

    edit(STATIC+'ui132_visual.css', styles)
    edit(STATIC+'action_center_ui82.js', main_routes)
    edit(STATIC+'fleet.js', lambda s: s+'\n'+routes)
    hashes = {k[len(STATIC):]: sha256(v).hexdigest()[:12] for k,v in changed.items()}
    pattern = re.compile(r'(/static/('+'|'.join(map(re.escape,hashes))+r')\?v=[\d.]+-)[0-9a-f]{12}')

    def refs(source):
        return pattern.sub(lambda m: m[1]+hashes[m[2]], source)

    for path in manifest['files']:
        if path.startswith(STATIC) and path.endswith('.html'):
            edit(path, refs)
    old_cache = 'ui162-20261122-handover-preview'
    def worker(source):
        if source.count(old_cache) != 1:
            raise ValueError('Unexpected service worker cache')
        return refs(source).replace(old_cache, 'ui162-20261122-card-feedback')
    edit(STATIC+'sw.js', worker)
    variant = manifest['variant']+'-card-feedback'
    info = json.loads((root/'UI_PATCH.json').read_bytes())
    info.update(patch_id=variant, parent_patch_id=manifest['variant'], parent_manifest_sha256=PARENT,
                scope='Task-style interactive states, responsive card layouts and record navigation.')
    changed['UI_PATCH.json'] = (json.dumps(info,indent=2)+'\n').encode()
    for path,raw in changed.items():
        (root/path).write_bytes(raw)
        manifest['files'][path] = sha256(raw).hexdigest()
    manifest['variant'] = variant
    receipt.write_bytes((json.dumps(manifest,indent=2)+'\n').encode())
    print(variant,sha256(receipt.read_bytes()).hexdigest())


if __name__ == '__main__':
    apply(Path(sys.argv[1]))
