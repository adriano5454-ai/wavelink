'use strict';
const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');

async function visit(page,hash){
 const url=new URL(page.url());url.hash=hash;await page.goto(url.href);
}
async function main(){
 const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
 try{
  for(const width of [1360,390]){
   const context=await browser.newContext({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block',isMobile:width<500,hasTouch:width<500});
   const page=await context.newPage();const errors=[];
   page.on('pageerror',err=>errors.push(err.message));
   try{
    await page.goto(process.argv[2]);
    await page.locator('#wl-global-search-trigger:visible').waitFor({timeout:60000});
    await page.locator('#wl-global-search-trigger').click();
    const site=page.locator('#wl-search-site');
    await page.waitForFunction(()=>document.querySelector('#wl-search-site')?.options.length>1);
    const ship=await site.locator('option').evaluateAll(rows=>rows.find(x=>x.textContent.includes('DEMO Meridian')).value);
    await site.selectOption(ship);
    await page.locator('[data-search-key^="faults:"]').first().waitFor();
    assert.ok(await page.locator('[data-search-key^="maintenance:"]').count());
    assert.ok(await page.locator('[data-search-key^="tasks:"]').count());
    await page.locator('#wl-search-kind').selectOption('maintenance');
    await page.waitForFunction(()=>{const r=[...document.querySelectorAll('[data-search-key]')];return r.length&&r.every(x=>x.dataset.searchKey.startsWith('maintenance:'));});
    await page.locator('[data-wl82-close="search"]').click();
    await page.locator('#wl-search-dialog').waitFor({state:'hidden'});
    await visit(page,'maintenance');
    const order=page.locator('article[data-mw-order]').filter({hasText:'Photo evidence training inspection'});
    await order.waitFor();
    await order.locator('p').first().click();
    await page.locator('#mw-selected h2').filter({hasText:'Photo evidence training inspection'}).waitFor();
    await page.locator('#mw-open-order').click();
    await page.locator('#maintenance-workspace.mw-work-order').waitFor();
    await page.locator('[data-mw-tab="steps"]').first().click();
    const step=page.locator('.maintenance-step:visible').first();await step.waitFor();
    assert.match(await step.innerText(),/Photo evidence · Optional/i);
    await step.locator('h2').click();
    await page.locator('dialog[open]').waitFor();
    await page.locator('#fw-form .evidence-editor').waitFor();
    page.once('dialog',d=>d.accept());
    await page.locator('#fw-discard').click();
    await page.locator('#fw-form').waitFor({state:'hidden'});
    await visit(page,'it');
    const ticket=page.locator('tr').filter({has:page.locator('a.it-request-link')}).first();
    await ticket.waitFor();
    await ticket.locator('td').last().click();
    await page.waitForURL(/#it\/requests\//);
    await visit(page,'checklists');
    const check=page.locator('article[data-cw-card]').first();await check.waitFor();
    await check.click({position:{x:6,y:6}});
    await page.locator('#cw-preview-items li').first().waitFor();
    await page.locator('#checklist-inspector > a[data-cw-open]').click();
    await page.waitForURL(/#dive\//);
    await visit(page,'faults');
    await page.locator('#fr-new').click();
    await page.locator('#fr-work_site_id').waitFor();
    assert.ok(await page.locator('#fr-work_site_id option').count()>2);
    assert.ok(await page.locator('#fr-work_site_id').evaluate(el=>el.required));
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
    assert.deepEqual(errors,[]);
    console.log(width+'px location search, fault picker, maintenance card and step passed');
   }catch(error){console.error(page.url(),(await page.locator('body').innerText()).slice(-1300),errors);throw error;}finally{await context.close();}
  }
 }finally{await browser.close();}
}
main().catch(err=>{console.error(err);process.exitCode=1;});
