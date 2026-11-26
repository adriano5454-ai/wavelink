const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);assert.equal(origin.hostname,'127.0.0.1');
async function check(browser,width) {
 const p=await browser.newPage({viewport:{width,height:919},ignoreHTTPSErrors:true});
 try {
  // Add synthetic vessel and project associations to one permitted list response; use the original report ID and details.
  await p.route('**/api/toolbox',async r=>{const response=await r.fetch(),d=await response.json();const talk=d.talks[0],site=d.sites.find(s=>s.type==='vessel'||s.kind==='vessel');assert(talk&&site);talk.work_site={id:site.id,name:site.name,code:site.code};talk.meta.project_number='LOCAL-123';await r.fulfill({response,json:d})});
  await p.goto(origin.origin+'/__demo/public?area=workspaces');await p.locator('a[href="#toolbox"]:visible').first().click();
  const project=p.locator('#tb-project'),query=p.locator('#tb-query'),vessel=p.locator('#tb-filters [data-page-vessel]'),filters=p.locator('#tb-filter-panel');
  await project.waitFor({state:'attached'});if(!await filters.evaluate(e=>e.open))await filters.locator('summary').click();
  await project.selectOption('LOCAL-123');const a=p.locator('[data-toolbox-id]').first();await a.waitFor();const title=await a.locator('h2').innerText(),id=await a.getAttribute('data-toolbox-id');
  await query.fill(title);for(const val of await vessel.locator('option').evaluateAll(opts=>opts.map(o=>o.value).filter(Boolean))){await vessel.selectOption(val);if(await a.count())break}
  const ship=await vessel.inputValue();assert(ship);await filters.locator('summary').click();await a.scrollIntoViewIfNeeded();const top=(await a.boundingBox()).y;await a.click();
  const preview=p.locator('.tb-talk-preview');await preview.getByRole('heading',{name:title,exact:true}).waitFor();await preview.getByRole('link').click();
  const heading=p.locator('.fw-heading h1');await p.getByRole('heading',{name:'Signing actions'}).waitFor();assert.equal(new URL(p.url()).hash,'#toolbox/'+id);assert(await heading.evaluate(e=>e===document.activeElement));assert((await heading.boundingBox()).y>=64);assert(await p.getByText(title,{exact:true}).isVisible());
  await p.goBack();await p.waitForFunction(id=>document.activeElement?.dataset.toolboxId===id,id);assert.equal(await query.inputValue(),title);assert.equal(await vessel.inputValue(),ship);assert.equal(await project.inputValue(),'LOCAL-123');assert.equal(await filters.evaluate(e=>e.open),false);assert(Math.abs((await a.boundingBox()).y-top)<4);
  // Forward re-enters the same full record, including after a previous Back
  // already restored the row. Release the read only after focus returns.
  const detailPath='/api/toolbox/talks/'+id;
  const isDetail=url=>url.pathname===detailPath;
  for(const result of ['success','error']){
   let release;
   const gate=new Promise(resolve=>{release=resolve;});
   const hold=async route=>{
    await gate;
    if(result==='error')await route.fulfill({status:503,contentType:'application/json',body:'{"error":"Fictional fixture unavailable"}'});
    else await route.continue();
   };
   await p.route(isDetail,hold);
   try{
    const started=p.waitForRequest(request=>isDetail(new URL(request.url())));
    await p.goForward();await started;
    await p.locator('#tb-read-state').waitFor();
    await p.goBack();
    await p.waitForFunction(id=>document.activeElement?.dataset.toolboxId===id,id,{timeout:4500});
    assert.equal(await query.inputValue(),title);
    assert.equal(await vessel.inputValue(),ship);
    assert.equal(await project.inputValue(),'LOCAL-123');
    assert.equal(await filters.evaluate(e=>e.open),false);
    assert(Math.abs((await a.boundingBox()).y-top)<4);
    const readFinished=p.waitForEvent('requestfinished',{predicate:r=>isDetail(new URL(r.url()))});
    release();await readFinished;
    await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
    assert.equal(new URL(p.url()).hash,'#toolbox');
    assert.equal(await a.evaluate(e=>document.activeElement===e),true);
    assert.equal(await p.locator('#tb-read-state,.tb-talk-preview,.tb-stale').count(),0);
   }finally{release();await p.unroute(isDetail,hold);}
  }
  console.log('PASS Toolbox',width,'settled and interrupted return, filtered identity and focus');
 } finally {await p.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const width of [1360,389])await check(browser,width)}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});