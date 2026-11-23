const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);
assert.equal(origin.hostname,'127.0.0.1');

async function verify(browser,width,pt){
 const page=await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try{
  await page.goto(origin.origin+'/__demo/public?area=hr');
  const sections=page.locator('#hr-section-select');
  await sections.waitFor({state:'attached'});
  if(pt){
   await page.evaluate(()=>{location.hash='profile'});
   await page.locator('#wl-language-select').selectOption('pt-BR');
   await page.locator('#profile-language button').click();
   await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
   await page.evaluate(()=>{location.hash='hr'});
   await sections.waitFor({state:'attached'});
  }
  if(await sections.isVisible())await sections.selectOption('calendar');
  else await page.locator('[data-hr-tab="calendar"]').click();
  const panel=page.locator('#hr-location-roster'),results=panel.locator('[data-location-results]');
  const row=(id,location,start,end,project='PTB001')=>({id,assignment_type:'offshore',status:'planned',project,location,start_on:'2025-04-'+start,end_on:'2025-04-'+end});
  const shifts=[row('a','Survey vessel','01','07'),row('b','Offshore vessel','08','13'),row('c','Offshore vessel','09','10','PTB002'),{...row('d','Shore base','13','18'),assignment_type:'onshore'},row('e','Outside period','14','15')];
  const requests=[];
  await page.route('**/api/hr/workspace?**',route=>{
   const q=new URL(route.request().url()).searchParams;
   requests.push([q.get('start_on'),q.get('end_on'),q.get('project')]);
   const select=rows=>rows.filter(r=>!q.get('project')||r.project===q.get('project'));
   return route.fulfill({json:{roster:[
    {id:'1',name:'Alex Demo',assignments:select(shifts)},
    {id:'2',name:'Sam Demo',assignments:select([row('f','','07','07')])},
    {id:'3',name:'Restricted fixture',programming_status:'restricted',assignments:shifts}
   ]}});
  });
  await panel.locator('summary').first().click();
  const start=panel.locator('[name=roster_day]'),end=panel.locator('[name=roster_until]');
  assert.equal(await end.inputValue(),'');
  await start.fill('2025-04-07');
  await results.getByRole('heading',{name:'Survey vessel (1)'}).waitFor();
  assert(!await results.getByText('Offshore vessel (1)').count());
  await end.fill('2025-04-13');
  const offshore=results.locator('article').filter({hasText:'Offshore vessel'});
  await offshore.waitFor();
  assert.equal(await offshore.locator('strong').count(),1);
  assert.equal(await offshore.locator('li').count(),2);
  for(const name of ['Shore base (1)','Survey vessel (1)',pt?'Local não informado (1)':'Location not recorded (1)'])await results.getByRole('heading',{name}).waitFor();
  assert.doesNotMatch(await results.innerText(),/Outside period|Restricted fixture/);
  assert.match(await results.innerText(),pt?/Embarque previsto/:/Planned joining/);
  assert.match(await results.innerText(),pt?/Desembarque previsto/:/Planned leaving/);
  assert(await panel.evaluate(e=>e.scrollWidth<=e.clientWidth+1&&e.getBoundingClientRect().right<=innerWidth));
  if(process.env.ROSTER_PREVIEW){
   await page.setViewportSize({width,height:1800});
   await panel.evaluate(e=>{e.scrollIntoView();window.scrollBy(0,-100);document.activeElement.blur()});
   await panel.screenshot({path:process.env.ROSTER_PREVIEW+'-'+width+'.png'});
   await page.setViewportSize({width,height:900});
  }
  await panel.locator('[name=roster_project]').fill('PTB002');
  await panel.locator('button[type=submit]').click();
  await page.waitForFunction(()=>document.querySelectorAll('[data-location-results] article li').length===1);
  assert.match(await results.innerText(),/PTB002/);
  assert(requests.some(([a,b,p])=>a==='2025-04-07'&&b==='2025-04-13'&&p==='PTB002'));
  await end.fill('2025-04-06');
  await results.getByText(pt?/Escolha de 1 a 93/:/Choose 1 to 93/).waitFor();
  await end.fill('2025-08-30');
  assert(!requests.some(([,b])=>b==='2025-08-30'));
  await end.fill('');
  await results.getByText(pt?/Nenhuma escala/:/No work assignments/).waitFor();
  console.log('PASS',width,pt?'pt-BR':'en','day, inclusive range, switches, overlaps, no location, restricted, project and range validation');
 }finally{await page.close()}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{await verify(browser,390,true);await verify(browser,1360,false)}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
