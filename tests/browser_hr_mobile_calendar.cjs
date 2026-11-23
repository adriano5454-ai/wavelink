const {chromium}=require('playwright-core');
const assert=require('node:assert/strict');
async function verify(browser,lang){
 const p=await browser.newPage({viewport:{width:390,height:844},timezoneId:'America/Sao_Paulo',ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try{
  await p.route('**/api/hr/workspace?**',async route=>{
   const response=await route.fetch(),ws=await response.json();
   if(!ws.roster?.length)return route.fulfill({response});
   const person=ws.roster[0],day=ws.start_on;
   ws.events=(lang==='pt-BR'?['Inspeção de treinamento','Reunião de equipe']:['Training inspection','Training briefing']).map((title,i)=>({kind:'shifts',id:'demo-'+i,user_id:person.id,user_name:lang==='pt-BR'?'Equipe Demo':person.name,date:day,label:title,title:''}));
   ws.records=[];ws.roster.forEach(person=>{person.assignments=[]});
   await route.fulfill({response,json:ws});
  });
  await p.goto(process.argv[2]+'/__demo/public?area=hr');
  await p.locator('#hr-section-select').waitFor({state:'attached'});
  if(lang==='pt-BR'){
   await p.evaluate(()=>{location.hash='profile'});
   await p.locator('#wl-language-select').selectOption(lang);
   await p.locator('#profile-language button').click();
   await p.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
   await p.evaluate(()=>{location.hash='hr'});
  }
  await p.locator('#hr-section-select').selectOption('calendar');
  const board=p.locator('.hr-mobile-calendar'),days=board.locator('[data-hr-day]'),detail=board.locator('.hr-mobile-detail');
  await days.first().waitFor();
  assert.equal(await days.first().evaluate(e=>getComputedStyle(e.parentElement).gridTemplateColumns.split(' ').length),7);
  assert((await days.allTextContents()).every(x=>/^\d{1,2}$/.test(x)));
  await days.first().click();assert.equal(await detail.locator('li').count(),2);
  const first=await days.first().getAttribute('data-hr-day');
  if(lang==='pt-BR'&&process.env.HR_CALENDAR_PREVIEW)await board.screenshot({path:process.env.HR_CALENDAR_PREVIEW});
  await days.nth(1).click();assert.match(await detail.innerText(),lang==='en'?/No events/:/Nenhum compromisso/);
  assert(await board.evaluate(e=>e.scrollWidth<=e.clientWidth+1 && e.getBoundingClientRect().right<=innerWidth));
  await p.locator('#hr-calendar-next').click();
  await p.waitForFunction(old=>document.querySelector('[data-hr-day]')?.dataset.hrDay && document.querySelector('[data-hr-day]').dataset.hrDay!==old,first);
  await days.first().click();assert.equal(await detail.locator('li').count(),2);
  await p.locator('#hr-planning-query').fill('no-such-fixture');
  await p.locator('#hr-planning-filter').evaluate(f=>f.requestSubmit());
  await p.waitForFunction(()=>!document.querySelector('.hr-mobile-detail li'));
  await p.setViewportSize({width:1360,height:900});assert.equal(await board.isVisible(),false);assert(await p.locator('.ux-timeline-desktop').isVisible());assert(await p.locator('#hr-location-roster').isVisible());
  console.log('PASS',lang,first,'days, multiple/empty, month, filter, width, desktop timeline and roster');
 }finally{await p.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{await verify(browser,'en');await verify(browser,'pt-BR')}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
