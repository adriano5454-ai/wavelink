const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');
const url = new URL(process.argv[2]);
assert.equal(url.hostname, '127.0.0.1');

async function check(browser, width, portuguese) {
  const page = await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
  try {
    await page.goto(url.origin+'/__demo/public?area=hr');
    const sections = page.locator('#hr-section-select');
    await sections.waitFor({state:'attached'});
    if (portuguese) {
      await page.evaluate(()=>location.hash='profile');
      await page.locator('#wl-language-select').selectOption('pt-BR');
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
      await page.evaluate(()=>location.hash='hr');
      await sections.waitFor({state:'attached'});
    }
    const open = async tab=>{
      if (await sections.isVisible()) await sections.selectOption(tab);
      else await page.locator('[data-hr-tab="'+tab+'"]').click();
    };
    await open('org');
    await page.getByRole('heading',{name:portuguese?'Organograma':'Organization chart',exact:true}).waitFor();
    const localized=value=>portuguese?({'Offshore Survey':'Levantamento offshore','DEMO Engineering':'Engenharia DEMO','DEMO Logistics':'Logística DEMO','Operations':'Operações','IT':'TI','Finance':'Finanças','Meridian Survey Team':'Equipe de levantamento Meridian','Survey coordinator':'Coordenação de levantamento'}[value]||value):value;
    const cards = page.locator('.hr-org-unit');
    for (const [department,name] of [['Offshore Survey','Mara Brisa'],['DEMO Engineering','Luca Bay'],['DEMO Logistics','Isa Moor']]) {
      const card=cards.filter({has:page.getByRole('heading',{name:localized(department),exact:true})});
      await card.getByText(name,{exact:true}).waitFor();
    }
    await cards.getByText(portuguese?'Sem chefia formal cadastrada':'No formal department head designated',{exact:true}).first().waitFor();
    await cards.getByText(localized('Survey coordinator'),{exact:true}).first().waitFor();
    assert(await page.locator('.hr-org-grid').evaluate(e=>e.scrollWidth<=e.clientWidth+1 && e.getBoundingClientRect().right<=innerWidth));
    const tree=page.locator('.org-tree');
    await page.getByText(portuguese?'Estrutura fictícia de exemplo':'Fictional reporting structure',{exact:true}).waitFor();
    const node=key=>tree.locator('.org-node').filter({has:page.getByRole('link',{name:key,exact:true})});
    const direct=(parent,child)=>parent.locator('..').locator(':scope > ul > li > .org-node').filter({has:page.getByRole('link',{name:child,exact:true})});
    const ceo=node('Demo Manager');
    assert.equal(await ceo.locator('.org-avatar').innerText(),'DM');
    assert.equal(await tree.locator('.org-avatar img').count(),0);

    await direct(ceo,'Eva Sol').waitFor();await direct(ceo,'Caio Rio').waitFor();
    await direct(node('Eva Sol'),'Talia Luz').waitFor();
    await direct(node('Caio Rio'),'Nico Serra').waitFor();await direct(node('Caio Rio'),'Rosa Lago').waitFor();
    await direct(node('Talia Luz'),'Rafael Lima').waitFor();await direct(node('Rafael Lima'),'Lia Costa').waitFor();
    assert((await node('Lia Costa').innerText()).includes(portuguese?'Chefe de equipe':'Party Chief'));
    const tech=direct(node('Lia Costa'),'Mara Brisa');await tech.waitFor();await direct(node('Lia Costa'),'Davi Coral').waitFor();
    await direct(tech,'Nina Mar').waitFor();
    await direct(node('Nico Serra'),'Ari Monte').waitFor();await direct(node('Rosa Lago'),'Iris Prado').waitFor();
    for(const [department,lead] of [['Operations','Talia Luz'],['Offshore Survey','Lia Costa'],['IT','Nico Serra'],['Finance','Rosa Lago']]){
      const unit=cards.filter({has:page.getByRole('heading',{name:localized(department),exact:true})});
      await unit.locator('.hr-org-head').getByRole('link',{name:lead,exact:true}).waitFor();
    }
    const meridian=direct(node('Rafael Lima'),'Alba Reis');
    await meridian.getByText(portuguese?/DEMO Meridian.*Chefe de equipe/:/DEMO Meridian.*Party Chief/).waitFor();
    await node('Lia Costa').getByText(portuguese?/MV Aurora.*Chefe de equipe/:/MV Aurora.*Party Chief/).waitFor();
    await direct(meridian,'Tom Faro').waitFor();await direct(meridian,'Cora Sal').waitFor();
    const auroraToggle=node('Lia Costa').getByRole('button');
    await auroraToggle.click();assert(!(await tech.isVisible()));assert(await node('Tom Faro').isVisible());await auroraToggle.click();
    const query=page.getByRole('searchbox',{name:portuguese?'Buscar nome ou cargo':'Search name or role'});
    const controls=page.locator('.org-filter-controls'), selects=controls.locator('select');
    const clear=controls.getByRole('button'), count=controls.locator('+ p');
    await auroraToggle.click();await query.fill(portuguese?'technician':'tecnico');assert((await count.innerText()).endsWith(' · 0'));
    await query.fill(portuguese?'tecnico':'technician');
    assert.equal(await count.innerText(),(portuguese?'Cargos encontrados':'Matching positions')+' · 4');
    await tech.waitFor();assert.equal(await node('Iris Prado').count(),0);
    await selects.nth(1).selectOption({label:'DEMO Meridian'});
    await selects.nth(0).selectOption({label:localized('Meridian Survey Team')});
    await selects.nth(2).selectOption('vacant');await page.getByText(portuguese?'Nenhum cargo corresponde aos filtros.':'No positions match these filters.').waitFor();
    await query.fill('trainee');assert((await count.innerText()).endsWith(' · 1'));
    await node('Cora Sal').waitFor();assert.equal(await node('Mara Brisa').count(),0);
    assert(await tree.evaluate(e=>document.documentElement.scrollWidth<=innerWidth+1 && e.getBoundingClientRect().right<=innerWidth+1));
    await query.fill('');await selects.nth(2).selectOption('filled');
    const tom=node('Tom Faro').getByRole('link');await tom.focus();await page.keyboard.press('Enter');
    await page.locator('.wl-profile-hero').waitFor();await page.goBack();await tom.waitFor();
    assert(await tom.evaluate(e=>document.activeElement===e));
    await clear.focus();await page.keyboard.press('Enter');assert(await query.evaluate(e=>document.activeElement===e));
    assert(!(await tech.isVisible()));await auroraToggle.click();
    const chief=node('Lia Costa');assert(!(await chief.innerText()).includes(' / '));
    assert((await chief.getByRole('button').getAttribute('aria-label')).includes(portuguese?'Chefe de equipe':'Party Chief'));
    const meridianToggle=meridian.getByRole('button');await meridianToggle.click();assert(!(await node('Cora Sal').isVisible()));assert(await tech.isVisible());await meridianToggle.click();
    const vacant=node('Cora Sal').locator('..').getByText(portuguese?'Vaga':'Vacant',{exact:true});await vacant.waitFor();
    assert(await tree.evaluate(e=>document.documentElement.scrollWidth<=innerWidth+1 && e.getBoundingClientRect().right<=innerWidth+1));
    const toggle=node('Talia Luz').getByRole('button');await toggle.click();assert(!(await tech.isVisible()));assert(await node('Iris Prado').isVisible());await toggle.click();await tech.waitFor();
    if(process.env.ORG_PREVIEW&&!portuguese)await tree.screenshot({path:process.env.ORG_PREVIEW+'-'+width+'.png'});
    assert.equal(await page.locator('.hr-position-form').count(),0);
    assert.equal(await page.getByRole('button',{name:portuguese?'Editar estrutura':'Edit structure'}).count(),0);
    assert.equal(await page.locator('.org-unit-actions,.org-card-actions').count(),0);
    const member=tech.getByRole('link',{name:'Mara Brisa',exact:true});
    const response=page.waitForResponse(r=>r.url().includes('/api/recognition/profile?')&&r.ok());
    await member.click();assert.equal((await (await response).json()).display_name,'Mara Brisa');
    await page.goBack();await member.waitFor();assert(await member.evaluate(e=>e===document.activeElement));
    await open('calendar');await page.locator('#hr-location-roster').waitFor({state:'attached'});
    await open('org');await cards.first().waitFor();
    if(!portuguese){
      await selects.nth(1).selectOption({label:'DEMO Meridian'});await selects.nth(2).selectOption('vacant');
      await page.evaluate(()=>location.hash='profile');
      await page.locator('#wl-language-select').selectOption('pt-BR');await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
      await page.evaluate(()=>location.hash='hr');await sections.waitFor({state:'attached'});await open('org');
      const vessel=page.getByRole('combobox',{name:'Embarcação'});await vessel.waitFor();
      // Language changes may restart the workspace. Exercise the same selection by stable vessel ID.
      console.log('Locale switch retained vessel:',await vessel.locator('option:checked').innerText());
      await vessel.selectOption({label:'DEMO Meridian'});await page.getByRole('combobox',{name:'Situação do cargo'}).selectOption('vacant');
      await tree.getByText('DEMO Meridian · Chefe de equipe',{exact:true}).waitFor();
      await tree.getByText('Vaga',{exact:true}).waitFor();assert.equal(await node('Lia Costa').count(),0);
    }
    console.log('PASS',width,portuguese?'PT':'EN',await cards.count(),'groups');
  } finally {await page.close();}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{
 for(const width of [1360,390,360])for(const pt of [false,true])await check(browser,width,pt);
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
