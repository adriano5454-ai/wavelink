const {chromium}=require('playwright-core');
const assert=require('node:assert/strict');
const path=require('node:path');
const fs=require('node:fs');
const runtime=path.resolve(process.argv[2]);
const {auth,manifest,received,inventory,directory}=require(path.join(runtime,'tests/test_ui139_fleet_dom.cjs'));
async function check(browser,width,empty){
 const page=await browser.newPage({viewport:{width,height:900}});
 page.setDefaultTimeout(6500);
 const records=structuredClone(inventory);
 Object.assign(received,{name:'DEMO Acoustic spares case',site_name:'DEMO Meridian',location:'Deck receiving',manifest_number:'DEMO-MAN-003'});
 const extras=['a','b','c','d'].map(id=>({...records[0],id}));
 manifest.lines=[...records.slice(0,1),...extras].map(x=>({root_id:received.root_id,item_id:x.id}));
 records.push(...extras);
 if(empty) records.splice(1,1);
 records.push({...inventory[1],id:'other',location:'Other ship store',custody:{state:'available',site_id:'horizon'}});
 let writes=0;
 await page.addInitScript(a=>sessionStorage.setItem('aj-fleet-session',JSON.stringify(a)),auth);
 await page.route('**/*',async route=>{
  const u=new URL(route.request().url()),n=u.pathname;
  if(u.hostname!=='fixture.localhost')return route.abort();
  if(n.startsWith('/api/')){
   if(route.request().method()!=='GET'){writes++;return route.abort();}
   let data=n.endsWith('/directory')?directory:n.endsWith('/receiving')?[received]:n.endsWith('/inventory')?records:n.endsWith('/info')?{hub_id:auth.hub_id}:manifest;
   if(n.endsWith('/inventory'))assert.equal(u.searchParams.get('site_id'),received.site_id);
   return route.fulfill({json:data});
  }
  const file=path.join(runtime,'app/static',path.basename(n)||'fleet.html');
  return fs.existsSync(file)?route.fulfill({path:file}):route.abort();
 });
 try{
  await page.goto('http://fixture.localhost/fleet.html#receiving');
  await page.locator('[data-receiving-open]').first().click();await page.locator('#receiving-place').click();
  if(process.argv[3]==='baseline'){await page.locator('#place-location').waitFor();assert(await page.locator('#place-location').isVisible());assert.equal(await page.locator('#place-location').getAttribute('list'),null);console.log('PASS baseline free text',width);return;}
  const group=page.locator('#place-known-fields'),search=group.locator('input[type=search]');
  assert.equal(await group.getByText('Other ship store',{exact:true}).count(),0);
  assert.equal(await group.getByText('Deck receiving',{exact:true}).count(),0);
  await page.locator('#place-next').click();assert.equal(await page.locator('#modal-form').getAttribute('data-logistics-step'),'0');
  if(empty){assert(await group.getByText(/No recorded final locations|Nenhum local final/).isVisible());}
  else{
   const option=group.locator('button[data-destination]').first();await option.waitFor();
   await search.fill('unmatched');assert(await group.locator('.wl-picker-empty').isVisible());
   await search.fill('almox');await option.focus();await page.keyboard.press('Enter');
   assert.equal(await page.locator('#place-known').inputValue(),'Almoxarifado');
   await page.locator('#place-next').click();assert.equal(await page.locator('#modal-form').getAttribute('data-logistics-step'),'1');
   assert(await page.locator('#place-note').isVisible());await page.locator('#place-back').click();
  }
  await page.locator('#place-step-destination .wl-mode-choices summary').click();await page.locator('[data-mode=manual]').click();
  await page.locator('#place-location').fill('Fixture locker');await page.locator('#place-next').click();
  assert.equal(await page.locator('#modal-form').getAttribute('data-logistics-step'),'1');assert.equal(writes,0);
  console.log('PASS',width,empty?'empty':'recorded','keyboard, Continue, manual, zero writes');
 }finally{await page.close();}
}
(async()=>{const b=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,389])for(const empty of process.argv[3]?[false]:[false,true])await check(b,w,empty)}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
