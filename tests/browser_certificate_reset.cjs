const {chromium}=require('playwright-core'),assert=require('node:assert/strict');const base=new URL(process.argv[2]);assert.equal(base.hostname,'127.0.0.1');const baseline=process.argv.includes('baseline');
async function run(p,width){
 await p.evaluate(()=>location.hash='certificates');const q=p.locator('[name=certsearch]'),rows=p.locator('[data-cert-preview]');
 await p.locator('[data-cert-view=expired]').click();await q.fill('NO-MATCH-709');assert.equal(await rows.count(),0);
 await p.locator('#cert-reset').click();console.log('reset',width,JSON.stringify(await q.inputValue()),await rows.count());
 if(baseline)return;assert.equal(await q.inputValue(),'');assert.equal(await rows.count(),4);assert.equal(await p.locator('[data-cert-view=current]').getAttribute('aria-pressed'),'true');
 await q.fill('003');assert.equal(await rows.count(),1);await q.fill('');assert.equal(await rows.count(),4);
 let release,started;const delayed=new Promise(r=>release=r),blocked=new Promise(r=>started=r);
 await p.route(u=>u.pathname==='/api/certificates',async route=>{const response=await route.fetch();started();await delayed;await route.fulfill({response});},{times:1});
 await q.fill('NO-MATCH-709');await p.locator('#cert-refresh').click();await blocked;
 await p.locator('#cert-reset').click();assert.equal(await rows.count(),4);
 const late=p.waitForResponse(r=>new URL(r.url()).pathname==='/api/certificates');
 release();await late;await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
 assert.equal(await q.inputValue(),'');assert.equal(await rows.count(),4);
 console.log('PASS reset and late refresh',width);
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const width of [1360,389]){const p=await browser.newPage({viewport:{width,height:919},ignoreHTTPSErrors:true,serviceWorkers:'block'});try{await p.goto(base.origin+'/__demo/public?area=hr');await p.locator('#hr-section-select').waitFor({state:'attached'});await run(p,width)}finally{await p.close()}}}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});