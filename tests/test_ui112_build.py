"""Inventory review navigation must replay from UI111 without changing operational resources."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = Path(os.environ['WAVELINK_UI111_TEST_SOURCE'])
SOURCE = Path(os.environ['WAVELINK_UI112_TEST_SOURCE'])
SHA = lambda data: hashlib.sha256(data).hexdigest()


def overlay():
    spec = importlib.util.spec_from_file_location('ui112_overlay', ROOT / 'deploy/apply_ui112.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(path):
    return {p.relative_to(path).as_posix(): SHA(p.read_bytes()) for p in path.rglob('*') if p.is_file()}


def clone(path):
    shutil.copytree(BASE, path, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache'))


def test_exact_overlay_replay_and_refusal_to_apply_twice(tmp_path):
    path = tmp_path / 'runtime'
    clone(path)
    module = overlay()
    module.apply(path)
    manifest = json.loads((SOURCE / 'RELEASE_FILES.json').read_text())
    assert (path / 'RELEASE_FILES.json').read_bytes() == (SOURCE / 'RELEASE_FILES.json').read_bytes()
    for name, digest in manifest['files'].items():
        assert SHA((path / name).read_bytes()) == digest, name
    before = snapshot(path)
    with pytest.raises(ValueError, match='exact UI111'):
        module.apply(path)
    assert snapshot(path) == before


@pytest.mark.parametrize('name', ['app/static/document_import.js', 'app/accounts.py', 'RELEASE_FILES.json'])
def test_modified_parent_refused_before_writes(tmp_path, name):
    path = tmp_path / 'runtime'
    clone(path)
    (path / name).write_text('modified parent')
    before = snapshot(path)
    with pytest.raises(ValueError):
        overlay().apply(path)
    assert snapshot(path) == before


def test_bad_overlay_payload_refused_before_writes(tmp_path):
    path = tmp_path / 'runtime'
    clone(path)
    before = snapshot(path)
    module = overlay()
    module.FILES = copy.deepcopy(module.FILES)
    module.FILES['app/static/document_import.js']['after'] = '0' * 64
    with pytest.raises(ValueError, match='payload integrity'):
        module.apply(path)
    assert snapshot(path) == before


def test_runtime_delta_and_deployment_assets_are_complete():
    parent = json.loads((BASE / 'RELEASE_FILES.json').read_text())
    target = json.loads((SOURCE / 'RELEASE_FILES.json').read_text())
    module = overlay()
    delta = {name for name, digest in target['files'].items() if parent['files'].get(name) != digest}
    assert delta == set(module.FILES)
    assert not any(name.startswith('app/') and name.endswith('.py') for name in delta)
    assert not any(Path(name).suffix.lower() in ('.svg', '.png', '.webp', '.ico', '.jpg') for name in delta)
    assert set(parent['files']) <= set(target['files'])
    for name, digest in target['files'].items():
        assert SHA((SOURCE / name).read_bytes()) == digest, name
    html = (SOURCE / 'app/static/index.html').read_text()
    worker = (SOURCE / 'app/static/sw.js').read_text()
    bundle = (SOURCE / 'app/static/work_execution_ui80.css').read_text()
    for asset in ('document_import.js', 'document_import.css'):
        url = '/static/' + asset + '?v=1.34.19-ui112'
        assert url in html and url in worker
    assert "const CACHE='pxgeo-dive-check-shell-1.34.19-ui112'" in worker
    for name in ('task_workspace.js', 'maintenance_workspace.js', 'work_execution_ui80.css', 'operations.js', 'setup_builders.js'):
        assert (SOURCE / 'app/static' / name).read_bytes() == (BASE / 'app/static' / name).read_bytes(), name
    docker = (ROOT / 'Dockerfile').read_text()
    assert docker.count('&& python apply_ui112.py /opt/wavelink/app') == 1
    assert docker.index('&& python apply_ui111.py') < docker.index('&& python apply_ui112.py') < docker.index('&& rm vendor/source.part*')


def test_new_resource_collision_refused_before_any_writes(tmp_path):
    path = tmp_path / 'runtime'
    clone(path)
    module = overlay()
    name = next(name for name, record in module.FILES.items() if record['before'] is None)
    p = path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b'Existing local resource')
    before = snapshot(path)
    with pytest.raises(ValueError, match='new resource already exists'):
        module.apply(path)
    assert snapshot(path) == before
