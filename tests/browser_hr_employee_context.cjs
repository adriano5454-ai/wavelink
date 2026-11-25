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
   if(pt)await p.waitForFunction(()=>document.documentElement.lang.toLowerCase().startsWith('pt'));
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
  // Select A, B, A before B finishes. The pending identity appears without previous records or actions.
  await lia.click();await title.filter({hasText:'Lia Costa'}).waitFor();
  let releaseB,startB;const pendingB=new Promise(r=>startB=r),gateB=new Promise(r=>releaseB=r);
  const rid=await rafael.getAttribute('data-hr-person-link');
  await p.route('**/api/hr/overview?**',async route=>{
    if(new URL(route.request().url()).searchParams.get('user_id')===rid){const response=await route.fetch();startB();await gateB;await route.fulfill({response}).catch(()=>{})}
    else await route.continue();
  });
  await rafael.click();await pendingB;assert.equal(await p.locator('#hr-status').isVisible(),false);const pendingName=p.locator('[data-pending-name]');assert.equal(await pendingName.innerText(),'Rafael Lima');assert.equal(await title.count(),0);assert.equal(await p.locator('.hr-person-layout > section button').count(),0);assert(await pendingName.evaluate(e=>!!e.closest('[inert]')));await lia.click();
  await p.waitForFunction(()=>!document.querySelector('.hr-person-layout [inert]'));releaseB();await p.unrouteAll({behavior:'wait'});
  assert.equal(await title.innerText(),'Lia Costa');await list.evaluate(e=>{window.originalShell=e.closest('#hr-workspace');window.originalDetail=e.closest('.hr-person-layout').querySelector(':scope > section')});
  for(const [tab,expected] of [['documents','Offshore survival training'],['expenses','Transfer to the heliport']]){
   const source=p.locator('[data-hr-jump="'+tab+'"]').first();await source.click();
   const sheet=p.locator('.hr-employee-sheet[open]');await sheet.waitFor();
   await sheet.locator('header strong').getByText('Lia Costa',{exact:true}).waitFor();
   const bounds=await sheet.boundingBox();assert(bounds.x>=0&&bounds.x+bounds.width<=width+1);
   if(width>700)assert(bounds.x>width/2);else assert(bounds.y>0);
   for(const control of [sheet.locator('header strong'),sheet.locator('header button')]){
    const r=await control.boundingBox();assert(r.y>=0&&r.y+r.height<=p.viewportSize().height);
   }
   const match=sheet.locator('.hr-record h3').filter({hasText:expected});await match.first().waitFor();
   const search=sheet.getByRole('searchbox');await search.fill('unmatched-qa');
   assert.equal(await sheet.locator('.hr-record:visible').count(),0);await search.fill(expected);await match.first().waitFor();
   assert(await search.evaluate(e=>document.activeElement===e));assert.equal(await p.evaluate(()=>performance.getEntriesByType('navigation').length),1);
   assert(await list.evaluate(e=>e===window.employeeList&&e.closest('#hr-workspace')===window.originalShell&&window.originalDetail.isConnected));
   await p.keyboard.press('Escape');await sheet.waitFor({state:'detached'});assert(await source.evaluate(e=>e===document.activeElement));
   assert.equal(await q.inputValue(),'Offshore Survey');await p.goForward();await sheet.waitFor();await p.goBack();await sheet.waitFor({state:'detached'});
   await source.click();await sheet.getByRole('button',{name:pt?'Fechar':'Close',exact:true}).click();await sheet.waitFor({state:'detached'});
   await source.click();await sheet.getByRole('button',{name:pt?'Abrir seção completa':'Open full section'}).click();
   await p.locator('.hr-employee-context').getByText('Lia Costa',{exact:true}).waitFor();assert(new URL(p.url()).hash.endsWith('/'+tab));
   await p.locator('.hr-employee-context button').click();await title.filter({hasText:'Lia Costa'}).waitFor();
   assert(await source.evaluate(e=>document.activeElement===e));
   if(width<700){const r=await title.boundingBox();assert(r.y>=64&&r.y+r.height<=844+1)}
   await list.evaluate(e=>{window.employeeList=e;window.originalShell=e.closest('#hr-workspace');window.originalDetail=e.closest('.hr-person-layout').querySelector(':scope > section')});
  }
  if(!guest){
   const v=p.locator('.hr-certificate-entry [data-hr-jump=documents]'),add=p.locator('.hr-certificate-entry [data-hr-cert-create]');
   await v.click();await p.locator('.hr-employee-sheet header strong').filter({hasText:'Lia Costa'}).waitFor();await p.keyboard.press('Escape');await p.locator('.hr-employee-sheet').waitFor({state:'detached'});
   for(const exit of ['#hr-cancel','#hr-close']){await add.click();await p.locator('#hr-save').waitFor();assert.equal(await p.locator('.hr-employee-sheet[open]').count(),0);await p.locator(exit).click();await p.locator('#hr-save').waitFor({state:'hidden'})}
   await p.route('**/api/hr/overview?**',route=>route.fulfill({status:503,contentType:'application/json',body:'{}'}),{times:1});
   await rafael.focus();await p.keyboard.press('Enter');await p.locator('#hr-retry').waitFor();assert.equal(await add.count(),0);assert.equal(await title.count(),0);
   await p.locator('#hr-retry').click();await title.filter({hasText:'Rafael Lima'}).waitFor();await lia.click();await title.filter({hasText:'Lia Costa'}).waitFor();
  }
  await p.evaluate(id=>location.hash='#hr/staff/'+id+'/expenses',liaId);
  await p.locator('.hr-employee-context').getByText('Lia Costa',{exact:true}).waitFor();
  await p.reload();await p.locator('.hr-employee-context').getByText('Lia Costa',{exact:true}).waitFor();
  assert.equal(await p.locator('.hr-employee-sheet[open]').count(),0);
  await p.locator('.hr-employee-context button').click();await title.filter({hasText:'Lia Costa'}).waitFor();
  assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
  console.log('PASS',width,guest?'public guest':'authorized editor',pt?'PT':'EN',total,'department matches; stable list; stale response; two records and history');
 }finally{await p.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{
 for(const [port,width,guest,pt] of [[18822,1360,true,false],[18822,360,true,false],[18820,1360,false,false],[18821,390,false,true]])await check(browser,port,width,guest,pt);
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
