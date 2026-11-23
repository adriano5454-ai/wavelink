const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');
const origin = new URL(process.argv[2]);
assert(['https://127.0.0.1:18553','https://demo.mywavelink.com'].includes(origin.origin));

async function verify(browser,width) {
 const page = await browser.newPage({viewport:{width,height:900},serviceWorkers:'block',ignoreHTTPSErrors:origin.hostname==='127.0.0.1'});
 try {
  await page.goto(origin.origin+'/__demo/public?area=faults');
  await page.waitForFunction(()=>location.search.includes('public_demo=1'));
  await page.waitForFunction(()=>document.querySelector('[href="#faults"]') || document.querySelector('#hr-section-select') || document.querySelector('#fr-workspace') || location.hash==='#home');
  await page.evaluate(()=>{location.hash='faults'});
  const panel=page.locator('#fr-filter-panel'), list=page.locator('#fr-list');
  const query=page.locator('#fr-query'), active=page.locator('#fr-applied');
  const toggle=panel.locator('summary');
  const open=()=>panel.evaluate(e=>e.open);
  const run=async(action,match)=>{
   const next=page.waitForResponse(r=>{
    const u=new URL(r.url());
    return u.pathname==='/api/faults' && r.request().method()==='GET' && match(u.searchParams);
   });
   await action();
   const response=await next;
   assert.equal(response.status(),200);
   const result=await response.json();
   await page.waitForFunction(total=>document.querySelectorAll('#fr-list .fr-row').length===Math.min(100,total),result.total);
   return result;
  };
  await list.locator('.fr-row').first().waitFor();
  assert.equal(await open(),width>800);
  if(!await open()) await toggle.click();
  if(width>800) assert((await panel.boundingBox()).x < (await query.boundingBox()).x);
  await run(()=>page.locator('#fr-status').selectOption('all'),p=>p.get('status')==='all');
  await run(()=>page.locator('#fr-assignment').selectOption('mine'),p=>p.get('assignment')==='mine');
  assert.match(await active.innerText(),/Assigned to me/i);
  const vessel=panel.locator('[data-page-vessel]');
  await vessel.locator('option').nth(1).waitFor({state:'attached'});
  const option=await vessel.locator('option').nth(1).evaluate(e=>({value:e.value,label:e.textContent}));
  await run(()=>vessel.selectOption(option.value),p=>p.get('vessel_id')===option.value);
  await page.waitForFunction(label=>document.getElementById('fr-applied').textContent.includes(label),option.label);
  await toggle.click();
  await query.fill('fixture-no-such-report-6721');
  const empty=await run(()=>query.press('Enter'),p=>p.get('query')==='fixture-no-such-report-6721'&&p.get('assignment')==='mine'&&p.get('vessel_id')===option.value);
  assert.equal(empty.total,0);
  assert.match(await active.innerText(),/fixture-no-such-report-6721/);
  await page.setViewportSize({width:width>800?390:1360,height:900});
  if(!await open())await toggle.click();
  assert.equal(await page.locator('#fr-assignment').inputValue(),'mine');
  const refreshed=await run(()=>page.getByRole('button',{name:'Clear filters'}).click(),p=>p.get('status')==='active'&&!p.get('query')&&!p.get('vessel_id')&&p.get('assignment')==='all');
  assert(refreshed.total>0);
  await Promise.all([page.waitForResponse(r=>new URL(r.url()).pathname.startsWith('/api/faults/') && r.status()===200),list.locator('.fr-row').first().click()]);
  await page.evaluate(()=>{location.hash='home'});
  await panel.waitFor({state:'detached'});
  await page.evaluate(()=>{location.hash='faults'});
  await list.locator('.fr-row').first().waitFor();
  assert(await query.isVisible());
  assert(await panel.evaluate(e=>e.closest('#fr-workspace').scrollWidth<=e.closest('#fr-workspace').clientWidth+1));
  console.log(JSON.stringify({width,reports:refreshed.total,vessel:option.label,combinedResults:empty.total}));
 } finally {await page.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const width of [1360,390])await verify(browser,width)}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
