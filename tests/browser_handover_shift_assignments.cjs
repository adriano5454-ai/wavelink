const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);assert.equal(origin.hostname,'127.0.0.1');
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{
 for(const [width,pt] of [[1360,false],[390,false],[1360,true],[390,true]]){
 const page=await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 await page.goto(origin.origin+'/__demo/public?area=hr');await page.locator('#hr-section-select').waitFor({state:'attached'});
 if(pt){await page.evaluate(()=>location.hash='profile');await page.locator('#wl-language-select').selectOption('pt-BR');await page.locator('#profile-language button').click();await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();}
 await page.evaluate(()=>location.hash='handovers');await page.locator('#ho-people-top').click();
 for(const name of ['Offshore Survey','DEMO Engineering','DEMO Logistics']){
  const card=page.locator('[data-shw-department]').filter({has:page.getByRole('heading',{name,exact:true})});
  const slots=card.locator('.shw-slot');await slots.first().waitFor();assert.equal(await slots.count(),2);
  for(const slot of await slots.all())assert.equal((await slot.locator('p.small').innerText()).split(', ').length,3);
  await card.locator('[data-shw-team]').click();
  const entries=page.locator('[data-hwd-open]');await entries.first().waitFor({state:'attached'});
  assert.equal(await entries.count(),2);assert((await page.locator('#hwd-subject option:checked').innerText()).includes(name));
  await page.locator('#ho-people-top').click();
 }
 await page.locator('[data-shw-department]').filter({has:page.getByRole('heading',{name:'Offshore Survey',exact:true})}).locator('[data-shw-setup]').click();
 const rows=page.locator('[data-sh-person-row]:visible'),show=page.locator('#sh-people-filter'),search=page.locator('#sh-people-search');
 await rows.first().waitFor();
 const records=await rows.evaluateAll(rs=>rs.map(r=>({id:r.dataset.shPersonRow,shift:r.querySelector('select').value,name:r.querySelector('span').firstChild.textContent.trim()})));
 assert.equal(new Set(records.map(r=>r.id)).size,6);
 for(const shift of ['0','1']){await show.selectOption(shift);assert.equal(await rows.count(),3);assert.equal(records.filter(r=>r.shift===shift).length,3);}
 await show.selectOption('all');await search.fill('Mara');assert.equal(await rows.count(),1);
 const row=rows.first(),selector=row.locator('select');
 const box=await row.evaluate(r=>{const n=r.querySelector('span').getBoundingClientRect(),s=r.querySelector('select').getBoundingClientRect();return {name:n.width,below:s.top>=n.bottom,overflow:document.documentElement.scrollWidth>innerWidth||r.scrollWidth>r.clientWidth+1,height:s.height}});
 assert.equal(box.overflow,false);assert(box.name>130);assert.equal(box.below,width===390);assert(box.height>=44);
 await selector.selectOption('');await show.selectOption('unassigned');assert.equal(await rows.count(),1);assert.equal(await selector.inputValue(),'');
 await selector.selectOption('0');assert.equal(await rows.count(),0);await search.fill('');await show.selectOption('0');assert.equal(await rows.count(),3);
 console.log('PASS',width,pt?'PT':'EN',records.map(r=>r.name+'='+r.shift).join(', '),box);
 await page.reload();await page.locator('#wl-global-search-trigger:visible').waitFor();await page.evaluate(()=>location.hash='hr');const tabs=page.locator('#hr-section-select');await tabs.waitFor({state:'attached'});if(await tabs.isVisible())await tabs.selectOption('calendar');else await page.locator('[data-hr-tab="calendar"]').click();
 const roster=page.locator('#hr-location-roster');await roster.locator('summary').first().click();
 const results=roster.locator('[data-location-results]');await results.getByText('Mara Brisa',{exact:true}).waitFor();
 for(const person of ['Demo Manager','Lia Costa','Rafael Lima','Mara Brisa','Davi Coral','Nina Mar','Luca Bay','Bia Lake','Noel Reef','Ida Brook','Teo Clay','Ana Fern','Isa Moor','Oli Pine','Luz Glen','Ben Lark','Mia Dune','Leo Elm']) assert((await results.innerText()).includes(person),person);
 if(width===390){
 const d=new Date();d.setUTCDate(d.getUTCDate()-2);const day=d.toISOString().slice(0,10);
 const button=page.locator('[data-hr-day="'+day+'"]');if(!await button.count())await page.locator('#hr-calendar-prev').click();await button.click();
 const list=page.locator('.hr-mobile-detail li'),count=Number(await button.locator('small').innerText());
 assert.equal(await list.count(),count);const names=await list.allInnerTexts();for(const name of ['Mara Brisa','Davi Coral','Nina Mar','Luca Bay','Isa Moor'])assert(names.some(x=>x.includes(name)),name);
 console.log('Calendar',day,count, names.map(t=>t.split('\n')[0]).join(' | '));
 }
 await page.close();
 }
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
