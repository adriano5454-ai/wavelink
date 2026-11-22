// Use a loopback company from home_news_fixture.py. Every post and draft is fictional.
const assert = require('node:assert/strict');
const path = require('node:path');
const { chromium } = require('playwright-core');

const origin = new URL(process.argv[2]).origin;
assert.equal(new URL(origin).hostname, '127.0.0.1');
const picture = path.join(__dirname, '../deploy/feed_news_drill.webp');

async function sidebar(page, hash) {
  if (await page.locator('#shell-sidebar').isHidden()) await page.locator('#shell-toggle').click();
  await page.locator('#shell-sidebar a[href="#' + hash + '"]').first().click();
}

async function arrived(page, hash, selector) {
  await page.waitForFunction(target => (location.hash || '#home') === '#' + target, hash);
  await page.locator(selector).first().waitFor({state:'visible'});
}

async function confirmation(page, trigger, discard) {
  const [message] = await Promise.all([
    page.waitForEvent('dialog', {timeout:6000}).then(async dialog => {
      assert.equal(dialog.type(), 'confirm');
      const text = dialog.message();
      if (discard) await dialog.accept(); else await dialog.dismiss();
      return text;
    }),
    trigger()
  ]);
  return message;
}

async function writer(browser, language, width) {
  const ctx = await browser.newContext({ignoreHTTPSErrors:true, serviceWorkers:'block',
    viewport:{width,height:850},locale:language==='pt'?'pt-BR':'en-GB',reducedMotion:'reduce'});
  try {
    const page = await ctx.newPage();
    page.setDefaultTimeout(12000);
    const errors = [];
    page.on('pageerror', e=>errors.push(e.message));
    const published = [];
    page.on('request', req=>{
      if(req.method()==='POST' && new URL(req.url()).pathname==='/api/recognition/news') published.push(req.postDataJSON().title);
    });
    await page.goto(origin);
    await page.locator('[name=login_id]').fill('homeqa.editor');
    await page.locator('[name=password]').fill('Fictional-home-news-password');
    await page.locator('#login-form [type=submit]').click();
    await page.locator('#personal-home').waitFor();
    const requestedLanguage = language==='pt'?'pt-BR':'en';
    if(await page.locator('html').getAttribute('lang')!==requestedLanguage){
      await sidebar(page,'profile');
      await page.locator('#wl-language-select').selectOption(requestedLanguage);
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="'+requestedLanguage+'"] #wl-language-select').waitFor();
      await sidebar(page,'home');
      await arrived(page,'home','#personal-home');
    }
    const compose = page.locator('#wl-news-compose');
    const form = page.locator('.wl-news-form');
    async function editor() {
      await sidebar(page,'team');
      await arrived(page,'team','#wl-rec-content #wl-news-compose');
      await compose.click();
      await form.waitFor();
    }
    await editor();
    await sidebar(page,'home');
    await arrived(page,'home','#personal-home');
    assert.equal(await form.count(),0);

    await editor();
    const title = 'Unpublished crew note';
    await form.locator('[name=title]').fill(title);
    await form.locator('[name=body]').fill('This fictional draft must stay with this account.');
    await form.locator('[name=site]').selectOption('all');
    await form.locator('[name=photo]').setInputFiles(picture);
    await form.locator('[data-news-preview] img').evaluate(img=>img.decode());
    const prompt = await confirmation(page, ()=>sidebar(page,'home'), false);
    assert.match(prompt,language==='pt'?/descart|sair/i:/discard|leave/i);
    await arrived(page,'team','.wl-news-form');
    assert.equal(await form.locator('[name=title]').inputValue(),title);
    assert.equal(await form.locator('[name=photo]').evaluate(input=>input.files.length),1);
    assert(await form.locator('[data-news-preview] img').evaluate(img=>img.complete && img.naturalWidth>0));
    assert(await form.evaluate(el=>!el.closest('[inert]')));
    await form.locator('[name=body]').press('End');
    await form.locator('[name=body]').press('!');
    assert((await form.locator('[name=body]').inputValue()).endsWith('!'));
    await confirmation(page, ()=>sidebar(page,'it'), true);
    await arrived(page,'it','#it-new');
    assert.equal(await form.count(),0);
    await sidebar(page,'workspaces');
    await arrived(page,'workspaces','#app h1');
    await sidebar(page,'home');
    await arrived(page,'home','#personal-home');
    assert.deepEqual(published,[]);

    await editor();
    await form.locator('[name=title]').fill('Fictional history draft');
    await confirmation(page, ()=>page.evaluate(()=>history.back()), false);
    await arrived(page,'team','.wl-news-form');
    assert.equal(await form.locator('[name=title]').inputValue(),'Fictional history draft');
    await confirmation(page, ()=>page.evaluate(()=>{location.hash='#profile';}), true);
    await arrived(page,'profile','#wl-edit-profile');
    await editor();
    await form.locator('[name=title]').fill('Fictional leave with Back');
    await confirmation(page, ()=>page.evaluate(()=>history.back()), true);
    await arrived(page,'profile','#wl-edit-profile');
    await editor();
    await sidebar(page,'home');
    await arrived(page,'home','#personal-home');
    await page.evaluate(()=>history.back());
    await arrived(page,'team','#wl-news-compose');
    await compose.click();
    await form.locator('[name=title]').fill('Fictional forward draft');
    const teamEntry = await page.evaluate(()=>navigation.currentEntry.key);
    const driver = await ctx.newCDPSession(page);
    const historyList = await driver.send('Page.getNavigationHistory');
    const nextEntry = historyList.entries[historyList.currentIndex + 1];
    assert.equal(new URL(nextEntry.url).hash, '#home');
    const forward = () => driver.send('Page.navigateToHistoryEntry', {entryId:nextEntry.id});
    await confirmation(page, forward, false);
    await page.waitForFunction(key=>navigation.currentEntry.key===key && navigation.canGoForward,teamEntry);
    await arrived(page,'team','.wl-news-form');
    assert.equal(await form.locator('[name=title]').inputValue(),'Fictional forward draft');
    await confirmation(page, forward, true);
    await arrived(page,'home','#personal-home');
    await editor();
    await form.locator('[name=title]').fill('Explicitly cancelled');
    await form.locator('[data-news-cancel]').click();
    await form.waitFor({state:'detached'});
    assert(await compose.evaluate(el=>el===document.activeElement));
    await sidebar(page,'it');
    await arrived(page,'it','#it-new');
    assert.deepEqual(published,[]);

    await editor();
    const saved = 'Crew bulletin ' + language + ' ' + Date.now();
    await form.locator('[name=title]').fill(saved);
    await form.locator('[name=body]').fill('Fictional successful post.');
    await form.locator('[name=site]').selectOption('all');
    let send;
    const held = new Promise(resolve=>{send=resolve;});
    await page.route('**/api/recognition/news',async route=>{
      if(route.request().method()==='POST') await held;
      await route.continue();
    });
    try {
      const posted = page.waitForRequest(req=>req.method()==='POST' && new URL(req.url()).pathname==='/api/recognition/news');
      await form.locator('[type=submit]').click();
      await posted;
      await sidebar(page,'home');
      await arrived(page,'team','.wl-news-form fieldset:disabled');
      assert.equal(await form.locator('[name=title]').inputValue(),saved);
    } finally {send();}
    await page.getByRole('heading',{name:saved,exact:true}).waitFor();
    assert.deepEqual(published,[saved]);
    await sidebar(page,'home');
    await arrived(page,'home','#personal-home');
    await page.locator('#personal-home').getByRole('button',{name:saved,exact:true}).waitFor();
    await sidebar(page,'it');
    await arrived(page,'it','#it-new');
    await sidebar(page,'team');
    await arrived(page,'team','#wl-news-compose');
    if(language==='en') await verifyOtherEditors(page);
    assert.deepEqual(errors,[]);
    console.log(language,width,'clean exit, stay + photo, discard, browser history, cancel, publishing guard and repeated navigation passed');
  } finally {await ctx.close();}
}

async function verifyOtherEditors(page) {
  await sidebar(page,'profile');
  await page.locator('#wl-edit-profile').click();
  await sidebar(page,'home');
  await arrived(page,'home','#personal-home');
  await sidebar(page,'profile');
  await page.locator('#wl-edit-profile').click();
  const bio = page.locator('.wl-profile-form [name=biography]');
  await bio.fill('Fictional profile text');
  await confirmation(page, ()=>sidebar(page,'home'), false);
  assert.equal(await bio.inputValue(),'Fictional profile text');
  await confirmation(page, ()=>sidebar(page,'home'), true);
  await arrived(page,'home','#personal-home');

  for(const [route,prefix] of [['faults','fr'],['qshe','qs']]) {
    await sidebar(page,route);
    await page.locator('#'+prefix+'-new').click();
    const heading = page.locator('#'+prefix+'-title');
    await heading.fill('Fictional reported observation');
    await confirmation(page, ()=>sidebar(page,'home'),false);
    assert.equal(await heading.inputValue(),'Fictional reported observation');
    await confirmation(page, ()=>sidebar(page,'home'),true);
    await arrived(page,'home','#personal-home');
  }
  await sidebar(page,'it');
  await page.locator('#it-new').click();
  const itTitle = page.locator('#it-form [name=title]');
  await itTitle.fill('IT test draft stays in this tab');
  // The IT modal owns a same-URL history entry. Back closes its window and keeps the draft.
  await page.evaluate(()=>history.back());
  await arrived(page,'it','#it-resume');
  await page.locator('#it-resume').click();
  assert.equal(await itTitle.inputValue(),'IT test draft stays in this tab');
  await confirmation(page, ()=>page.evaluate(()=>{location.hash='#home';}),false);
  await arrived(page,'it','#it-form');
  await confirmation(page, ()=>page.evaluate(()=>{location.hash='#home';}),true);
  await arrived(page,'home','#personal-home');
  await sidebar(page,'it');
  await page.locator('#it-resume').click();
  assert.equal(await itTitle.inputValue(),'IT test draft stays in this tab');
  await confirmation(page, ()=>page.locator('#it-form-cancel').click(),true);
  await sidebar(page,'home');
  await arrived(page,'home','#personal-home');
  console.log('Profile, fault, HSE and IT forms can stay or leave; IT resumes the original draft');
}

(async()=>{
  const browser = await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
  try {
    await writer(browser,'en',1360);
    await writer(browser,'pt',390);
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
