'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');

// Run against the disposable local native showcase used by guest_inventory_expiry_fixture.py.
const base = new URL(process.argv[2]);
assert.ok(base.protocol === 'https:' && base.hostname === '127.0.0.1' && !base.username && !base.password,
  'Use a loopback HTTPS showcase fixture.');
const pollPaths = ['/api/tasks/summary', '/api/assets/alerts'];

async function verify(browser) {
  const page = await browser.newPage({ignoreHTTPSErrors: true, viewport: {width: 1360, height: 919}});
  page.setDefaultTimeout(12000);
  let release;
  const held = new Promise(resolve => { release = resolve; });
  try {
    await page.goto(base.origin + '/__demo/public?area=inventory', {waitUntil: 'commit'});
    await page.locator('a[data-inventory-id]').filter({hasText: 'Offshore equipment'}).click();
    const rows = page.locator('#inv-rows [data-select-row]');
    await rows.first().waitFor();
    assert.equal(await rows.count(), 17);
    const saved = page.url();

    const errors = [];
    const earlyPolls = [];
    page.on('pageerror', error => errors.push(error.name + ': ' + error.message));
    const whileHeld = request => {
      const url = new URL(request.url());
      if (url.origin === base.origin && pollPaths.includes(url.pathname)) earlyPolls.push(url.pathname);
    };
    page.on('request', whileHeld);
    await page.route(url => url.origin === base.origin && url.pathname === '/static/app.js', async route => {
      await held;
      await route.continue();
    }, {times: 1});
    await page.reload({waitUntil: 'commit'});
    await page.waitForFunction(() => window.AJOperations && window.AJAssets && typeof state === 'undefined');
    // Wait on the real page clock from the moment both early modules have executed.
    await page.evaluate(() => new Promise(resolve => setTimeout(resolve, 16000)));
    assert.ok(await page.evaluate(() => typeof state === 'undefined'), 'Core must still be held at the first poll');
    assert.deepEqual(errors, [], 'Errors before core initialization');
    assert.deepEqual(earlyPolls, [], 'Optional modules polled before the core was ready');
    page.off('request', whileHeld);
    release();

    await rows.first().waitFor();
    assert.equal(await rows.count(), 17);
    assert.ok(page.url() === saved, 'Reload must retain the same visit and book');
    // Start listening after the book settles to verify both live periodic reads still run.
    await Promise.all(pollPaths.map(path => page.waitForResponse(response => {
      const url = new URL(response.url());
      return url.origin === base.origin && url.pathname === path &&
        response.request().method() === 'GET' && response.status() === 200;
    }, {timeout: 25000})));
    assert.deepEqual(errors, [], 'Errors after core initialization');
    console.log('Delayed same-book reload passed: 17 rows, zero page errors, both alert polls returned 200.');
  } finally {
    release();
    await page.unrouteAll({behavior: 'wait'});
    await page.close();
  }
}

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.WAVELINK_TEST_CHROMIUM, headless: true,
    args: ['--ignore-certificate-errors', '--disable-background-networking', '--no-proxy-server',
      '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1, EXCLUDE localhost']
  });
  try { await verify(browser); } finally { await browser.close(); }
})().catch(error => {
  console.error(String(error.message).replace(/https?:\/\/[^\s]+/g, '[fixture URL]'));
  process.exitCode = 1;
});
