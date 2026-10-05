"""Pinned UI98 -> UI99 replay and unchanged hosted/authentication boundaries."""
import hashlib,importlib.util,json,os,shutil
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
BASE=Path(os.environ['WAVELINK_UI98_TEST_SOURCE']);SOURCE=Path(os.environ['WAVELINK_UI99_TEST_SOURCE'])
spec=importlib.util.spec_from_file_location('overlay_ui99',ROOT/'deploy/apply_ui99.py');OVERLAY=importlib.util.module_from_spec(spec);spec.loader.exec_module(OVERLAY)
SHA=lambda b:hashlib.sha256(b).hexdigest()
def identical(p):
 assert (p/'RELEASE_FILES.json').read_bytes()==(SOURCE/'RELEASE_FILES.json').read_bytes()
 for n,d in json.loads((SOURCE/'RELEASE_FILES.json').read_text())['files'].items():assert SHA((p/n).read_bytes())==d,n
def test_exact_replay_and_second_apply_rejected(tmp_path):
 p=tmp_path/'runtime';shutil.copytree(BASE,p);OVERLAY.apply(p);identical(p)
 with pytest.raises(ValueError,match='exact UI97'):OVERLAY.apply(p)
 identical(p)
@pytest.mark.parametrize('path',['app/static/app.js','app/accounts.py','RELEASE_FILES.json'])
def test_tampered_parent_rejected_before_writes(tmp_path,path):
 p=tmp_path/'runtime';shutil.copytree(BASE,p);(p/path).write_text('tampered');before=(p/'app/static/index.html').read_bytes()
 with pytest.raises(ValueError):OVERLAY.apply(p)
 assert (p/'app/static/index.html').read_bytes()==before;assert not (p/'app/static/browser_workspace.js').exists()
def test_full_cumulative_replay(tmp_path):
 p=tmp_path/'runtime';shutil.copytree(Path(os.environ['WAVELINK_UI92_TEST_SOURCE']),p)
 for n in ['ui93','ui94','ui95','ui96','ui97','ui99']:
  sp=importlib.util.spec_from_file_location(n,ROOT/'deploy'/('apply_'+n+'.py'));m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.apply(p)
 identical(p)
def test_non_browser_runtime_is_identical_to_ui98():
 changed={'app/static/app.js','app/static/index.html','app/static/sw.js','app/static/save_status.js','app/static/save_status_ui.js','UI_PATCH.json'}
 for n in json.loads((BASE/'RELEASE_FILES.json').read_text())['files']:
  if n not in changed:assert (SOURCE/n).read_bytes()==(BASE/n).read_bytes(),n
 for n in ['deploy/company_runtime.py','deploy/nginx_config.py','requirements.lock','deploy/extract_source.py']:
  assert (ROOT/n).read_bytes()==(Path(os.environ['WAVELINK_UI98_REPO'])/n).read_bytes(),n
def test_every_local_transaction_uses_selected_tab_keys():
 s=(SOURCE/'app/static/app.js').read_text()
 assert ".get('main')" not in s and ".get('lease')" not in s and ",'main')" not in s and ",'lease')" not in s
 for n in ['discardLocalBatch','switchProjectWorkspace','commitLocalSignOut']:
  at=s.index('function '+n);part=s[at:s.index('\n}\n',at)];assert 'browserWorkspace.leaseKey()' in part and 'browserWorkspace.stateKey()' in part
 # Account adoption remains the original identity/unsent-work gate.
 def adopt(p):
  t=(p/'app/static/app.js').read_text();return t[t.index('async function adoptAccountLogin('):t.index('function mfaLoginView(')]
 assert adopt(SOURCE)==adopt(BASE)
def test_worker_and_entry_load_matching_tab_modules():
 from bs4 import BeautifulSoup
 html=BeautifulSoup((SOURCE/'app/static/index.html').read_text(),'html.parser');sources=[s['src'] for s in html.select('script[src]')]
 assert sources.index('/static/browser_workspace.js?v=1.34.19-ui99')<sources.index('/static/app.js?v=1.34.19-ui99')
 worker=(SOURCE/'app/static/sw.js').read_text()
 for src in sources:assert src in worker,src
 assert "u.pathname.startsWith('/api/')" in worker
 assert "u.pathname==='/reset-password'" in worker and "u.pathname==='/sign'" in worker
def test_docker_applies_overlay_after_existing_chain_once():
 s=(ROOT/'Dockerfile').read_text();last=-1
 for n in ['ui93','ui94','ui95','ui96','ui97','ui99']:
  term='&& python apply_'+n+'.py /opt/wavelink/app';assert s.count(term)==1;at=s.index(term);assert at>last;last=at
 assert 'apply_ui98.py' not in s
