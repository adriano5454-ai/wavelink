const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);
assert.equal(origin.hostname,'127.0.0.1');

async function verify(browser,width){
 const page=await browser.newPage({viewport:{width,height:900},serviceWorkers:'block',ignoreHTTPSErrors:true});
 try {
  await page.goto(origin.origin+'/__demo/public?area=hr');
  const sections=page.locator('#hr-section-select');
  await sections.waitFor({state:'attached'});
  if(await sections.isVisible())await sections.selectOption('calendar');
  else await page.locator('[data-hr-tab="calendar"]').click();
  const box=page.locator('#hr-location-roster'), results=box.locator('[data-location-results]');
  await box.locator('summary').first().click();
  const day=box.locator('[name=roster_day]'), until=box.locator('[name=roster_until]');
  const offset=d=>{const t=new Date(today+'T12:00:00Z');t.setUTCDate(t.getUTCDate()+d);return t.toISOString().slice(0,10)};
  const today=await day.inputValue(),start=offset(-4),end=offset(13);
  await day.fill(start);
  const response=page.waitForResponse(r=>r.request().method()==='GET'&&new URL(r.url()).pathname==='/api/hr/workspace'&&new URL(r.url()).searchParams.get('end_on')===end);
  await until.fill(end);
  assert.equal((await response).status(),200);
  await results.getByText('Cleo Finch',{exact:true}).waitFor();
  const groups=results.locator('article');
  assert.equal(await groups.count(),4);
  assert.equal(await groups.locator('li').count(),18);
  const names=await groups.locator('strong').allTextContents();
  assert.equal(new Set(names).size,16);
  for(const [name,cut] of [['Mira Vale',3],['Idris Fen',4]]){
   const legs=groups.locator('section').filter({has:page.getByText(name,{exact:true})});
   assert.equal(await legs.count(),2);
   const rows=await legs.locator('li').allInnerTexts();
   assert(rows.some(s=>s.includes('Planned leaving '+offset(cut))));
   assert(rows.some(s=>s.includes('Planned joining '+offset(cut+1))));
  }
  console.log(width,start,end,await groups.locator('h3').allInnerTexts());
  await box.locator('[name=roster_project]').fill('DEMO-101');
  await box.locator('[name=roster_project]').press('Enter');
  await page.waitForFunction(()=>document.querySelectorAll('[data-location-results] article li').length===5);
  assert.equal(await groups.count(),3);
  assert((await groups.locator('li').allInnerTexts()).every(s=>s.includes('DEMO-101')));
  assert(await box.evaluate(e=>e.scrollWidth<=e.clientWidth+1));
  if(process.env.ROSTER_PREVIEW){
   await page.setViewportSize({width,height:2000});
   await box.evaluate(e=>{e.scrollIntoView();window.scrollBy(0,-100);document.activeElement.blur()});
   await box.screenshot({path:process.env.ROSTER_PREVIEW+'-'+width+'.png'});
  }
 }finally{await page.close()}
}
(async()=>{const b=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const width of [1360,390])await verify(b,width)}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
