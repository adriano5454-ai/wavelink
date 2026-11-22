// Run against home_news_fixture.py on loopback. Both projects and all posts are fictional.
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require('playwright-core');

const origin = new URL(process.argv[2]).origin;
assert.equal(new URL(origin).hostname, '127.0.0.1');
const screenshots = process.env.WAVELINK_NEWS_SCREENSHOT_DIR;
const drill = 'Fire alarm drill aboard MV Aurora';
const welcome = 'Welcome aboard the Maré Alta demo';
const home = '#personal-home > #wl-news';

async function screenshot(page, name) {
  if (!screenshots) return;
  await fs.mkdir(screenshots, {recursive:true});
  await page.screenshot({path:path.join(screenshots, name + '.png'), animations:'disabled'});
}

async function publicHome(browser, language, width) {
  const pt = language === 'pt';
  const context = await browser.newContext({
    viewport:{width, height:width > 800 ? 920 : 844}, locale:pt ? 'pt-BR' : 'en-GB',
    ignoreHTTPSErrors:true, serviceWorkers:'block', reducedMotion:'reduce'
  });
  const errors = [];
  try {
    const page = await context.newPage();
    page.on('pageerror', e => errors.push(e.message));
    page.setDefaultTimeout(15000);
    await page.goto(origin + '/__demo/public?area=home');
    await page.locator('#personal-home:visible').waitFor({timeout:45000});
    if (pt) {
      await page.goto(page.url().split('#')[0] + '#profile');
      await page.locator('#wl-language-select').selectOption('pt-BR');
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
      await page.goto(page.url().split('#')[0] + '#home');
    }
    const news = page.locator(home);
    await news.getByRole('heading', {name:pt ? 'Notícias da equipe' : 'Team news'}).waitFor();
    const article = news.locator('article');
    const open = article.getByRole('button', {name:drill});
    await open.waitFor();
    assert.equal(await article.count(), 1);
    assert.equal(await page.locator('#recognition-home #wl-news, aside .wl-news-post').count(), 0);
    const layout = await news.evaluate(panel => {
      const box = panel.getBoundingClientRect();
      const overview = document.querySelector('.ph-overview').getBoundingClientRect();
      const hero = document.querySelector('.ph-hero').getBoundingClientRect();
      return {width:box.width, overview:overview.width, belowHero:box.top>=hero.bottom-1,
              beforeOverview:box.bottom<=overview.top+1, top:box.top + scrollY, overflow:document.documentElement.scrollWidth-innerWidth};
    });
    assert(layout.belowHero && layout.beforeOverview && layout.width >= 0.9 * layout.overview,
      JSON.stringify(layout));
    assert(layout.overflow <= 1);
    await article.getByText('Safety Officer', {exact:true}).waitFor();
    await article.getByText('MV Aurora', {exact:true}).waitFor();
    const photo = article.locator('.wl-news-photo img');
    await photo.evaluate(img => img.decode());
    assert(await photo.evaluate(img => img.naturalWidth >= 600));
    assert.equal(await news.locator('#wl-news-compose').isVisible(), false);
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate(() => scrollTo(0,0));
    await screenshot(page, `Wavelink-Home-news-${language}-${width}`);
    if (width < 800) {
      await news.evaluate(el => scrollTo({top:scrollY+el.getBoundingClientRect().top-76, behavior:'instant'}));
      await screenshot(page, `Wavelink-Home-card-${language}-${width}`);
    }

    async function verifyDetail() {
      const modal = page.getByRole('dialog', {name:drill});
      await modal.waitFor();
      assert.equal(new URL(page.url()).hash, '#home');
      await modal.getByText('Safety Officer', {exact:true}).waitFor();
      await modal.getByText('MV Aurora', {exact:true}).waitFor();
      await modal.getByText(/Fictional demo notice/).waitFor();
      await modal.getByRole('img').evaluate(img => img.decode());
      assert(await modal.evaluate(el => el.matches(':modal') && document.documentElement.scrollWidth<=innerWidth + 1));
      return modal;
    }
    // Real coordinate clicks exercise hit testing even when the opener's pseudo-element covers the photo.
    await photo.scrollIntoViewIfNeeded();
    const bounds = await photo.boundingBox();
    await page.mouse.click(bounds.x + bounds.width / 2, bounds.y + bounds.height / 2);
    let modal = await verifyDetail();
    if (width > 800) await screenshot(page, `Wavelink-Home-post-${language}-${width}`);
    await page.keyboard.press('Escape');
    await modal.waitFor({state:'detached'});
    assert(await open.evaluate(button => button === document.activeElement));
    await article.evaluate(el => el.scrollIntoView({block:'center', behavior:'instant'}));
    const box = await article.boundingBox();
    assert(await article.evaluate((el, point) => el.contains(document.elementFromPoint(point.x, point.y)),
      {x:box.x+9,y:box.y+9}), 'The tested background point is visible in the viewport');
    await page.mouse.click(box.x + 9, box.y + 9);
    modal = await verifyDetail();
    await modal.getByRole('button', {name:pt?'Fechar':'Close'}).click();
    await modal.waitFor({state:'detached'});
    await open.press('Enter');
    modal = await verifyDetail();
    await page.keyboard.press('Escape');
    await modal.waitFor({state:'detached'});
    assert(await open.evaluate(button => button === document.activeElement));

    const newer = news.locator('#wl-home-news-newer'), older = news.locator('#wl-home-news-older');
    assert(await newer.isDisabled());
    await older.click();
    const second = article.getByRole('button', {name:welcome});
    await second.waitFor();
    assert(await older.isDisabled());
    assert.equal(await article.count(), 1);
    await second.press('Space');
    const olderModal = page.getByRole('dialog', {name:welcome});
    await olderModal.waitFor();
    await olderModal.getByText(/where the vessel and shore teams share news/).waitFor();
    await page.keyboard.press('Escape');
    await olderModal.waitFor({state:'detached'});
    assert(await second.evaluate(button => button === document.activeElement));
    await newer.click();
    await open.waitFor();
    await news.getByRole('link', {name:pt ? 'Ver todas as notícias' : 'View all news'}).click();
    await page.locator('#wl-rec-content #wl-news').getByRole('heading', {name:welcome}).waitFor();
    assert.equal(new URL(page.url()).hash, '#team');
    assert.deepEqual(errors, []);
    console.log(language, width, 'main-column ordering, photo/background/keyboard, dialog focus, Home paging and Team navigation passed');
  } finally {
    await context.close();
  }
}

async function privateReader(browser) {
  const context = await browser.newContext({viewport:{width:1360, height:900}, ignoreHTTPSErrors:true,
                                            serviceWorkers:'block', reducedMotion:'reduce'});
  let release;
  const waiting = new Promise(resolve => { release = resolve; });
  try {
    const page = await context.newPage();
    const delayed = new Set();
    await page.route(/\/api\/recognition\/(?:profile(?:\?|$)|feed\?)/, async route => {
      delayed.add(new URL(route.request().url()).pathname);
      await waiting;
      await route.fulfill({status:503, json:{error:'Fictional unavailable sidebar'}});
    });
    await page.goto(origin);
    await page.locator('[name=login_id]').fill('homeqa.reader');
    await page.locator('[name=password]').fill('Fictional-home-news-password');
    await page.locator('#login-form [type=submit]').click();
    const news = page.locator(home);
    const first = 'Bridge watch on Survey North';
    const open = news.getByRole('button', {name:first});
    await open.waitFor({timeout:18000});
    const homeURL = page.url();
    assert.deepEqual([...delayed].sort(), ['/api/recognition/feed','/api/recognition/profile']);
    await open.click();
    const detail = page.getByRole('dialog', {name:first});
    await detail.getByText(/Full report ends here\./).waitFor();
    assert((await detail.locator('.wl-home-news-detail-body').innerText()).length > 1500);
    release();
    await page.locator('#recognition-home .notice.warn').waitFor();
    assert(await detail.isVisible(), 'Finishing the sidebar request must preserve the open story');
    await page.keyboard.press('Escape');
    await detail.waitFor({state:'detached'});
    const visible = [];
    for (let n=15; n>=1; n--) {
      await news.locator('#wl-home-news-older').click();
      const title = 'Company briefing ' + n;
      await news.getByRole('button', {name:title, exact:true}).waitFor();
      assert.equal(await news.locator('article').count(), 1);
      assert.equal(await news.getByText('South Base private bulletin', {exact:true}).count(), 0);
      assert(await news.evaluate(el => el.getBoundingClientRect().height <= innerHeight));
      visible.push(title);
    }
    assert.equal(visible.length, 15);
    assert(await news.locator('#wl-home-news-older').isDisabled());
    assert.equal(page.url(), homeURL);
    await news.getByRole('link', {name:'View all news'}).click();
    const feed = page.locator('#wl-rec-content #wl-news');
    await feed.getByRole('heading', {name:first}).waitFor();
    assert.equal(await feed.getByText('South Base private bulletin', {exact:true}).count(), 0);
    console.log('16 eligible stories paged one at a time; latest restricted post excluded; delayed/failed sidebar isolated');
  } finally {
    release();
    await context.close();
  }
}

(async () => {
  const browser = await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
  try {
    for (const width of [1360,390]) {
      for (const language of ['en','pt']) await publicHome(browser, language, width);
    }
    await privateReader(browser);
  } finally {
    await browser.close();
  }
})().catch(e => { console.error(e); process.exitCode = 1; });
