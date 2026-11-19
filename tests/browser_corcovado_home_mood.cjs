'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');

// Run against the disposable Corcovado C01 fixture with HRCompany's Alice and Bob.
async function verify(origin, options = {}) {
  const browser = await chromium.launch(options.launch);
  try {
    const width = options.width || 1360;
    const context = await browser.newContext({
      viewport: {width, height: 900}, ignoreHTTPSErrors: Boolean(options.local),
    });
    const errors = [];
    async function signIn(member) {
      const page = await context.newPage();
      page.on('pageerror', err => errors.push(err.message));
      await page.goto(origin + '/');
      await page.locator('[name="login_id"]').fill('hr.test.' + member);
      await page.locator('[name="password"]').fill('Fictional HR acceptance password 117.');
      await page.locator('#login-form [type="submit"]').click();
      await page.locator('#personal-home').waitFor();
      return page;
    }
    async function open(page, area) {
      const url = new URL(page.url());
      url.hash = area;
      await page.goto(url.href);
      const parent = area === 'team' ? '#wl-rec-content' : '#personal-home';
      await page.locator(parent + ' #wl-mood-editor:visible').waitFor();
    }
    async function choose(page, code) {
      await page.locator('#wl-mood-editor label').filter({has: page.locator('input[value="' + code + '"]')}).click();
      await page.locator('#wl-mood-share').click();
      await page.getByText('Sua carinha foi compartilhada.', {exact:true}).waitFor();
    }
    const member = await signIn('alice');
    const home = member.locator('#personal-home');
    await home.locator('#wl-mood-editor:visible').waitFor();
    assert.equal(await home.locator('#wl-mood-heading').innerText(), 'Como você está se sentindo hoje?');
    assert.equal(await home.locator('input[name="wl-team-mood"]').count(), 5);
    assert.equal(await home.locator('#wl-mood-remove').isVisible(), false);
    await choose(member, 'happy');
    await open(member, 'team');
    assert.equal(await member.locator('input[value="happy"]').isChecked(), true);
    await choose(member, 'calm');
    await open(member, 'home');
    assert.equal(await home.locator('input[value="calm"]').isChecked(), true);
    assert.equal(await home.locator('#wl-mood-shared li').filter({hasText:'Fictional employee Alice'}).count(), 1);
    await member.reload();
    await home.locator('#wl-mood-remove:visible').waitFor();
    assert.equal(await home.locator('input[value="calm"]').isChecked(), true);
    const colleagueContext = await browser.newContext({ignoreHTTPSErrors:Boolean(options.local)});
    const colleague = await colleagueContext.newPage();
    await colleague.goto(origin + '/');
    await colleague.locator('[name="login_id"]').fill('hr.test.bob');
    await colleague.locator('[name="password"]').fill('Fictional HR acceptance password 117.');
    await colleague.locator('#login-form [type="submit"]').click();
    await colleague.locator('#wl-mood-shared li').filter({hasText:'Fictional employee Alice'}).waitFor();
    assert.equal(await colleague.locator('input:checked[name="wl-team-mood"]').count(), 0);
    await member.locator('#wl-mood-remove').click();
    await member.getByText('Sua carinha foi retirada.', {exact:true}).waitFor();
    await open(member, 'team');
    assert.equal(await member.locator('#wl-mood-remove').isVisible(), false);
    await open(colleague, 'team');
    assert.equal(await colleague.locator('#wl-mood-shared li').filter({hasText:'Fictional employee Alice'}).count(), 0);
    assert.equal(await member.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1), false);
    assert.deepEqual(errors, []);
    console.log(width + 'px: five Portuguese faces, optional sharing, Home/Team update, reload, colleague visibility and removal');
  } finally {
    await browser.close();
  }
}
module.exports = {verify};
if (require.main === module) {
  (async () => {
    const launch = {executablePath:process.env.WAVELINK_TEST_CHROMIUM};
    for (const width of [1360, 390]) await verify(process.argv[2], {launch, width});
  })().catch(err => {console.error(err); process.exitCode = 1;});
}
