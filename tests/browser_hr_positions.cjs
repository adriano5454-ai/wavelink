const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
async function verify(browser, port, width, pt){
 const p=await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
 try{
  await p.goto('https://127.0.0.1:'+port);await p.locator('input[type=text]:visible').fill('demo.admin');
  await p.locator('#login-password').fill(process.env.ORG_QA_PASSWORD);await p.locator('#login-password').press('Enter');
  await p.locator('#wl-global-search-trigger:visible').waitFor();
  await p.locator(pt?'html[lang="pt-BR"] #wl-global-search-trigger:visible':'html[lang="en"] #wl-global-search-trigger:visible').waitFor();
  const open=async()=>{await p.evaluate(()=>location.hash='hr');const tabs=p.locator('#hr-section-select');await tabs.waitFor({state:'attached'});
   if(await tabs.isVisible())await tabs.selectOption('org');else await p.locator('[data-hr-tab=org]').click()};
  await open();const editMode=p.getByRole('button',{name:pt?'Editar estrutura':'Edit structure',exact:true});
  assert.equal(await p.locator('.hr-position-form').count(),0);await editMode.click();const add=p.getByRole('button',{name:pt?'Adicionar posição':'Add position',exact:true});
  const form=p.locator('.hr-position-form'),select=n=>form.locator('select').nth(n);
  const save=async()=>{await form.getByRole('button',{name:pt?'Salvar posição':'Save position'}).click();await form.waitFor({state:'detached'})};
  const suffix=Date.now(),name='QA '+suffix,department='QA unit '+suffix;
  await add.click();await select(0).selectOption('');await form.locator('input').first().fill(department);
  await form.locator('input').last().fill(name);await save();
  const lines=p.locator('.hr-position-row'),vacant=lines.filter({hasText:name}).first();await vacant.waitFor();assert((await vacant.innerText()).includes(pt?'Vaga':'Vacant'));
  const position=async person=>{await add.click();await select(0).selectOption({label:'Offshore Survey'});await select(1).selectOption({label:name});await select(3).selectOption({label:person});await save()};
  await position('Mara Brisa');await position('Davi Coral');
  const mara=lines.filter({has:p.getByText(name+' · Mara Brisa',{exact:true})}),davi=lines.filter({has:p.getByText(name+' · Davi Coral',{exact:true})});
  if(width>600){await davi.dragTo(mara);await form.waitFor();assert((await select(2).locator('option:checked').innerText()).includes('Mara Brisa'))}
  else{await davi.locator('button').click();await select(2).selectOption({label:name+' · Mara Brisa'})}
  await save();await davi.locator('small').waitFor();assert((await davi.innerText()).includes('Mara Brisa'));
  assert(await davi.evaluate(e=>e.scrollWidth<=e.clientWidth+1&&e.getBoundingClientRect().right<=innerWidth));
  await p.reload();await p.locator('#wl-global-search-trigger:visible').waitFor();await open();const tree=p.locator('.org-tree').filter({has:p.getByRole('heading',{name:'Offshore Survey',exact:true})});
  const toggle=tree.locator('[aria-controls]').first();await toggle.waitFor();await toggle.focus();await p.keyboard.press('Enter');
  assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert.equal(await tree.getByRole('link',{name:'Davi Coral'}).count(),0);
  const link=tree.getByRole('link',{name:'Mara Brisa'});const href=await link.getAttribute('href');const profile=p.waitForResponse(r=>r.url().includes('/api/recognition/profile?')&&r.ok());await link.click();const record=await (await profile).json();assert.equal(record.display_name,'Mara Brisa');assert.equal(new URL(p.url()).hash,href);
  await p.goBack();await toggle.waitFor();assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert(await link.evaluate(e=>e===document.activeElement));
  await toggle.click();await tree.getByRole('link',{name:'Davi Coral'}).waitFor();assert(await tree.evaluate(e=>e.getBoundingClientRect().right<=innerWidth));
  await editMode.click();await davi.locator('small').waitFor();
  console.log('PASS',pt?'pt-BR':'en',width,'new department, vacant role, assignment, reparent and reload');
 }finally{await p.close()}
}
(async()=>{const b=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{
 await verify(b,18600,1360,false);await verify(b,18601,390,true);
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
