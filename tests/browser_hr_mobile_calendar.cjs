const {chromium}=require('playwright-core');
const assert=require('node:assert/strict');
async function verify(browser,lang,width,theme){
 const p=await browser.newPage({viewport:{width,height:844},isMobile:true,hasTouch:true,colorScheme:theme,timezoneId:'America/Sao_Paulo',ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try{
  await p.route('**/api/hr/workspace?**',async route=>{
   const response=await route.fetch(),ws=await response.json();
   if(!ws.roster?.length)return route.fulfill({response});
   const person=ws.roster[0],day=ws.start_on;
   ws.events=(lang==='pt-BR'?['Inspeção de treinamento','Reunião de equipe']:['Training inspection','Training briefing']).map((title,i)=>({kind:'shifts',id:'demo-'+i,user_id:person.id,user_name:lang==='pt-BR'?'Equipe Demo':person.name,date:day,label:title,title:''}));
   const tomorrow=new Date(day+'T12:00:00Z');tomorrow.setUTCDate(tomorrow.getUTCDate()+1);
   ws.events.push({...ws.events[0],id:'demo-next',date:tomorrow.toISOString().slice(0,10)});
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
  assert((await days.locator('b').allTextContents()).every(x=>/^\d{1,2}$/.test(x)));
  await days.first().click();assert.equal(await detail.locator('li').count(),2);
  assert.equal(await days.first().locator('small').innerText(),'2');
  assert.equal(await days.nth(1).locator('small').innerText(),'1');
  assert.equal(await days.nth(2).locator('small').count(),0);
  for(const day of [days.first(),days.nth(1)]){
   const fits=await day.evaluate(button=>{
    const bounds=button.getBoundingClientRect(),numeral=button.querySelector('b').getBoundingClientRect(),badge=button.querySelector('small').getBoundingClientRect();
    return badge.width>0 && badge.height>0 && badge.top>=numeral.bottom && badge.bottom<=bounds.bottom && badge.right<=bounds.right;
   });
   assert(fits);
  }
  const first=await days.first().getAttribute('data-hr-day');
  if(lang==='pt-BR'&&process.env.HR_CALENDAR_PREVIEW)await board.screenshot({path:process.env.HR_CALENDAR_PREVIEW.replace('.png','-'+theme+'.png')});
  await days.nth(1).tap();assert.equal(await detail.locator('li').count(),1);
  await days.nth(2).tap();assert.match(await detail.innerText(),lang==='en'?/No events/:/Nenhum compromisso/);
  assert(await board.evaluate(e=>e.scrollWidth<=e.clientWidth+1 && e.getBoundingClientRect().right<=innerWidth));
  await p.locator('#hr-calendar-next').click();
  await p.waitForFunction(old=>document.querySelector('[data-hr-day]')?.dataset.hrDay && document.querySelector('[data-hr-day]').dataset.hrDay!==old,first);
  await days.first().click();assert.equal(await detail.locator('li').count(),2);
  await p.locator('#hr-planning-query').fill('no-such-fixture');
  await p.locator('#hr-planning-filter').evaluate(f=>f.requestSubmit());
  await p.waitForFunction(()=>!document.querySelector('.hr-mobile-detail li'));
  assert.equal(await board.locator('button small').count(),0);
  await p.setViewportSize({width:1360,height:900});assert.equal(await board.isVisible(),false);assert(await p.locator('.ux-timeline-desktop').isVisible());assert(await p.locator('#hr-location-roster').isVisible());
  console.log('PASS',lang,first,'days, multiple/empty, month, filter, width, desktop timeline and roster');
 }finally{await p.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const lang of ['en','pt-BR'])for(const [width,theme] of [[320,'dark'],[390,'light']])await verify(browser,lang,width,theme)}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
