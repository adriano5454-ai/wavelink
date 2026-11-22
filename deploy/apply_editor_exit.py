"""Apply editor exit handling and opt-in birthdays to the verified Home release."""
from graphlib import TopologicalSorter
from hashlib import sha256
import json
from pathlib import Path
import re
import runpy
import sys

BASE = Path(__file__).resolve().parent
PARENT = "2c980eea0a90cff970bd0f92678a45d3a9075f2c4c6179a0061b0b3313096013"
OVERLAYS = ("editor_exit_news.py", "editor_exit_navigation.py",
            "editor_exit_birthdays.py", "editor_exit_birthday_ui.py")
STATIC = "app/static/"
VERSIONED_ASSET = re.compile(r'(/static/([^?"\s]+)\?v=[\d.]+-)[0-9a-f]{12}')
PREVIOUS_CACHE = "ui162-20261122-home-news"
CACHE = "ui162-20261122-editor-exit"


def apply(root):
    receipt = root / "RELEASE_FILES.json"
    raw = receipt.read_bytes()
    if sha256(raw).hexdigest() != PARENT:
        raise ValueError("Unexpected release before editor exits")
    manifest = json.loads(raw)
    files = manifest["files"]
    changes = {}
    additions = []
    static_hashes = {}

    def record(name, data):
        changes[name] = data
        if name.startswith(STATIC):
            static_hashes[name[len(STATIC):]] = sha256(data).hexdigest()[:12]

    def edit(name, transform):
        before = changes.get(name)
        if before is None:
            before = (root / name).read_bytes()
            if sha256(before).hexdigest() != files[name]:
                raise ValueError("Unexpected resource: " + name)
        after = transform(before.decode("utf-8")).encode("utf-8")
        if before == after:
            return False
        record(name, after)
        return True

    for overlay in OVERLAYS:
        patch = runpy.run_path(str(BASE / overlay))
        for name, content in patch.get("additions", dict)().items():
            if name in files or name in changes or (root / name).exists():
                raise ValueError("New resource already exists: " + name)
            record(name, content.encode("utf-8") if isinstance(content, str) else content)
            additions.append(name)
        for name, transform in patch["transforms"]().items():
            if not edit(name, transform):
                raise ValueError(f"{overlay} did not change {name}")

    def refs(source):
        return VERSIONED_ASSET.sub(
            lambda match: match[1] + static_hashes[match[2]] if match[2] in static_hashes else match[0], source)

    # Help pages and scripts can reference other versioned HTML resources.
    # Resolve their dependencies before stamping referring pages and the shell.
    dependencies = {}
    for path in (*files, *additions):
        if path.startswith(STATIC) and path.endswith((".html", ".js", ".css")) and path != STATIC + "sw.js":
            data = changes[path] if path in changes else (root / path).read_bytes()
            dependencies[path[len(STATIC):]] = {m[2] for m in VERSIONED_ASSET.finditer(data.decode("utf-8"))}
    for asset in TopologicalSorter(dependencies).static_order():
        if dependencies.get(asset, set()).intersection(static_hashes):
            edit(STATIC + asset, refs)

    def worker(source):
        marker = "const ASSETS=["
        if source.count(PREVIOUS_CACHE) != 1 or source.count(marker) != 1:
            raise ValueError("Unexpected service worker")
        urls = []
        for name in additions:
            if name.startswith(STATIC) and name.endswith((".js", ".css")):
                asset = name[len(STATIC):]
                if f'"/static/{asset}?' not in source:
                    urls.append(json.dumps(f"/static/{asset}?v=1.34.61-{static_hashes[asset]}") + ",")
        return refs(source).replace(PREVIOUS_CACHE, CACHE).replace(marker, marker + "".join(urls))

    edit(STATIC + "sw.js", worker)
    variant = manifest["variant"] + "-editor-exit"

    def metadata(source):
        info = json.loads(source)
        info.update(patch_id=variant, parent_patch_id=manifest["variant"], parent_manifest_sha256=PARENT,
                    scope="Preserve unfinished edits on navigation and show opt-in birthdays on Home and Team.")
        return json.dumps(info, indent=2) + "\n"

    edit("UI_PATCH.json", metadata)
    for name, data in changes.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        files[name] = sha256(data).hexdigest()
    manifest["variant"] = variant
    result = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    receipt.write_bytes(result)
    print(variant, sha256(result).hexdigest())


if __name__ == "__main__":
    apply(Path(sys.argv[1]))
