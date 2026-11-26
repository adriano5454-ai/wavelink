'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');

const origin = new URL(process.argv[2]);
assert.equal(origin.hostname, '127.0.0.1', 'Run only with the disposable loopback showcase.');
const catalogue = /\/api\/inventory\/lists\?include_vessels=true$/;
const bookDetail = /\/api\/inventory\/lists\/[^/?]+$/;

async function holdNext(page, pattern) {
  let entered, release, completed;
  const requested = new Promise(resolve => { entered = resolve; });
  const gate = new Promise(resolve => { release = resolve; });
  const finished = new Promise(resolve => { completed = resolve; });
  await page.route(pattern, async route => {
    try {
      const response = await route.fetch();
      entered();
      await gate;
      await route.fulfill({response});
    } finally {
      completed();
    }
  }, {times: 1});
  return {requested, release, finished};
}

async function pending(page, title, status) {
  const heading = page.locator('#inventory-open-heading');
  await heading.waitFor();
  assert.equal(await heading.innerText(), title);
  assert.equal(await page.locator('#inventory-open-status[role="status"]').innerText(), status);
  assert.equal(await page.locator('#app [aria-busy=true]').count(), 1);
  assert.equal(await page.locator('#inventory-catalog, #inv-rows, #fw-refresh').count(), 0);
  const box = await heading.boundingBox();
  assert.ok(box.y >= 0 && box.y + box.height <= page.viewportSize().height, 'Opening heading visible in viewport');
}

async function verify(browser, width) {
  const ctx = await browser.newContext({viewport: {width, height: 919}, ignoreHTTPSErrors: true});
  const page = await ctx.newPage();
  page.setDefaultTimeout(13000);
  try {
    const cold = await holdNext(page, catalogue);
    await page.goto(origin.origin + '/__demo/public?area=inventory', {waitUntil: 'domcontentloaded'});
    await pending(page, 'Inventories', 'Loading inventories…');
    cold.release();

    const books = page.locator('a[data-inventory-id]');
    const offshore = books.filter({hasText: 'Offshore equipment'});
    await offshore.waitFor();
    const title = await offshore.locator('h2').innerText();
    const href = await offshore.getAttribute('href');
    const other = books.filter({hasNotText: 'Offshore equipment'});
    const otherTitle = await other.locator('h2').innerText();
    const otherHref = await other.getAttribute('href');

    const late = await holdNext(page, bookDetail);
    await offshore.focus();
    await page.keyboard.press('Enter');
    await pending(page, title, 'Opening ' + title + '…');
    await late.requested;
    await page.goBack();
    await other.waitFor();
    await other.click();
    await page.locator('[data-equipment-workspace="inventory-record"]').waitFor();
    assert.ok((await page.locator('#app').innerText()).includes(otherTitle));
    late.release();
    await late.finished;
    await page.waitForFunction(hash => location.hash === hash &&
      !!document.querySelector('[data-equipment-workspace="inventory-record"]'), otherHref);
    assert.ok((await page.locator('#app').innerText()).includes(otherTitle));
    assert.equal(await page.locator('#app').getByText('DEMO Bench interface unit', {exact: true}).count(), 0);

    await page.goBack();
    await offshore.click();
    const rows = page.locator('#inv-rows [data-select-row]');
    await rows.first().waitFor();
    assert.equal(await rows.count(), 17);
    const refresh = await holdNext(page, bookDetail);
    await page.locator('#fw-refresh').click();
    await refresh.requested;
    assert.equal(await rows.count(), 17);
    assert.equal(await page.locator('#inventory-open-status').count(), 0);
    refresh.release();
    await refresh.finished;

    const direct = await holdNext(page, bookDetail);
    await page.reload({waitUntil: 'domcontentloaded'});
    await pending(page, 'Inventory', 'Loading inventory items…');
    assert.equal(new URL(page.url()).hash, href);
    direct.release();
    await rows.first().waitFor();
    console.log(width + 'px PASS: catalogue, named opening by keyboard, late book vs second book, warm refresh, unnamed deep link (17 records).');
  } finally {
    await ctx.close();
  }
}

async function verifyPortuguese(browser, width) {
  const ctx = await browser.newContext({viewport: {width, height: 919}, ignoreHTTPSErrors: true});
  try {
    const page = await ctx.newPage();
    page.setDefaultTimeout(13000);
    await page.goto(origin.origin + '/__demo/public?area=home');
    await page.locator('#personal-home a[hreflang="pt-BR"]').click();
    await page.locator('html[lang="pt-BR"] .ph-footer a[href="#workspaces"]').click();
    await page.locator('#home-find').waitFor();
    const cold = await holdNext(page, catalogue);
    await page.locator('#app a[href="#inventory"]:visible').first().click();
    await pending(page, 'Inventários', 'Carregando inventários…');
    cold.release();
    const offshore = page.locator('a[data-inventory-id]').filter({hasText: 'Offshore equipment'});
    await offshore.waitFor();
    const title = await offshore.locator('h2').innerText();
    const selected = await holdNext(page, bookDetail);
    await offshore.click();
    await pending(page, title, 'Abrindo ' + title + '…');
    selected.release();
    await page.waitForFunction(() => document.querySelectorAll('#inv-rows [data-select-row]').length === 17);
    console.log(width + 'px PASS: Portuguese selected on Home, catalogue and exact inventory title/status, 17 records.');
  } finally {
    await ctx.close();
  }
}

(async () => {
  const browser = await chromium.launch({executablePath: process.env.WAVELINK_TEST_CHROMIUM, args: ['--no-proxy-server']});
  try {
    for (const width of [1360,389]) {
      await verify(browser, width);
      await verifyPortuguese(browser, width);
    }
  } finally {
    await browser.close();
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
