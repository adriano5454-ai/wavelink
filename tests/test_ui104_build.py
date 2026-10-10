"""Pinned UI104 replay, complete Docker chain and preserved data/auth boundaries."""
from __future__ import annotations
import ast, copy, hashlib, importlib.util, json, os, re, shutil
from pathlib import Path
from urllib.parse import urlsplit

import pytest

ROOT=Path(__file__).resolve().parents[1]
BASE=Path(os.environ['WAVELINK_UI103_TEST_SOURCE'])
SOURCE=Path(os.environ['WAVELINK_UI104_TEST_SOURCE'])
PARENT_SHA='f26d5c2201451c727eb243f362dbb3fef366aec386ecb8f5a5377ff2de40c828'
CHAIN=('ui93','ui94','ui95','ui96','ui97','ui99','ui100','ui101','ui102','ui103','ui104')
SHA=lambda value:hashlib.sha256(value).hexdigest()


def load_overlay(name):
    spec=importlib.util.spec_from_file_location('overlay_'+name,ROOT/'deploy'/('apply_'+name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


OVERLAY=load_overlay('ui104')


def clone_runtime(source,destination):
    shutil.copytree(source,destination,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))


def snapshot(path):
    return {p.relative_to(path).as_posix():SHA(p.read_bytes()) for p in path.rglob('*') if p.is_file()}


def identical(path):
    assert (path/'RELEASE_FILES.json').read_bytes()==(SOURCE/'RELEASE_FILES.json').read_bytes()
    for name,digest in json.loads((SOURCE/'RELEASE_FILES.json').read_text())['files'].items():
        assert SHA((path/name).read_bytes())==digest,name


def test_exact_replay_and_second_apply_rejected(tmp_path):
    path=tmp_path/'runtime';clone_runtime(BASE,path)
    assert SHA((path/'RELEASE_FILES.json').read_bytes())==PARENT_SHA
    OVERLAY.apply(path);identical(path);before=snapshot(path)
    with pytest.raises(ValueError,match='exact UI103'):OVERLAY.apply(path)
    assert snapshot(path)==before


@pytest.mark.parametrize('name',['app/document_import.py','app/accounts.py','RELEASE_FILES.json'])
def test_tampered_parent_rejected_before_any_writes(tmp_path,name):
    path=tmp_path/'runtime';clone_runtime(BASE,path);(path/name).write_text('tampered')
    before=snapshot(path)
    with pytest.raises(ValueError):OVERLAY.apply(path)
    assert snapshot(path)==before


def test_new_resource_collision_rejected_before_any_writes(tmp_path):
    path=tmp_path/'runtime';clone_runtime(BASE,path)
    name=next(name for name,record in OVERLAY.FILES.items() if record['before'] is None)
    collision=path/name;collision.parent.mkdir(parents=True,exist_ok=True);collision.write_bytes(b'existing local resource')
    before=snapshot(path)
    with pytest.raises(ValueError,match='new resource already exists'):OVERLAY.apply(path)
    assert snapshot(path)==before


def test_payload_integrity_failure_rejected_before_any_writes(tmp_path,monkeypatch):
    path=tmp_path/'runtime';clone_runtime(BASE,path);before=snapshot(path)
    records=copy.deepcopy(OVERLAY.FILES)
    name=next(name for name in records if name!='UI_PATCH.json')
    records[name]['after']='0'*64
    monkeypatch.setattr(OVERLAY,'FILES',records)
    with pytest.raises(ValueError,match='payload integrity'):OVERLAY.apply(path)
    assert snapshot(path)==before


def test_full_cumulative_replay(tmp_path):
    path=tmp_path/'runtime';clone_runtime(Path(os.environ['WAVELINK_UI92_TEST_SOURCE']),path)
    for name in CHAIN:load_overlay(name).apply(path)
    identical(path)


def test_provenance_matches_exact_runtime_delta():
    parent=json.loads((BASE/'RELEASE_FILES.json').read_text())
    current=json.loads((SOURCE/'RELEASE_FILES.json').read_text())
    provenance=json.loads((ROOT/'docs/UI104_SOURCE_PROVENANCE.json').read_text())
    assert OVERLAY.PARENT_MANIFEST_SHA256==PARENT_SHA==SHA((BASE/'RELEASE_FILES.json').read_bytes())
    assert provenance['parent_manifest_sha256']==PARENT_SHA
    assert provenance['parent_patch_id']==parent['variant']
    assert provenance['patch_id']==current['variant']==OVERLAY.TARGET_VARIANT
    assert provenance['boundaries']['sql_schema_migration'] is False
    assert provenance['boundaries']['browser_storage_clear'] is False
    assert provenance['boundaries']['database_reset'] is False
    records={record['path']:record for record in provenance['files']}
    delta={name for name,digest in current['files'].items() if name!='UI_PATCH.json' and parent['files'].get(name)!=digest}
    assert set(records)==delta
    assert set(OVERLAY.FILES)==delta|{'UI_PATCH.json'}
    assert set(parent['files'])<=set(current['files'])
    for name,record in records.items():
        assert record['before_sha256']==parent['files'].get(name),name
        assert record['after_sha256']==current['files'][name]==SHA((SOURCE/name).read_bytes()),name
    identical(SOURCE)


def test_auth_mail_tabs_recovery_extractors_and_all_art_preserved():
    preserved=(
        'app/accounts.py','app/email_alerts.py','app/password_recovery.py','app/membership_mail.py',
        'app/company_membership.py','app/account_security.py','app/static/app.js',
        'app/static/browser_workspace.js','app/static/save_status.js','app/static/save_status_ui.js',
        'app/document_extract.py','app/static/log_package_worker.js',
        'app/builder_hub.py','app/verification_tools.py',
    )
    for name in preserved:assert (SOURCE/name).read_bytes()==(BASE/name).read_bytes(),name
    parent=json.loads((BASE/'RELEASE_FILES.json').read_text())['files']
    art=[name for name in parent if name.startswith('app/static/') and Path(name).suffix.lower() in ('.png','.jpg','.jpeg','.webp','.svg','.ico')]
    assert len(art)==72
    for name in art:assert (SOURCE/name).read_bytes()==(BASE/name).read_bytes(),name


def test_sql_schema_definition_resources_preserved():
    parent=json.loads((BASE/'RELEASE_FILES.json').read_text())['files']
    current=json.loads((SOURCE/'RELEASE_FILES.json').read_text())['files']
    ddl=re.compile(rb'\b(?:CREATE\s+(?:TABLE|INDEX)|ALTER\s+TABLE|DROP\s+TABLE)\b',re.I)
    schema_resources=[name for name in parent if name.startswith('app/') and name.endswith('.py') and ddl.search((BASE/name).read_bytes())]
    current_schema_resources=[name for name in current if name.startswith('app/') and name.endswith('.py') and ddl.search((SOURCE/name).read_bytes())]
    assert set(current_schema_resources)==set(schema_resources)
    assert 'app/store.py' in schema_resources and 'app/fieldwork_common.py' in schema_resources
    def definitions(path):
        tree=ast.parse(path.read_text());result=[]
        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)) and any(isinstance(c,ast.Constant) and isinstance(c.value,str) and ddl.search(c.value.encode()) for c in ast.walk(node)):
                result.append(ast.dump(node,include_attributes=False))
        for node in tree.body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TABLES' for t in node.targets):
                result.append(ast.dump(node,include_attributes=False))
        return result
    for name in schema_resources:
        assert definitions(SOURCE/name)==definitions(BASE/name),name


def test_hosted_extractor_dependencies_and_vendored_sources_preserved():
    reference=Path(os.environ['WAVELINK_UI103_REPO'])
    names=['deploy/company_runtime.py','deploy/nginx_config.py','deploy/entrypoint.py','requirements.lock','deploy/extract_source.py']
    names.extend(p.relative_to(reference).as_posix() for p in (reference/'vendor').rglob('*') if p.is_file())
    assert len([name for name in names if re.fullmatch(r'vendor/source\.part[0-9]+',name)])==5
    for name in names:assert (ROOT/name).read_bytes()==(reference/name).read_bytes(),name


def entry_assets(path):
    from bs4 import BeautifulSoup
    html=BeautifulSoup((path/'app/static/index.html').read_text(),'html.parser')
    return [s['src'] for s in html.select('script[src]')]+[s['href'] for s in html.select('link[rel=stylesheet]')]


def test_loaded_changed_assets_and_worker_use_current_versions():
    assets=entry_assets(SOURCE);parent_assets={urlsplit(url).path:url for url in entry_assets(BASE)}
    worker=(SOURCE/'app/static/sw.js').read_text()
    provenance=json.loads((ROOT/'docs/UI104_SOURCE_PROVENANCE.json').read_text())
    changed={record['path'] for record in provenance['files']}
    checked=[]
    for url in assets:
        assert url in worker,url
        route=urlsplit(url).path
        if not route.startswith('/static/'):continue
        resource='app'+route
        if resource in changed and Path(resource).suffix in ('.js','.css'):
            assert url==route+'?v=1.34.19-ui104',url
            checked.append(resource)
        elif route in parent_assets:
            assert url==parent_assets[route],url
    assert 'app/static/document_import.js' in checked
    assert 'app/static/document_import.css' in checked
    assert "const CACHE='pxgeo-dive-check-shell-1.34.19-ui104'" in worker
    assert "u.pathname.startsWith('/api/')" in worker and "u.pathname==='/reset-password'" in worker
    assert '/static/browser_workspace.js?v=1.34.19-ui102' in assets
    assert '/static/log_package_worker.js?v=1.34.19-ui101' in worker


def test_docker_applies_complete_chain_once_in_order():
    docker=(ROOT/'Dockerfile').read_text();last=-1
    for name in CHAIN:
        command='&& python apply_'+name+'.py /opt/wavelink/app'
        assert docker.count(command)==1,name
        at=docker.index(command);assert at>last,name;last=at
    assert 'apply_ui98.py' not in docker
    assert docker.index('python extract_source.py vendor/source_parts.json /opt/wavelink/app')<docker.index('&& python apply_ui93.py /opt/wavelink/app')
    assert docker.index('&& python apply_ui104.py /opt/wavelink/app')<docker.index('&& rm vendor/source.part*')
