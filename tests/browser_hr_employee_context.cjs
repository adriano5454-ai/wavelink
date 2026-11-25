const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');

async function check(browser,port,width,guest,pt){
 const p=await browser.newPage({viewport:{width,height:width>700?900:844},hasTouch:width<700,ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try{
  const origin='https://127.0.0.1:'+port;
  await p.goto(origin+(guest?'/__demo/public?area=hr':''));
  if(!guest){
   await p.locator('input[type=text]:visible').fill('demo.admin');
   await p.locator('#login-password').fill(process.env.ORG_QA_PASSWORD);await p.locator('#login-password').press('Enter');
   await p.locator('#wl-global-search-trigger:visible').waitFor();
   await p.evaluate(()=>location.hash='hr');
  }
  const tabs=p.locator('#hr-section-select');await tabs.waitFor({state:'attached'});
  if(await tabs.isVisible())await tabs.selectOption('people');else await p.locator('[data-hr-tab=people]').click();
  const list=p.locator('.hr-person-list'),q=p.locator('#hr-people-search'),title=p.locator('.ux-profile-hero h2');
  await list.waitFor();
  const lower=list.locator('button').last();await lower.scrollIntoViewIfNeeded();await lower.focus();
  const scrolled=await list.evaluate(e=>e.scrollTop);assert(scrolled>0);
  const lowerName=(await lower.locator('strong').innerText()).split(' · ')[0];
  await p.keyboard.press('Enter');await title.filter({hasText:lowerName}).waitFor();
  assert.equal(await list.evaluate(e=>e.scrollTop),scrolled);assert(await lower.evaluate(e=>document.activeElement===e));
  await q.fill('Offshore Survey');
  const total=await list.locator('li:visible').count();assert(total>=2);
  const person=name=>list.getByRole('button',{name:new RegExp(name)});
  const lia=person('Lia Costa'),rafael=person('Rafael Lima');
  const liaId=await lia.getAttribute('data-hr-person-link');
  await list.evaluate(e=>window.employeeList=e);
  let release,started;const pending=new Promise(r=>started=r),gate=new Promise(r=>release=r);
  await p.route('**/api/hr/overview?**',async route=>{
   if(new URL(route.request().url()).searchParams.get('user_id')===liaId){
    const response=await route.fetch();started();await gate;await route.fulfill({response}).catch(()=>{});
   }else await route.continue();
  });
  await lia.click();await pending;await rafael.focus();await p.keyboard.press('Enter');
  await title.filter({hasText:'Rafael Lima'}).waitFor();release();await p.unrouteAll({behavior:'wait'});
  assert.equal(await list.locator('li:visible').count(),total);
  assert(await list.evaluate(e=>e===window.employeeList));assert.equal(await rafael.getAttribute('aria-current'),'true');
  assert.equal(await title.innerText(),'Rafael Lima');assert.equal(await q.inputValue(),'Offshore Survey');
  for(const tab of ['documents','expenses']){
   const source=p.locator('[data-hr-jump="'+tab+'"]').first();await source.focus();
   const before=await list.evaluate(e=>e.scrollTop);await p.keyboard.press('Enter');
   const context=p.locator('.hr-employee-context');await context.getByText('Rafael Lima',{exact:true}).waitFor();
   assert(new URL(p.url()).hash.endsWith('/'+tab));
   await context.getByRole('button',{name:pt?'Voltar ao perfil':'Back to employee profile'}).click();
   await title.filter({hasText:'Rafael Lima'}).waitFor();
   assert.equal(await q.inputValue(),'Offshore Survey');assert.equal(await list.evaluate(e=>e.scrollTop),before);
   assert(await source.evaluate(e=>document.activeElement===e));
   await p.goForward();await context.waitFor();await p.goBack();await title.waitFor();
  }
  await p.locator('[data-hr-jump="documents"]').first().click();await p.locator('.hr-employee-context').waitFor();
  await p.reload();await p.locator('.hr-employee-context').getByText('Rafael Lima',{exact:true}).waitFor();
  await p.locator('.hr-employee-context button').click();await title.filter({hasText:'Rafael Lima'}).waitFor();
  await p.locator('[data-hr-jump="documents"]').first().click();await p.locator('.hr-employee-context').waitFor();
  if(await tabs.isVisible()){
   await tabs.selectOption('expenses');await p.waitForURL('**/expenses');
   await p.locator('.hr-employee-context button').click();await title.filter({hasText:'Rafael Lima'}).waitFor();
  }
  assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  console.log('PASS',width,guest?'public guest':'authorized editor',pt?'PT':'EN',total,'department matches; stable list; stale response; two records and history');
 }finally{await p.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{
 for(const [port,width,guest,pt] of [[18762,1360,true,false],[18762,360,true,false],[18760,1360,false,false],[18761,390,false,true]])await check(browser,port,width,guest,pt);
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
