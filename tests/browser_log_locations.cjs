'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');

async function visit(page,hash) {
 const url=new URL(page.url());
 url.hash=hash;
 await page.goto(url.href);
}

async function checkStage(page,language) {
 await visit(page,'checklists');
 await page.locator('article.cw-record .cw-type').first().click();
 const picker=page.getByRole('combobox',{name:language==='en'?'Stage':'Etapa',exact:true});
 await picker.waitFor();
 for(const width of [1360,1280,1024,850,390,320]) {
  await page.setViewportSize({width,height:844});
  const reading=await picker.evaluate(select=>{
   const label=select.labels[0];
   const caption=[...label.childNodes].find(node=>node.nodeType===Node.TEXT_NODE && node.textContent.trim());
   const range=document.createRange();
   range.setStart(caption,caption.textContent.search(/\S/));
   range.setEnd(caption,caption.textContent.trimEnd().length);
   const text=Array.from(range.getClientRects()).filter(rect=>rect.height>0);
   const menu=select.getBoundingClientRect(), panel=select.closest('aside').getBoundingClientRect();
   return {lines:text.length,beside:text.length===1&&text[0].right<=menu.left+1,
    fits:menu.right<=panel.right+1&&document.documentElement.scrollWidth<=innerWidth+1};
  });
  assert.deepEqual(reading,{lines:1,beside:true,fits:true},`${language} stage selector at ${width}px`);
 }
 await picker.selectOption('post');
 assert.equal(await picker.inputValue(),'post');
 await page.setViewportSize({width:1280,height:844});
}

async function checkLogbooks(page,language) {
 const bySite=page.locator('#logs-location-filter');
 await visit(page,'logs');
 await bySite.waitFor();
 const books=page.locator('#logs-by-site .log-book-card');
 assert.ok(await books.count()>=2);
 const choices=await bySite.locator('option').evaluateAll(options=>options.map(o=>({value:o.value,text:o.textContent})));
 const vessel=choices.find(option=>option.text.includes('DEMO Meridian'));
 const other=choices.find(option=>option.text.includes('DEMO Horizon'));
 const base=choices.find(option=>option.text.includes('DEMO Shore'));
 assert.ok(vessel&&other&&base);
 await bySite.selectOption(vessel.value);
 assert.match(await books.allInnerTexts().then(items=>items.join(' ')),/Meridian Operations Log/);
 assert.doesNotMatch(await books.allInnerTexts().then(items=>items.join(' ')),/Horizon Engineering Log/);
 await books.first().locator('a').click();
 await page.locator('.log-workspace .log-site-line strong').filter({hasText:'DEMO Meridian'}).waitFor();
 await visit(page,'logs');
 assert.equal(await bySite.inputValue(),vessel.value);
 await bySite.selectOption(other.value);
 assert.match(await books.allInnerTexts().then(items=>items.join(' ')),/Horizon Engineering Log/);
 await bySite.selectOption(base.value);
 await page.locator('.log-site-empty').waitFor();
 assert.equal(await books.count(),0);
 await bySite.selectOption('__unassigned__');
 assert.equal(await books.count(),0);
 await bySite.selectOption('');
 assert.ok(await books.count()>=2);
 await page.locator('a[href="#admin/logbooks/new"]').click();
 const next=page.locator('#ld-next');
 await next.click();
 const createSite=page.locator('select[name="work_site_id"]');
 await createSite.locator('option').filter({hasText:'DEMO Meridian'}).waitFor({state:'attached'});
 await createSite.selectOption(vessel.value);
 assert.equal(await createSite.inputValue(),vessel.value);
 console.log(`${language} verified the logbook register, retained filter, book location and builder picker`);
}

async function main() {
 const [url,lang='en']=process.argv.slice(2);
 const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
 try {
  const context=await browser.newContext({viewport:{width:1280,height:844},ignoreHTTPSErrors:true,serviceWorkers:'block'});
  const page=await context.newPage();
  page.setDefaultTimeout(8000);
  await page.goto(url);
  await page.locator('#wl-global-search-trigger:visible').waitFor({timeout:45000});
  if(lang==='pt'){
   await visit(page,'profile');
   await page.locator('#wl-language-select').selectOption('pt-BR');
   await page.locator('#profile-language button').click();
   await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
  }
  await checkStage(page,lang);
  console.log(`${lang} checklist stage label stayed on one line at six viewport widths`);
  await checkLogbooks(page,lang);
 } finally {await browser.close();}
}
main().catch(error=>{console.error(error);process.exitCode=1;});
