"""Real IndexedDB and Web Locks with actual C01/core APIs, fictional company only."""
import json,os,sys,tempfile,mimetypes
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from test_company_c01 import instance,client,activate,PASS
OUT=Path(os.environ.get('WAVELINK_UI99_EVIDENCE_DIR','/tmp/wavelink-ui99/evidence/browser'))
BASE=Path(os.environ.get('WAVELINK_UI98_TEST_SOURCE','/tmp/wavelink-ui98/runtime'))

def main():
 OUT.mkdir(parents=True,exist_ok=True);report={'checks':[],'errors':[],'method':'Real shared-origin Chromium IndexedDB, sessionStorage, Web Locks and history; actual fictional C01 HostedBoundary/CompanyAccess/core API responses. WebSockets and service-worker registration suppressed in this harness.'}
 def ok(name):report['checks'].append(name);(OUT/'PROGRESS.json').write_text(json.dumps(report,indent=2)+'\n')
 with tempfile.TemporaryDirectory(prefix='fictional-ui99-tabs-') as td:
  i=instance.__wrapped__(Path(td))
  with client(i) as c,sync_playwright() as pw:
   activate(c);origin=i[2].external_origin;browser=pw.chromium.launch(headless=True,args=['--no-sandbox']);pages=[]
   def page(width=1440,baseline=False,no_locks=False):
    p=browser.new_page(viewport={'width':width,'height':950});pages.append(p);p.set_default_timeout(20000);p.on('pageerror',lambda e:report['errors'].append(str(e)));p.on('dialog',lambda d:d.accept())
    p.add_init_script("""class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();""")
    if no_locks:p.add_init_script("Object.defineProperty(navigator,'locks',{value:undefined});")
    def route(r):
     req=r.request;u=urlsplit(req.url);path=u.path+('?' +u.query if u.query else '')
     if baseline and (u.path=='/' or u.path.startswith('/static/')):
      name='app/static/index.html' if u.path=='/' else 'app'+u.path;f=BASE/name
      if f.is_file():r.fulfill(status=200,body=f.read_bytes(),content_type=mimetypes.guess_type(str(f))[0] or 'application/octet-stream');return
     response=c.request(req.method,path,headers=req.headers,content=req.post_data_buffer);r.fulfill(status=response.status_code,body=response.content,headers=dict(response.headers))
    p.route(origin+'/**',route);return p
   def ready(p):expect(p.locator('#workspace-nav')).to_be_visible();assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
   def signin(p):
    p.locator('[name=login_id]').fill('admin');p.locator('[name=password]').fill(PASS);p.locator('#login-form button[type=submit]').click();ready(p)
   def snapshot(p):return p.evaluate('({id:browserWorkspace.id(),auth:state.auth?.person?.user_id,token:state.auth?.token,device:state.device_id,drafts:state.fieldworkDrafts||{},key:browserWorkspace.stateKey()})')
   def draft(p,name):p.evaluate("""async name=>{state.fieldworkDrafts={...(state.fieldworkDrafts||{}),[name]:{id:name,kind:'Task',scope:state.hub_id+':'+state.auth.person.user_id,values:{title:name,notes:'UNSENT '+name}}};await persist();}""",name)
   try:
    a=page(baseline=True);a.goto(origin+'/');signin(a)
    a.evaluate("async()=>{state.fieldworkDrafts={legacy:{id:'legacy',kind:'Task',scope:state.hub_id+':'+state.auth.person.user_id,values:{title:'Legacy draft',notes:'KEEP BEFORE MIGRATION'}}};await persist();}")
    before=a.evaluate('JSON.stringify(state.fieldworkDrafts)');b=page(baseline=True);b.goto(origin+'/');expect(b.locator('#workspace-issue')).to_contain_text('Waiting for the other Dive Check tab');ok('UI98 reproduced: second ordinary tab is blocked by the global workspace lease')
    b.close()
    # Start the correction while a previous UI98 page still owns the original lease.
    b=page();b.goto(origin+'/');ready(b);sb=snapshot(b);assert sb['id']!='primary' and sb['drafts']=={};assert a.evaluate('JSON.stringify(state.fieldworkDrafts)')==before;ok('UI99 coexists with a live old page without stealing or cloning its drafts')
    assert b.evaluate("()=>new Promise(r=>{const t=db.transaction('state'),q=t.objectStore('state').get('main');q.onsuccess=()=>r(JSON.stringify(q.result.fieldworkDrafts));})")==before;ok('Original IndexedDB draft bytes remain intact during upgrade')
    a.close();draft(b,'tab-b');btoken=sb['token'];key=sb['key'];
    d=page();d.goto(origin+'/');ready(d);sd=snapshot(d);assert sd['id']!=sb['id'] and sd['device']!=sb['device'] and sd['token']==btoken and not sd['drafts'];ok('New tab reuses a server-validated session and has a separate device workspace')
    draft(d,'tab-d');assert snapshot(b)['drafts']['tab-b']['values']['notes']=='UNSENT tab-b';assert list(snapshot(d)['drafts'])==['tab-d'];ok('Concurrent tabs persist independent unsent forms without copying or overwriting')
    b.goto(origin+'/help');b.go_back();ready(b);assert snapshot(b)['key']==key and 'tab-b' in snapshot(b)['drafts'];ok('Browser Back restores the original tab and its local draft')
    b.reload();ready(b);assert snapshot(b)['key']==key and 'tab-b' in snapshot(b)['drafts'];ok('Reload restores the same tab without a competing-writer warning')
    # A duplicated tab inherits sessionStorage; its live Web Lock must cause a fork.
    dup=page();dup.goto(origin+'/help');dup.evaluate('(id)=>sessionStorage.setItem("wavelink-browser-window-1",id)',sb['id']);dup.goto(origin+'/');ready(dup);assert snapshot(dup)['id']!=sb['id'] and snapshot(dup)['drafts']=={};ok('Copied sessionStorage cannot give two live documents the same writer')
    # Timestamp expiration never overrides a live Web Lock.
    b.evaluate("""async()=>{await new Promise(r=>{const t=db.transaction('state','readwrite'),s=t.objectStore('state'),q=s.get(browserWorkspace.leaseKey());q.onsuccess=()=>s.put({...q.result,expires:0},browserWorkspace.leaseKey());t.oncomplete=r;});}""")
    expiry=page();expiry.goto(origin+'/?browser_workspace='+sb['id']);ready(expiry);eid=snapshot(expiry)['id'];assert eid!=sb['id'];ok('Background/expired timestamp cannot steal an actively locked tab')
    assert 'browser_workspace='+eid in expiry.url;expiry.reload();ready(expiry);assert snapshot(expiry)['id']==eid;ok('Forked saved-tab links keep their new workspace through Reload')
    # Close and explicitly reopen exact durable workspace.
    b.close();d.evaluate("""async id=>{await new Promise(r=>{const t=db.transaction('state','readwrite');t.objectStore('state').put({owner:'fictional-closed-page',expires:Date.now()+30000,web_lock:true},'window:'+id+':lease');t.oncomplete=r;});}""",sb['id']);reopened=page();reopened.goto(origin+'/?browser_workspace='+sb['id']);ready(reopened);assert snapshot(reopened)['id']==sb['id'] and 'tab-b' in snapshot(reopened)['drafts'];ok('Closed tab reopens exact drafts immediately despite an unreleased future lease')
    reopened.evaluate('browserWindowsDialog()');expect(reopened.locator('#browser-saved-tabs')).to_contain_text('saved local');assert reopened.locator('#browser-saved-tabs a').count()>=2;ok('Saved-tabs chooser discovers original and independent workspaces for the current account')
    for width in [1440,390,320]:
     reopened.set_viewport_size({'width':width,'height':950});assert reopened.evaluate('document.documentElement.scrollWidth<=innerWidth+1');reopened.screenshot(path=str(OUT/f'saved_tabs_{width}.png'),full_page=True);ok('Saved-tabs recovery dialog fits '+str(width)+'px')
    reopened.keyboard.press('Escape');reopened.set_viewport_size({'width':1440,'height':950});reopened.locator('#menu-button').click();reopened.locator('[data-connection-tools]').click();expect(reopened.locator('#save-panel-windows')).to_be_visible();reopened.locator('#save-panel-windows').click();expect(reopened.locator('#browser-saved-tabs')).to_be_visible();reopened.keyboard.press('Escape');ok('Connection & saves links directly to other saved tabs')
    # The real scoped discard must leave the other tab untouched.
    reopened.evaluate("""async()=>{const selection=AJLocalWork.catalogue(state).filter(x=>!x.blocked).map(({id,fingerprint})=>({id,fingerprint}));await discardLocalBatch(selection,connectionSession());}""");assert snapshot(reopened)['drafts']=={} and 'tab-d' in snapshot(d)['drafts'];ok('Batch discard edits only its selected tab and preserves the other tab draft')
    # Independent legacy project archives are namespaced too.
    assert reopened.evaluate('browserWorkspace.projectKey("hub-other")')!=d.evaluate('browserWorkspace.projectKey("hub-other")');ok('Company-switch archives remain isolated by tab')
    # The precise same saved log window still retains the original one-writer guard.
    det=page();det.goto(origin+'/?log_window=11111111-1111-4111-8111-111111111111&book=22222222-2222-4222-8222-222222222222');expect(det.locator('#login-form')).to_be_visible();assert det.evaluate('!browserWorkspace.enabled&&browserWorkspace.stateKey()==="main"');ok('Explicit detached log windows retain their existing separate database and handoff boundary')
    det.close()
    # Existing offline work can reopen; new empty tab cannot adopt unverified seed offline.
    d.close();off=page();off.route(origin+'/api/**',lambda r:r.abort());off.goto(origin+'/?browser_workspace='+sd['id']);ready(off);assert 'tab-d' in snapshot(off)['drafts'];ok('Existing saved workspace remains recoverable when the API is unreachable')
    fresh_off=page();fresh_off.route(origin+'/api/**',lambda r:r.abort());fresh_off.goto(origin+'/');expect(fresh_off.locator('#login-form')).to_be_visible();assert not snapshot(fresh_off)['auth'];ok('A new tab never treats an unverified offline session seed as authenticated')
    fresh_off.close();off.close();d=page();d.goto(origin+'/?browser_workspace='+sd['id']);ready(d)
    # A fresh sign-in publishes a new valid session; stale sign-out must preserve it.
    dup.evaluate('state.auth=null;render()');signin(dup);newtoken=snapshot(dup)['token'];assert newtoken!=btoken
    d.evaluate("async()=>{await commitLocalSignOut({hub_id:state.hub_id,token:state.auth.token,user_id:state.auth.person.user_id},connectionSession());render();}");assert snapshot(d)['drafts']['tab-d'];check=page();check.goto(origin+'/');ready(check);assert snapshot(check)['token']==newtoken;ok('Stale tab sign-out preserves drafts and cannot clear a newer shared sign-in')
    # Actual logout revokes shared token; a subsequently opened tab must not revive it.
    dup.evaluate('async()=>{await leaveSession(connectionSession());render();}');expect(dup.locator('#login-form')).to_be_visible();revoked=page();revoked.goto(origin+'/');expect(revoked.locator('#login-form')).to_be_visible();assert not snapshot(revoked)['auth'];ok('Real server logout prevents fresh tabs from reviving the revoked shared session')
    # Lease-only fallback is still safe without Web Locks.
    signin(revoked);fallback=page(no_locks=True);fallback.goto(origin+'/');ready(fallback);fid=snapshot(fallback)['id'];draft(fallback,'no-lock-draft');cloned=page(no_locks=True);cloned.goto(origin+'/?browser_workspace='+fid);ready(cloned);assert snapshot(cloned)['id']!=fid and not snapshot(cloned)['drafts'];ok('Browsers without Web Locks use guarded leases and fork instead of blocking')
    # Cross-tab saves guard only the matching record; uncertainty never blocks navigation.
    fallback.evaluate("async()=>{const m=AJSaveStatus.describe('/api/tasks/action','POST',{action:'update',payload:{id:'fictional-record'},op_id:uid()},'#tasks');window.pendingTicket=await deliveryJournal.begin(m);}")
    refused=cloned.evaluate("async()=>{try{await deliveryJournal.begin(AJSaveStatus.describe('/api/tasks/action','POST',{action:'update',payload:{id:'fictional-record'},op_id:uid()},'#tasks'));return null;}catch(e){return {text:e.message,ready:workspaceReady,receipts:deliveryJournal.list().length};}}")
    assert 'another tab' in refused['text'] and refused['ready'] and refused['receipts']==0;ok('Matching cross-tab write is blocked atomically before send without pausing the app')
    fallback.evaluate("async()=>{await deliveryJournal.finish(window.pendingTicket,'uncertain');}");refused=cloned.evaluate("async()=>{try{await deliveryJournal.begin(AJSaveStatus.describe('/api/tasks/action','POST',{action:'update',payload:{id:'fictional-record'},op_id:uid()},'#tasks'));return null;}catch(e){return e.message;}}")
    assert 'another tab' in refused;ok('Uncertain result remains protected across tabs until explicitly reviewed')
    cloned.evaluate("async()=>{const t=await deliveryJournal.begin(AJSaveStatus.describe('/api/tasks/action','POST',{action:'update',payload:{id:'different-record'},op_id:uid()},'#tasks'));await deliveryJournal.finish(t,'confirmed');}");ok('A pending action for one record does not block saves for another record')
    fallback.evaluate("async()=>{await deliveryJournal.review(window.pendingTicket.id);}");cloned.evaluate("async()=>{const t=await deliveryJournal.begin(AJSaveStatus.describe('/api/tasks/action','POST',{action:'update',payload:{id:'fictional-record'},op_id:uid()},'#tasks'));await deliveryJournal.finish(t,'confirmed');}");ok('Reviewing the original receipt releases the matching cross-tab save guard')
    # Quota failure stays a real local-saving issue and preserves already saved bytes.
    old_disk=fallback.evaluate('()=>dbRead()');fallback.evaluate("async()=>{const original=db.transaction.bind(db);db.transaction=()=>{throw new DOMException('Fictional quota failure','QuotaExceededError');};try{await persist();}catch(_){}finally{db.transaction=original;}}")
    assert fallback.evaluate('storageFailed&&!workspaceReady&&workspaceIssue.kind==="quota"');assert fallback.evaluate('()=>dbRead()')==old_disk;ok('Actual storage failure fails closed and retains the last durable drafts and receipts')
    assert not report['errors'],report['errors']
   except Exception:
    for n,p in enumerate(pages):
     if not p.is_closed():
      try:p.screenshot(path=str(OUT/f'failure_{n}.png'),full_page=True)
      except Exception:pass
    raise
   finally:
    (OUT/'UI99_TABS_BROWSER_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');browser.close()
 print(json.dumps({'checks':len(report['checks']),'errors':report['errors']}))
if __name__=='__main__':main()
