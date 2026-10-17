"""Exact source replay and protocol/data-preservation release checks."""
import ast
import base64
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import types
import zlib
import pytest

ROOT=Path(__file__).resolve().parents[1]
BASE=Path(os.environ['WAVELINK_UI117_TEST_SOURCE'])
TARGET=Path(os.environ['WAVELINK_TEST_SOURCE'])
SHA=lambda b:hashlib.sha256(b).hexdigest()

def overlay():
    spec=importlib.util.spec_from_file_location('ui118',ROOT/'deploy/apply_ui118.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def clone(tmp_path):
    p=tmp_path/'runtime';shutil.copytree(BASE,p,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'));return p

def test_exact_replay_and_second_application_refused(tmp_path):
    p=clone(tmp_path);m=overlay();m.apply(p)
    assert (p/'RELEASE_FILES.json').read_bytes()==(TARGET/'RELEASE_FILES.json').read_bytes()
    for name,digest in json.loads((p/'RELEASE_FILES.json').read_text())['files'].items():
        assert SHA((p/name).read_bytes())==digest
    with pytest.raises(ValueError,match='exact UI117'):m.apply(p)

@pytest.mark.parametrize('name',['app/hr.py','app/accounts.py','app/inventory.py','app/static/app.js'])
def test_modified_parent_refused_before_writes(tmp_path,name):
    p=clone(tmp_path);(p/name).write_text('outside edit')
    before={n:SHA((p/n).read_bytes()) for n in json.loads((p/'RELEASE_FILES.json').read_text())['files']}
    with pytest.raises(ValueError):overlay().apply(p)
    assert before=={n:SHA((p/n).read_bytes()) for n in before}

def test_data_writers_and_account_credentials_are_unchanged():
    for name in ['app/hr.py','app/hr_api.py','app/accounts.py','app/access.py','app/store.py','app/inventory.py','app/document_import.py','app/project_transfer.py','app/membership_policy.py']:
        assert (BASE/name).read_bytes()==(TARGET/name).read_bytes(),name

def test_bootstrap_never_cached_and_new_assets_are_versioned():
    worker=(TARGET/'app/static/sw.js').read_text();html=(TARGET/'app/static/index.html').read_text()
    assert 'shell-1.34.19-ui118' in worker
    assert '/static/workspace-locale.js' not in worker.split('const ASSETS=[')[1].split('];')[0]
    for name in ['i18n_pt_br.js','locale_pt_br.js','app.js','hr_workspace.js']:
        assert '/static/'+name+'?v=1.34.19-ui118' in html
    assert html.index('/static/workspace-locale.js')<html.index('/static/i18n_pt_br.js')<html.index('/static/app.js')

def test_no_artwork_changed_and_all_help_topics_have_variants():
    m=overlay()
    assert not any(Path(n).suffix.lower() in {'.svg','.png','.webp','.jpg','.woff','.woff2'} for n in m.FILES)
    originals=TARGET/'app/static/help_topics';pt=TARGET/'app/static/pt-BR/help_topics'
    assert {p.name for p in originals.glob('*.html')}=={p.name for p in pt.glob('*.html')}


def snapshot_tree(root):
    result = {}
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            result[name] = ('symlink', str(path.readlink()))
        elif path.is_dir():
            result[name] = ('directory',)
        else:
            result[name] = ('file', SHA(path.read_bytes()))
    return result


@pytest.fixture
def small_replay(tmp_path):
    """Exercise the generator's actual replay template without a large clone.

    The existing exact-replay test separately checks the frozen generated script
    against the complete UI117 source. These cases isolate preflight failures.
    """
    tree = ast.parse((ROOT/'deploy/build_ui118_overlay.py').read_text())
    template = next(ast.literal_eval(node.value) for node in ast.walk(tree)
                    if isinstance(node, ast.Assign) and any(
                        isinstance(target, ast.Name) and target.id == 'template'
                        for target in node.targets))
    runtime = tmp_path/'runtime'
    (runtime/'app').mkdir(parents=True)
    (runtime/'retained').mkdir()
    (runtime/'app/changed.txt').write_bytes(b'parent source')
    (runtime/'retained/unchanged.txt').write_bytes(b'retained source')
    parent = {'variant': 'parent', 'files': {
        'app/changed.txt': SHA(b'parent source'),
        'retained/unchanged.txt': SHA(b'retained source')}}
    raw = (json.dumps(parent, indent=2)+'\n').encode()
    (runtime/'RELEASE_FILES.json').write_bytes(raw)
    files = {}
    for name, data in [('app/changed.txt', b'new source'),
                       ('app/new/module.txt', b'new resource')]:
        files[name] = dict(before=parent['files'].get(name), after=SHA(data), bytes=len(data),
                           payload=base64.b64encode(zlib.compress(data)).decode())
    target = dict(parent, variant='target', files=dict(sorted({
        **parent['files'], **{name: record['after'] for name, record in files.items()}}.items())))
    target_raw = (json.dumps(target, indent=2)+'\n').encode()
    script = template.replace('PARENT_VALUE', repr(SHA(raw))).replace(
        'TARGET_VALUE', repr(SHA(target_raw))).replace(
        'VARIANT_VALUE', repr('target')).replace('FILES_VALUE', repr(files))
    module = types.ModuleType('ui118_preflight_fixture')
    exec(compile(script, '<UI118 replay template>', 'exec'), module.__dict__)
    return runtime, module, target_raw


def test_bad_target_digest_is_refused_before_any_write(small_replay):
    runtime, replay, _ = small_replay
    before = snapshot_tree(runtime)
    replay.TARGET_MANIFEST_SHA256 = '0'*64
    with pytest.raises(ValueError, match='manifest composition mismatch'):
        replay.apply(runtime)
    assert snapshot_tree(runtime) == before


def test_symlink_manifest_is_refused_before_any_write(small_replay, tmp_path):
    runtime, replay, _ = small_replay
    manifest = runtime/'RELEASE_FILES.json'
    original = manifest.read_bytes()
    external = tmp_path/'external-manifest.json'
    external.write_bytes(original)
    manifest.unlink()
    manifest.symlink_to(external)
    before = snapshot_tree(runtime)
    with pytest.raises(ValueError, match='manifest.*symlink'):
        replay.apply(runtime)
    assert snapshot_tree(runtime) == before
    assert external.read_bytes() == original


def test_symlink_destination_root_is_refused_before_any_write(small_replay, tmp_path):
    runtime, replay, _ = small_replay
    alias = tmp_path/'linked-runtime'
    alias.symlink_to(runtime, target_is_directory=True)
    before = snapshot_tree(runtime)
    with pytest.raises(ValueError, match='root symlink'):
        replay.apply(alias)
    assert snapshot_tree(runtime) == before
    assert alias.is_symlink()


def test_symlink_ancestor_of_retained_file_is_refused_before_any_write(small_replay, tmp_path):
    runtime, replay, _ = small_replay
    external = tmp_path/'external-retained'
    (runtime/'retained').rename(external)
    (runtime/'retained').symlink_to(external, target_is_directory=True)
    before = snapshot_tree(runtime)
    external_before = snapshot_tree(external)
    with pytest.raises(ValueError, match='Symlink.*retained'):
        replay.apply(runtime)
    assert snapshot_tree(runtime) == before
    assert snapshot_tree(external) == external_before


def test_preflight_template_accepts_an_exact_valid_replay(small_replay):
    runtime, replay, target_raw = small_replay
    replay.apply(runtime)
    assert (runtime/'RELEASE_FILES.json').read_bytes() == target_raw
    assert (runtime/'app/changed.txt').read_bytes() == b'new source'
    assert (runtime/'app/new/module.txt').read_bytes() == b'new resource'
    assert (runtime/'retained/unchanged.txt').read_bytes() == b'retained source'
