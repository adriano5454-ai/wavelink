'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
async function visit(page,hash){
 const url=new URL(page.url());url.hash=hash;await page.goto(url.href);
}
async function main(){
 const [url,lang='en']=process.argv.slice(2),pt=lang==='pt';
 const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
 try{
  const context=await browser.newContext({viewport:{width:1280,height:850},ignoreHTTPSErrors:true,serviceWorkers:'block'});
  const page=await context.newPage();page.setDefaultTimeout(10000);
  const writes=[],previews=[];
  page.on('request',req=>{
   const u=new URL(req.url());if(!u.pathname.startsWith('/api/handovers'))return;
   if(req.method()!=='GET')writes.push(req.method()+' '+u.pathname);
   if(u.pathname.endsWith('/preview'))previews.push(u);
  });
  await page.goto(url);await page.locator('#wl-global-search-trigger:visible').waitFor({timeout:45000});
  if(pt){
   await visit(page,'profile');
   for(let i=0;i<4 && await page.locator('html').getAttribute('lang')!=='pt-BR';i++){
    await page.locator('#wl-language-select').selectOption('pt-BR');
    await page.locator('#profile-language button').click({timeout:1800}).catch(()=>{});
   }
   await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
  }
  await visit(page,'handovers');
  const panel=page.locator('#ho-record-preview'),heading=panel.locator('.hop-body h2'),evidence=panel.locator('.hop-evidence');
  const book=page.locator('.hwd-day[open] .hwd-record').first(),trigger=book.locator('[data-hwd-open]');
  await book.waitFor();const ident=await trigger.getAttribute('data-hwd-open');
  await book.click({position:{x:9,y:9}});await heading.waitFor();
  const title=await heading.innerText();
  assert.equal(previews.at(-1).pathname,`/api/handovers/${ident}/preview`);
  assert.ok(await panel.locator('.hop-note').count());
  assert.ok(await panel.locator('.hop-context').textContent());
  assert.match(await evidence.locator('summary').innerText(),pt?/Fotos e documentos/:/Photos and documents/);
  await evidence.locator('summary').click();assert.ok(await evidence.getAttribute('open')!==null);
  const file=evidence.locator('[data-ha-open]').first();
  await file.waitFor();
  const download=page.waitForEvent('download');
  await file.click();
  assert.match((await download).suggestedFilename(),/^(Day-survey-coverage|Night-navigation-checks)\.txt$/);
  const back=panel.locator('.hop-head button');
  for(const width of [1360,1280,1024,850,390,320]){
   await page.setViewportSize({width,height:850});
   const g=await panel.evaluate(p=>{
    const list=p.previousElementSibling,b=list.getBoundingClientRect(),s=p.getBoundingClientRect();
    return {scroll:document.documentElement.scrollWidth,w:innerWidth,left:s.left,right:s.right,side:b.width>0&&b.right<=s.left+1,one:b.width===0};
   });
   assert.ok(g.scroll<=width+1&&g.left>=-1&&g.right<=width+1,`${width} ${JSON.stringify(g)}`);
   assert.ok(width>850?g.side:g.one,`${width} preview placement`);
  }
  await back.click();assert.equal(await panel.count(),0);
  assert.equal(await trigger.evaluate(b=>document.activeElement===b),true);
  await trigger.press('Enter');await heading.waitFor();assert.equal(await heading.innerText(),title);
  await back.press('Escape');assert.equal(await panel.count(),0);
  await page.setViewportSize({width:1280,height:850});
  await page.locator('#ho-tab-incoming').click();
  const incoming=page.locator('#ho-incoming .ho-card').first();await incoming.waitFor();
  const chosen=incoming.locator('[data-ho-incoming]'),incomingId=await chosen.getAttribute('data-ho-incoming'),revision=await chosen.getAttribute('data-ho-incoming-revision');
  const publishedResponse=page.waitForResponse(r=>new URL(r.url()).pathname.endsWith('/preview'));
  await incoming.locator('h3').click();await heading.waitFor();
  const published=await (await publishedResponse).json();
  assert.equal(previews.at(-1).pathname,`/api/handovers/${incomingId}/preview`);
  assert.equal(previews.at(-1).searchParams.get('revision'),revision);
  assert.equal(await panel.locator('.hop-actions button').count(),1);
  assert.ok(await page.locator('#ho-detail').isHidden());
  await page.locator('#ho-incoming-search').fill('no such handover');await panel.waitFor({state:'detached'});
  await page.locator('#ho-incoming-search').fill('');
  let releaseResponse,notifyStarted;
  const hold=new Promise(resolve=>{releaseResponse=resolve});
  const started=new Promise(resolve=>{notifyStarted=resolve});
  await page.route('**/api/handovers/*/preview*',async route=>{notifyStarted();await hold;await route.fulfill({json:published});},{times:1});
  await chosen.click();await started;
  await page.locator('#ho-tab-days').click();
  const late=page.waitForResponse(r=>new URL(r.url()).pathname.endsWith('/preview'));releaseResponse();await late;
  await page.locator('.hwd-day[open] .hwd-record').first().waitFor();
  assert.equal(await panel.count(),0);
  await page.locator('#ho-tab-incoming').click();await incoming.waitFor();
  await page.route('**/api/handovers/*/preview*',route=>route.fulfill({status:403,json:{error:'Unavailable'}}),{times:1});
  await incoming.locator('h3').click();await panel.locator('[role=status]').filter({hasText:pt?'indisponível':'unavailable'}).waitFor();
  assert.equal(await heading.count(),0);assert.equal(await panel.locator('.hop-actions button').count(),0);
  await back.click();
  await chosen.click();await heading.waitFor();
  await panel.locator('.hop-actions button').click();await page.locator('#ho-detail:visible #ho-reader-title').waitFor();
  assert.deepEqual(writes,[],'preview and reading did not submit handover changes');
  console.log(`${lang}: day and incoming card previews, keyboard, six widths, evidence, filtered/denied access and full reader passed`);
 }finally{await browser.close();}
}
main().catch(error=>{console.error(error);process.exitCode=1;});
