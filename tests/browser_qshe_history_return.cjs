const assert = require('node:assert/strict');
const { chromium } = require('playwright-core');

const origin = new URL(process.argv[2]);
assert.equal(origin.hostname, '127.0.0.1');
const reportTitle = 'DEMO Unplanned interruption during deck preparation';
const reportRef = 'QH-000003';

async function expectVisibleFocus(locator) {
  await locator.evaluate(element => {
    if (element !== document.activeElement) {
      throw Error('Lost focus to ' + document.activeElement.tagName);
    }
    const box = element.getBoundingClientRect();
    if (box.y < 60 || box.bottom > innerHeight) {
      throw Error('Focus outside usable viewport ' + JSON.stringify(box));
    }
  });
}

async function journey(browser, width) {
  const page = await browser.newPage({
    viewport: { width, height: 919 }, ignoreHTTPSErrors: true, serviceWorkers: 'block',
  });
  try {
    await page.goto(origin.origin + '/__demo/public?area=hr');
    await page.locator('#hr-section-select').waitFor({ state: 'attached' });
    await page.getByRole('link', { name: 'All workspaces', exact: true }).first().click();
    await page.locator('#home-qshe').click();
    const query = page.locator('#qs-query');
    const row = page.locator('[data-qs-id]').filter({ hasText: reportTitle });
    const detail = page.locator('#qs-detail');
    const historyButton = page.locator('#qs-history');
    const returnButton = page.locator('#qs-return');

    await query.fill('preparation');
    const applied = page.waitForResponse(response => {
      const url = new URL(response.url());
      return url.pathname.endsWith('/api/qshe') && url.searchParams.get('query') === 'preparation';
    });
    await query.press('Enter');
    await applied;
    await page.waitForFunction(() => document.querySelector('#qs-active')?.textContent.includes('preparation'));
    await row.waitFor();
    const id = await row.getAttribute('data-qs-id');
    await row.click();
    await historyButton.waitFor();
    const identity = await detail.locator('.eyebrow').innerText();
    assert.match(identity, /^QH-000003 \/ SAVED REVISION \d+$/);
    assert.equal(await detail.locator('h2').first().innerText(), reportTitle);

    async function checkReport() {
      await historyButton.waitFor();
      assert.equal(await detail.locator('.eyebrow').innerText(), identity);
      assert.equal(await detail.locator('h2').first().innerText(), reportTitle);
      assert.equal(await query.inputValue(), 'preparation');
      assert.equal(await row.getAttribute('data-qs-id'), id);
    }

    async function checkHistory() {
      await returnButton.waitFor();
      const text = await detail.innerText();
      assert(text.includes(identity));
      assert(text.includes(reportTitle));
    }

    await historyButton.click();
    await returnButton.waitFor();
    await returnButton.click();
    await historyButton.waitFor();
    if (process.argv.includes('baseline')) {
      console.log('BASELINE', width, identity, 'return focus:', await historyButton.evaluate(el => el === document.activeElement));
      await page.goBack();
      console.log('BASELINE native Back:', new URL(page.url()).hash);
      return;
    }
    await checkReport();
    await expectVisibleFocus(historyButton);
    await page.goForward();
    await checkHistory();
    await page.goBack();
    await checkReport();
    await expectVisibleFocus(historyButton);
    await page.goBack();
    await historyButton.waitFor({ state: 'detached' });
    assert.equal(await query.inputValue(), 'preparation');
    assert((await row.innerText()).includes(reportRef));
    await expectVisibleFocus(row);
    await page.goForward();
    await checkReport();
    await page.goForward();
    await checkHistory();
    await returnButton.click();
    await checkReport();
    await expectVisibleFocus(historyButton);
    console.log('PASS', width, reportTitle, identity, 'list / report / history, search, row and focus');
  } finally {
    await page.close();
  }
}

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.WAVELINK_TEST_CHROMIUM });
  try {
    for (const width of [1360, 389]) await journey(browser, width);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
