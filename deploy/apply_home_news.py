"""Move news into the main Home column of the verified news release."""
from graphlib import TopologicalSorter
from hashlib import sha256
import json
from pathlib import Path
import re
import runpy
import sys

PARENT = "cb890dc6566d7243b1c44480f748903e1e996876348b2d6e9c3f362521e13993"
SOURCE = Path(__file__).with_name("home_news_ui.py")
STATIC = "app/static/"
REFERENCE = re.compile(r'(/static/([^?"\s]+)\?v=[\d.]+-)[0-9a-f]{12}')


def apply(root):
    receipt = root / "RELEASE_FILES.json"
    original = receipt.read_bytes()
    if sha256(original).hexdigest() != PARENT:
        raise ValueError("Unexpected release before Home news layout")
    manifest = json.loads(original)
    files = manifest["files"]
    changes = {}
    hashes = {}

    def edit(path, transform):
        data = changes.get(path)
        if data is None:
            data = (root / path).read_bytes()
            if sha256(data).hexdigest() != files[path]:
                raise ValueError("Unexpected resource: " + path)
        updated = transform(data.decode("utf-8")).encode("utf-8")
        if updated == data:
            return False
        changes[path] = updated
        if path.startswith(STATIC):
            hashes[path[len(STATIC):]] = sha256(updated).hexdigest()[:12]
        return True

    for path, transform in runpy.run_path(str(SOURCE))["transforms"]().items():
        if not edit(path, transform):
            raise ValueError("Home news layout did not change " + path)

    def refs(source):
        return REFERENCE.sub(lambda m: m[1] + hashes[m[2]] if m[2] in hashes else m[0], source)

    worker = STATIC + "sw.js"
    dependencies = {}
    for path in files:
        if path.startswith(STATIC) and path.endswith((".html", ".js", ".css")) and path != worker:
            data = changes[path] if path in changes else (root / path).read_bytes()
            dependencies[path[len(STATIC):]] = {m[2] for m in REFERENCE.finditer(data.decode("utf-8"))}
    for asset in TopologicalSorter(dependencies).static_order():
        if dependencies.get(asset, set()).intersection(hashes):
            edit(STATIC + asset, refs)

    def worker_version(source):
        previous = "ui162-20261122-feed-news"
        if source.count(previous) != 1:
            raise ValueError("Unexpected service worker cache")
        return refs(source).replace(previous, "ui162-20261122-home-news")

    edit(worker, worker_version)
    variant = manifest["variant"] + "-home-news"

    def metadata(source):
        info = json.loads(source)
        info.update(patch_id=variant, parent_patch_id=manifest["variant"], parent_manifest_sha256=PARENT,
                    scope="Display company and location news in the main Home column.")
        return json.dumps(info, indent=2) + "\n"

    edit("UI_PATCH.json", metadata)
    for path, data in changes.items():
        (root / path).write_bytes(data)
        files[path] = sha256(data).hexdigest()
    manifest["variant"] = variant
    result = (json.dumps(manifest, indent=2) + "\n").encode()
    receipt.write_bytes(result)
    print(variant, sha256(result).hexdigest())


if __name__ == "__main__":
    apply(Path(sys.argv[1]))
