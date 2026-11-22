'use strict';
const assert = require('node:assert/strict');
const { chromium } = require('playwright-core');

async function run() {
  const entry = new URL(process.argv[2]);
  assert.equal(entry.hostname, '127.0.0.1');
  const browser = await chromium.launch({executablePath: process.env.WAVELINK_TEST_CHROMIUM});
  try {
    const context = await browser.newContext({ignoreHTTPSErrors:true,serviceWorkers:'block'});
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.setDefaultTimeout(15000);
    await page.goto(entry.href);
    await page.locator('#wl-global-search-trigger').waitFor();
    const workspace = new URL(page.url());
    let equipment;
    for (const [route, prefix] of [['faults','fr'], ['qshe','qs']]) {
      workspace.hash = route;
      await page.goto(workspace.href);
      await page.locator('#'+prefix+'-new').click();
      await page.locator('[data-rw-section="source"] > summary').click();
      const lookup = page.waitForResponse(r => new URL(r.url()).pathname === '/api/'+route+'/links');
      await page.locator('#'+prefix+'-find-source').click();
      const result = await (await lookup).json();
      const index = result.items.findIndex(item => item.work_site?.active);
      assert.ok(index>=0,route+' fixture needs an asset allocated to a ship or base');
      const linkedSite = result.items[index].work_site.id;
      equipment=result.items[index];
      const field = page.locator('#'+prefix+'-work_site_id');
      const picker = page.locator('#'+prefix+'-source');
      await picker.selectOption(String(index));
      assert.equal(await field.inputValue(),linkedSite);
      assert.deepEqual(await field.evaluate(el=>WLWorkSites.equipmentBody(el,el.value)),{equipment_site_hint:linkedSite});
      await page.locator('#'+prefix+'-clear-source').click();
      assert.equal(await field.inputValue(),'');
      const alternate = await field.locator('option').evaluateAll((rows,id)=>rows.find(x=>x.value&&x.value!==id).value,linkedSite);
      await field.selectOption(alternate);
      await picker.selectOption(String(index));
      assert.equal(await field.inputValue(),alternate);
      assert.deepEqual(await field.evaluate(el=>WLWorkSites.equipmentBody(el,el.value)),{work_site_id:alternate});
      await page.locator('#'+prefix+'-clear-source').click();
      assert.equal(await field.inputValue(),alternate);
      page.once('dialog',dialog=>dialog.accept());
      await page.locator('#'+prefix+'-close').click();
    }
    const navigate=async hash=>{workspace.hash=hash;await page.goto(workspace.href);};
    const discard=async()=>{
      page.once('dialog',dialog=>dialog.accept());
      await page.locator('#fw-discard').click();
      await page.locator('#fw-form').waitFor({state:'hidden'});
    };
    const expected=equipment.work_site.id;
    const formSite=page.locator('#fw-form [name=work_site_id]');
    const isInferred=async()=>{
      await page.waitForFunction(id=>document.querySelector('#fw-form [name=work_site_id]')?.value===id,expected);
      assert.equal(await formSite.evaluate(el=>WLWorkSites.equipmentHint(el)),expected);
    };
    await navigate('tasks');
    await page.locator('#task-new').click();
    await page.locator('[data-task-choice="general"]').click();
    await page.locator('#tf-link > summary').click();
    await page.locator('select[name=link_kind]').selectOption('asset');
    await page.locator('select[name=link_id] option[value="'+equipment.id+'"]').waitFor({state:'attached'});
    await page.locator('select[name=link_id]').selectOption(equipment.id);
    await isInferred();
    await page.locator('#fw-keep').click();
    await page.locator('#fw-form').waitFor({state:'hidden'});
    await page.locator('#op-drafts').click();
    await page.locator('dialog[open] [data-task-resume]').first().click();
    await isInferred();
    await discard();
    await navigate('certificates');
    await page.locator('#certificate-new').click();
    await page.locator('#cf-equipment > summary').click();
    await page.locator('input[name="asset_'+equipment.id+'"]').check();
    await isInferred();
    await page.locator('input[name="asset_'+equipment.id+'"]').uncheck();
    assert.equal(await formSite.inputValue(),'');
    await discard();
    await navigate('asset/'+equipment.id);
    await page.locator('[data-asset-nav][aria-controls="asset-maintenance"]').click();
    await page.locator('#asset-new-maintenance').click();
    await isInferred();
    assert.ok((await page.locator('#fw-form').innerText()).includes(equipment.work_site.name));
    await discard();
    // Verify a mounted native picker with delayed catalogue data and mixed/unknown links.
    const transitions = await page.evaluate(async () => {
      const host=document.createElement('div');
      document.body.append(host);
      const a={id:'ship-a',name:'Ship A',kind:'vessel',active:true};
      const b={id:'port-b',name:'Port B',kind:'shore_base',active:true};
      let resolve;
      const api=()=>new Promise(done=>{resolve=done;});
      const picker=WLWorkSites.picker(host,api);
      const read=()=>[picker.select.value,WLWorkSites.equipmentHint(picker.select)];
      WLWorkSites.equipmentSites(picker.select,[a,a]);
      resolve({sites:[a,b]});
      await Promise.resolve();
      const results=[read()];
      for(const links of [[a,b],[a,null],[b],[null],[],[a]]) {
        WLWorkSites.equipmentSites(picker.select,links);
        results.push(read());
      }
      picker.select.value=b.id;
      picker.select.dispatchEvent(new Event('change',{bubbles:true}));
      WLWorkSites.equipmentSites(picker.select,[a]);
      results.push(read());
      host.remove();
      return results;
    });
    assert.deepEqual(transitions,[
      ['ship-a','ship-a'],['',''],['',''],['port-b','port-b'],['',''],['',''],['ship-a','ship-a'],['port-b','']
    ]);
    assert.deepEqual(errors,[]);
    console.log('Passed equipment linking on Faults, HSE, Tasks (including a reopened draft), Certificates, Maintenance, delayed catalogue loading, mixed locations and manual overrides.');
  } finally {
    await browser.close();
  }
}
run().catch(error=>{console.error(error);process.exitCode=1;});
