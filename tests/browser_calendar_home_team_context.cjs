const { chromium } = require('playwright-core');
const assert = require('node:assert/strict');

async function metrics(locator) {
  return locator.evaluate(element => {
    const { top, bottom } = element.getBoundingClientRect();
    return { top, bottom, focused: document.activeElement === element };
  });
}

async function focused(page, selector) {
  await page.waitForFunction(s => document.querySelector(s) === document.activeElement, selector);
  const box = await metrics(page.locator(selector));
  assert(box.top >= 60 && box.bottom < page.viewportSize().height, JSON.stringify({ selector, box }));
  return box.top;
}

async function check(browser, origin, width) {
  const page = await browser.newPage({ viewport: { width, height: 919 }, ignoreHTTPSErrors: true, serviceWorkers: 'block' });
  try {
    await page.goto(origin + '/__demo/public?area=hr');
    await page.locator('#hr-section-select').waitFor({ state: 'attached' });
    await page.evaluate(() => { location.hash = 'calendar'; });
    const month = page.locator('[name="calmonth"]');
    if (await month.inputValue() !== '2026-11') await month.fill('2026-11');
    const day = '.calendar-day[data-calendar-day="2026-11-26"]';
    await page.locator(day).click();
    const agenda = '#calendar-agenda-title';
    const position = await focused(page, agenda);
    if (!await page.locator('a[data-workspace="team"]').isVisible()) await page.locator('#shell-toggle').click();
    await page.locator('a[data-workspace="team"]').click();
    const heading = '.wl-rec-heading h1';
    const teamTop = await focused(page, heading);
    async function calendarReturned() {
      const top = await focused(page, agenda);
      assert.equal(await page.locator(day).getAttribute('aria-pressed'), 'true');
      assert(Math.abs(top - position) <= 3, JSON.stringify({ top, position }));
    }
    await page.goBack();
    await calendarReturned();
    await page.goForward();
    await focused(page, heading);
    await page.goBack();
    await calendarReturned();

    await page.evaluate(() => { location.hash = 'home'; });
    const article = page.locator('.wl-news-post h3').first();
    const first = await article.innerText();
    await page.locator('#wl-home-news-older:enabled').click();
    await page.waitForFunction(original => {
      const title = document.querySelector('.wl-news-post h3')?.textContent;
      return title && title !== original;
    }, first);
    const second = await article.innerText();
    const link = '.wl-home-news-all';
    await page.locator(link).scrollIntoViewIfNeeded();
    const linkTop = (await metrics(page.locator(link))).top;
    await page.locator(link).click();
    const newsTop = await focused(page, '#wl-news-title');
    async function newsReturned() {
      const top = await focused(page, link);
      assert.equal(await article.innerText(), second);
      assert(Math.abs(top - linkTop) <= 3, JSON.stringify({ top, linkTop }));
    }
    await page.goBack();
    await newsReturned();
    await page.goForward();
    await focused(page, '#wl-news-title');
    await page.goBack();
    await newsReturned();
    await page.locator('#wl-home-news-newer').click();
    await page.waitForFunction(original => document.querySelector('.wl-news-post h3')?.textContent === original, first);
    console.log('PASS', width, { teamTop, agendaOnReturn: position, newsTop, second, linkTop });
  } finally {
    await page.close();
  }
}

(async () => {
  const origin = new URL(process.argv[2]).origin;
  assert.equal(new URL(origin).hostname, '127.0.0.1');
  const browser = await chromium.launch({ executablePath: process.env.WAVELINK_TEST_CHROMIUM });
  try {
    for (const width of [1360, 389]) await check(browser, origin, width);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
