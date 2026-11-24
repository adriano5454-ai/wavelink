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
    const tree=page.locator('.org-tree');
    await page.getByText(portuguese?'Estrutura fictícia de exemplo':'Fictional reporting structure',{exact:true}).waitFor();
    const root=tree.locator('.org-roots > li > .org-node'),mid=tree.locator('.org-roots > li > ul > li > .org-node'),leaves=tree.locator('.org-roots > li > ul > li > ul > li > .org-node');
    assert.equal(await root.count(),1);assert.equal(await mid.count(),2);assert.equal(await leaves.count(),3);
    const a=await root.boundingBox(),b=await mid.first().boundingBox(),c=await mid.last().boundingBox(),d=await leaves.first().boundingBox();
    if(width>640){
      assert(a.y+a.height<=b.y && b.y+b.height<=d.y && Math.abs(b.y-c.y)<2 && b.x+b.width<=c.x);
      assert(a.x+a.width/2>b.x+b.width/2 && a.x+a.width/2<c.x+c.width/2);
      assert(await mid.last().evaluate(e=>parseFloat(getComputedStyle(e.parentElement,'::before').borderRightWidth)>0));
    }else{assert(c.y>b.y);assert(await tree.evaluate(e=>e.scrollWidth<=e.clientWidth+1))}
    console.log('tree geometry',width,a,b,c,d);
    if(process.env.ORG_PREVIEW && !portuguese)await tree.screenshot({path:process.env.ORG_PREVIEW+'-'+width+'.png'});
    const toggle=root.getByRole('button');await toggle.focus();await page.keyboard.press('Enter');assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert(!(await mid.first().isVisible()));await toggle.click();assert(await leaves.first().isVisible());
    assert.equal(await page.locator('.hr-position-form').count(),0);
    assert.equal(await page.getByRole('button',{name:portuguese?'Editar estrutura':'Edit structure'}).count(),0);
    assert.equal(await page.locator('.org-unit-actions,.org-card-actions').count(),0);
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
