// Run against the disposable public/private projects from home_news_fixture.py.
const assert = require('node:assert/strict');
const { chromium } = require('playwright-core');

const origin = new URL(process.argv[2]).origin;
assert.equal(new URL(origin).hostname, '127.0.0.1');
const preference = '#profile-team-birthday';
const panel = '#wl-team-birthdays';

async function openRoute(page, route) {
  const target = new URL(page.url());
  target.hash = route;
  await page.goto(target.href);
}

async function viewPublic(browser, width, language) {
  const context = await browser.newContext({viewport:{width,height:900}, locale:language,
    ignoreHTTPSErrors:true, serviceWorkers:'block', reducedMotion:'reduce'});
  try {
    const page = await context.newPage();
    await page.goto(origin + '/__demo/public?area=home');
    await page.locator('#personal-home:visible').waitFor({timeout:45000});
    if (language === 'pt-BR') {
      await openRoute(page, 'profile');
      await page.locator('#wl-language-select').selectOption('pt-BR');
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
    }
    await openRoute(page, 'home');
    const homeBirthdays = page.locator('#wl-home-birthdays:visible');
    await homeBirthdays.getByRole('heading', {name:language === 'pt-BR' ? /anivers/i : /birthday/i}).waitFor();
    await homeBirthdays.getByText('Lia Costa', {exact:true}).waitFor();
    await homeBirthdays.getByText('Rafael Lima', {exact:true}).waitFor();
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    await openRoute(page, 'team');
    const birthdays = page.locator(panel);
    await birthdays.getByRole('heading', {name:language === 'pt-BR' ? /anivers/i : /birthday/i}).waitFor();
    await birthdays.getByText('Lia Costa', {exact:true}).waitFor();
    await birthdays.getByText('Rafael Lima', {exact:true}).waitFor();
    await birthdays.getByText(language === 'pt-BR' ? /\bhoje\b/i : /\btoday\b/i).first().waitFor();
    const news = page.locator('#wl-news:visible');
    await news.getByRole('heading', {name:language === 'pt-BR' ? /notícias/i : /team news/i}).waitFor();
    const birthdayBox = await birthdays.boundingBox();
    const newsBox = await news.boundingBox();
    if (width >= 1000) {
      assert(Math.abs(birthdayBox.y - newsBox.y) < 24, 'News and birthdays should share a row on desktop');
      assert(birthdayBox.x >= newsBox.x + newsBox.width - 1 || newsBox.x >= birthdayBox.x + birthdayBox.width - 1);
    } else {
      assert(birthdayBox.y >= newsBox.y + newsBox.height - 1 || newsBox.y >= birthdayBox.y + birthdayBox.height - 1);
    }
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    await openRoute(page, 'profile');
    await page.locator('#wl-language-select').waitFor();
    assert.equal(await page.locator(`${preference} [data-birthday-save]:visible:enabled`).count(), 0);
    console.log('Public read-only birthdays, layout and copy verified', width, language);
  } finally { await context.close(); }
}

async function login(context, account) {
  const page = await context.newPage();
  await page.goto(origin);
  await page.locator('[name=login_id]').fill('homeqa.' + account);
  await page.locator('[name=password]').fill('Fictional-home-news-password');
  await page.locator('#login-form [type=submit]').click();
  await page.locator('#personal-home:visible').waitFor();
  return page;
}

async function setDateField(field, value) {
  if (await field.evaluate(e => e.tagName === 'SELECT')) {
    await field.selectOption(String(value));
  } else {
    await field.fill(String(value));
  }
}

async function submitBirthday(page, action) {
  const response = page.waitForResponse(r => new URL(r.url()).pathname === '/api/recognition/birthday'
    && r.request().method() === 'POST');
  await page.locator(`${preference} [data-birthday-${action}]`).click();
  assert.equal((await response).status(), 200);
}

async function privatePreference(browser) {
  const options = {viewport:{width:1360,height:900}, ignoreHTTPSErrors:true, serviceWorkers:'block'};
  const owner = await browser.newContext(options);
  const colleague = await browser.newContext(options);
  try {
    const writer = await login(owner, 'reader');
    const reader = await login(colleague, 'editor');
    await openRoute(writer, 'profile');
    const fields = writer.locator(preference);
    const month = fields.locator('[name=birth_month]');
    const day = fields.locator('[name=birth_day]');
    const now = new Date();
    await setDateField(month, now.getUTCMonth()+1);
    await setDateField(day, now.getUTCDate());
    await submitBirthday(writer, 'save');
    await writer.reload();
    await fields.locator('[data-birthday-remove]').waitFor();
    assert.equal(Number(await month.inputValue()), now.getUTCMonth()+1);
    assert.equal(Number(await day.inputValue()), now.getUTCDate());
    await openRoute(reader, 'team');
    await reader.locator(panel).getByText('Fictional reader', {exact:true}).waitFor();
    await submitBirthday(writer, 'remove');
    const refreshed = reader.waitForResponse(r => new URL(r.url()).pathname === '/api/recognition/birthdays');
    await reader.reload();
    assert.equal((await refreshed).status(), 200);
    await reader.locator(panel).getByRole('heading').waitFor();
    assert.equal(await reader.locator(panel).getByText('Fictional reader', {exact:true}).count(), 0);
    console.log('Private birthday registration, reload, independent colleague and opt-out verified');
  } finally { await owner.close(); await colleague.close(); }
}

(async () => {
  const browser = await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
  try {
    for (const width of [1360,390]) {
      for (const language of ['en-GB','pt-BR']) await viewPublic(browser,width,language);
    }
    await privatePreference(browser);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
