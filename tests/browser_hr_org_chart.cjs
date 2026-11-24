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
    const cards = page.locator('.hr-org-unit');
    for (const [department,name] of [['Offshore Survey','Mara Brisa'],['DEMO Engineering','Luca Bay'],['DEMO Logistics','Isa Moor']]) {
      const card=cards.filter({has:page.getByRole('heading',{name:department,exact:true})});
      await card.getByText(name,{exact:true}).waitFor();
    }
    await cards.getByText(portuguese?'Sem chefia formal cadastrada':'No formal department head designated',{exact:true}).first().waitFor();
    await cards.getByText('Survey coordinator',{exact:true}).first().waitFor();
    assert(await page.locator('.hr-org-grid').evaluate(e=>e.scrollWidth<=e.clientWidth+1 && e.getBoundingClientRect().right<=innerWidth));
    const tree=page.locator('.org-tree');
    await page.getByText(portuguese?'Estrutura fictícia de exemplo':'Fictional reporting structure',{exact:true}).waitFor();
    const node=key=>tree.locator('.org-node').filter({has:page.getByRole('link',{name:key,exact:true})});
    const direct=(parent,child)=>parent.locator('..').locator(':scope > ul > li > .org-node').filter({has:page.getByRole('link',{name:child,exact:true})});
    const ceo=node('Demo Manager');
    await direct(ceo,'Eva Sol').waitFor();await direct(ceo,'Caio Rio').waitFor();
    await direct(node('Eva Sol'),'Talia Luz').waitFor();
    await direct(node('Caio Rio'),'Nico Serra').waitFor();await direct(node('Caio Rio'),'Rosa Lago').waitFor();
    await direct(node('Talia Luz'),'Rafael Lima').waitFor();await direct(node('Rafael Lima'),'Lia Costa').waitFor();
    assert((await node('Lia Costa').innerText()).includes('Party Chief'));
    const tech=direct(node('Lia Costa'),'Mara Brisa');await tech.waitFor();await direct(node('Lia Costa'),'Davi Coral').waitFor();
    await direct(tech,'Nina Mar').waitFor();
    await direct(node('Nico Serra'),'Ari Monte').waitFor();await direct(node('Rosa Lago'),'Iris Prado').waitFor();
    for(const [department,lead] of [['Operations','Talia Luz'],['Offshore Survey','Lia Costa'],['IT','Nico Serra'],['Finance','Rosa Lago']]){
      const unit=cards.filter({has:page.getByRole('heading',{name:department,exact:true})});
      await unit.locator('.hr-org-head').getByRole('link',{name:lead,exact:true}).waitFor();
    }
    const vacant=node('Davi Coral').locator('..').getByText(portuguese?'Vaga':'Vacant',{exact:true});await vacant.waitFor();
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
    console.log('PASS',width,portuguese?'PT':'EN',await cards.count(),'groups');
  } finally {await page.close();}
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{
 for(const width of [1360,390])for(const pt of [false,true])await check(browser,width,pt);
}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
