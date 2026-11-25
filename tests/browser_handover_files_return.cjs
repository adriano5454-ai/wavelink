const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);assert.equal(origin.hostname,'127.0.0.1');
async function check(browser,width){
 const p=await browser.newPage({viewport:{width,height:919},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try{
  await p.goto(origin.origin+'/__demo/public?area=hr');await p.locator('#hr-section-select').waitFor({state:'attached'});
  await p.evaluate(()=>location.hash='original-files');
  const q=p.locator('#of-search'),rows=p.locator('.of-file');
  await q.waitFor();const sidebar=p.locator('.wf-sidebar');if(!await sidebar.evaluate(e=>e.open))await sidebar.locator('summary').first().click();
  const group=sidebar.getByRole('button',{name:/^Equipment certificates/i}).first();await group.click();
  await p.getByLabel('Sort',{exact:true}).selectOption('name');
  await p.locator('.wf-filter summary').click();await p.locator('#of-archived').focus();await p.keyboard.press('Space');
  await q.fill('003');await rows.first().locator('summary').click();
  const source=rows.getByRole('link',{name:'Open source record'}),target=await source.getAttribute('href'),file=await rows.first().getAttribute('data-document-id');
  const fileTop=(await rows.first().boundingBox()).y;
  for(const appBack of [false,true]){
   await source.click();await p.getByRole('heading',{name:'DEMO Certificate register 003',exact:true}).waitFor();
   assert.equal(new URL(p.url()).hash,target);
   if(appBack)await p.locator('#cert-back-source').click();else await p.goBack();
   await source.waitFor();assert.equal(await q.inputValue(),'003');assert(await p.locator('#of-archived').isChecked());assert.equal(await p.getByLabel('Sort',{exact:true}).inputValue(),'name');assert.equal(await rows.count(),1);
   assert.equal(await rows.getAttribute('data-document-id'),file);assert(await source.evaluate(e=>e===document.activeElement));
   assert(Math.abs((await rows.boundingBox()).y-fileTop)<=3);
  }
  await q.fill('');assert(await group.evaluate(e=>e.getAttribute('aria-current')==='location'));
  await q.fill('');await sidebar.getByRole('button',{name:/^Unfiled/}).first().click();await q.fill('DEMO-REF-001');
  assert.equal(await rows.count(),1);const revisionFile=await rows.getAttribute('data-document-id');
  await rows.locator('summary').click();await rows.getByRole('button',{name:'Revision details'}).click();
  const back=p.getByRole('button',{name:'Back to list',exact:true});await back.waitFor();await p.reload();await back.waitFor();
  await p.getByText('Identity & import details',{exact:true}).waitFor();if(width<700){const r=await back.boundingBox();assert(r.y>=64&&r.y+r.height<=919,JSON.stringify(r))}
  await back.click();await q.waitFor();assert.equal(await q.inputValue(),'DEMO-REF-001');assert.equal(await rows.count(),1);assert.equal(await rows.getAttribute('data-document-id'),revisionFile);
  await p.evaluate(()=>location.hash='handovers');
  const vessel=p.locator('#ho-vessel-filter select'),subject=p.locator('#hwd-subject'),jump=p.locator('#hwd-jump');
  await vessel.selectOption({label:'MV Aurora · AUR'});await subject.selectOption({label:'MV Aurora · Offshore Survey'});
  const days=p.locator('.hwd-day').filter({has:p.getByRole('heading',{name:'Days',exact:true})});
  await days.first().waitFor();const requested=days.and(p.locator('[data-hwd-day="2026-11-25"]'));
  const day=await requested.count()?requested:days.first();
  const date=await day.getAttribute('data-hwd-day');await jump.selectOption(date);
  const b=day.locator('.hwd-record').filter({has:p.getByRole('heading',{name:'Days',exact:true})}).locator('[data-hwd-open]').first();
  const id=await b.getAttribute('data-hwd-open');
  const v=await vessel.inputValue(),s=await subject.inputValue();
  const reader=p.locator('.ho-publication-reader');
  await b.scrollIntoViewIfNeeded();const top=(await b.boundingBox()).y;await b.click();
  if(width<700){const r=await p.locator('.hop-head button').boundingBox();assert(r.y>=64&&r.y+r.height<=919,JSON.stringify(r))}
  await p.locator('.hop-actions button').first().click();await reader.waitFor();
  const hash=new URL(p.url()).hash;assert(hash.startsWith('#handover/'+id+'/'));const title=await p.locator('#ho-detail h2').first().innerText();
  async function returned(){
   const exact=p.locator('[data-hwd-open="'+id+'"]');await exact.waitFor();await p.waitForFunction(id=>document.activeElement?.dataset.hwdOpen===id,id);
   assert.deepEqual([await vessel.inputValue(),await subject.inputValue(),await jump.inputValue()],[v,s,date]);
   assert.equal(await exact.evaluate(e=>e.closest('details').open),true);assert.equal(await exact.evaluate(e=>e.closest('article').querySelector('h3').textContent),'Days');
   assert(Math.abs((await exact.boundingBox()).y-top)<=3);
  }
  await p.goBack();await returned();await p.goForward();await reader.waitFor();assert.equal(new URL(p.url()).hash,hash);assert.equal(await p.locator('#ho-detail h2').first().innerText(),title);
  await p.locator('#ho-back').click();await returned();await b.click();await p.locator('.hop-head button').click();await returned();
  await b.click();await p.locator('.hop-actions button').first().click();await reader.waitFor();await p.reload();await reader.waitFor();
  assert.equal(new URL(p.url()).hash,hash);assert.equal(await p.locator('#ho-detail h2').first().innerText(),title);
  if(width<700){
    await p.evaluate(()=>location.hash='hr');const tabs=p.locator('#hr-section-select');await tabs.selectOption('people');
    const list=p.locator('.hr-person-list'),heading=p.locator('.ux-profile-hero h2');await list.waitFor();
    const row=name=>list.getByRole('button',{name:new RegExp(name)});
    async function visible(name){
      await heading.filter({hasText:name}).waitFor();const r=await heading.boundingBox();
      assert(r.y>=64&&r.y+r.height<=919,JSON.stringify(r));console.log('employee title',width,name,r.y,r.y+r.height);
    }
    await row('Alba Reis').click();await visible('Alba Reis');await row('Cora Sal').click();await visible('Cora Sal');
    await p.goBack();await visible('Alba Reis');assert(await row('Alba Reis').evaluate(e=>e===document.activeElement));
    await p.goForward();await visible('Cora Sal');const expense=p.locator('[data-hr-jump="expenses"]').first();
    await expense.click();await p.locator('.hr-employee-sheet').getByRole('button',{name:'Close',exact:true}).click();await p.locator('.hr-employee-sheet').waitFor({state:'detached'});await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));await visible('Cora Sal');
    assert(await expense.evaluate(e=>e===document.activeElement));
  }
  console.log('PASS',width,date,'Aurora | Offshore Survey | Days',hash,'file 003',file);
 }finally{await p.close()}
}
(async()=>{const b=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,389,390])await check(b,w)}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
