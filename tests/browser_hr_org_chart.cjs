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
    await cards.getByText(portuguese?'Liderança não definida':'Leadership not defined',{exact:true}).first().waitFor();
    await cards.getByText('Survey coordinator',{exact:true}).first().waitFor();
    assert(await page.locator('.hr-org-grid').evaluate(e=>e.scrollWidth<=e.clientWidth+1 && e.getBoundingClientRect().right<=innerWidth));
    // Fresh showcase data has department membership but no saved reporting lines.
    await page.getByText(portuguese?'Nenhuma posição visível na estrutura. Consulte os departamentos abaixo.':'No reporting positions visible. Browse the departments below.').waitFor();
    assert.equal(await page.locator('.org-node,.hr-position-form').count(),0);
    assert.equal(await page.getByRole('button',{name:portuguese?'Editar estrutura':'Edit structure'}).count(),0);
    const member=cards.getByRole('link',{name:'Mara Brisa',exact:true});
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
