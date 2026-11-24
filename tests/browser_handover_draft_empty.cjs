const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);
assert.equal(origin.hostname,'127.0.0.1');
async function check(browser,width,pt){
 const page=await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 let inject=false, deny=false;
 const writes=[];
 page.on('request',r=>{if(new URL(r.url()).pathname.startsWith('/api/handovers')&&r.method()!=='GET')writes.push(r.method())});
 try{
  await page.route('**/api/handovers?*',async route=>{
   const response=await route.fetch(),data=await response.json();
   if(inject){
    const row={...data.rows[0],daily:null,kind:'full_hitch',state:'private_draft',archived:false,mine:true,title:'QA private rotation',published_revision:0,location:'MV Aurora'};
    data.rows.push({...row,id:'00000000-0000-4000-a000-000000000001'},{...row,id:'00000000-0000-4000-a000-000000000002',mine:false,title:'Other fictional author'});
   }
   await route.fulfill({response,json:data});
  });
  await page.route('**/api/handovers/directory',async route=>{
   const response=await route.fetch(),data=await response.json();if(deny)data.can_create=false;
   await route.fulfill({response,json:data});
  });
  await page.goto(origin.origin+'/__demo/public?area=hr');await page.locator('#hr-section-select').waitFor({state:'attached'});
  if(pt){await page.evaluate(()=>location.hash='profile');await page.locator('#wl-language-select').selectOption('pt-BR');await page.locator('#profile-language button').click();await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();}
  await page.evaluate(()=>location.hash='handovers');await page.locator('.hwd-record').first().waitFor();
  await page.locator('#ho-tab-drafts').click();
  const start=page.locator('#ho-drafts-start'),all=page.locator('#ho-drafts-all'),list=page.locator('#ho-resume-list,.ho-resume-list');
  assert.equal(await start.innerText(),pt?'Iniciar rascunho':'Start a draft');
  await start.click();await page.locator('#handover-choice-grid').waitFor();await page.keyboard.press('Escape');
  await start.waitFor();inject=true;
  await page.locator('#ho-refresh').click();await list.getByText('QA private rotation').waitFor();assert.equal(await list.getByText('Other fictional author').count(),0);
  const vessel=page.locator('#ho-vessel-filter select');await vessel.selectOption({label:'DEMO Horizon · DEMO-HORIZON'});
  assert.equal(await all.innerText(),pt?'Mostrar todas as embarcações':'Show all vessels');
  assert.equal(await start.count(),0);await all.click();await list.getByText('QA private rotation').waitFor();assert.equal(await vessel.inputValue(),'');
  assert.equal(await list.locator('[data-ho-resume]').count(),1);
  inject=false;deny=true;await page.locator('#ho-refresh').click();await list.getByText(pt?'Você não tem rascunhos salvos.':'You have no saved drafts.').waitFor();assert.equal(await start.count(),0);
  assert.deepEqual(writes,[]);console.log('PASS',width,pt?'pt-BR':'en');
 }finally{await page.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,390])for(const pt of [false,true])await check(browser,w,pt)}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
