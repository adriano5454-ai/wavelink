'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');

const base = new URL(process.argv[2]);
assert.ok(base.protocol === 'https:' && base.hostname === '127.0.0.1' && !base.username && !base.password,
  'Use the disposable HTTPS loopback showcase.');
const checklistPaths = new Set(['/api/templates', '/api/template', '/api/records']);

async function verify(browser) {
  const page = await browser.newPage({ignoreHTTPSErrors: true, viewport: {width: 1360, height: 919}});
  page.setDefaultTimeout(20000);
  try {
    const reads = [];
    page.on('request', request => {
      const url = new URL(request.url());
      if (request.method() === 'GET' && url.origin === base.origin && checklistPaths.has(url.pathname)) {
        reads.push(url.pathname);
      }
    });
    await page.goto(base.origin + '/__demo/public?area=inventory', {waitUntil: 'commit'});
    await page.locator('a[data-inventory-id]').filter({hasText: 'Offshore equipment'}).click();
    const rows = page.locator('#inv-rows [data-select-row]');
    await rows.first().waitFor();
    assert.equal(await rows.count(), 17);
    assert.deepEqual(reads, [], 'An unrelated checklist read started before Offshore equipment was usable.');

    const checklists = page.locator('#workspace-nav a[data-workspace="checklists"]');
    if (!await checklists.isVisible()) await page.locator('#shell-toggle').click();
    const [response] = await Promise.all([
      page.waitForResponse(response => {
        const url = new URL(response.url());
        return response.request().method() === 'GET' && url.origin === base.origin && url.pathname === '/api/records';
      }),
      checklists.click()
    ]);
    assert.equal(response.status(), 200);
    const card = page.locator('article[data-cw-card]').filter({hasText: 'DEMO-CHECK-001'});
    await card.waitFor();
    assert.equal(new URL(page.url()).hash, '#checklists');
    console.log('PASS: 17 Offshore equipment rows with no early checklist reads; Checklists fetched records and showed DEMO-CHECK-001.');
  } finally {
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
