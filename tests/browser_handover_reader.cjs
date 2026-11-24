const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);assert.equal(origin.hostname,'127.0.0.1');
async function check(browser,width,pt){
 const page=await browser.newPage({viewport:{width,height:950},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 let keys,mode='original';const writes=[];
 page.on('request',r=>{if(new URL(r.url()).pathname.startsWith('/api/handovers')&&r.method()!=='GET')writes.push(r.method())});
 try{
  await page.route('**/api/handovers/directory',async route=>{const response=await route.fetch();keys=(await response.json()).sections.map(x=>x[0]);await route.fulfill({response});});
  await page.route(/\/api\/handovers\/[a-f0-9-]{36}(?:\?|$)/,async route=>{
   const response=await route.fetch(),record=await response.json();
   if(mode!=='original'&&record.publication)for(const k of keys)record.publication.edit[k]=mode==='empty'?'   ':'QA '+k;
   await route.fulfill({response,json:record});
  });
  await page.goto(origin.origin+'/__demo/public?area=hr');await page.locator('#hr-section-select').waitFor({state:'attached'});
  if(pt){await page.evaluate(()=>location.hash='profile');await page.locator('#wl-language-select').selectOption('pt-BR');await page.locator('#profile-language button').click();await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();}
  for(mode of ['original','empty','filled']){
   await page.evaluate(()=>location.hash='handovers');await page.locator('#ho-tab-incoming').click();await page.locator('[data-ho-incoming]').first().click();
   await page.locator('.hop-actions button').first().click();const reader=page.locator('.ho-publication-reader');await reader.waitFor();
   const notes=reader.locator('[data-ho-read-section]');assert.equal(await reader.locator('.ho-reader-nav,.ho-read-blank').count(),0);
   assert.equal(await reader.locator('#ho-reader-notes-start').isVisible(),mode!=='empty');
   if(mode==='empty'){assert.equal(await notes.count(),0);await reader.getByText(pt?'Nenhuma nota registrada nesta revisão.':'No notes recorded in this revision.').waitFor();}
   else{
    assert.equal(await notes.first().getAttribute('data-ho-read-section'),'next_actions');await reader.locator('#ho-reader-notes-start').click();
    assert.equal(await page.evaluate(()=>document.activeElement.id),'ho-read-next_actions');
    if(mode==='filled'){assert.equal(await notes.count(),keys.length);for(const k of keys)assert.equal(await notes.locator('p').filter({hasText:new RegExp('^QA '+k+'$')}).count(),1);}
   }
   assert(await reader.evaluate(e=>e.scrollWidth<=e.clientWidth+1));
   if(process.env.HANDOVER_READER_PREVIEW && mode==='original'&&!pt)await reader.screenshot({path:process.env.HANDOVER_READER_PREVIEW+'-'+width+'.png'});
   const file=page.locator('#ho-detail [data-ha-open]').first();await file.waitFor();
   const dl=page.waitForEvent('download');await file.click();assert.match((await dl).suggestedFilename(),/\.txt$/);
   await reader.locator('#ho-reader-ack-jump').click();assert.equal(await page.evaluate(()=>document.activeElement.id),'ho-acknowledgement');
   await page.evaluate(()=>location.hash='home');await reader.waitFor({state:'detached'});
  }
  assert.deepEqual(writes,[]);console.log('PASS',width,pt?'pt-BR':'en',keys.length,'sections');
 }finally{await page.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,390])for(const pt of [false,true])await check(browser,w,pt)}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
