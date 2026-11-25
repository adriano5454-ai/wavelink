const assert=require('node:assert/strict'),{chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);assert.equal(origin.hostname,'127.0.0.1');const baseline=process.argv.includes('baseline');
async function receiving(p,w,detail){
 await p.evaluate(()=>location.hash='fleet/receiving');const f=p.frameLocator('iframe').first(),site=f.locator('#receiving-site');
 const meridian=await site.locator('option').filter({hasText:/Meridian/}).getAttribute('value');await site.selectOption(meridian);
 await f.locator('#receiving-search').fill('Acoustic');const group=f.locator('[data-receiving-open]').filter({hasText:/Acoustic/});if(detail)await group.click();
 const link=detail?f.locator('#receiving-detail').getByRole('link',{name:'Open manifest',exact:true}):f.locator('#receiving-results a').filter({hasText:'DEMO-MAN-003'});await link.scrollIntoViewIfNeeded();await link.focus();
 const at=()=>link.evaluate(e=>({inner:scrollY,outer:parent.scrollY,list:document.querySelector('#receiving-results').scrollTop,focus:document.activeElement===e,top:e.getBoundingClientRect().top+frameElement.getBoundingClientRect().top}));
 const before=await at();await link.click();await p.waitForFunction(()=>location.hash.includes('/manifest/'));await f.locator('#receiving-results').waitFor({state:'detached'});await p.goBack();await link.waitFor();await link.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
 const after=await at();console.log('Manifest',w,{before,after});assert.equal(await site.inputValue(),meridian);assert.equal(await f.locator('#receiving-search').inputValue(),'Acoustic');
 if(!baseline){assert(after.focus);assert.equal(after.list,before.list);assert.equal(after.inner,before.inner);assert.equal(after.outer,before.outer);assert(Math.abs(after.top-before.top)<5);}
}
(async()=>{const b=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,389])for(const detail of [false,true]){const p=await b.newPage({viewport:{width:w,height:919},ignoreHTTPSErrors:true,serviceWorkers:'block'});try{await p.goto(origin.origin+'/__demo/public?area=hr');await p.locator('#hr-section-select').waitFor({state:'attached'});await receiving(p,w,detail)}catch(e){console.error(detail,w,e.message);process.exitCode=1}finally{await p.close()}}}finally{await b.close()}})();