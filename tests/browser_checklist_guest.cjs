const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);assert.equal(origin.hostname,'127.0.0.1');
async function run(browser,width,view,ref){
 const p=await browser.newPage({viewport:{width,height:919},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try{
  await p.goto(origin.origin+'/__demo/public?area=hr');
  await p.locator('#hr-section-select').waitFor({state:'attached'});
  if(width===390&&process.argv[3]!=='baseline'){
   await p.evaluate(()=>location.hash='profile');await p.locator('#wl-language-select').selectOption('pt-BR');
   await p.locator('#profile-language button').click();await p.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
  }
  await p.evaluate(()=>location.hash='checklists');
  await p.locator('[data-cw-view="'+view+'"]').click();
  const q=p.locator('#checklist-search');await q.fill(ref);
  const card=p.locator('article[data-cw-card]').filter({hasText:ref});await card.waitFor();
  const id=await card.getAttribute('data-cw-card'), requests=[];
  p.on('response',r=>{if(new URL(r.url()).pathname.includes('/api/records/'+id))requests.push([r.request().method(),new URL(r.url()).pathname.split(id)[1],r.status()])});
  await card.locator('[data-cw-open]').click();
  if(process.argv[3]==='baseline'){await p.locator('#record-access-unavailable').waitFor();console.log('baseline',ref,requests);return;}
  const panel=p.locator('#checklist-inspector');await panel.locator('.cw-item-list').waitFor();assert.equal(await panel.locator('h2').innerText(),ref);
  await panel.locator('[data-cw-read-stage]').first().click();await p.waitForFunction(()=>document.activeElement.id==='cw-preview-items');
  await panel.locator('details').filter({has:p.locator('[data-cw-read-stage]')}).locator('summary').click();await panel.locator('details [data-cw-read-stage]').first().click();await p.waitForFunction(()=>document.activeElement.id==='cw-preview-items');
  assert.equal(await panel.locator('[href^="#dive/"]').count(),0);
  assert.equal(new URL(p.url()).hash,'#checklists');assert(requests.some(([m,s,c])=>m==='GET'&&!s&&c===200));
  assert(requests.every(([m])=>m==='GET'));await panel.locator('#cw-back-list').click();
  assert.equal(await q.inputValue(),ref);assert.equal(await p.locator('[data-cw-view="'+view+'"]').getAttribute('aria-pressed'),'true');
  await p.waitForFunction(id=>document.activeElement.dataset.cwSelect===id||document.activeElement.dataset.cwOpen===id,id);
  console.log('PASS',width,view,ref,'saved items, read only, filter and focus');
 }finally{await p.close();}
}
(async()=>{const b=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,390])for(const [view,ref] of [['closed','DEMO-CHECK-004'],['open','DEMO-CHECK-001']])await run(b,w,view,ref)}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
