const assert = require('node:assert/strict');
const { chromium } = require('playwright-core');
const origin = new URL(process.argv[2] || process.env.WAVELINK_BASE_URL);
assert.equal(origin.hostname, '127.0.0.1');
const baseline = process.argv.includes('--baseline');

async function run(browser, width) {
  const page = await browser.newPage({viewport: {width, height: 919}, ignoreHTTPSErrors: true, serviceWorkers: 'block'});
  try {
    await page.goto(origin.origin + '/__demo/public?area=inventory');
    await page.locator('[data-inventory-id]').filter({hasText: 'Offshore equipment'}).click();
    await page.locator('[name=search]').fill('TRAIN-LOOSE-002');
    await page.getByText('DEMO Bench interface unit', {exact: true}).first().click();
    await page.locator('#inv-asset-profile').click();
    await page.locator('.asset-metric[data-asset-jump="asset-documents"]').click();
    const assetHash = new URL(page.url()).hash;
    const docs = page.locator('#asset-documents');
    const query = docs.locator('[data-asset-linked-query]');
    const row = docs.locator('[data-asset-linked]:visible').filter({hasText: 'DEMO-CERT-002'});
    await query.fill('DEMO-CERT-002');
    await row.evaluate(el => el.scrollIntoView({block: 'center', behavior: 'instant'}));
    const before = (await row.boundingBox()).y;
    const certHash = await row.getAttribute('href');
    const record = page.locator('#certificate-workspace');
    const title = record.getByRole('heading', {name: 'DEMO Certificate register 002', exact: true});
    const back = page.locator('#cert-back-asset');
    async function checkRecord() {
      await title.waitFor();
      assert.equal(new URL(page.url()).hash, certHash);
      const position = await title.boundingBox();
      const identity = record.locator('[data-certificate-identity]');
      const summary = await identity.innerText();
      for (const value of ['DEMO-CERT-002', 'DEMO R1', 'TRAIN-LOOSE-002']) assert(summary.includes(value), summary);
      const identityBox = await identity.boundingBox();
      assert(position.y >= 60 && identityBox.y + identityBox.height <= 919, JSON.stringify({width, position, identityBox}));
      assert(await title.evaluate(e => e === document.activeElement));
      return position.y;
    }
    async function checkOrigin() {
      await docs.waitFor();
      await page.waitForFunction(() => document.activeElement?.matches('#asset-documents [data-asset-linked]'));
      assert.equal(new URL(page.url()).hash, assetHash);
      assert.equal(await query.inputValue(), 'DEMO-CERT-002');
      assert.equal(await docs.locator('[data-asset-linked]:visible').count(), 1);
      assert.equal(await row.getAttribute('href'), certHash);
      assert(await row.evaluate(e => e === document.activeElement));
      assert.equal(await page.locator('[data-asset-nav][aria-pressed=true]').getAttribute('data-asset-jump'), 'asset-documents');
      await page.locator('#asset-documents-context[aria-busy="false"]').waitFor({state: 'attached'});
      await page.waitForFunction(target => Math.abs(document.activeElement.getBoundingClientRect().top - target) <= 4, before);
      const y = (await row.boundingBox()).y;
      assert(Math.abs(y - before) <= 4, JSON.stringify({width, before, y}));
    }
    await row.click();
    if (baseline) {
      await title.waitFor();
      const titleY = (await title.boundingBox()).y;
      await page.goBack();
      await page.waitForFunction(hash => location.hash === hash, assetHash);
      await page.waitForTimeout(500);
      console.log(JSON.stringify({width, titleY, certificateStillShowing: await record.count() > 0,
        assetShowing: await page.locator('.asset-workspace').count() > 0, focus: await page.evaluate(() => document.activeElement.tagName)}));
      return;
    }
    const titleY = await checkRecord();
    const history = page.locator('#cert-history');
    await history.click();
    const modal = page.locator('dialog[open]');
    const text = await modal.innerText();
    for (const value of ['DEMO Certificate register 002', 'DEMO-CERT-002', 'TRAIN-LOOSE-002', 'DEMO R1']) assert(text.includes(value), text);
    await modal.getByRole('button', {name: /Close window/i}).click();
    await page.waitForFunction(() => document.activeElement?.id === 'cert-history');
    await page.goBack();
    await checkOrigin();
    await page.goForward();
    await checkRecord();
    await back.click();
    await checkOrigin();
    await row.click();
    await checkRecord();
    const linked = page.locator('details').filter({has: page.locator('summary').filter({hasText: 'Linked equipment'})});
    if (!await linked.evaluate(el => el.open)) await linked.locator('summary').click();
    const equipment = linked.getByRole('link', {name: /DEMO Bench interface unit/});
    const target = await equipment.getAttribute('href');
    assert.equal(target.split('/').at(-1), assetHash.split('/').at(-1));
    await equipment.click();
    const linkedTitle = page.getByRole('heading', {name: 'DEMO Bench interface unit', exact: true}).first();
    await linkedTitle.waitFor();
    assert.equal(new URL(page.url()).hash, target);
    assert.equal(await page.locator('.asset-workspace').getAttribute('data-asset-id'), assetHash.split('/').at(-1));
    assert.equal(await record.count(), 0);
    assert.equal(await page.locator('[data-asset-nav][aria-pressed=true]').getAttribute('data-asset-jump'), 'asset-overview');
    await page.goBack();
    await checkRecord();
    console.log(JSON.stringify({width, titleY, originY: before, certificate: 'DEMO-CERT-002', revision: 'DEMO R1',
      asset: 'TRAIN-LOOSE-002', nativeBackForward: true, contextualBack: true, linkedEquipment: true, historyCloseFocus: true}));
  } finally { await page.close(); }
}
(async () => {
  const browser = await chromium.launch({executablePath: process.env.WAVELINK_TEST_CHROMIUM});
  try { for (const width of [1360, 389]) await run(browser, width); }
  finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
