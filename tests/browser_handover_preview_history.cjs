const {chromium}=require('playwright-core'),assert=require('node:assert/strict');const base=new URL(process.argv[2]);assert.equal(base.hostname,'127.0.0.1');const baseline=process.argv.includes('baseline');
async function run(p,width){
 await p.getByRole('link',{name:'All workspaces',exact:true}).first().click();
 await p.locator('#home-handovers').click();
 const ship=p.locator('#ho-vessel-filter select'),team=p.locator('#hwd-subject'),jump=p.locator('#hwd-jump');
 await ship.selectOption(await ship.locator('option').filter({hasText:/Meridian/i}).getAttribute('value'));
 await team.selectOption(await team.locator('option').filter({hasText:/DEMO Survey/i}).first().getAttribute('value'));
 const date=await jump.locator('option[value$="-09-23"]').getAttribute('value');await jump.selectOption(date);
 const day=p.locator('[data-hwd-day="'+date+'"]'),buttons=day.locator('[data-hwd-open]');
 assert.equal(await buttons.count(),2);const shipId=await ship.inputValue(),teamId=await team.inputValue();
 for(let i=0;i<2;i++){
  const b=buttons.nth(i),id=await b.getAttribute('data-hwd-open');await b.scrollIntoViewIfNeeded();const y=(await b.boundingBox()).y;
  const panel=p.locator('#ho-record-preview');await b.click();await panel.locator('h2').waitFor();
  const title=await panel.locator('h2').innerText(),rev=await panel.locator('.hwd-state').innerText();
  await p.goBack();if(baseline){console.log('baseline',width,new URL(p.url()).hash);await p.goForward();await jump.waitFor();console.log('forward',await team.locator('option:checked').innerText(),await jump.inputValue());return;}
  await panel.waitFor({state:'detached'});assert.equal(new URL(p.url()).hash,'#handovers');assert.deepEqual([await ship.inputValue(),await team.inputValue(),await jump.inputValue()],[shipId,teamId,date]);
  assert(await b.evaluate(e=>document.activeElement===e));assert(Math.abs((await b.boundingBox()).y-y)<4);
  await p.goForward();await panel.locator('h2').waitFor();assert.equal(await panel.locator('h2').innerText(),title);assert.equal(await panel.locator('.hwd-state').innerText(),rev);assert.equal(await b.getAttribute('aria-expanded'),'true');
  await panel.locator('.hop-head button').click();await panel.waitFor({state:'detached'});assert(await b.evaluate(e=>document.activeElement===e));console.log('PASS',width,date,id,title,rev);
 }
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const width of [1360,389]){const p=await browser.newPage({viewport:{width,height:919},ignoreHTTPSErrors:true,serviceWorkers:'block'});try{await p.goto(base.origin+'/__demo/public?area=hr');await p.locator('#hr-section-select').waitFor({state:'attached'});await run(p,width)}finally{await p.close()}}}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});