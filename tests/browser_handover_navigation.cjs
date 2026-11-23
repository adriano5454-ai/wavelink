'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);
assert.equal(origin.hostname,'127.0.0.1');
async function check(browser,width,pt){
 const page=await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 const writes=[];
 page.on('request',r=>{if(new URL(r.url()).pathname.startsWith('/api/handovers')&&r.method()!=='GET')writes.push(r.method())});
 try{
  await page.goto(origin.origin+'/__demo/public?area=hr');
  await page.locator('#hr-section-select').waitFor({state:'attached'});
  if(pt){
   await page.evaluate(()=>location.hash='profile');
   await page.locator('#wl-language-select').selectOption('pt-BR');await page.locator('#profile-language button').click();
   await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
  }
  await page.evaluate(()=>location.hash='handovers');
  await page.locator('.hwd-record').first().waitFor();
  assert.equal(await page.locator('.ho-nav-group strong').first().innerText(),pt?'Encontrar passagens':'Find handovers');
  const vessel=page.locator('#ho-vessel-filter select');
  await vessel.selectOption({label:'MV Aurora · AUR'});
  const subject=page.locator('#hwd-subject');
  await subject.selectOption({label:'MV Aurora · Offshore Survey'});
  const days=page.locator('.hwd-day');
  await days.nth(1).waitFor({state:'attached'});
  const day=await days.nth(1).getAttribute('data-hwd-day');
  await page.locator('#hwd-jump').selectOption(day);
  const trigger=days.nth(1).locator('[data-hwd-open]').first(),id=await trigger.getAttribute('data-hwd-open');
  const before=[await vessel.inputValue(),await subject.inputValue(),day];
  await trigger.click();
  const panel=page.locator('#ho-record-preview');
  await panel.locator('.hop-next-action').waitFor();
  assert.equal(await panel.locator('.hop-next-action').evaluate(e=>getComputedStyle(e).borderInlineStartWidth),'3px');
  assert.match(await panel.locator('.hop-note').first().innerText(),/Review the night navigation check sheet/);
  await panel.locator('.hop-evidence summary').click();
  const download=page.waitForEvent('download');await panel.locator('[data-ha-open]').first().click();
  assert.equal((await download).suggestedFilename(),'Night-navigation-checks.txt');
  await panel.locator('.hop-head button').click();
  assert.equal(await panel.count(),0);
  assert.deepEqual([await vessel.inputValue(),await subject.inputValue(),await days.nth(1).getAttribute('data-hwd-day')],before);
  assert.equal(await page.evaluate(()=>document.activeElement.dataset.hwdOpen),id);
  await page.locator('#hwd-jump').selectOption(await days.first().getAttribute('data-hwd-day'));
  const own=days.first().locator('.hwd-record').first();assert.match(await own.innerText(),/Demo Manager/);
  await own.locator('[data-hwd-open]').click();await panel.locator('.hop-context').waitFor();
  assert.match(await panel.locator('.hop-context').innerText(),/Demo Manager/);
  await panel.locator('.hop-head button').click();await page.locator('#ho-tab-drafts').click();
  await page.locator('#ho-resume:visible').waitFor();
  assert.deepEqual(writes,[]);console.log('PASS',width,pt?'pt-BR':'en',day);
 }finally{await page.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,390])for(const pt of [false,true])await check(browser,w,pt)}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
