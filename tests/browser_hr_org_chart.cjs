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
    const levels=[];
    for(let i=0;i<6;i++) levels.push(tree.locator('.org-roots'+' > li > ul'.repeat(i)+' > li > .org-node'));
    assert.deepEqual(await Promise.all(levels.map(nodes=>nodes.count())),[1,1,1,2,3,2]);
    for(const [i,label] of ['CEO','Director','Manager','Supervisor','Technician','Trainee'].entries())
      assert((await levels[i].first().locator('strong').innerText()).includes(label));
    const tech=levels[4].filter({has:page.getByRole('link',{name:'Mara Brisa',exact:true})});
    const trainee=tech.locator('..').locator(':scope > ul .org-node');await trainee.getByRole('link',{name:'Nina Mar'}).waitFor();
    const vacant=levels[5].filter({has:page.getByText(portuguese?'Vaga':'Vacant',{exact:true})});assert.equal(await vacant.count(),1);assert.equal(await vacant.locator('a').count(),0);
    const supervisor=levels[3].filter({has:page.getByRole('link',{name:'Rafael Lima',exact:true})});
    const children=supervisor.locator('..').locator(':scope > ul > li > .org-node');assert.equal(await children.count(),2);
    const [parentBox,left,right]=await Promise.all([supervisor,children.first(),children.last()].map(n=>n.boundingBox()));
    if(width>640){assert(parentBox.y+parentBox.height<=left.y && Math.abs(left.y-right.y)<2 && left.x+left.width<=right.x);assert(parentBox.x+parentBox.width/2>left.x&&parentBox.x+parentBox.width/2<right.x+right.width)}
    else assert(right.y>left.y);
    assert(await tree.evaluate(e=>e.scrollWidth<=e.clientWidth+1 && document.documentElement.scrollWidth<=innerWidth+1));
    const toggle=supervisor.getByRole('button');await toggle.focus();await page.keyboard.press('Enter');assert(!(await tech.isVisible()));assert(await vacant.isVisible());await toggle.click();await trainee.waitFor();
    const top=levels[0].getByRole('button');await top.click();assert(!(await supervisor.isVisible()));await top.click();await trainee.waitFor();
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
