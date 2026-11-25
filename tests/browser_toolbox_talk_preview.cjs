const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);assert.equal(origin.hostname,'127.0.0.1');
async function check(browser,width){
 const page=await browser.newPage({viewport:{width,height:919},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try{
  await page.goto(origin.origin+'/__demo/public?area=hr');
  await page.locator('#hr-section-select').waitFor({state:'attached'});
  await page.evaluate(()=>location.hash='toolbox');
  const rows=page.locator('#tb-results a[data-toolbox-id]'),panel=page.locator('.tb-talk-preview');
  await rows.nth(1).waitFor();const initial=await rows.evaluateAll(es=>es.map(e=>({id:e.dataset.toolboxId,title:e.querySelector('h2').textContent,status:e.querySelector('.eyebrow').textContent.split(' ')[0]})));
  let detailReads=0;page.on('request',r=>{if(new URL(r.url()).pathname.startsWith('/api/toolbox/talks/'))detailReads++});
  const seen=new Set();
  for(const r of initial){
   const row=rows.and(page.locator('[data-toolbox-id="'+r.id+'"]'));
   await row.click();await panel.getByRole('heading',{name:r.title,exact:true}).waitFor();
   assert.equal(new URL(page.url()).hash,'#toolbox');assert.equal(await panel.getByRole('button').count(),1);
   assert.equal(await panel.getByRole('link').getAttribute('href'),await row.evaluate(e=>e.href));
   assert.equal(await panel.evaluate(e=>e.tagName),width>800?'SECTION':'DIALOG');seen.add(r.status);assert.equal((await panel.locator('dt').filter({hasText:/^Status$/}).locator('xpath=following-sibling::dd[1]').innerText()).toLowerCase(),r.status.toLowerCase());
   if(width>800){const a=await row.boundingBox(),b=await panel.boundingBox();assert(a.x+a.width<=b.x+1);}
   await page.keyboard.press('Escape');await panel.waitFor({state:'detached'});
   await page.waitForFunction(id=>document.activeElement.dataset.toolboxId===id,r.id);
   await page.goForward();await panel.getByRole('heading',{name:r.title,exact:true}).waitFor();
   await panel.getByRole('button').click();await panel.waitFor({state:'detached'});
  }
  assert.equal(detailReads,0);assert.deepEqual([...seen].map(s=>s.toLowerCase()).sort(),['finalised','open']);
  if(width>800){await rows.first().click();await rows.nth(1).click();await panel.getByRole('heading',{name:initial[1].title,exact:true}).waitFor();await panel.getByRole('button').click();await panel.waitFor({state:'detached'});}
  await rows.first().click();await panel.getByRole('link').click();await page.getByRole('heading',{name:'Signing actions'}).waitFor();await page.reload();await page.getByRole('heading',{name:'Signing actions'}).waitFor();
  console.log('PASS preview',width,'states',Array.from(seen),'talks',initial.length,'no detail reads before full open');
 }finally{await page.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const width of [1360,390])await check(browser,width)}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});