// Verify the disposable public workspace in desktop English and mobile Portuguese.
const assert = require('node:assert/strict');
const path = require('node:path');
const { chromium } = require('playwright-core');

async function navigate(page, route) {
  const link = page.locator('a[href="#' + route + '"]:visible').first();
  if (await link.count()) return link.click();
  const url = new URL(page.url());
  url.hash = route;
  return page.goto(url.href);
}

async function verify(browser, entry, language, width) {
  const context = await browser.newContext({
    viewport: { width, height: 850 }, serviceWorkers: 'block',
    reducedMotion: 'reduce', ignoreHTTPSErrors: true
  });
  try {
    const page = await context.newPage();
    page.setDefaultTimeout(18000);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(entry);
    await page.locator('#wl-global-search-trigger:visible').waitFor({timeout: 60000});
    if (language === 'pt') {
      await navigate(page, 'profile');
      await page.locator('#wl-language-select').selectOption('pt-BR');
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
    }
    for (const route of ['home','team']) {
      await navigate(page, route);
      const panel = page.locator('#wl-news:visible');
      await panel.getByRole('heading', {name: language === 'pt' ? 'Notícias da equipe' : 'Team news'}).waitFor();
      const notice = panel.locator('article').filter({hasText:'Fire alarm drill aboard MV Aurora'});
      await notice.evaluate(element => element.scrollIntoView({block:'center', behavior:'instant'}));
      await notice.getByText('Safety Officer', {exact:true}).waitFor();
      await notice.getByText('MV Aurora', {exact:true}).waitFor();
      await notice.locator('.wl-news-photo').evaluate(element => element.scrollIntoView({block:'center', behavior:'instant'}));
      const photo = notice.getByRole('img');
      await photo.evaluate(image => image.scrollIntoView({block:'center', behavior:'instant'}));
      await page.waitForFunction(() => [...document.querySelectorAll('#wl-news article img')].some(image => image.complete && image.naturalWidth >= 600));
      assert(await photo.evaluate(image => image.naturalWidth >= 600), 'Drill photograph must display inline');
      assert.equal(await panel.locator('#wl-news-compose').isVisible(), false);
      if (route === 'home') {
        assert.equal(await panel.locator('article').count(), 1, 'Home shows one recent post');
      } else {
        await panel.getByText('Welcome aboard the Maré Alta demo', {exact:true}).waitFor();
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
        if (process.env.WAVELINK_NEWS_SCREENSHOT_DIR) {
          await panel.scrollIntoViewIfNeeded();
          await panel.locator('.wl-news-list').evaluate(element => { element.scrollTop = 0; });
          await panel.screenshot({path:path.join(process.env.WAVELINK_NEWS_SCREENSHOT_DIR, 'Wavelink-team-news-'+language+'.png')});
        }
      }
    }
    assert.deepEqual(errors, []);
    console.log(language, width, 'home preview, team list, Safety Officer byline, audience, inline image and read-only controls passed');
  } finally {
    await context.close();
  }
}

(async () => {
  const entry = new URL(process.argv[2]);
  assert.equal(entry.hostname, '127.0.0.1', 'Use a disposable demo workspace');
  const browser = await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
  try {
    await verify(browser, entry.href, 'en', 1360);
    await verify(browser, entry.href, 'pt', 390);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
