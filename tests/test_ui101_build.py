"""Pinned and cumulative UI101 replay; preserve unrelated app/data boundaries."""
import hashlib,importlib.util,json,os,shutil
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
BASE=Path(os.environ['WAVELINK_UI100_TEST_SOURCE']);SOURCE=Path(os.environ['WAVELINK_UI101_TEST_SOURCE'])
spec=importlib.util.spec_from_file_location('overlay_ui101',ROOT/'deploy/apply_ui101.py');OVERLAY=importlib.util.module_from_spec(spec);spec.loader.exec_module(OVERLAY)
SHA=lambda b:hashlib.sha256(b).hexdigest()
def identical(p):
 assert (p/'RELEASE_FILES.json').read_bytes()==(SOURCE/'RELEASE_FILES.json').read_bytes()
 for n,d in json.loads((SOURCE/'RELEASE_FILES.json').read_text())['files'].items():assert SHA((p/n).read_bytes())==d,n
def test_exact_replay_and_second_apply_rejected(tmp_path):
 p=tmp_path/'runtime';shutil.copytree(BASE,p);OVERLAY.apply(p);identical(p)
 with pytest.raises(ValueError,match='exact UI100'):OVERLAY.apply(p)
 identical(p)
@pytest.mark.parametrize('path',['app/document_import.py','app/accounts.py','RELEASE_FILES.json'])
def test_tampered_parent_rejected_before_writes(tmp_path,path):
 p=tmp_path/'runtime';shutil.copytree(BASE,p);(p/path).write_text('tampered');before=(p/'app/static/index.html').read_bytes()
 with pytest.raises(ValueError):OVERLAY.apply(p)
 assert (p/'app/static/index.html').read_bytes()==before;assert not (p/'app/static/log_package_worker.js').exists()
def test_full_cumulative_replay(tmp_path):
 p=tmp_path/'runtime';shutil.copytree(Path(os.environ['WAVELINK_UI92_TEST_SOURCE']),p)
 for n in ['ui93','ui94','ui95','ui96','ui97','ui99','ui100','ui101']:
  sp=importlib.util.spec_from_file_location(n,ROOT/'deploy'/('apply_'+n+'.py'));m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.apply(p)
 identical(p)
def test_auth_mail_tabs_gateways_dependencies_and_art_preserved():
 for n in ['app/accounts.py','app/email_alerts.py','app/password_recovery.py','app/membership_mail.py','app/company_membership.py','app/static/browser_workspace.js','app/static/save_status.js','app/static/save_status_ui.js']:
  assert (SOURCE/n).read_bytes()==(BASE/n).read_bytes(),n
 for n in ['deploy/company_runtime.py','deploy/nginx_config.py','requirements.lock','deploy/extract_source.py']:
  assert (ROOT/n).read_bytes()==(Path(os.environ['WAVELINK_UI98_REPO'])/n).read_bytes(),n
 names=[n for n in json.loads((BASE/'RELEASE_FILES.json').read_text())['files'] if n.startswith('app/static/') and Path(n).suffix.lower() in ('.png','.jpg','.jpeg','.webp','.svg','.ico')]
 assert len(names)==72
 for n in names:assert (SOURCE/n).read_bytes()==(BASE/n).read_bytes(),n
def test_worker_and_entry_load_matching_changed_modules():
 from bs4 import BeautifulSoup
 html=BeautifulSoup((SOURCE/'app/static/index.html').read_text(),'html.parser');assets=[s['src'] for s in html.select('script[src]')]+[x['href'] for x in html.select('link[rel=stylesheet]')]
 worker=(SOURCE/'app/static/sw.js').read_text()
 for src in assets:assert src in worker,src
 for n in ['document_import.js','document_import.css','setup_builders.js','admin_workspace_ui75.css']:
  assert '/static/'+n+'?v=1.34.19-ui101' in assets,n
 assert "u.pathname.startsWith('/api/')" in worker and "u.pathname==='/reset-password'" in worker
 assert 'browser_workspace.js?v=1.34.19-ui99' in str(assets)
 assert '/static/log_package_worker.js?v=1.34.19-ui101' in worker
def test_docker_applies_overlay_after_chain_once():
 s=(ROOT/'Dockerfile').read_text();last=-1
 for n in ['ui93','ui94','ui95','ui96','ui97','ui99','ui100','ui101']:
  term='&& python apply_'+n+'.py /opt/wavelink/app';assert s.count(term)==1;at=s.index(term);assert at>last;last=at
 assert 'apply_ui98.py' not in s
