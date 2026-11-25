const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
async function verify(browser, port, width, pt){
 const p=await browser.newPage({viewport:{width,height:900},hasTouch:pt,ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try{
  await p.goto('https://127.0.0.1:'+port);await p.locator('input[type=text]:visible').fill('demo.admin');
  await p.locator('#login-password').fill(process.env.ORG_QA_PASSWORD);await p.locator('#login-password').press('Enter');
  await p.locator('#wl-global-search-trigger:visible').waitFor();
  await p.locator(pt?'html[lang="pt-BR"] #wl-global-search-trigger:visible':'html[lang="en"] #wl-global-search-trigger:visible').waitFor();
  const open=async()=>{await p.evaluate(()=>location.hash='hr');const tabs=p.locator('#hr-section-select');await tabs.waitFor({state:'attached'});
   if(await tabs.isVisible())await tabs.selectOption('org');else await p.locator('[data-hr-tab=org]').click()};
  await open();
  const t=(en,br)=>pt?br:en;
  const area=p.locator('.hr-org-unit').filter({has:p.getByRole('heading',{name:'Offshore Survey',exact:true})});
  const leader=area.getByRole('button',{name:t('Add top-level position','Adicionar cargo no nível superior')});
  const member=area.getByRole('button',{name:t('Add person to chart','Adicionar pessoa ao organograma')});
  const form=p.locator('.hr-position-form'),sel=n=>form.locator('select').nth(n);
  const enter=async b=>{if(pt)await b.tap();else await b.click()};
  const save=async()=>{await enter(form.getByRole('button',{name:t('Save position','Salvar posição')}));await form.waitFor({state:'detached'})};
  const role=async name=>{await sel(1).selectOption('');await form.locator('input').last().fill(name)};
  const card=name=>p.locator('.org-node').filter({has:p.getByText(name,{exact:true})});
  const act=async(name,en,br)=>{const c=card(name),summary=c.locator('summary');if(pt)await summary.tap();else{await summary.focus();await p.keyboard.press('Enter')}await enter(c.getByRole('button',{name:t(en,br)}))};
  assert.equal(await p.locator('.org-node').count(),0);
  await enter(leader);await role('QA Lead / Offshore');await sel(3).selectOption({label:'Mara Brisa'});await save();
  await enter(member);await role('QA Member');await sel(2).selectOption({label:'QA Lead / Offshore · Mara Brisa'});await sel(3).selectOption({label:'Davi Coral'});await save();
  await act('Davi Coral','Add position above','Adicionar cargo acima');assert(await sel(2).isDisabled());await role('QA Intermediate');await save();
  const intermediate=card('QA Intermediate');await intermediate.getByText(t('Vacant','Vaga'),{exact:true}).waitFor();
  assert(await intermediate.locator('..').locator(':scope > ul').getByRole('link',{name:'Davi Coral'}).isVisible());
  await act('QA Intermediate','Assign or change person','Atribuir ou trocar pessoa');await sel(3).selectOption({label:'Lia Costa'});await save();
  await act('Mara Brisa','Add position below','Adicionar cargo abaixo');assert((await sel(2).locator('option:checked').innerText()).includes('Mara Brisa'));await role('QA Sibling');await save();
  if(width>600){await card('QA Sibling').dragTo(intermediate);await form.waitFor();await save()}
  else{await act('QA Sibling','Edit position','Editar posição');await sel(2).selectOption({label:'QA Intermediate · Lia Costa'});await save()}
  assert(await intermediate.locator('..').locator(':scope > ul').getByText('QA Sibling',{exact:true}).isVisible());
  assert(await intermediate.evaluate(e=>e.getBoundingClientRect().right<=innerWidth));
  await p.reload();await p.locator('#wl-global-search-trigger:visible').waitFor();await open();
  await intermediate.waitFor();assert.equal(await p.locator('.org-card-actions').count(),0);
  assert.equal(await intermediate.locator('..').locator(':scope > ul > li').count(),2);
  if(process.env.ORG_QA_AVATARS){
   const good=card('Davi Coral').locator('.org-avatar img');await good.waitFor();
   assert(await good.evaluate(img=>img.complete&&img.naturalWidth>0));
   assert.equal(await card('Mara Brisa').locator('.org-avatar').innerText(),'MB');
   assert.equal(await card('Lia Costa').locator('.org-avatar').innerText(),'LC');
   assert.equal(await card('QA Sibling').locator('.org-avatar').count(),0);
   await card('QA Sibling').locator('.org-vacancy').waitFor();
   const person=card('Davi Coral').getByRole('link',{name:'Davi Coral',exact:true});
   await person.focus();assert(await person.evaluate(e=>document.activeElement===e));
   const denied='**/api/recognition/avatar/*';
   let deniedRequests=0;
   await p.route(denied,route=>{deniedRequests++;return route.fulfill({status:403,body:''})});
   await p.reload();await p.locator('#wl-global-search-trigger:visible').waitFor();await open();
   await card('Davi Coral').waitFor();await p.waitForFunction(()=>performance.getEntriesByType('resource').some(r=>r.name.includes('/api/recognition/avatar/')));
   assert(deniedRequests>0);assert.equal(await card('Davi Coral').locator('.org-avatar').innerText(),'DC');
   assert.equal(await card('Davi Coral').locator('.org-avatar img').count(),0);
   await p.unroute(denied);

  }
  const filters=p.locator('.org-filter-controls');assert.equal(await filters.locator('select').count(),2);
  await filters.getByRole('searchbox').fill('sibling');await filters.locator('select').last().selectOption('vacant');
  await card('QA Sibling').waitFor();assert((await filters.locator('+ p').innerText()).endsWith(' · 1'));
  assert.equal(await card('Davi Coral').count(),0);await intermediate.waitFor();
  await filters.getByRole('button').click();await card('Davi Coral').waitFor();
  console.log('PASS',width,pt?'PT':'EN','directory bootstrap, member, above, below, vacancy, assignment, move, reload');
 }finally{await p.close()}
}
(async()=>{const b=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{
 await verify(b,Number(process.env.ORG_QA_EN_PORT||18640),1360,false);await verify(b,Number(process.env.ORG_QA_PT_PORT||18641),390,true);
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
