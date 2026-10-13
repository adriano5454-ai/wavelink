import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES?require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'playwright')):require('playwright');
const root=process.env.WAVELINK_TEST_SOURCE;if(!root)throw Error('Set WAVELINK_TEST_SOURCE to the reviewed runtime.');
const out=process.env.WAVELINK_UI110_TASK_EVIDENCE_DIR||path.resolve('evidence/ui110-task');fs.mkdirSync(out,{recursive:true});
const executable=process.env.WAVELINK_CHROMIUM_EXECUTABLE;
if(!executable)throw Error('Set WAVELINK_CHROMIUM_EXECUTABLE to the available Chromium binary.');
const browser=await chromium.launch({executablePath:executable,headless:true,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[],checks=[];
page.on('pageerror',e=>errors.push(e.stack));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const tasks=Array.from({length:25},(_,i)=>({id:'00000000-0000-4000-8000-'+String(i+1).padStart(12,'0'),title:'Fictional task '+(i+1),kind:'general',version:1,status:i===1?'submitted':'not_started',assignees:[{name:'Fictional worker'}],assignee_ids:['person-a'],department_name:'Fictional Survey',can_review:true,can_perform:false,priority:'normal',due_at:'2026-10-15T12:00:00Z',instructions:'READ ONLY INSTRUCTIONS '+(i+1),unread:true,total:0,verified:0,remaining:0}));
const detail=(i,extras={})=>({...tasks[i],result_note:'Saved finding '+(i+1),verification:null,...extras});
const setup=async()=>{
 await page.setContent('<!doctype html><html><head><style>body{font-family:Arial;margin:0;background:#f2f6f8;color:#17364c}#app{padding:20px;max-width:1280px;margin:auto;box-sizing:border-box}*{box-sizing:border-box}.btn{display:inline-flex;align-items:center;min-height:40px;border:1px solid #bccdd7;border-radius:8px;padding:8px 12px;background:#edf6f8;color:#17364c;cursor:pointer;text-decoration:none;font:inherit}.actions{display:flex;gap:8px;flex-wrap:wrap}input,select{width:100%;padding:10px;border:1px solid #bccdd7;border-radius:8px;font:inherit}label{display:grid;gap:6px}.eyebrow{font-size:10px}.small{font-size:12px}.muted{color:#526d7c}.preserve-lines{white-space:pre-wrap}.notice{background:#fff5e8;border:1px solid #d9b87e;padding:12px;border-radius:8px}dialog{width:80%;}</style></head><body><header id="wl-topbar"></header><main id="app"></main><dialog id="dialog"><div id="dialog-content"></div></dialog></body></html>');
 await page.addStyleTag({content:fs.readFileSync(path.join(root,'app/static/task_workspace.css'),'utf8')});
 await page.evaluate(tasks=>{
  window.root=document.querySelector('#app');window.dlg=document.querySelector('#dialog');window.requests=[];window.errors=[];window.writes=[];
  window.state={hub_id:'fictional-hub',auth:{token:'token-a',person:{user_id:'person-a'}},fieldworkDrafts:{keep:{values:{notes:'KEEP DRAFT'}}}};
  window.location.hash='#tasks';window.permission=true;window.busy=false;window.taskScope={value:'all'};window.taskFilter={query:'',kind:'all',status:'open',expanded:false,reviewOnly:false};window.tasks=tasks;
  window.esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  window.canUse=k=>permission;window.editingMeta=false;window.pageBusy=()=>!!document.querySelector('dialog[open]')||editingMeta||(root.contains(document.activeElement)&&document.activeElement.matches('input,textarea,select,[contenteditable="true"]'));window.message=e=>e.userMessage||e.message||String(e);
  window.AJInterface={markup:s=>s};
  window.AJGeneralTasks={types:{general:'General work',maintenance:'Maintenance activity',certificate_review:'Certificate check',stock_verification:'Inventory verification'},choose:()=>{window.chooserOpened=true;}};
  window.AJOperations={canResume:()=>true};
  window.AJFieldwork={scope:()=>state.hub_id+':'+state.auth?.person?.user_id,button:(id,text)=>'<button type="button" class="btn" id="'+id+'">'+esc(text)+'</button>',input:(name,label,value='',type='text',attrs='')=>'<label>'+esc(label)+'<input name="'+name+'" type="'+type+'" value="'+esc(value)+'" '+attrs+'></label>',select:(name,label,rows,value)=>'<label>'+esc(label)+'<select name="'+name+'">'+rows.map(([id,label])=>'<option value="'+esc(id)+'" '+(id===value?'selected':'')+'>'+esc(label)+'</option>').join('')+'</select></label>',textarea:()=>'',myDrafts:()=>[],page:html=>{root.innerHTML='<section>'+html+'</section>';},click:(id,fn)=>{const b=root.querySelector('#'+id);if(b)b.onclick=fn;},showError:e=>errors.push(message(e))};
  window.api=(url,opts={})=>{opts.beforeSend?.();if((opts.method||'GET')!=='GET')writes.push({url,...opts});return new Promise((resolve,reject)=>requests.push({url,opts,resolve,reject}));};
  window.dashboardWorkDialog=()=>{};window.modal=()=>{};
 },tasks);
 await page.addScriptTag({content:fs.readFileSync(path.join(root,'app/static/task_workspace.js'),'utf8')});
 await page.evaluate(()=>{window.mount=()=>AJTaskWorkspace.list(tasks,taskScope,taskFilter,mount);mount();});
};
const row=i=>page.locator('[data-task-id="'+tasks[i].id+'"]');
const requestCount=()=>page.evaluate(()=>requests.length);
const resolve=async(index,value)=>{await page.evaluate(({index,value})=>requests[index].resolve(value),{index,value});await page.waitForTimeout(20);};
const reject=async(index,status=403)=>{await page.evaluate(({index,status})=>requests[index].reject(Object.assign(new Error('Access revoked'),{status})),{index,status});await page.waitForTimeout(20);};
const check=async(name,fn)=>{await setup();await fn();checks.push(name);process.stdout.write('PASS '+name+'\n');};
try{
 await check('Task selection is a GET-only preview and does not acknowledge notifications',async()=>{
  assert.equal(await requestCount(),0);await row(0).click();assert.equal(await requestCount(),1);assert.equal(await page.evaluate(()=>requests[0].url),'/api/tasks/'+tasks[0].id);await resolve(0,detail(0));assert.match(await page.locator('#tw110-detail').innerText(),/READ ONLY INSTRUCTIONS 1/);assert.equal(await page.evaluate(()=>writes.length),0);assert.equal(await page.locator('#tw110-open').getAttribute('href'),'#tasks/'+tasks[0].id);assert.equal(await row(0).getAttribute('aria-current'),'true');
 });
 await check('Newest selection rejects a reversed late detail response',async()=>{
  await row(0).click();await row(1).click();await resolve(1,detail(1));await resolve(0,detail(0));assert.match(await page.locator('#tw110-detail').innerText(),/Fictional task 2/);assert.doesNotMatch(await page.locator('#tw110-detail').innerText(),/READ ONLY INSTRUCTIONS 1/);
 });
 await check('Production focused-register busy checks permit query, type, status and scope changes',async()=>{
  await row(1).click();await resolve(0,detail(1));await page.locator('[name=task-query]').fill('task 1');assert.equal(await page.locator('[name=task-query]').inputValue(),'task 1');assert.equal(await row(1).isVisible(),false);assert.match(await page.locator('#tw110-detail').innerText(),/Select a task/);
  await page.locator('[name=task-query]').fill('');await page.locator('#task-filter-options summary').click();await page.locator('[name=task-kind]').selectOption('maintenance');assert.equal(await page.evaluate(()=>taskFilter.kind),'maintenance');assert.equal(await page.locator('#task-empty').isVisible(),true);await page.locator('[name=task-kind]').selectOption('all');await page.locator('[name=task-status]').selectOption('submitted');assert.equal(await page.evaluate(()=>taskFilter.status),'submitted');assert.equal(await row(1).isVisible(),true);assert.equal(await row(0).isVisible(),false);await page.locator('[name=task-status]').selectOption('open');await page.locator('[name=scope]').selectOption('mine');assert.equal(await page.evaluate(()=>taskScope.value),'mine');assert.equal(await page.locator('[name=scope]').inputValue(),'mine');assert.equal(await row(0).isVisible(),true);
 });
 await check('Pending preview survives an owned filter focus only while its selected record remains visible',async()=>{
  await row(0).click();await page.locator('[name=task-query]').fill('task 1');assert.equal(await page.evaluate(()=>pageBusy()),true);await resolve(0,detail(0));assert.match(await page.locator('#tw110-detail').innerText(),/READ ONLY INSTRUCTIONS 1/);assert.equal(await page.locator('[name=task-query]').inputValue(),'task 1');
 });
 await check('Focused non-filter edits and actual editor state still block Tasks controls',async()=>{
  await page.evaluate(()=>{const input=document.createElement('input');input.id='actual-editor';input.value='UNSENT ROOT EDIT';root.firstElementChild.append(input);input.focus();document.querySelector('[data-task-id]').click();document.querySelector('#op-refresh').click();});assert.equal(await requestCount(),0);assert.equal(await page.locator('#actual-editor').inputValue(),'UNSENT ROOT EDIT');
  await page.locator('[name=task-query]').focus();await page.evaluate(()=>{editingMeta=true;const q=document.querySelector('[name=task-query]');q.value='task 2';q.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#op-refresh').click();});assert.equal(await page.evaluate(()=>taskFilter.query),'');assert.equal(await requestCount(),0);assert.equal(await page.locator('#actual-editor').inputValue(),'UNSENT ROOT EDIT');
 });
 await check('Filtered-out pending selection is cleared and its response is ignored',async()=>{
  await row(0).click();await page.locator('[name=task-query]').fill('task 2');await resolve(0,detail(0));assert.match(await page.locator('#tw110-detail').innerText(),/Select a task/);assert.equal(await page.locator('#tw110-open').count(),0);assert.equal(await row(0).getAttribute('aria-current'),'false');
 });
 await check('Scope changes clear selection and require a new permitted read',async()=>{
  await row(0).click();await resolve(0,detail(0));await page.locator('#task-filter-options summary').click();await page.locator('[name=scope]').selectOption('mine');assert.equal(await requestCount(),1);assert.match(await page.locator('#tw110-detail').innerText(),/Select a task/);assert.equal(await page.locator('#tw110-open').count(),0);
 });
 await check('Refresh preserves selection but clears unverified content and revalidates the detail',async()=>{
  await row(0).click();await resolve(0,detail(0));await page.locator('#op-refresh').click();assert.equal(await requestCount(),2);assert.equal(await row(0).getAttribute('aria-current'),'true');assert.equal(await page.locator('#tw110-open').count(),0);assert.doesNotMatch(await page.locator('#tw110-detail').innerText(),/READ ONLY INSTRUCTIONS/);await resolve(1,detail(0,{version:2,instructions:'REFRESHED INSTRUCTION'}));assert.match(await page.locator('#tw110-detail').innerText(),/REFRESHED INSTRUCTION/);
 });
 await check('Denied detail refresh does not expose the previous detail',async()=>{
  await row(0).click();await resolve(0,detail(0));await page.locator('#op-refresh').click();await reject(1);assert.doesNotMatch(await page.locator('#tw110-detail').innerText(),/READ ONLY INSTRUCTIONS/);assert.equal(await page.locator('#tw110-open').count(),0);
 });
 await check('A returned task outside the current filters or assignment scope clears selection',async()=>{
  await row(0).click();await resolve(0,detail(0,{status:'completed'}));assert.equal(await page.locator('#tw110-open').count(),0);assert.equal(await row(0).getAttribute('aria-current'),'false');assert.equal(await row(0).isVisible(),false);assert.match(await page.locator('#tw110-read-state').innerText(),/no longer matches/);
  await setup();await page.locator('#task-filter-options summary').click();await page.locator('[name=scope]').selectOption('mine');await row(0).click();await resolve(0,detail(0,{assignee_ids:[]}));assert.equal(await page.locator('#tw110-open').count(),0);assert.equal(await row(0).getAttribute('aria-current'),'false');
 });
 await check('An older detail revision cannot replace a newer listed task',async()=>{
  await page.evaluate(()=>{tasks[0].version=4;mount();});await row(0).click();await resolve(0,detail(0,{version:3}));assert.match(await page.locator('#tw110-detail').innerText(),/could not be verified/);assert.equal(await page.locator('#tw110-open').count(),0);
 });
 await check('Mismatched identities and malformed permissions never enable full task opening',async()=>{
  await row(0).click();await resolve(0,detail(1));assert.match(await page.locator('#tw110-detail').innerText(),/could not be verified/);assert.equal(await page.locator('#tw110-open').count(),0);await page.locator('#tw110-retry').click();await resolve(1,detail(0,{can_perform:null}));assert.match(await page.locator('#tw110-detail').innerText(),/could not be verified/);assert.equal(await page.locator('#tw110-open').count(),0);
 });
 await check('Open editor blocks selection, filtering, refresh and task chooser without changing typed work',async()=>{
  await page.evaluate(()=>{document.querySelector('#dialog-content').innerHTML='<textarea id="draft-note">UNSENT WORDING</textarea>';dlg.showModal();});
  await page.evaluate(()=>{document.querySelector('[data-task-id]').click();const q=document.querySelector('[name=task-query]');q.value='task 2';q.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('#op-refresh').click();document.querySelector('#task-new').click();});
  assert.equal(await requestCount(),0);assert.equal(await page.locator('#draft-note').inputValue(),'UNSENT WORDING');assert.equal(await page.evaluate(()=>state.fieldworkDrafts.keep.values.notes),'KEEP DRAFT');assert.equal(await page.evaluate(()=>taskFilter.query),'');assert.equal(await page.evaluate(()=>Boolean(window.chooserOpened)),false);assert.equal(await page.evaluate(()=>dlg.open),true);
 });
 await check('A dialog epoch interruption rejects a detail even after the dialog closes',async()=>{
  await row(0).click();await page.evaluate(()=>{document.querySelector('#dialog-content').innerHTML='<div>Other editor</div>';dlg.showModal();dlg.close();});await resolve(0,detail(0));assert.match(await page.locator('#tw110-detail').innerText(),/interrupted/);assert.equal(await page.locator('#tw110-open').count(),0);await page.locator('#tw110-retry').click();await resolve(1,detail(0));assert.match(await page.locator('#tw110-detail').innerText(),/READ ONLY INSTRUCTIONS 1/);
 });
 await check('Changed token, route, host or permission suppresses outstanding detail content',async()=>{
  for(const change of ['token','route','host','permission']){await setup();await row(0).click();await page.evaluate(change=>{if(change==='token')state.auth.token='token-b';if(change==='route')location.hash='#home';if(change==='host')root.innerHTML='<section>Other workspace</section>';if(change==='permission')permission=false;},change);await resolve(0,detail(0));assert.doesNotMatch(await page.locator('#app').innerText(),/READ ONLY INSTRUCTIONS/);assert.equal(await page.locator('#tw110-open').count(),0);}
 });
 await check('Return from the full task route retains valid selection and rechecks its detail',async()=>{
  await row(0).click();await resolve(0,detail(0));await page.locator('#tw110-open').click();assert.equal(await page.evaluate(()=>location.hash),'#tasks/'+tasks[0].id);await page.evaluate(()=>{location.hash='#tasks';mount();});assert.equal(await requestCount(),2);assert.equal(await page.locator('#tw110-open').count(),0);await resolve(1,detail(0,{version:3}));assert.match(await page.locator('#tw110-detail').innerText(),/SAVED REVISION 3/);
 });
 await check('Desktop compact list supports nested scroll and retains it when returning',async()=>{
  await page.evaluate(()=>{document.querySelector('#tw110-list').scrollTop=450;document.querySelector('#tw110-list').dispatchEvent(new Event('scroll'));});await row(4).click();await resolve(0,detail(4));const before=await page.locator('#tw110-list').evaluate(e=>e.scrollTop);await page.locator('#tw110-open').click();await page.evaluate(()=>{location.hash='#tasks';mount();});assert.equal(await page.locator('#tw110-list').evaluate(e=>e.scrollTop),before);await resolve(1,detail(4));await page.screenshot({path:path.join(out,'tasks_desktop.png'),fullPage:true});
 });
 await check('Phone summary and Back preserve filter, selection and focus without horizontal overflow',async()=>{
  await page.setViewportSize({width:390,height:844});await page.locator('[name=task-query]').fill('task 1');await row(0).click();await resolve(0,detail(0));assert.equal(await page.locator('.tw110-register').isVisible(),false);assert.equal(await page.locator('#tw110-detail').isVisible(),true);assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);await page.screenshot({path:path.join(out,'tasks_phone_detail.png'),fullPage:true});await page.locator('#tw110-back').click();assert.equal(await page.locator('.tw110-register').isVisible(),true);assert.equal(await row(0).getAttribute('aria-current'),'true');assert.equal(await page.locator('[name=task-query]').inputValue(),'task 1');assert.equal(await page.evaluate(()=>document.activeElement.dataset.taskId),tasks[0].id);assert.equal(await requestCount(),1);await page.screenshot({path:path.join(out,'tasks_phone_list.png'),fullPage:true});await page.setViewportSize({width:1440,height:1000});
 });
 assert.deepEqual(errors,[]);fs.writeFileSync(path.join(out,'task_inspector_results.json'),JSON.stringify({checks,errors,scope:'Real Chromium DOM with controlled current-task GET responses. Full operational writer/API regression is tested separately.'},null,2));
}catch(e){fs.writeFileSync(path.join(out,'task_inspector_results.json'),JSON.stringify({checks,errors,failure:e.stack},null,2));throw e;}finally{await browser.close();}
