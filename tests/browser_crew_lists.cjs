'use strict';

const assert = require('node:assert/strict');
const path = require('node:path');
const {chromium} = require('playwright-core');

async function visit(page, area) {
  const url = new URL(page.url());
  url.hash = area;
  await page.goto(url.href);
}

async function busyVisit(page, counts) {
  const faces = ['happy', 'calm', 'focused', 'tired', 'difficult'];
  const first = ['Alex', 'Amira', 'Ana', 'Bruno', 'Camila', 'Daniel', 'Eva', 'Felipe', 'Hugo', 'Inês'];
  const last = ['Alves', 'Brito', 'Costa', 'Dias', 'Freitas', 'Gomes', 'Lima', 'Matos', 'Nunes', 'Ramos', 'Reis', 'Santos', 'Silva'];
  await page.route(url => url.pathname === '/api/recognition/moods', async route => {
    const response = await route.fetch();
    const data = await response.json();
    const items = Array.from({length:counts.moods}, (_, i) => ({
      user_id:'fixture-person-'+i, display_name:first[Math.floor(i/last.length)]+' '+last[i%last.length],
      mood:faces[i%faces.length],
    }));
    await route.fulfill({response, json:{...data,items}});
  });
  await page.route(url => url.pathname === '/api/maintenance', async route => {
    const response = await route.fetch();
    const data = await response.json();
    const seed = data.jobs.find(j => j.status === 'open');
    assert.ok(seed, 'the native demo contains an open work order');
    const titles = ['Deck crane inspection', 'Sensor calibration', 'Battery enclosure checks', 'Winch inspection'];
    const jobs = Array.from({length:counts.orders}, (_, i) => {
      const number = String(i+1).padStart(3,'0');
      return {...seed, id:i ? 'fixture-order-'+number : seed.id, reference:'WO-'+number,
        name:'WO-'+number+' '+titles[i%titles.length],
        asset_name:['Deck crane','Survey reference sensor','AUV battery enclosure','Survey winch'][i%4],
        due_at:new Date(Date.UTC(2026,8,24,12)+i*3600000).toISOString()};
    });
    await route.fulfill({response, json:{...data,jobs}});
  });
}

async function moodsReady(page, count) {
  await page.waitForFunction(n => {
    const shared = document.querySelector('#wl-mood-shared');
    return shared && !shared.hidden && shared.querySelectorAll('li').length === n;
  }, count);
}

async function measureMoods(page) {
  return page.locator('#wl-mood-shared ul').evaluate(el => ({
    height:el.clientHeight, content:el.scrollHeight, card:document.querySelector('#wl-team-moods').offsetHeight,
    overflow:getComputedStyle(el).overflowY, width:el.clientWidth, contentWidth:el.scrollWidth,
  }));
}

async function testWidth(browser, origin, width) {
  const context = await browser.newContext({viewport:{width,height:width===390?844:900},
    ignoreHTTPSErrors:true, serviceWorkers:'block', hasTouch:width===390});
  try {
    const page = await context.newPage();
    page.setDefaultTimeout(14000);
    const counts = {moods:36,orders:125}, errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await busyVisit(page, counts);
    await page.goto(origin+'/__demo/public?area=home');
    await moodsReady(page, counts.moods);
    const smaller = await measureMoods(page);
    counts.moods = 125;
    await page.reload();
    await moodsReady(page, counts.moods);
    const busy = await measureMoods(page);
    assert.equal(busy.card, smaller.card);
    assert.equal(busy.height, smaller.height);
    assert.ok(busy.content > busy.height*2);
    assert.ok(busy.contentWidth <= busy.width+1);
    assert.equal(busy.overflow, 'auto');
    assert.ok(await page.getByText('Scroll to see everyone',{exact:true}).isVisible());
    const moods = page.getByRole('list',{name:/Shared today.*125/});
    await moods.focus();
    await moods.press('End');
    await page.waitForFunction(() => {
      const el = document.querySelector('#wl-mood-shared ul');
      return el.scrollTop + el.clientHeight >= el.scrollHeight-2;
    });
    const fixed = await page.locator('#wl-mood-shared ul').evaluate(el => {
      const before = [scrollY, document.querySelector('#ph-local').getBoundingClientRect().top];
      const end = el.lastElementChild.getBoundingClientRect().bottom;
      const visibleEnd = el.getBoundingClientRect().bottom;
      el.scrollTop = 0;
      return {before,after:[scrollY,document.querySelector('#ph-local').getBoundingClientRect().top],atEnd:end<=visibleEnd+2};
    });
    assert.deepEqual(fixed.before, fixed.after);
    assert.ok(fixed.atEnd);
    if(process.env.WAVELINK_TEST_EVIDENCE && width===1360){
      await page.locator('#wl-mood-heading').click();
      await page.locator('#wl-team-moods').screenshot({path:path.join(process.env.WAVELINK_TEST_EVIDENCE,'Wavelink-check-ins.png')});
    }
    await visit(page,'team');
    await moodsReady(page,125);
    assert.equal((await measureMoods(page)).height,busy.height);
    counts.moods=1;
    await visit(page,'home');
    await moodsReady(page,1);
    const one=await measureMoods(page);
    assert.equal(one.height,one.content);
    assert.ok(one.height<busy.height);
    assert.equal(await page.locator('#wl-mood-scroll-hint').isVisible(),false);
    counts.moods=0;
    await page.reload();
    await moodsReady(page,0);
    assert.ok(await page.locator('#wl-mood-empty').isVisible());

    await visit(page,'maintenance');
    const cards=page.locator('#mw-results [data-mw-order]');
    await cards.first().waitFor();
    assert.equal(await cards.count(),10);
    assert.equal(await page.locator('#mw-range').innerText(),'1–10 of 125');
    const box=page.locator('#mw-results');
    const metrics=await box.evaluate(el=>({height:el.clientHeight,content:el.scrollHeight}));
    assert.ok(metrics.height<=((width===390?844:900)*.66));
    assert.ok(metrics.content>metrics.height);
    const pick=cards.first();
    const title=await pick.locator('.mw-order-title').innerText();
    // The upper-right padding opens the same inspector as the title.
    const rect=await pick.boundingBox();
    const pad={x:rect.width-8,y:8};
    if(width===390)await pick.tap({position:pad});else await pick.click({position:pad});
    await page.locator('#mw-selected h2').filter({hasText:title}).waitFor();
    if(width===390)await page.locator('#mw-list-back').click();
    await cards.first().locator('.mw-order-title').press('Enter');
    await page.locator('#mw-selected h2').filter({hasText:title}).waitFor();
    await page.locator('#mw-open-order').click();
    await page.locator('#mw-back-orders').waitFor();
    assert.match(new URL(page.url()).hash,/^#maintenance\/.+/);
    await page.locator('#mw-back-orders').click();
    await cards.first().waitFor();
    if(process.env.WAVELINK_TEST_EVIDENCE && width===1360){
      await page.locator('.mw-list-detail').screenshot({path:path.join(process.env.WAVELINK_TEST_EVIDENCE,'Wavelink-work-orders.png')});
    }
    await page.locator('#mw-next').click();
    assert.equal(await page.locator('#mw-range').innerText(),'11–20 of 125');
    assert.ok((await cards.first().innerText()).includes('WO-011'));
    await page.locator('#mw-search').fill('WO-125');
    assert.equal(await cards.count(),1);
    assert.equal(await page.locator('#mw-pages').isVisible(),false);
    assert.ok((await cards.first().innerText()).includes('WO-125'));
    await page.locator('#mw-search').fill('');
    assert.equal(await page.locator('#mw-range').innerText(),'1–10 of 125');
    for(let i=0;i<12;i++)await page.locator('#mw-next').click();
    assert.equal(await cards.count(),5);
    assert.equal(await page.locator('#mw-range').innerText(),'121–125 of 125');
    assert.ok(await page.locator('#mw-next').isDisabled());
    await page.locator('#mw-previous').click();
    assert.equal(await page.locator('#mw-range').innerText(),'111–120 of 125');
    counts.orders=3;
    await page.locator('#op-refresh').click();
    await page.waitForFunction(()=>document.querySelectorAll('[data-mw-order]').length===3);
    assert.equal(await page.locator('#mw-pages').isVisible(),false);
    assert.ok((await cards.first().innerText()).includes('WO-001'));
    if(width===390){
      counts.moods=125;
      counts.orders=125;
      await visit(page,'profile');
      await page.locator('#wl-language-select').selectOption('pt-BR');
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
      await visit(page,'maintenance');
      await page.getByRole('navigation',{name:'Páginas de ordens de serviço'}).waitFor();
      assert.equal(await page.locator('#mw-range').innerText(),'1–10 de 125');
      await page.getByRole('button',{name:'Próxima',exact:true}).click();
      assert.equal(await page.locator('#mw-range').innerText(),'11–20 de 125');
      await visit(page,'home');
      await moodsReady(page,125);
      assert.ok(await page.getByText('Role para ver toda a equipe',{exact:true}).isVisible());
      assert.doesNotMatch(await page.locator('#wl-mood-shared-title').innerText(),/Shared today/);
    }
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
    assert.deepEqual(errors,[]);
    console.log(JSON.stringify({width,moods:busy,oneMood:one.height,orders:metrics}));
  } finally {
    await context.close();
  }
}

module.exports={busyVisit,moodsReady,measureMoods,visit,testWidth};
if(require.main===module){
  (async()=>{
    const args=process.env.WAVELINK_TEST_CHROMIUM_MAP?['--no-proxy-server','--host-resolver-rules='+process.env.WAVELINK_TEST_CHROMIUM_MAP]:[];
    const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM,args});
    try{for(const width of [1360,390])await testWidth(browser,process.argv[2],width);}
    finally{await browser.close();}
  })().catch(err=>{console.error(err);process.exitCode=1;});
}
