'use strict';

const assert = require('node:assert/strict');
const path = require('node:path');
const { chromium } = require('playwright-core');

async function capture(page, view, language) {
  if (process.env.WAVELINK_SCREENSHOT_DIR) {
    await page.screenshot({ path: path.join(process.env.WAVELINK_SCREENSHOT_DIR, 'Wavelink-inventory-' + view + '-' + language + '.png') });
  }
}

async function visit(page, hash) {
  const url = new URL(page.url());
  url.hash = hash;
  await page.goto(url.href);
}

async function verify(browser, entry, language, width) {
  const pt = language === 'pt';
  const context = await browser.newContext({
    viewport: { width, height: 900 }, serviceWorkers: 'block', ignoreHTTPSErrors: true,
  });
  try {
    const page = await context.newPage();
    page.setDefaultTimeout(10000);
    await page.goto(entry);
    await page.locator('#wl-global-search-trigger:visible').waitFor({ timeout: 60000 });
    if (pt) {
      await visit(page, 'profile');
      await page.locator('#wl-language-select').selectOption('pt-BR');
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
    }

    await visit(page, 'inventory');
    const vessel = page.getByRole('combobox', { name: pt ? 'Embarcação' : 'Vessel', exact: true });
    const offshore = page.locator('.iw162-inventory-row').filter({ hasText: 'DEMO Offshore equipment' });
    const consumables = page.locator('.iw162-inventory-row').filter({ hasText: 'DEMO Consumables' });
    await offshore.waitFor();
    await consumables.waitFor();
    await vessel.locator('option').filter({ hasText: 'DEMO Meridian' }).waitFor({ state: 'attached' });
    const options = await vessel.locator('option').evaluateAll(all =>
      all.map(o => ({ value: o.value, label: o.textContent.trim() }))
    );
    const idOf = name => {
      const match = options.find(o => o.label.includes(name));
      assert.ok(match, 'Fleet vessel appears in the picker: ' + name);
      return match.value;
    };
    const meridian = idOf('DEMO Meridian');
    const horizon = idOf('DEMO Horizon');
    const aurora = idOf('MV Aurora');
    assert.equal(options.find(o => !o.value).label, pt ? 'Todas as embarcações' : 'All vessels');
    assert.ok(!options.some(o => /DEMO (Shore Base|Workshop)/i.test(o.label)), 'Vessel options exclude other site types');
    assert.equal(await vessel.inputValue(), '');
    const fits = await vessel.evaluate(el => {
      const r = el.getBoundingClientRect();
      return r.left >= 0 && r.right <= innerWidth + 1 && document.documentElement.scrollWidth <= innerWidth + 1;
    });
    assert.ok(fits, 'Inventory catalogue vessel picker fits the viewport');

    await vessel.selectOption(aurora);
    await page.locator('#inventory-catalog-empty').waitFor();
    assert.equal(await page.locator('.iw162-inventory-row').count(), 0);
    await vessel.selectOption(meridian);
    await offshore.waitFor();
    assert.equal(await consumables.count(), 0, 'The book with no onboard inventory is excluded');
    await capture(page, 'vessel-filter', language);
    const onboard = parseInt(await offshore.locator('.iw162-inventory-counts span').first().innerText(), 10);
    assert.ok(onboard > 0);
    const catalogueSearch = page.locator('[name="inventory_catalog_query"]');
    await catalogueSearch.fill('consumables');
    await page.locator('#inventory-catalog-empty').waitFor();
    await catalogueSearch.fill('offshore');
    await offshore.waitFor();
    const bookId = await offshore.getAttribute('data-inventory-id');
    const response = page.waitForResponse(r => new URL(r.url()).pathname === '/api/inventory/lists/' + bookId);
    await offshore.click();
    const book = await (await response).json();
    const records = page.locator('#inv-rows [data-select-row]');
    const record = name => records.filter({ has: page.getByRole('button', { name, exact: true }) });
    const multimeter = 'DEMO Training multimeter';
    await record(multimeter).waitFor();
    assert.equal(await vessel.inputValue(), meridian, 'Entering a book keeps the chosen vessel');
    const ids = async () => (await records.evaluateAll(all => all.map(el => el.dataset.selectRow))).sort();
    // Both conditions matter: a received record can have its former destination,
    // and a dispatched record can still carry its old operational work site.
    const physicalSite = x => x.fleet_custody
      ? (x.fleet_custody.state === 'in_transit' ? '' : x.fleet_custody.site_id)
      : x.work_site?.id;
    const expected = id => book.items.filter(x => !x.archived && physicalSite(x) === id);
    assert.deepEqual(await ids(), expected(meridian).map(x => x.id).sort());
    assert.equal(await records.count(), onboard, 'Catalogue and register count the same onboard items');
    assert.ok(expected(meridian).some(x => x.name === multimeter && x.container_id), 'Nested stock appears without opening the box');
    assert.equal(await page.locator('#inv-filters').getAttribute('aria-expanded'), 'false', 'The vessel picker is visible in the main toolbar');
    await vessel.scrollIntoViewIfNeeded();
    await capture(page, 'onboard-records', language);
    const search = page.locator('.iw-search-panel [name="search"]');
    await search.fill('multimeter');
    assert.equal(await records.count(), 1);
    await page.locator('#inv-filters').click();
    await page.locator('select[name="location"]').selectOption('Shore warehouse / Bay A');
    await page.locator('#inv-empty-clear').waitFor();
    assert.equal(await records.count(), 0, 'Storage location intersects the vessel and text filters');
    await page.locator('#inv-empty-clear').click();
    assert.equal(await vessel.inputValue(), '');
    assert.equal(await search.inputValue(), '');

    await vessel.selectOption(horizon);
    assert.deepEqual(await ids(), expected(horizon).map(x => x.id).sort(), 'A manifest destination is not an onboard assignment');
    await vessel.selectOption(meridian);
    await record(multimeter).locator('input[type=checkbox]').check();
    await vessel.selectOption(aurora);
    await page.locator('#inv-empty-clear').waitFor();
    assert.equal(await records.count(), 0);
    await vessel.selectOption(meridian);
    assert.equal(await record(multimeter).locator('input[type=checkbox]').isChecked(), false, 'A hidden item is removed from bulk selection');
    await page.locator('#inv-clear-filters').click();
    await page.locator('#inv-expand').click();
    assert.equal(await records.count(), book.items.filter(x => !x.archived).length, 'All vessels restores the complete inventory');
    console.log(language + ' ' + width + 'px: vessel catalogue, onboard counts, nested stock, combined filters and reset passed');
  } finally {
    await context.close();
  }
}

async function main() {
  const entry = process.argv[2];
  assert.ok(entry, 'Provide the fictional demonstration entry URL');
  const browser = await chromium.launch({ executablePath: process.env.WAVELINK_TEST_CHROMIUM });
  try {
    await verify(browser, entry, 'en', 1280);
    await verify(browser, entry, 'pt', 390);
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
