'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');

async function profile(page, lang) {
    const url = new URL(page.url());
    url.hash = 'profile';
    await page.goto(url.href);
    await page.locator('html[lang="' + lang + '"] #wl-language-select').waitFor();
    assert.equal(await page.locator('#wl-language-select').inputValue(), lang);
}
async function choose(page, lang) {
    const selector = page.locator('#wl-language-select');
    await selector.selectOption(lang);
    await page.locator('#profile-language button').click();
    await page.locator('html[lang="' + lang + '"] #wl-language-select').waitFor();
    assert.equal(await selector.inputValue(), lang);
    assert.equal(new URL(page.url()).hash, '#profile');
}
async function checkCompany(browser, origin) {
    async function member(id, expected) {
        const ctx = await browser.newContext({locale:'en-US',viewport:{width:1360,height:850}});
        const page = await ctx.newPage();
        await page.goto(origin);
        await page.locator('html[lang="pt-BR"] #login-form').waitFor();
        await page.locator('[name=login_id]').fill('hr.test.' + id);
        await page.locator('[name=password]').fill('Fictional HR acceptance password 117.');
        await page.locator('#login-form [type=submit]').click();
        await page.locator('html[lang="' + expected + '"] #personal-home').waitFor();
        await profile(page, expected);
        return page;
    }
    const alice = await member('alice', 'pt-BR');
    const bob = await member('bob', 'pt-BR');
    await choose(alice, 'en');
    await alice.getByText('Preferred language', {exact:true}).waitFor();
    await alice.reload();
    await profile(alice, 'en');
    const freshAlice = await member('alice', 'en');
    const home = new URL(freshAlice.url());
    home.hash = 'home';
    await freshAlice.goto(home.href);
    await freshAlice.getByRole('heading',{name:'How are you feeling today?'}).waitFor();
    const help = freshAlice.locator('a[href*="/help/topics/dashboard"]').first();
    const popup = freshAlice.waitForEvent('popup');
    await help.click();
    const guide = await popup;
    await guide.locator('html[lang="en"]').waitFor();
    await guide.close();
    await bob.reload();
    await profile(bob, 'pt-BR');
    await choose(alice, 'pt-BR');
    await member('alice', 'pt-BR');
    console.log('Company: Portuguese at entry, two independent profiles, English across sign-ins and devices, translated Home and Help, switch back.');
}
async function checkDemo(browser, origin) {
    const options = {locale:'pt-BR',ignoreHTTPSErrors:true,viewport:{width:390,height:844}};
    const context = await browser.newContext(options);
    async function enter(ctx, path='/__demo/public?lang=pt&area=profile') {
        const page = await ctx.newPage();
        await page.goto(origin+path);
        await page.locator('html[lang=en] #wl-language-select').waitFor();
        return page;
    }
    const first = await enter(context);
    const visit = new URL(first.url()).searchParams.get('browser_workspace');
    assert.ok(visit);
    await choose(first, 'pt-BR');
    assert.equal(new URL(first.url()).searchParams.get('browser_workspace'), visit);
    await first.reload();
    await profile(first, 'pt-BR');
    const url = new URL(first.url());
    url.hash = 'home';
    await first.goto(url.href);
    await first.getByRole('heading',{name:'Como você está se sentindo hoje?'}).waitFor();
    const sameBrowser = await enter(context);
    assert.notEqual(new URL(sameBrowser.url()).searchParams.get('browser_workspace'),visit);
    const secondBrowser = await browser.newContext(options);
    const other = await enter(secondBrowser);
    await profile(other, 'en');
    await profile(first, 'pt-BR');
    assert.equal(await first.locator('html').evaluate(el => el.scrollWidth <= innerWidth+1),true);
    await choose(first, 'en');
    assert.equal(new URL(first.url()).searchParams.get('browser_workspace'), visit);
    console.log('Demo: English on fresh entry with Portuguese browser settings, own visit survives routes/reload, two concurrent visits in one browser and a separate browser stay independent.');
}
(async () => {
    const origin = process.argv[2], mode = process.argv[3] || 'company';
    const args = process.env.WAVELINK_TEST_CHROMIUM_MAP ? ['--host-resolver-rules='+process.env.WAVELINK_TEST_CHROMIUM_MAP] : [];
    const browser = await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM,args});
    try { await (mode==='demo' ? checkDemo : checkCompany)(browser,origin); }
    finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode=1; });
