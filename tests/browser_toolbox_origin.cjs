const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);assert.equal(origin.hostname,'127.0.0.1');
async function check(browser,width) {
 const p=await browser.newPage({viewport:{width,height:919},ignoreHTTPSErrors:true});
 try {
  // Add synthetic vessel and project associations to one permitted list response; use the original report ID and details.
  await p.route('**/api/toolbox',async r=>{const response=await r.fetch(),d=await response.json();const talk=d.talks[0],site=d.sites.find(s=>s.type==='vessel'||s.kind==='vessel');assert(talk&&site);talk.work_site={id:site.id,name:site.name,code:site.code};talk.meta.project_number='LOCAL-123';await r.fulfill({response,json:d})});
  await p.goto(origin.origin+'/__demo/public?area=workspaces');await p.locator('a[href="#toolbox"]:visible').first().click();
  const project=p.locator('#tb-project'),query=p.locator('#tb-query'),vessel=p.locator('#tb-filters [data-page-vessel]'),filters=p.locator('#tb-filter-panel');
  await project.waitFor({state:'attached'});if(!await filters.evaluate(e=>e.open))await filters.locator('summary').click();
  await project.selectOption('LOCAL-123');const a=p.locator('[data-toolbox-id]').first();await a.waitFor();const title=await a.locator('h2').innerText(),id=await a.getAttribute('data-toolbox-id');
  await query.fill(title);for(const val of await vessel.locator('option').evaluateAll(opts=>opts.map(o=>o.value).filter(Boolean))){await vessel.selectOption(val);if(await a.count())break}
  const ship=await vessel.inputValue();assert(ship);await filters.locator('summary').click();await a.scrollIntoViewIfNeeded();const top=(await a.boundingBox()).y;await a.click();
  const preview=p.locator('.tb-talk-preview');await preview.getByRole('heading',{name:title,exact:true}).waitFor();await preview.getByRole('link').click();
  const heading=p.locator('.fw-heading h1');await p.getByRole('heading',{name:'Signing actions'}).waitFor();assert.equal(new URL(p.url()).hash,'#toolbox/'+id);assert(await heading.evaluate(e=>e===document.activeElement));assert((await heading.boundingBox()).y>=64);assert(await p.getByText(title,{exact:true}).isVisible());
  await p.goBack();await p.waitForFunction(id=>document.activeElement?.dataset.toolboxId===id,id);assert.equal(await query.inputValue(),title);assert.equal(await vessel.inputValue(),ship);assert.equal(await project.inputValue(),'LOCAL-123');assert.equal(await filters.evaluate(e=>e.open),false);assert(Math.abs((await a.boundingBox()).y-top)<4);
  // Forward re-enters the same full record, including after a previous Back
  // already restored the row. Release the read only after focus returns.
  const detailPath='/api/toolbox/talks/'+id;
  const isDetail=url=>url.pathname===detailPath;
  for(const result of ['success','error']){
   let release;
   const gate=new Promise(resolve=>{release=resolve;});
   const hold=async route=>{
    await gate;
    if(result==='error')await route.fulfill({status:503,contentType:'application/json',body:'{"error":"Fictional fixture unavailable"}'});
    else await route.continue();
   };
   await p.route(isDetail,hold);
   try{
    const started=p.waitForRequest(request=>isDetail(new URL(request.url())));
    await p.goForward();await started;
    await p.locator('#tb-read-state').waitFor();
    await p.goBack();
    await p.waitForFunction(id=>document.activeElement?.dataset.toolboxId===id,id,{timeout:4500});
    assert.equal(await query.inputValue(),title);
    assert.equal(await vessel.inputValue(),ship);
    assert.equal(await project.inputValue(),'LOCAL-123');
    assert.equal(await filters.evaluate(e=>e.open),false);
    assert(Math.abs((await a.boundingBox()).y-top)<4);
    const readFinished=p.waitForEvent('requestfinished',{predicate:r=>isDetail(new URL(r.url()))});
    release();await readFinished;
    await p.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
    assert.equal(new URL(p.url()).hash,'#toolbox');
    assert.equal(await a.evaluate(e=>document.activeElement===e),true);
    assert.equal(await p.locator('#tb-read-state,.tb-talk-preview,.tb-stale').count(),0);
   }finally{release();await p.unroute(isDetail,hold);}
  }
  console.log('PASS Toolbox',width,'settled and interrupted return, filtered identity and focus');
 } finally {await p.close()}
}
// A native Back during the link's activation reaches the retained list before the
// asynchronous detail route can mount. Back after the GET starts is exercised separately.
async function retainedListBack(browser, width) {
  const page = await browser.newPage({
    viewport: {width, height: 919}, hasTouch: width < 700, ignoreHTTPSErrors: true
  });
  try {
    await page.goto(origin.origin + '/__demo/public?area=workspaces');
    const toolbox = page.locator('a[href="#toolbox"]:visible').first();
    await toolbox.waitFor();
    if (width < 700) {
      const navigate = async key => {
        const link = page.locator('#workspace-nav [data-workspace="' + key + '"]').first();
        if (!await link.isVisible()) await page.locator('#shell-toggle').click();
        await link.click();
      };
      await navigate('profile');
      await page.locator('#wl-language-select').selectOption('pt-BR');
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
      await navigate('workspaces');
    }
    await toolbox.click();
    const rows = page.locator('#tb-results a[data-toolbox-id]');
    const preview = page.locator('.tb-talk-preview');
    const filters = page.locator('#tb-filter-panel');
    const vessel = page.locator('#tb-filters [data-page-vessel]');
    const project = page.locator('#tb-project');
    const query = page.locator('#tb-query');
    const term = 'Fictional software-training';
    await rows.nth(1).waitFor();
    if (!await filters.evaluate(element => element.open)) await filters.locator('summary').click();
    await query.fill(term);
    const ship = await vessel.locator('option').filter({hasText:'Meridian'}).getAttribute('value');
    await vessel.selectOption(ship);
    await filters.locator('summary').click();
    const records = await rows.evaluateAll(elements => elements.map(row => ({
      id: row.dataset.toolboxId, title: row.querySelector('h2').innerText
    })));
    assert.equal(records.length, 2);
    assert.notEqual(records[0].id, records[1].id);
    const detailReads = [];
    page.on('request', request => {
      const pathname = new URL(request.url()).pathname;
      if (request.method() === 'GET' && pathname.startsWith('/api/toolbox/talks/')) detailReads.push(pathname);
    });
    const position = row => row.evaluate(element => ({
      y: Math.round(element.getBoundingClientRect().top),
      page: Math.round(window.scrollY),
      list: element.closest('#tb-results').scrollTop
    }));
    for (const record of [records[1], records[0], records[1]]) {
      const row = rows.and(page.locator('[data-toolbox-id="' + record.id + '"]'));
      await row.scrollIntoViewIfNeeded();
      await row.focus();
      const before = await position(row);
      await page.keyboard.press('Enter');
      await preview.getByRole('heading', {name:record.title, exact:true}).waitFor();
      const full = preview.getByRole('link');
      assert.equal(new URL(await full.getAttribute('href')).hash, '#toolbox/' + record.id);
      await page.keyboard.press('Tab');
      assert(await preview.getByRole('button').evaluate(element => element === document.activeElement));
      await page.keyboard.press('Tab');
      assert(await full.evaluate(element => element === document.activeElement));
      const beforeReads = detailReads.length;
      await full.evaluate(link => {
        // The shell can request a foreground or polling render before hashchange.
        // Pause only entry to this one detail until native Back reaches the list.
        // The list render, history, requests, focus handling and data remain real.
        const hash = new URL(link.href).hash;
        const list = document.querySelector('#tb-results');
        const workspace = window.AJFieldwork;
        const open = workspace.open, poll = workspace.poll;
        const holdDetail = method => function(...args) {
          if (location.hash !== hash) return method.apply(this, args);
          return Promise.resolve();
        };
        workspace.open = holdDetail(open);
        workspace.poll = holdDetail(poll);
        link.addEventListener('click', () => {
          const phase = window.toolboxReturnPhase = {
            hash: location.hash, rows: document.querySelectorAll('#tb-results a[data-toolbox-id]').length,
            loading: Boolean(document.querySelector('#tb-read-state')),
            detail: Boolean(document.querySelector('.fw-prewrap')), complete: false
          };
          const releaseAfterBack = event => {
            if (new URL(event.newURL).hash !== '#toolbox') return;
            window.removeEventListener('hashchange', releaseAfterBack);
            setTimeout(() => {
              workspace.open = open;
              workspace.poll = poll;
              phase.retainedList = list === document.querySelector('#tb-results');
              phase.complete = true;
            }, 0);
          };
          window.addEventListener('hashchange', releaseAfterBack);
          history.back();
        }, {once:true});
      });
      await page.keyboard.press('Enter');
      await page.waitForFunction(() => location.hash === '#toolbox' && window.toolboxReturnPhase?.complete);
      const phase = await page.evaluate(() => {
        const phase = window.toolboxReturnPhase;
        delete window.toolboxReturnPhase;
        return phase;
      });
      assert.deepEqual(phase, {hash:'#toolbox/' + record.id, rows:2, loading:false, detail:false,
        retainedList:true, complete:true});
      assert.equal(detailReads.length, beforeReads, 'Back must precede the detail GET');
      assert.equal(await query.inputValue(), term);
      assert.equal(await vessel.inputValue(), ship);
      assert.equal(await project.inputValue(), '');
      assert.equal(await filters.evaluate(element => element.open), false);
      assert.equal(await rows.count(), 2);
      assert.equal(await preview.count(), 0);
      await page.waitForFunction(id => document.activeElement?.dataset.toolboxId === id,
        record.id, {timeout:2500}).catch(() => {});
      const after = await position(row);
      assert.equal(after.list, before.list);
      assert(Math.abs(after.y - before.y) <= 3);
      assert(Math.abs(after.page - before.page) <= 3);
      const active = await row.evaluate(element => ({
        original: element === document.activeElement, tag: document.activeElement.tagName
      }));
      assert(active.original, 'Filtered list and position restored; expected exact row, focus was on ' + active.tag);
      assert.equal(detailReads.length, beforeReads, 'Late detail work must not run after returning');
    }
    console.log('PASS retained Toolbox row', width, 'keyboard B/A/B, pre-GET Back, filters, focus and scroll');
  } finally {
    await page.close();
  }
}
(async () => {
  const browser = await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
  const failures = [];
  try {
    for (const width of [1360, 389]) {
      await check(browser, width);
      try { await retainedListBack(browser, width); }
      catch (error) {
        console.error('FAIL retained Toolbox row', width, error.message);
        failures.push(width);
      }
    }
    assert.deepEqual(failures, [], 'Retained list Back failed at the listed widths');
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
