const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const { chromium } = require('playwright-core');

// Requires a disposable loopback showcase fixture. Its Gate.clock advances on a local file signal;
// short-next shortens only the first browser cookie Max-Age to 6s. The actual
// signature, native session, 401 handling and public admission stay in use.
const base = new URL(process.argv[2]);
assert.equal(base.protocol, 'https:');
assert.equal(base.hostname, '127.0.0.1');
const control = path.resolve(process.argv[3]);
const entry = new URL('/__demo/public?area=inventory', base).href;
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
const trace = [];
const results = [];
const mobile = 389;

function observe(page) {
  page.setDefaultTimeout(10000);
  page.on('response', response => {
    const url = new URL(response.url());
    if (url.origin !== base.origin) return;
    const document = response.request().isNavigationRequest() && response.frame() === page.mainFrame();
    if (document || response.status() === 401) {
      trace.push({document, path:url.pathname, area:url.searchParams.get('area'), status:response.status()});
    }
  });
}
function options(width) {
  return {
    headless:true, executablePath:process.env.WAVELINK_TEST_CHROMIUM,
    viewport:{width, height:919}, ignoreHTTPSErrors:true, hasTouch:width === mobile,
    serviceWorkers:'allow',
    args:['--ignore-certificate-errors','--no-proxy-server','--disable-background-networking',
      '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1, EXCLUDE localhost']
  };
}
let advances = 0;
async function expireSession() {
  // Immutable signals avoid Windows file sharing races with the server clock.
  await fs.writeFile(path.join(control, 'advance-' + (++advances)), '', {flag:'wx'});
}
async function ownsOldWorkspace(page, id) {
  return page.evaluate(async old => {
    const db = await new Promise((resolve,reject) => {
      const op = indexedDB.open('pxgeo-dive-check-1', 1);
      op.onsuccess = () => resolve(op.result);
      op.onerror = () => reject(op.error);
    });
    try {
      return await new Promise((resolve,reject) => {
        const key = db.transaction('state').objectStore('state').getKey('window:' + old + ':main');
        key.onsuccess = () => resolve(key.result !== undefined);
        key.onerror = () => reject(key.error);
      });
    } finally { db.close(); }
  }, id);
}
async function openBook(page) {
  const book = page.locator('[data-inventory-id]').filter({hasText:'Offshore equipment'}).first();
  await book.waitFor();
  assert.equal(await page.locator('[data-inventory-id]').count(), 2);
  await book.click();
  const rows = page.locator('#inv-rows [data-select-row]');
  await rows.first().waitFor();
  assert.equal(await rows.count(), 17);
  const url = new URL(page.url());
  assert(url.hash.startsWith('#inventory/'));
  assert.equal(url.searchParams.get('public_demo'), '1');
  const id = url.searchParams.get('browser_workspace');
  assert(id && await ownsOldWorkspace(page, id));
  return {url:url.href, id};
}
async function goToWorkspaceResult(page) {
  const link = page.locator('a[href="#workspaces"]:visible').first();
  if (!await link.count()) await page.locator('#shell-toggle').click();
  await link.click();
  await page.locator('#home-find').fill('Inventory');
  const result = page.locator('[data-home-workspace="inventory"]:visible a[href="#inventory"]').first();
  await result.waitFor();
  return result;
}
async function assertCatalogue(page, id) {
  await page.locator('[data-inventory-id]').filter({hasText:'Offshore equipment'}).first().waitFor();
  const url = new URL(page.url());
  assert.equal(url.hash, '#inventory');
  assert.equal(url.searchParams.get('public_demo'), '1');
  const next = url.searchParams.get('browser_workspace');
  assert(next && next !== id, 'expected fresh admission');
  assert(await ownsOldWorkspace(page, id), 'previous profile retained');
  assert.equal(await page.locator('[data-inventory-id]').count(), 2);
  assert.equal(await page.locator('input[type=password]:visible').count(), 0);
  assert(!trace.some(e => e.document && e.path === '/__demo/login'));
}
async function runCase(profile, width, mode) {
  let ctx = await chromium.launchPersistentContext(profile, options(width));
  let page = ctx.pages()[0];
  observe(page);
  const name = width + '-' + mode;
  await fs.writeFile(path.join(control,'case.txt'), name);
  try {
    if (mode === 'reopened') await fs.writeFile(path.join(control,'short-next'), '6');
    await page.goto(entry, {waitUntil:'commit'});
    const saved = await openBook(page);
    if (mode === 'open-tab') {
      const result = await goToWorkspaceResult(page);
      trace.length = 0;
      await expireSession();
      await result.click();
      const reopen = page.getByRole('link', {name:'Reopen Inventory demo',exact:true});
      await reopen.waitFor();
      assert.equal(await reopen.getAttribute('href'), '/__demo/public?area=inventory');
      assert.equal(await page.locator('input[type=password]:visible').count(),0);
      assert(!trace.some(e => e.document && e.path === '/__demo/public'), 'should wait for action');
      assert(trace.some(e => e.path === '/api/inventory/lists' && e.status === 401), 'actual catalog response');
      if (width === mobile) await reopen.tap();
      else {
        const heading = page.getByRole('heading', {name:'Your demo visit has ended'});
        assert(await heading.evaluate(el => el === document.activeElement));
        await page.keyboard.press('Tab');
        assert(await reopen.evaluate(el => el === document.activeElement));
        await page.keyboard.press('Enter');
      }
      await assertCatalogue(page, saved.id);
      const admissions = trace.filter(e => e.document && e.path === '/__demo/public');
      assert.equal(admissions.length,1);
      assert.equal(admissions[0].area,'inventory');
    } else {
      await ctx.close(); ctx = null;
      await delay(6800);
      await expireSession();
      ctx = await chromium.launchPersistentContext(profile, options(width));
      page = ctx.pages()[0]; observe(page);
      trace.length = 0;
      await page.goto(saved.url, {waitUntil:'commit'});
      await assertCatalogue(page, saved.id);
      assert(trace.some(e => e.document && e.path === '/' && e.status === 303));
      const admissions = trace.filter(e => e.document && e.path === '/__demo/public');
      assert.equal(admissions.length,1);
      assert.equal(admissions[0].area,null, 'gate kept its existing redirect');
    }
    await openBook(page);
    results.push({width,mode,freshVisit:true,oldKey:true,catalogues:2,rows:17,staffLogin:false,events:trace.slice()});
    console.log('PASS',name,'fresh read-only inventory; 2 catalogues, 17 rows; prior workspace retained');
  } finally {
    if (ctx) await ctx.close();
  }
}
async function awayInPortuguese(profile, width) {
  const ctx = await chromium.launchPersistentContext(profile, options(width));
  try {
    const page = ctx.pages()[0]; observe(page);
    await fs.writeFile(path.join(control,'case.txt'), width+'-expired-away-pt');
    await page.goto(new URL('/__demo/public?area=home',base).href);
    await page.locator('#personal-home a[hreflang="pt-BR"]').click();
    await page.locator('html[lang="pt-BR"] .ph-footer a[href="#workspaces"]').click();
    await page.locator('#home-find').waitFor();
    await page.locator('#app a[href="#inventory"]:visible').first().click();
    const saved = await openBook(page);
    const home = page.locator('a[href="#home"]:visible').first();
    if (!await home.count()) await page.locator('#shell-toggle').click();
    await home.click();
    const refresh = page.locator('#ph-refresh');
    await refresh.waitFor();
    assert.equal(new URL(page.url()).hash,'#home');
    trace.length = 0;
    await expireSession();
    const signIn = page.locator('#login-form input[type=password]');
    // A Home request already in flight can expire before another refresh is clicked.
    try { await refresh.click({timeout:2000}); }
    catch (error) { if (!await signIn.isVisible()) throw error; }
    await signIn.waitFor();
    assert(trace.some(e => e.status === 401 && e.path.startsWith('/api/') && !e.path.startsWith('/api/inventory')));
    const link = page.getByRole('link',{name:'Reabrir a demo do Inventário',exact:true});
    assert.equal(await link.count(),0,'Inventory-specific recovery is absent on Home');
    await page.goBack();
    await link.waitFor();
    assert.equal(new URL(page.url()).hash,new URL(saved.url).hash);
    assert(await page.getByRole('heading',{name:'Sua visita à demo terminou'}).isVisible());
    assert.equal(await page.locator('input[type=password]:visible').count(),0);
    assert.equal(await link.getAttribute('href'),'/__demo/public?area=inventory');
    if (width === mobile) await link.tap();
    else await link.click();
    await assertCatalogue(page,saved.id);
    await openBook(page);
    results.push({width,mode:'expired-away-pt',readDeniedOutsideInventory:true,
      returnedToOriginalBookRoute:true,portugueseRecovery:true,catalogues:2,rows:17,oldKey:true});
    console.log('PASS',width,'Portuguese; Home read expired, browser Back to original Inventory then public readmission');
  } finally { await ctx.close(); }
}

async function homeControls(profile, width) {
  const ctx = await chromium.launchPersistentContext(profile, options(width));
  try {
    const page = ctx.pages()[0]; observe(page);
    for (const suffix of ['', '?area=home#inventory/ignored']) {
      await page.goto(new URL('/__demo/public'+suffix, base).href, {waitUntil:'commit'});
      await page.locator('#personal-home').waitFor();
      assert.equal(new URL(page.url()).hash,'#home');
      assert.equal(await page.getByRole('link',{name:'Reopen Inventory demo',exact:true}).count(),0);
    }
    results.push({width,mode:'healthy-home',defaultHome:true,explicitAreaWins:true});
    console.log('PASS',width,'ordinary public Home and explicit Home both land on Home');
  } finally { await ctx.close(); }
}
(async () => {
  const temp = path.resolve(os.tmpdir());
  const profiles = await fs.mkdtemp(path.join(temp,'wl-inventory-expiry-'));
  try {
    for (const width of [1360, mobile]) {
      for (const mode of ['open-tab', 'reopened']) {
        await runCase(path.join(profiles,width+'-'+mode), width, mode);
      }
      await homeControls(path.join(profiles,width+'-home'),width);
      await awayInPortuguese(path.join(profiles,width+'-away'),width);
    }
  } finally {
    await fs.writeFile(path.join(control,'browser-results.json'),JSON.stringify(results,null,2));
    assert.equal(path.dirname(profiles),temp);
    assert(path.basename(profiles).startsWith('wl-inventory-expiry-'));
    await fs.rm(profiles,{recursive:true,force:true,maxRetries:5,retryDelay:150});
  }
})().catch(error => {
  console.error(String(error.stack).replace(/https?:\/\/[^\s]+/g,'[local fixture]'));
  process.exitCode=1;
});
