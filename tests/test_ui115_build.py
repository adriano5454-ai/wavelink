"""UI115 must replay from exact UI114 and preserve every unrelated runtime resource."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
BASE = Path(os.environ['WAVELINK_UI114_TEST_SOURCE'])
SOURCE = Path(os.environ['WAVELINK_UI115_TEST_SOURCE'])
PARENT_MANIFEST = 'e15c1fcd284be4224c83199836f27def2af10d44c758ff1118c088005d5e6b7b'
SHA = lambda data: hashlib.sha256(data).hexdigest()
ALLOWED_CHANGED = {
    'UI_PATCH.json',
    'app/static/document_import.js',
    'app/static/document_import.css',
    'app/static/help_catalogue.json',
    'app/static/help_topics/documentimport.html',
    'app/static/help_topics/inventorybuilder.html',
    'app/static/index.html',
    'app/static/sw.js',
    'docs/user/topics/documentimport.html',
    'docs/user/topics/inventorybuilder.html',
    # Retained UI108 harness now supplies native DOM connectivity for its nodes.
    'tests/test_inventory_source_review_ui108.js',
}


def overlay():
    spec = importlib.util.spec_from_file_location('ui115_overlay', ROOT / 'deploy/apply_ui115.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(path):
    return {p.relative_to(path).as_posix(): SHA(p.read_bytes())
            for p in path.rglob('*') if p.is_file()}


def clone(path):
    shutil.copytree(BASE, path, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache'))


def test_exact_overlay_replay_and_refusal_to_apply_twice(tmp_path):
    path = tmp_path / 'runtime'
    clone(path)
    module = overlay()
    assert SHA((path / 'RELEASE_FILES.json').read_bytes()) == PARENT_MANIFEST
    assert module.PARENT_MANIFEST_SHA256 == PARENT_MANIFEST
    module.apply(path)
    target = json.loads((SOURCE / 'RELEASE_FILES.json').read_text())
    assert (path / 'RELEASE_FILES.json').read_bytes() == (SOURCE / 'RELEASE_FILES.json').read_bytes()
    for name, digest in target['files'].items():
        assert SHA((path / name).read_bytes()) == digest, name
    before = snapshot(path)
    with pytest.raises(ValueError, match='exact UI114'):
        module.apply(path)
    assert snapshot(path) == before


@pytest.mark.parametrize('name', [
    'app/static/document_import.js',
    'app/accounts.py',
    'app/membership_mail.py',
    'app/template_schema.py',
    'app/static/operations.js',
    'RELEASE_FILES.json',
])
def test_modified_parent_refused_before_writes(tmp_path, name):
    path = tmp_path / 'runtime'
    clone(path)
    (path / name).write_text('modified parent')
    before = snapshot(path)
    with pytest.raises(ValueError):
        overlay().apply(path)
    assert snapshot(path) == before


@pytest.mark.parametrize('field,value', [
    ('after', '0' * 64),
    ('bytes', 1),
    ('payload', 'Not valid base64!'),
])
def test_bad_overlay_payload_refused_before_writes(tmp_path, field, value):
    path = tmp_path / 'runtime'
    clone(path)
    before = snapshot(path)
    module = overlay()
    module.FILES = copy.deepcopy(module.FILES)
    module.FILES['app/static/document_import.js'][field] = value
    with pytest.raises(ValueError):
        module.apply(path)
    assert snapshot(path) == before


def test_runtime_delta_and_all_unrelated_boundaries_are_preserved():
    parent = json.loads((BASE / 'RELEASE_FILES.json').read_text())
    target = json.loads((SOURCE / 'RELEASE_FILES.json').read_text())
    module = overlay()
    delta = {name for name, digest in target['files'].items()
             if parent['files'].get(name) != digest}
    added = set(target['files']) - set(parent['files'])
    assert len(added) == 1
    node_test = next(iter(added))
    assert re.fullmatch(r'tests/test_inventory_[a-z_]+_ui115\.js', node_test), node_test
    assert delta == ALLOWED_CHANGED | {node_test}
    assert delta == set(module.FILES)
    assert set(parent['files']) <= set(target['files'])
    for name, digest in target['files'].items():
        assert SHA((SOURCE / name).read_bytes()) == digest, name
        if name not in delta:
            assert digest == parent['files'][name], name
            assert (SOURCE / name).read_bytes() == (BASE / name).read_bytes(), name
    # The strict delta allow-list protects all application Python, schemas,
    # authentication/mail, artwork and operational writers, not selected samples.
    assert not any(name.startswith('app/') and name.endswith('.py') for name in delta)
    assert not any(Path(name).suffix.lower() in
                   ('.svg', '.png', '.webp', '.ico', '.jpg', '.jpeg', '.gif') for name in delta)


def test_deployment_assets_and_chain_order_are_complete():
    html = (SOURCE / 'app/static/index.html').read_text()
    worker = (SOURCE / 'app/static/sw.js').read_text()
    for asset in ('document_import.js', 'document_import.css'):
        url = '/static/' + asset + '?v=1.34.19-ui115'
        assert url in html and url in worker
        assert '?v=1.34.19-ui114' not in next(
            line for line in html.splitlines() if '/static/' + asset in line)
    assert "const CACHE='pxgeo-dive-check-shell-1.34.19-ui115'" in worker
    docker = (ROOT / 'Dockerfile').read_text()
    assert docker.count('&& python apply_ui115.py /opt/wavelink/app') == 1
    assert docker.index('&& python apply_ui114.py') < docker.index('&& python apply_ui115.py')
    assert docker.index('&& python apply_ui115.py') < docker.index('&& rm vendor/source.part*')
    assert 'deploy/apply_ui115.py' in next(line for line in docker.splitlines()
                                        if line.startswith('COPY deploy/extract_source.py'))


@pytest.mark.parametrize('collision', ['file', 'symlink'])
def test_new_resource_collision_refused_before_any_writes(tmp_path, collision):
    path = tmp_path / 'runtime'
    clone(path)
    module = overlay()
    name = next(name for name, record in module.FILES.items() if record['before'] is None)
    p = path / name
    p.parent.mkdir(parents=True, exist_ok=True)
    if collision == 'symlink':
        p.symlink_to(path / 'nonexistent-local-resource')
    else:
        p.write_bytes(b'Existing local resource')
    before = snapshot(path)
    with pytest.raises(ValueError, match='new resource already exists'):
        module.apply(path)
    assert snapshot(path) == before
    if collision == 'symlink':
        assert p.is_symlink()
        assert p.readlink() == path / 'nonexistent-local-resource'
