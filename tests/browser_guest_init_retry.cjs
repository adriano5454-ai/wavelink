const assert = require('node:assert/strict');
const { mkdtemp, rm } = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');
const { chromium } = require('playwright-core');

const url = new URL(process.argv[2]);
assert.equal(url.protocol, 'https:');
assert.equal(url.hostname, '127.0.0.1');
const launch = { executablePath: process.env.WAVELINK_TEST_CHROMIUM, headless: true };
const marker = 'window:qa-guest-retry-preservation:main';

// Only instrument the public entry document. The abort is a real IndexedDB abort.
// The recovered app and all other database operations use the native implementation.
function failOnce(mode) {
  if (location.pathname !== '/__demo/public') return;
  let failed = false;
  const open = IDBFactory.prototype.open;
  window.guestOpeningAttempts = 0;
  IDBFactory.prototype.open = function (name, version) {
    const request = open.apply(this, arguments);
    if (name !== 'pxgeo-dive-check-1' || version !== 1) return request;
    window.guestOpeningAttempts++;
    if (mode === 'fresh' && !failed) {
      const setter = Object.getOwnPropertyDescriptor(IDBOpenDBRequest.prototype, 'onupgradeneeded').set;
      Object.defineProperty(request, 'onupgradeneeded', {set(callback) {
        setter.call(request, function (event) {
          callback.call(this, event);
          failed = true;
          request.transaction.abort();
        });
      }});
    }
    return request;
  };
  if (mode === 'reopened') {
    const transaction = IDBDatabase.prototype.transaction;
    IDBDatabase.prototype.transaction = function (stores, access) {
      const tx = transaction.apply(this, arguments);
      if (!failed && this.name === 'pxgeo-dive-check-1' && stores === 'state' && access === 'readwrite') {
        failed = true;
        // Let the actual bootstrap attach its onabort handler before aborting the transaction.
        queueMicrotask(() => tx.abort());
      }
      return tx;
    };
  }
  window.addEventListener('pagehide', () => {
    sessionStorage.setItem('qaGuestOpenAttempts', String(window.guestOpeningAttempts));
  }, {once:true});
}

async function savedState(input) {
  const db = await new Promise((resolve,reject) => {
    const open = indexedDB.open('pxgeo-dive-check-1',1);
    open.onsuccess = () => resolve(open.result);
    open.onerror = () => reject(open.error);
  });
  try {
    return await new Promise((resolve,reject) => {
      const tx = db.transaction('state', input.seed ? 'readwrite' : 'readonly');
      const store = tx.objectStore('state');
      if (input.seed) store.add({qa:'existing synthetic workspace'},input.marker);
      // Never read saved account or session objects. Only the isolated marker's
      // value and existence of the earlier workspace's key are needed.
      const marker = store.get(input.marker);
      const previous = store.getKey('window:'+input.workspace+':main');
      tx.oncomplete = () => resolve({marker:marker.result?.qa, previous:!!previous.result});
      tx.onabort = () => reject(tx.error);
    });
  } finally { db.close(); }
}

async function exercise(ctx, mode) {
  await ctx.addInitScript(failOnce, mode);
  const page = await ctx.newPage();
  let entries = 0, staff = 0;
  page.on('request', request => {
    const u = new URL(request.url());
    if (request.isNavigationRequest() && u.pathname === '/__demo/public') entries++;
    if (u.pathname === '/__demo/login') staff++;
  });
  const guest = new URL('/__demo/public?area=inventory',url);
  await page.goto(guest.href);
  const message = mode === 'fresh' ? 'The demo could not open browser storage. Please try again.'
    : 'The demo could not save this visit. Please try again.';
  const retry = page.getByRole('button',{name:'Try again',exact:true});
  await retry.waitFor();
  assert.equal(page.url(),guest.href);
  assert.equal(await page.getByRole('alert').innerText(),message);
  assert.equal(await retry.count(),1);
  assert(await retry.isEnabled());
  assert((await retry.boundingBox()).height >= 44);
  // Simulate an extra activation in the same event turn before the async open succeeds.
  await retry.evaluate(button => button.addEventListener('click',()=>{
    sessionStorage.setItem('qaRetryWasDisabled', String(button.disabled));
    button.click();
  },{once:true}));
  if (mode === 'fresh') {
    await page.keyboard.press('Tab');
    assert(await retry.evaluate(button=>button === document.activeElement));
    await page.keyboard.press('Enter');
  } else await retry.tap();
  const book = page.locator('[data-inventory-id]').filter({hasText:'Offshore equipment'}).first();
  await book.waitFor();
  assert.equal(new URL(page.url()).hash,'#inventory');
  assert.equal(await page.evaluate(()=>document.documentElement.lang),'en');
  assert.equal(await page.evaluate(()=>sessionStorage.getItem('qaGuestOpenAttempts')),'2');
  assert.equal(await page.evaluate(()=>sessionStorage.getItem('qaRetryWasDisabled')),'true');
  assert.equal(entries,1);
  assert.equal(staff,0);
  await book.click();
  const rows = page.locator('#inv-rows [data-select-row]');
  await rows.first().waitFor();
  assert(await rows.count()>0);
  console.log('PASS',mode,page.viewportSize().width,'one admission, two IDB attempts, Offshore equipment rows',await rows.count());
  return page;
}

(async () => {
  const browser = await chromium.launch(launch);
  try {
    const ctx = await browser.newContext({ignoreHTTPSErrors:true, viewport:{width:1360,height:919}});
    await exercise(ctx,'fresh');
    await ctx.close();
  } finally { await browser.close(); }

  const tmp = path.resolve(os.tmpdir());
  const profile = await mkdtemp(path.join(tmp,'wl-guest-retry-'));
  const settings = {...launch,ignoreHTTPSErrors:true,viewport:{width:389,height:919},hasTouch:true};
  let ctx;
  try {
    ctx = await chromium.launchPersistentContext(profile,settings);
    const first = await ctx.newPage();
    await first.goto(new URL('/__demo/public?area=home',url).href);
    await first.locator('#personal-home').waitFor();
    const workspace = new URL(first.url()).searchParams.get('browser_workspace');
    assert(workspace);
    const before = await first.evaluate(savedState,{marker,workspace,seed:true});
    assert.deepEqual(before,{marker:'existing synthetic workspace',previous:true});
    await ctx.close();
    ctx = await chromium.launchPersistentContext(profile,settings);
    const recovered = await exercise(ctx,'reopened');
    assert.deepEqual(await recovered.evaluate(savedState,{marker,workspace}),before);
    console.log('PASS reopened profile retained prior workspace and untouched fictional marker');
  } finally {
    if (ctx) await ctx.close();
    assert.equal(path.dirname(profile),tmp);
    assert(path.basename(profile).startsWith('wl-guest-retry-'));
    await rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:150});
  }
})().catch(error => { console.error(error); process.exitCode=1; });
