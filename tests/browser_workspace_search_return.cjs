const assert=require('node:assert/strict'),{chromium}=require('playwright-core');
const origin=new URL(process.argv[2]);assert.equal(origin.hostname,'127.0.0.1');const baseline=process.argv.includes('baseline');
async function workspaces(p,w){
 await p.getByRole('link',{name:'All workspaces',exact:true}).first().click();
 const q=p.locator('#home-find'),cards=p.locator('[data-home-workspace]:visible');
 await q.fill('Receiving');assert.equal(await cards.count(),2);
 await cards.filter({hasText:/Receiving & placement/}).getByRole('link').click();
 await p.frameLocator('iframe').first().locator('#receiving-count').waitFor();
 await p.getByRole('link',{name:'All workspaces',exact:true}).first().click();
 await q.fill('Handovers');const after=await cards.allTextContents();
 await p.locator('#home-clear-find').click({timeout:1500}).catch(()=>{});
 const cleared=await q.inputValue();await p.locator('[data-home-group]').nth(1).click();
 const category=await p.locator('[data-home-group]').nth(1).getAttribute('aria-pressed');
 console.log('Workspaces',w,after.length,after[0]?.trim().slice(0,35),{cleared,category});
 if(!baseline){assert.equal(after.length,1);assert.match(after[0],/Handovers/);assert.equal(cleared,'');assert.equal(category,'true');}
}
(async()=>{const b=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,389])for(const test of [workspaces]){const p=await b.newPage({viewport:{width:w,height:919},ignoreHTTPSErrors:true,serviceWorkers:'block'});try{await p.goto(origin.origin+'/__demo/public?area=hr');await p.locator('#hr-section-select').waitFor({state:'attached'});await test(p,w)}catch(e){console.error(test.name,w,e.message);process.exitCode=1}finally{await p.close()}}}finally{await b.close()}})();