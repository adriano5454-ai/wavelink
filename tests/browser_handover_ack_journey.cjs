const assert=require('node:assert/strict');
const {chromium}=require('playwright-core');
const [url,widthText,language]=process.argv.slice(2);
const origin=new URL(url),width=Number(widthText),pt=language==='pt';
assert.equal(origin.hostname,'127.0.0.1');assert(+origin.port>=18570 && +origin.port<=18579);
async function verify(){
 const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
 try{
  const p=await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
  const writes=[];p.on('request',r=>{if(new URL(r.url()).pathname.startsWith('/api/handovers')&&r.method()!=='GET')writes.push(new URL(r.url()).pathname)});
  await p.goto(origin.origin);await p.locator('input[type=text]:visible').fill('demo.admin');
  await p.locator('#login-password').fill('Fictional-Loopback-Only-3250');await p.locator('#login-password').press('Enter');
  await p.locator('#wl-global-search-trigger:visible').waitFor();
  await p.locator(pt?'html[lang="pt-BR"]':'html[lang="en"]').waitFor({state:'attached'});
  await p.evaluate(()=>location.hash='handovers');await p.locator('#ho-tab-incoming').click();
  const ship=p.locator('#ho-vessel-filter select'),status=p.locator('#ho-incoming-status'),kind=p.locator('#ho-incoming-kind'),search=p.locator('#ho-incoming-search');
  await ship.selectOption({label:'MV Aurora · AUR'});await status.selectOption('all');await kind.selectOption('daily_shift');
  const row=p.locator('[data-ho-incoming]').first();const title=await row.locator('..').locator('h3').innerText();
  await search.fill(title);const id=await row.getAttribute('data-ho-incoming'),revision=await row.getAttribute('data-ho-incoming-revision'),target=p.locator('[data-ho-incoming="'+id+'"]');
  const ctx=async()=>[await ship.inputValue(),await status.inputValue(),await kind.inputValue(),await search.inputValue()];
  const before=await ctx();
  const open=async()=>{await target.click();await p.locator('.hop-actions button').first().click();await p.locator('#ho-reader-title').waitFor();await p.locator('#ho-reader-ack-jump').click();};
  await open();await p.locator('#ho-detail [data-ha-open]').first().waitFor();
  await p.locator('#ho-ack').click();await p.locator('#ho-guide-next').click();assert.equal(await p.locator('#ho-save').isDisabled(),true);
  await p.locator('#ho-confirm').check();
  const saved=p.waitForResponse(r=>r.request().method()==='POST'&&new URL(r.url()).pathname.startsWith('/api/handovers'));
  await p.locator('#ho-save').click();const response=await saved;assert(response.ok());assert.equal(String(response.request().postDataJSON().revision??response.request().postDataJSON().payload?.revision),revision);
  await p.locator('#ho-reader-title').waitFor();assert.equal(await p.locator('#ho-ack').count(),0);
  await p.locator('#ho-back').click();await target.waitFor();assert.deepEqual(await ctx(),before);
  await open();assert.equal(await p.locator('#ho-ack').count(),0);assert.match(await p.locator('#ho-acknowledgement + p').innerText(),/\d{4}/);await p.locator('#ho-back').click();await target.waitFor();assert.deepEqual(await ctx(),before);
  assert.equal(writes.length,1);console.log('PASS',width,language,'revision',revision,'already acknowledged; filters preserved');
 }finally{await browser.close()}
}
verify().catch(e=>{console.error(e);process.exitCode=1});
