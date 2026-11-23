// Run with home_news_fixture.py on loopback. The daily response uses fictional records only.
const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');
const origin = new URL(process.argv[2]).origin;
assert.equal(new URL(origin).hostname,'127.0.0.1');

async function verify(browser,width) {
 const page = await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try {
  await page.goto(origin);
  await page.locator('[name=login_id]').fill('homeqa.editor');
  await page.locator('[name=password]').fill('Fictional-home-news-password');
  await page.locator('#login-form [type=submit]').click();
  await page.locator('#personal-home').waitFor();
  await page.evaluate(()=>{location.hash='#hr';});
  const calendar = page.locator('[data-hr-tab="calendar"]');
  await page.locator('#hr-section-select').waitFor({state:'attached'});
  if(await page.locator('#hr-section-select').isVisible()) await page.locator('#hr-section-select').selectOption('calendar');
  else {await calendar.waitFor(); if(await page.locator('#hr-section-select').isVisible())await page.locator('#hr-section-select').selectOption('calendar');else await calendar.click();}
  const panel=page.locator('#hr-location-roster'), results=panel.locator('[data-location-results]');
  await panel.waitFor();
  const initial=await panel.locator('[name=roster_day]').inputValue();
  assert.equal(initial,await page.evaluate(()=>{const d=new Date();return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-')}));
  const shift={assignment_type:'offshore',status:'confirmed',start_on:initial,end_on:initial,shift_name:'Day shift',project:'PTB001',work_site:{id:'ship',name:'Survey vessel'}};
  const person=(id,name,rows,access='registered')=>({id,name,enabled:true,programming_status:access,assignments:rows});
  const people=[person('a','Fictional Ada',[shift,shift]),person('b','Fictional Bo',[{...shift,status:'planned'}]),person('c','Fictional Cy',[{...shift,work_site:null,location:''}]),person('d','Fictional Dee',[]),person('r','Restricted name',[shift],'restricted')];
  const queries=[];
  await page.route('**/api/hr/workspace?**',route=>{
   const q=new URL(route.request().url()).searchParams;queries.push(q);
   if(q.get('start_on')!==q.get('end_on'))return route.continue();
   return route.fulfill({json:{roster:q.get('start_on')===initial?people:[],truncated:false,records:[{destination:'Private travel detail'}]}});
  });
  await page.route('**/api/hr/timesheet-projects',route=>route.fulfill({json:{projects:[{name:'PTB001',active:true},{name:'Archived code',active:false}]}}));
  await panel.locator('summary').first().click();
  await results.getByRole('heading',{name:'Survey vessel (2)'}).waitFor();
  const text=await results.innerText();
  assert.match(text,/PTB001/);assert.doesNotMatch(text,/Restricted name|Private travel detail/);
  assert.equal(await results.getByText('Fictional Ada',{exact:true}).count(),1);
  assert.equal(await results.locator('article').count(),2);
  const shot=process.env.ROSTER_PREVIEW;
  if(shot)await panel.screenshot({path:shot+'-'+width+'.png'});
  assert(await panel.evaluate(e=>e.scrollWidth<=e.clientWidth+1));
  await panel.locator('[name=roster_project]').fill('PTB001');
  await panel.locator('button[type=submit]').click();
  await panel.locator('[name=roster_day]').fill('2021-07-03');
  await results.locator('article').first().waitFor({state:'detached'});
  await results.locator('p').waitFor();
  assert(queries.some(q=>q.get('start_on')==='2021-07-03'&&q.get('project')==='PTB001'));
  assert.equal(await page.locator('[data-hr-planning-view="timeline"]').count(),1);
  await page.locator('#hr-add-assignment').click();
  const projectInput=page.locator('#hr-form input[name=project]');
  await projectInput.waitFor();
  assert.equal(await projectInput.getAttribute('list'),'hr-shift-projects');
  assert.equal(await projectInput.inputValue(),'');
  assert.equal(await projectInput.getAttribute('required'),null);
  await page.waitForFunction(()=>[...document.querySelectorAll('#hr-shift-projects option')].some(o=>o.value==='PTB001'));
  assert.equal(await page.locator('#hr-shift-projects option').count(),1);
  console.log('PASS',width,'today, counts, planned/confirmed, missing location and assignment, past date/project, empty state and preserved timeline');
 }finally{await page.close();}
}
async function publicPreview(browser, locale) {
 const page=await browser.newPage({ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try {
  await page.goto(origin+'/__demo/public?area=hr');
  await page.locator('#hr-section-select').waitFor({state:'attached',timeout:45000});
  if(locale==='pt-BR'){
   await page.evaluate(()=>{location.hash='#profile';});
   await page.locator('#wl-language-select').selectOption('pt-BR');
   await page.locator('#profile-language button').click();
   await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
   await page.evaluate(()=>{location.hash='#hr';});
  }
  await page.locator('#hr-section-select').waitFor({state:'attached',timeout:45000});
  if(await page.locator('#hr-section-select').isVisible()) await page.locator('#hr-section-select').selectOption('calendar');
  else await page.locator('[data-hr-tab="calendar"]').click();
  const panel=page.locator('#hr-location-roster');
  const summary=panel.locator('summary').first();
  assert.equal(await page.locator('html').getAttribute('lang'),locale);
  assert.match(await summary.innerText(),locale==='en'?/Roster by vessel/:/Escala por embarcação/);
  const get=page.waitForResponse(r=>{const u=new URL(r.url());return u.pathname==='/api/hr/workspace' && u.searchParams.get('start_on')===u.searchParams.get('end_on')});
  await summary.click();
  assert.equal((await get).status(),200);
  await panel.locator('[data-location-results] article, [data-location-results] p').first().waitFor();
  console.log('PASS fictional public demo',locale,'authorized daily workspace and translated roster');
 } finally {await page.close();}
}

(async()=>{const b=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,390])await verify(b,w);for(const locale of ['en','pt-BR'])await publicPreview(b,locale);}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1;});
