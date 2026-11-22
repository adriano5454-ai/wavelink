"""Install the fleet vessel filter into the verified Inventory runtime."""
from hashlib import sha256
import json
from pathlib import Path
import re
import runpy
import sys

BASE = Path(__file__).resolve().parent
PARENT = '0904f5a3c156bdb7212cf9daa822b5a7f7486513a8a40749352a42cf12586155'
STATIC = 'app/static/'
CACHE = 'ui162-20261122-card-feedback'
VERSIONED_ASSET = re.compile(r'(/static/([^?"\s]+)\?v=[\d.]+-)[0-9a-f]{12}')
OVERLAYS = ('inventory_vessels_patch.py', 'inventory_vessel_data.py',
            'linked_equipment_locations.py', 'linked_equipment_ui.py')


def apply(root):
    receipt = root / 'RELEASE_FILES.json'
    if sha256(receipt.read_bytes()).hexdigest() != PARENT:
        raise ValueError('Unexpected runtime before Inventory vessel filter')
    manifest = json.loads(receipt.read_bytes())
    changed = {}
    asset_digests = {}

    def edit(name, transform):
        original = (root / name).read_bytes()
        if sha256(original).hexdigest() != manifest['files'][name]:
            raise ValueError('Unexpected resource: ' + name)
        result = transform(changed.get(name, original).decode('utf-8')).encode('utf-8')
        if result != original:
            changed[name] = result
            if name.startswith(STATIC):
                asset_digests[name[len(STATIC):]] = sha256(result).hexdigest()[:12]

    for overlay in OVERLAYS:
        patches = runpy.run_path(str(BASE / overlay))['transforms']()
        for name, transform in patches.items():
            previous = changed.get(name)
            edit(name, transform)
            if changed.get(name) == previous:
                raise ValueError(f'{overlay} did not change {name}')

    def references(source):
        def version(match):
            digest = asset_digests.get(match[2])
            return match[1] + digest if digest else match[0]
        return VERSIONED_ASSET.sub(version, source)

    for name in manifest['files']:
        if name.startswith(STATIC) and name.endswith('.html'):
            edit(name, references)

    def worker(source):
        if source.count(CACHE) != 1:
            raise ValueError('Unexpected service worker cache before Inventory vessel filter')
        return references(source).replace(CACHE, 'ui162-20261122-inventory-vessels')

    edit(STATIC + 'sw.js', worker)
    variant = manifest['variant'] + '-inventory-vessels'

    def patch_info(source):
        info = json.loads(source)
        info.update(patch_id=variant, parent_patch_id=manifest['variant'], parent_manifest_sha256=PARENT,
                    scope='Filter Inventory by vessel and suggest the site of linked equipment for work records.')
        return json.dumps(info, indent=2) + '\n'

    edit('UI_PATCH.json', patch_info)
    for name, data in changed.items():
        (root / name).write_bytes(data)
        manifest['files'][name] = sha256(data).hexdigest()
    manifest['variant'] = variant
    receipt.write_bytes((json.dumps(manifest, indent=2) + '\n').encode())
    print(variant, sha256(receipt.read_bytes()).hexdigest())


if __name__ == '__main__':
    apply(Path(sys.argv[1]))
