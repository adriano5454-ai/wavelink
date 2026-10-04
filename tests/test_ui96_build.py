"""UI96 exact UI95 parent replay and immutable account/import/art boundaries."""
import hashlib,importlib.util,json,os,shutil
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'deploy'/f'apply_{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
OVERLAYS=[module(n) for n in ('ui93','ui94','ui95','ui96')]
BASE=Path(os.environ['WAVELINK_UI95_TEST_SOURCE']);SOURCE=Path(os.environ['WAVELINK_UI96_TEST_SOURCE'])
def identical(p):
    assert (p/'RELEASE_FILES.json').read_bytes()==(SOURCE/'RELEASE_FILES.json').read_bytes()
    for n,d in json.loads((SOURCE/'RELEASE_FILES.json').read_text())['files'].items():assert hashlib.sha256((p/n).read_bytes()).hexdigest()==d,n
def test_exact_ui95_replay_and_double_apply_rejected(tmp_path):
    p=tmp_path/'runtime';shutil.copytree(BASE,p);OVERLAYS[-1].apply(p);identical(p);before=(p/'RELEASE_FILES.json').read_bytes()
    with pytest.raises(ValueError,match='exact UI95'):OVERLAYS[-1].apply(p)
    assert (p/'RELEASE_FILES.json').read_bytes()==before
def test_tampered_parent_rejected_before_writes(tmp_path):
    p=tmp_path/'runtime';shutil.copytree(BASE,p);(p/'app/static/app.js').write_text('tampered');before=(p/'RELEASE_FILES.json').read_bytes()
    with pytest.raises(ValueError,match='parent resource'):OVERLAYS[-1].apply(p)
    assert (p/'RELEASE_FILES.json').read_bytes()==before;assert not (p/'app/static/login_ui96.css').exists()
def test_cumulative_build_preserves_accounts_imports_and_art(tmp_path):
    p=tmp_path/'runtime';shutil.copytree(Path(os.environ['WAVELINK_UI92_TEST_SOURCE']),p)
    for m in OVERLAYS:m.apply(p)
    identical(p)
    for n in ['app/accounts.py','app/account_security.py','app/server.py','app/email_alerts.py','app/document_import.py','app/static/document_import.js','app/static/fieldwork.js','app/static/visual_system_ui94.css','app/static/wavelink-approved-offshore-ui87.webp']:
        assert (p/n).read_bytes()==(BASE/n).read_bytes(),n
    def adopt(p):
        s=(p/'app/static/app.js').read_text();return s[s.index('async function adoptAccountLogin('):s.index('function mfaLoginView(')]
    assert adopt(p)==adopt(BASE)
def test_docker_applies_each_overlay_once_in_order():
    s=(ROOT/'Dockerfile').read_text();last=s.index('python extract_source.py')
    for n in ('ui93','ui94','ui95','ui96'):
        term='&& python apply_'+n+'.py /opt/wavelink/app';assert s.count(term)==1;at=s.index(term);assert at>last;last=at
    expected={'deploy/extract_source.py': '57550f076fe6474523d77ecb9fc5b119c0a183f0f6a45be3361c61de0c381fc1', 'deploy/apply_ui93.py': 'b864c3ef24a53e23cfd8dd627178968eea0954cb7c126f4049bc639827fa7b71', 'deploy/apply_ui94.py': '8eab555681b14f1ed7ef6e27f0974525cda905cfd342813fce035ea7324e4c0e', 'deploy/apply_ui95.py': '48ac16642fdd1bfcfcfa52f71e1fe6b336ed227739d7ea1f8ab229d3398c7137', 'requirements.lock': '6c510bc4ac5a9d348dc4c029985a6327304e6ee68af0315f433bd6ef4c3642a2'}
    for n,d in expected.items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==d,n
