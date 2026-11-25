const assert = require('node:assert/strict');
const { chromium } = require('playwright-core');
const base = new URL(process.argv[2]);
assert.equal(base.hostname, '127.0.0.1');
const baseline = process.argv.includes('--baseline');

function plus(day, offset) {
  const date = new Date(day + 'T12:00:00Z');
  date.setUTCDate(date.getUTCDate() + offset);
  return date.toISOString().slice(0,10);
}

async function verify(browser, width) {
  const page = await browser.newPage({ viewport: {width, height: 919}, ignoreHTTPSErrors: true, serviceWorkers: 'block' });
  try {
    await page.goto(base.origin + '/__demo/public?area=hr');
    const tabs = page.locator('#hr-section-select');
    await tabs.waitFor({state: 'attached'});
    if (await tabs.isVisible()) await tabs.selectOption('calendar');
    else await page.locator('[data-hr-tab=calendar]').click();
    const panel = page.locator('#hr-location-roster');
    const ship = page.locator('#hr-workspace [data-page-vessel]').first();
    const day = panel.locator('[name=roster_day]'), to = panel.locator('[name=roster_until]');
    const project = panel.locator('[name=roster_project]');
    const out = panel.locator('[data-location-results]');
    const seedDay=await day.inputValue(), from=plus(seedDay,10), until=plus(seedDay,11);
    const gridFrom=plus(seedDay,9), gridTo=plus(seedDay,12);
    const grid = page.locator('#hr-board-filters');
    await page.locator('#hr-query-options > summary').click();
    await grid.locator('[name=start_on]').fill(gridFrom);
    await grid.locator('[name=end_on]').fill(gridTo);
    await grid.locator('button[type=submit]').first().click();
    await page.waitForFunction(d=>!!document.querySelector('.hr-mobile-days [data-hr-day="'+d+'"]'),gridFrom);
    const gridDay = page.locator('.hr-mobile-days [data-hr-day="'+until+'"]');
    const mobileGrid = await gridDay.isVisible();
    const agendaTitle = page.locator('.hr-mobile-detail h3');
    let expectedAgendaTitle;
    if (mobileGrid) {
      await gridDay.click();
      expectedAgendaTitle = await agendaTitle.innerText();
      assert.equal(await gridDay.getAttribute('aria-pressed'), 'true');
    }
    const idFor = async name => {
      const option = ship.locator('option').filter({hasText: name});
      await option.waitFor({state:'attached'});
      return option.getAttribute('value');
    };
    const meridian=await idFor(/Meridian/),aurora=await idFor(/Aurora/);
    async function changeShip(id) {
      const prior=await panel.elementHandle();
      await ship.selectOption(id);
      await page.waitForFunction(el=>!el.isConnected, prior);
      await page.waitForFunction(id=>document.querySelector('#hr-workspace [data-page-vessel]')?.value===id,id);
      assert.equal(await grid.locator('[name=start_on]').inputValue(),gridFrom);
      assert.equal(await grid.locator('[name=end_on]').inputValue(),gridTo);
      assert.deepEqual(await page.locator('.hr-mobile-days [data-hr-day]').evaluateAll(es=>es.map(e=>e.dataset.hrDay)),
        [gridFrom,from,until,gridTo]);
      if (mobileGrid) {
        assert.equal(await gridDay.getAttribute('aria-pressed'), 'true');
        assert.equal(await agendaTitle.innerText(), expectedAgendaTitle);
        const count = await gridDay.evaluate(el => Number(el.querySelector('small')?.textContent || 0));
        assert.equal(await page.locator('.hr-mobile-detail li').count(), count);
      }
    }
    async function period() {
      await day.fill(from); await to.fill(until);
      await panel.getByRole('button',{name:'Show roster'}).click();
    }
    async function rows(group, count) {
      await out.getByRole('heading',{name:group+' ('+count+')',exact:true}).waitFor();
      assert.equal(await out.locator('article').count(),1);
      const names=await out.locator('article section > strong').allTextContents();
      assert.equal(names.length,count);assert.equal(new Set(names).size,count);
      return names.sort();
    }
    await changeShip(meridian);
    assert.equal(await panel.evaluate(e=>e.open),false);
    await panel.locator('summary').first().click();
    await period();
    const first=await rows('DEMO Meridian',2);
    assert.deepEqual(first,['Oren North','Vera Brook']);
    await changeShip(aurora);
    if (baseline) {
      const state={open:await panel.evaluate(e=>e.open),from:await day.inputValue(),until:await to.inputValue()};
      console.log('BEFORE',JSON.stringify({width,requested:[from,until],...state,meridian:first}));
      assert.equal(state.open,false);assert.equal(state.from,seedDay);assert.equal(state.until,'');
      await panel.locator('summary').first().click(); await period();
    }
    assert.equal(await panel.evaluate(e=>e.open),true);
    assert.equal(await day.inputValue(),from);assert.equal(await to.inputValue(),until);
    const second=await rows('MV Aurora',7);
    assert.deepEqual(second,['Demo Manager','Idris Fen','Lena Cove','Lia Costa','Noa Martins','Rafael Lima','Rui Dale']);
    assert(!second.some(name=>first.includes(name)));
    if (!baseline) {
      await project.fill('DEMO-303');await panel.getByRole('button',{name:'Show roster'}).click();
      assert.deepEqual(await rows('MV Aurora',2),['Lena Cove','Rui Dale']);
      // Deliver an older genuine Aurora response after Meridian has finished rendering.
      let release, started;
      const hold=new Promise(done=>{release=done;});
      const reached=new Promise(done=>{started=done;});
      const oldQuery=url=>{const q=new URL(url).searchParams;
        return q.get('vessel_id')===aurora&&q.get('start_on')===from&&q.get('end_on')===until&&q.get('project')==='DEMO-303';
      };
      const held=async route=>{if(oldQuery(route.request().url())){started();await hold;}await route.continue();};
      await page.route('**/api/hr/workspace?**',held);
      await panel.getByRole('button',{name:'Show roster'}).click(); await reached;
      const arrival=page.waitForResponse(r=>r.url().includes('/api/hr/workspace?')&&oldQuery(r.url()));
      try {
        await changeShip(meridian);
        assert.deepEqual(await rows('DEMO Meridian',2),first);
      } finally {release();}
      await (await arrival).finished();
      await page.evaluate(()=>new Promise(done=>requestAnimationFrame(()=>requestAnimationFrame(done))));
      await page.unroute('**/api/hr/workspace?**',held);
      assert.equal(await day.inputValue(),from);assert.equal(await to.inputValue(),until);
      assert.equal(await project.inputValue(),'DEMO-303');
      assert.deepEqual(await rows('DEMO Meridian',2),first);
      // A collapsed disclosure keeps the optional end date blank across another vessel change.
      await to.fill('');await panel.locator('summary').first().click();
      await changeShip(aurora);
      assert.equal(await panel.evaluate(e=>e.open),false);assert.equal(await day.inputValue(),from);
      assert.equal(await to.inputValue(),'');assert.equal(await project.inputValue(),'DEMO-303');
      await panel.locator('summary').first().click();
      assert.deepEqual(await rows('MV Aurora',2),['Lena Cove','Rui Dale']);
    }
    console.log('PASS',JSON.stringify({width,range:[from,until],meridian:first,aurora:second,grid:[gridFrom,gridTo]}));
  } finally { await page.close(); }
}
(async()=>{
  const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
  try { for(const width of [1360,389])await verify(browser,width); }
  finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
