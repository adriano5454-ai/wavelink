const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);
assert.equal(origin.hostname,'127.0.0.1');

async function verify(browser,width,pt){
 const page=await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 const go=route=>page.evaluate(r=>{location.hash=r},route);
 const open=async id=>{const panel=page.locator(id);if(!await panel.evaluate(e=>e.open))await panel.locator('summary').click();};
 const toggle=id=>page.locator(id+' summary').click();
 const checkText=async(id,text)=>page.waitForFunction(([id,text])=>document.querySelector(id)?.textContent.includes(text),[id,text]);
 try{
  await page.route('**/api/toolbox',async route=>{
   const response=await route.fetch(), data=await response.json();
   assert(response.ok() && data.talks.length>=2);
   const [ship1,ship2]=data.sites.filter(s=>s.type==='vessel'||s.kind==='vessel');
   assert(ship1 && ship2);
   const cases=[[ship1,'TEST-101','Deck inspection'],[ship2,'TEST-101','Deck inspection'],[ship1,'TEST-202','Deck inspection'],[ship1,'TEST-101','Bridge briefing'],[ship1,null,'Legacy briefing']];
   data.talks=cases.map(([ship,project,title],i)=>{
    const t=structuredClone(data.talks[i%2]);
    t.id='00000000-0000-4000-a000-'+String(i+1).padStart(12,'0');
    t.work_site={id:ship.id,name:ship.name,code:ship.code};
    t.meta.work_description=title;
    if(project)t.meta.project_number=project;
    else delete t.meta.project_number;
    return t;
   });
   await route.fulfill({response,json:data});
  });
  await page.goto(origin.origin+'/__demo/public?area=hr');
  await page.locator('#hr-section-select').waitFor({state:'attached'});
  if(pt){
   await go('profile');await page.locator('#wl-language-select').selectOption('pt-BR');
   await page.locator('#profile-language button').click();await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
  }
  await go('toolbox');
  const panel=page.locator('#tb-filter-panel'), query=page.locator('#tb-query'), cards=page.locator('[data-toolbox-id]');
  await query.waitFor();assert.equal(await panel.evaluate(e=>e.open),width>800);
  assert.equal(await panel.locator('summary').innerText(),pt?'Filtros':'Filters');
  await open('#tb-filter-panel');if(width>800)assert((await panel.boundingBox()).x<(await query.boundingBox()).x);
  assert.equal(await cards.count(),5);
  await query.fill('test-101');assert.equal(await cards.count(),3);
  await query.fill('Deck');await page.locator('#tb-project').selectOption('TEST-101');assert.equal(await cards.count(),2);
  const vessel=page.locator('#tb-filters [data-page-vessel]');
  const options=await vessel.locator('option').evaluateAll(opts=>opts.slice(1).map(x=>x.value));
  let found=false;
  for(const option of options){await vessel.selectOption(option);if(await cards.count()===1){found=true;break;}}
  assert(found);assert.match(await cards.first().innerText(),/TEST-101/);
  await toggle('#tb-filter-panel');await checkText('#tb-active','TEST-101');
  assert(await query.isVisible());await query.fill('absent');assert.equal(await cards.count(),0);
  await open('#tb-filter-panel');await page.locator('#tb-clear').click();assert.equal(await cards.count(),5);
  await query.fill('Legacy');assert.equal(await cards.count(),1);assert.doesNotMatch(await cards.first().innerText(),/TEST-101|TEST-202/);
  await go('qshe');const qs=page.locator('#qs-filter-panel');await qs.waitFor();
  assert.equal(await qs.evaluate(e=>e.open),width>800);
  assert.equal(await page.locator('.qs-related h2').innerText(),pt?'Áreas relacionadas':'Related workspaces');
  await open('#qs-filter-panel');
  const category=page.locator('#qs-category');await category.selectOption({index:1});
  const categoryText=await category.locator('option:checked').innerText();await checkText('#qs-active',categoryText);
  await toggle('#qs-filter-panel');await page.locator('#qs-query').fill('no-match-test');await page.locator('#qs-query').press('Enter');
  await checkText('#qs-active','no-match-test');await open('#qs-filter-panel');await page.locator('#qs-clear').click();
  assert.equal(await category.inputValue(),'all');assert.equal(await page.locator('#qs-query').inputValue(),'');
  await page.locator('.qs-related a[href="#toolbox"]').click();await query.waitFor();await go('faults');await page.locator('#fr-filter-panel').waitFor();
  assert.equal(await page.locator('#fr-filter-panel').evaluate(e=>e.open),width>800);
  await go('qshe');await qs.waitFor();
  assert(await qs.evaluate(e=>e.closest('#qs-workspace').scrollWidth<=e.closest('#qs-workspace').clientWidth+1));
  console.log('PASS',width,pt?'pt-BR':'en');
 }finally{await page.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const width of [1360,390])for(const pt of [false,true])await verify(browser,width,pt)}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
