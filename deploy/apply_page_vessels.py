"""Apply the page-level vessel filters to the verified Inventory release."""
from hashlib import sha256
import json
from pathlib import Path
import re
import runpy
import sys

BASE = Path(__file__).resolve().parent
PARENT = '469a867e5a8f0b42ddf1edaf27abd6700c7d5061f33d36aa91367854ab9ed148'
OVERLAYS = ('page_vessel_common.py', 'page_vessel_work.py', 'page_vessel_reports.py',
            'page_vessel_other.py', 'page_vessel_files.py')
STATIC = 'app/static/'
VERSIONED_ASSET = re.compile(r'(/static/([^?"\s]+)\?v=[\d.]+-)[0-9a-f]{12}')
PREVIOUS_CACHE = 'ui162-20261122-inventory-vessels'
CACHE = 'ui162-20261122-page-vessels'


def apply(root):
    receipt = root / 'RELEASE_FILES.json'
    raw = receipt.read_bytes()
    if sha256(raw).hexdigest() != PARENT:
        raise ValueError('Unexpected runtime before page vessel filters')
    manifest = json.loads(raw)
    changes = {}
    static_hashes = {}

    def edit(name, transform):
        original = (root / name).read_bytes()
        if sha256(original).hexdigest() != manifest['files'][name]:
            raise ValueError('Unexpected resource: ' + name)
        before = changes.get(name, original)
        after = transform(before.decode('utf-8')).encode('utf-8')
        if before == after:
            return False
        changes[name] = after
        if name.startswith(STATIC):
            static_hashes[name[len(STATIC):]] = sha256(after).hexdigest()[:12]
        return True

    for overlay in OVERLAYS:
        for name, transform in runpy.run_path(str(BASE / overlay))['transforms']().items():
            if not edit(name, transform):
                raise ValueError(f'{overlay} did not change {name}')

    def refs(source):
        return VERSIONED_ASSET.sub(
            lambda m: m[1] + static_hashes[m[2]] if m[2] in static_hashes else m[0], source)

    for path in manifest['files']:
        if path.startswith(STATIC) and path.endswith('.html'):
            edit(path, refs)

    def worker(source):
        if source.count(PREVIOUS_CACHE) != 1:
            raise ValueError('Unexpected service worker cache')
        return refs(source).replace(PREVIOUS_CACHE, CACHE)

    edit(STATIC + 'sw.js', worker)
    variant = manifest['variant'] + '-page-vessels'

    def metadata(source):
        info = json.loads(source)
        info.update(patch_id=variant, parent_patch_id=manifest['variant'], parent_manifest_sha256=PARENT,
                    scope='Filter operational register searches by Fleet vessel on each applicable page.')
        return json.dumps(info, indent=2) + '\n'

    edit('UI_PATCH.json', metadata)
    for name, data in changes.items():
        (root / name).write_bytes(data)
        manifest['files'][name] = sha256(data).hexdigest()
    manifest['variant'] = variant
    result = (json.dumps(manifest, indent=2) + '\n').encode()
    receipt.write_bytes(result)
    print(variant, sha256(result).hexdigest())


if __name__ == '__main__':
    apply(Path(sys.argv[1]))
