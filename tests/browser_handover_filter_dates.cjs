const assert = require('node:assert/strict');
const { chromium } = require('playwright-core');

async function journey(browser, origin, width, pt) {
  const page = await browser.newPage({
    viewport: { width, height: 919 }, ignoreHTTPSErrors: true, serviceWorkers: 'block',
  });
  const overviewReads = [], writes = [];
  page.on('request', request => {
    const url = new URL(request.url());
    if (url.pathname.startsWith('/api/handovers') && request.method() !== 'GET') writes.push(request.method());
    if (url.pathname === '/api/handovers/overview/days') overviewReads.push(Object.fromEntries(url.searchParams));
  });
  try {
    await page.goto(origin + '/__demo/public?area=home');
    if (pt) {
      await page.locator('.ph-footer a[hreflang="pt-BR"]').click();
      await page.locator('html[lang="pt-BR"] #personal-home').waitFor();
    }
    await page.locator('.ph-footer a[href="#workspaces"]').click();
    await page.locator('#home-handovers').click();
    const ship = page.locator('#ho-vessel-filter select'), subject = page.locator('#hwd-subject');
    const range = page.locator('#hwd-range'), from = page.locator('#hwd-from'), to = page.locator('#hwd-to');
    const records = page.locator('.hwd-record'), jump = page.locator('#hwd-jump');

    async function pick(select, label) {
      const option = select.locator('option').filter({ hasText: label });
      await option.first().waitFor({ state: 'attached' });
      await select.selectOption(await option.first().getAttribute('value'));
    }
    async function settled(count) {
      await page.waitForFunction(expected => {
        const summary = document.querySelector('#hwd-count')?.textContent;
        return Number.parseInt(summary?.match(/\d+/)?.[0], 10) === expected && document.querySelectorAll('.hwd-record').length === expected;
      }, count);
    }
    async function readAfter(action, expectedDate) {
      const [response] = await Promise.all([page.waitForResponse(response => {
        const url = new URL(response.url());
        return url.pathname === '/api/handovers/overview/days' &&
          url.searchParams.get('date_from') === expectedDate && url.searchParams.get('date_to') === expectedDate;
      }), action()]);
      assert.equal(response.status(), 200);
      const saved = await response.json();
      await settled(saved.rows.length);
      const openers = await records.locator('[data-hwd-open]').evaluateAll(nodes => nodes.map(n => n.dataset.hwdOpen));
      assert.deepEqual(openers.slice().sort(), saved.rows.map(row => row.id).sort());
      return saved;
    }
    async function assertRange(day) {
      assert.equal(await from.inputValue(), day);
      assert.equal(await to.inputValue(), day);
      assert(await from.isVisible());
      assert(await to.isVisible());
    }
    async function enterDate(input, value) {
      await input.fill(value);
      await input.blur();
    }

    await records.first().waitFor();
    await pick(subject, /Meridian.*DEMO Survey/);
    const meridianSubject = await subject.inputValue();
    await settled(2);
    const september = await jump.locator('option[value$="-09-23"]').getAttribute('value');
    const november = september.slice(0, 4) + '-11-24';
    await range.locator('summary').click();
    await enterDate(from, november);
    await enterDate(to, november);
    await settled(0);
    const meridian = await readAfter(() => pick(ship, /Meridian/), november);
    assert.equal(meridian.rows.length, 0);
    await assertRange(november);
    assert.equal(await subject.inputValue(), meridianSubject);
    assert.equal(overviewReads.at(-1).date_from, november);
    assert.equal(overviewReads.at(-1).date_to, november);
    assert.equal(overviewReads.at(-1).vessel_id, await ship.inputValue());
    assert.equal(overviewReads.at(-1).subject_key, meridianSubject);
    assert(await page.locator('.hwd-empty').isVisible());
    await readAfter(() => ship.selectOption(''), november);
    await assertRange(november);
    const unfilteredShip = await readAfter(() => pick(subject, /Aurora.*DEMO Engineering/), november);
    const engineering = await subject.inputValue();
    const before = unfilteredShip.rows.map(row => row.id).sort();
    const aurora = await readAfter(() => pick(ship, /Aurora/), november);
    assert.deepEqual(aurora.rows.map(row => row.id).sort(), before);
    await assertRange(november);
    assert.equal(await subject.inputValue(), engineering);
    assert.deepEqual(await records.locator('[data-hwd-open]').evaluateAll(nodes => nodes.map(n => n.dataset.hwdOpen).sort()), before);
    const readsBefore = overviewReads.length;
    await pick(ship, /Meridian/);
    await page.locator('#hwd-status').getByText(pt ? /assunto selecionado está indisponível/i : /selected subject is unavailable/i).waitFor();
    await assertRange(november);
    assert.equal(await subject.inputValue(), '');
    assert.equal(await records.count(), 0);
    assert.equal(overviewReads.length, readsBefore);
    await ship.selectOption('');
    await settled(before.length);
    assert.equal(await subject.inputValue(), engineering);
    assert.deepEqual(await records.locator('[data-hwd-open]').evaluateAll(nodes => nodes.map(n => n.dataset.hwdOpen).sort()), before);

    await pick(subject, /Meridian.*DEMO Survey/);
    await settled(0);
    await enterDate(from, september);
    await enterDate(to, september);
    await settled(2);
    await pick(ship, /Meridian/);
    await settled(2);
    await assertRange(september);
    assert.equal(await subject.inputValue(), meridianSubject);
    await jump.selectOption(september);
    const button = records.nth(1).locator('[data-hwd-open]');
    const openerId = await button.getAttribute('data-hwd-open');
    await button.click();
    const preview = page.locator('#ho-record-preview'), title = preview.locator('h2');
    await title.waitFor();
    const firstTitle = await title.innerText();
    await page.goBack();
    await preview.waitFor({ state: 'detached' });
    assert.equal(await button.evaluate(e => e === document.activeElement && e.dataset.hwdOpen), openerId);
    await assertRange(september);
    await page.goForward();
    await title.waitFor();
    assert.equal(await title.innerText(), firstTitle);
    await preview.locator('.hop-head button').click();
    await preview.waitFor({ state: 'detached' });
    assert.equal(await jump.inputValue(), september);
    assert.deepEqual(writes, []);
    console.log('PASS', width, pt ? 'PT' : 'EN', november, 'Meridian 0; Engineering', before.length,
      '; unavailable subject explicit, no days read;', september, 'Meridian 2; preview Back/Forward');
  } finally {
    await page.close();
  }
}

(async () => {
  const url = new URL(process.argv[2]);
  assert.equal(url.hostname, '127.0.0.1');
  const browser = await chromium.launch({ executablePath: process.env.WAVELINK_TEST_CHROMIUM });
  try {
    await journey(browser, url.origin, 1360, false);
    await journey(browser, url.origin, 389, true);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
