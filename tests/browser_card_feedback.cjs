'use strict';
const assert = require('node:assert/strict');
const { chromium } = require('playwright-core');

const registers = [
 ['tasks', '.tw110-row:not([aria-current="true"])'],
 ['handovers', '.hwd-day[open] .hwd-record'],
 ['checklists', '.cw-record:not(.selected)'],
 ['maintenance', '.mw-order:not(.is-selected)'],
 ['logs', '.log-book-card'],
 ['toolbox', '.fw-card'],
 ['faults', '.fr-row'],
 ['original-files', '.wf-row.of-file'],
 ['workspaces', '.home-destination'],
 ['home', '.ph-row[data-home-record]'],
 ['fleet', '.fleet77-site-grid > article.fleet77-card'],
 ['inventory', '.iw162-inventory-row'],
 ['qshe', '.qs-row'],
 ['calendar', '.calendar-agenda-row:has(a[data-calendar-source])'],
 ['certificates', '.certificate-card'],
 ['builders', '.sb-card:has(button.sb-library:enabled)'],
 ['admin', '.admin-hub-card'],
 ['it', '.it-table tbody tr:has(a.it-request-link)']
];

async function settle(card) {
 await card.evaluate(async el => {
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  await Promise.allSettled(el.getAnimations().filter(a => a instanceof CSSTransition).map(a => a.finished));
 });
}
async function paint(card) {
 await settle(card);
 return card.evaluate(el => {
  const s=getComputedStyle(el);
  return {background:s.backgroundColor, border:s.borderColor, shadow:s.boxShadow, outline:s.outline};
 });
}
async function navigate(page, hash) {
 const url=new URL(page.url());url.hash=hash;await page.goto(url.href);
}

async function main() {
 const url=process.argv[2], reportOnly=process.argv.includes('--inspect');
 assert.ok(url, 'Provide the public demonstration entry URL');
 const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
 const failures=[];
 try {
  const context=await browser.newContext({viewport:{width:1280,height:850},ignoreHTTPSErrors:true,serviceWorkers:'block',reducedMotion:'reduce'});
  const page=await context.newPage();
  page.setDefaultTimeout(7500);
  await page.goto(url);
  await page.locator('#wl-global-search-trigger:visible').waitFor({timeout:45000});
  let taskHover;
  for (const [hash, selector] of registers) {
   try {
    await page.setViewportSize({width:1280,height:850});
    await navigate(page,hash);
    const host=hash==='fleet'?page.frameLocator('#fleet-workspace-frame'):page;
    const card=host.locator(selector+':visible').first();
    await card.waitFor();await card.scrollIntoViewIfNeeded();await page.mouse.move(0,0);
    const rest=await paint(card);
    await card.hover({position:{x:8,y:8}});
    const hover=await paint(card);
    if(hash==='tasks')taskHover=hover.background;
    const hit=await card.evaluate(el=>el.matches(':hover'));
    await page.mouse.move(0,0);await page.keyboard.press('Tab');
    const target=await card.evaluate(el=>el.matches('button,a[href],[tabindex="0"],[role="button"]')?'self':'child');
    const control=target==='self'?card:card.locator('button:visible:enabled,a[href]:visible,[tabindex="0"]:visible').first();
    await control.focus();
    const focused=await paint(card);
    const nativeFocus=await control.evaluate(el=>el.matches(':focus-visible')&&getComputedStyle(el).outlineStyle!=='none');
    const geometry=[];
    for(const width of [1280,390,320]){
     await page.setViewportSize({width,height:850});
     geometry.push(await card.evaluate(el=>{
      const css=getComputedStyle(el), rect=el.getBoundingClientRect();
      return {width:innerWidth,pageWidth:document.documentElement.scrollWidth,right:Math.round(rect.right),
        cardWidth:Math.round(rect.width),height:Math.round(rect.height),extraY:el.scrollHeight-el.clientHeight,
        extraX:el.scrollWidth-el.clientWidth,overflowY:css.overflowY};
     }));
    }
    console.log(JSON.stringify({hash,rest,hover,focused,nativeFocus,geometry}));
    assert.ok(hit, 'Pointer reaches card');
    assert.notEqual(hover.background,rest.background,'Whole card responds to hover');
    assert.equal(hover.background,taskHover,'Uses Tasks hover color');
    assert.equal(focused.background,taskHover,'Keyboard focus highlights the whole card');
    assert.ok(nativeFocus||JSON.stringify(focused)!==JSON.stringify(rest),'Keyboard focus is visible');
    for(const g of geometry){
     assert.ok(g.pageWidth<=g.width+1&&g.right<=g.width+1,'Page and card fit at '+g.width+'px');
     assert.ok(g.extraX<=1,'Card fits horizontally at '+g.width+'px');
     assert.ok(g.extraY<=2||g.overflowY==='visible','Card content fits without its own scrollbar at '+g.width+'px');
    }
   }catch(error){
    failures.push(hash+': '+error.message.split('\n')[0]);console.error(failures.at(-1));
   }
  }
  await page.setViewportSize({width:1280,height:850});
  await navigate(page,'handovers');
  const register=page.locator('.hwd-day[open] .hwd-record').first();
  await register.locator('.hwd-note').click();
  const panel=page.locator('#ho-record-preview');
  await panel.locator('.hop-body h2').waitFor();
  await page.mouse.move(0,0);
  const selected=await paint(register);
  assert.ok(await register.evaluate(el=>el.classList.contains('hop-selected')));
  assert.notEqual(selected.background,taskHover,'Selection remains distinct after the pointer leaves');
  assert.notEqual(selected.shadow,'none','Selected handover has a persistent edge');
  await panel.locator('.hop-head button').click();
  await navigate(page,'team');
  const feed=page.locator('.wl-feed-card:visible').first();
  await feed.waitFor();await feed.scrollIntoViewIfNeeded();await page.mouse.move(0,0);
  const staticColor=(await paint(feed)).background;
  await feed.hover({position:{x:8,y:8}});
  assert.equal((await paint(feed)).background,staticColor,'A feed card does not advertise a whole-card action');
  console.log('Verified selection, return to the register and a passive feed card.');
  await context.close();
 }finally{await browser.close();}
 if(!reportOnly)assert.deepEqual(failures,[]);
}
main().catch(e=>{console.error(e);process.exitCode=1;});
