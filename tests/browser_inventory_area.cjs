'use strict';
const assert = require('node:assert/strict');
const { chromium } = require('playwright-core');

async function verify(browser, entry, width, pt) {
  const page = await browser.newPage({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
  try {
    await page.route('**/api/inventory/lists/*', async route => {
      const response = await route.fetch();
      const book = await response.json();
      if (!book.items?.length) return route.fulfill({response});
      const template = book.items[0];
      const box = {...template,id:'box-a',name:'Training case',archived:false,is_container:true,container_id:'',container_path:[],department_id:'d1'};
      const item = {...box,id:'gauge',name:'Training gauge',is_container:false,container_id:box.id,container_path:[{id:box.id,name:box.name}]};
      book.items=[box,item,{...item,id:'other',name:'Training gauge B',department_id:'d2'},{...item,id:'unknown',name:'Training spare',department_id:null}];
      book.directory.departments=[{id:'d1',name:'Survey',active:true},{id:'d2',name:'Engineering',active:true}];
      await route.fulfill({response,json:book});
    });
    await page.goto(entry+(pt?'&lang=pt':''));
    await page.locator('#wl-global-search-trigger:visible').waitFor({timeout:60000});
    if (pt) {
      await page.evaluate(()=>{location.hash='profile'});
      await page.locator('#wl-language-select').selectOption('pt-BR');
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
    }
    await page.evaluate(()=>{location.hash='inventory'});
    await page.locator('.iw162-inventory-row').first().click();
    const area=page.getByRole('combobox',{name:pt?'Área responsável (departamento)':'Responsible area (department)',exact:true});
    await area.waitFor();
    const bounds=await area.boundingBox();
    assert.ok(bounds.x>=0 && bounds.x+bounds.width<=width+1);
    const rowIds=()=>page.locator('#inv-rows [data-select-row]').evaluateAll(rows=>rows.map(r=>r.dataset.selectRow).sort());
    await area.selectOption('d1');
    assert.deepEqual(await rowIds(),['box-a','gauge']);
    assert.match(await page.locator('#inv-total').innerText(),/2/);
    await page.locator('#inv-expand').click();
    await page.locator('[name=search]').fill('gauge');
    assert.deepEqual(await rowIds(),['gauge']);
    await page.locator('[data-inv-locate=gauge]').click();
    assert.equal(await area.inputValue(),'d1');
    assert.deepEqual(await rowIds(),['gauge']);
    await area.selectOption('__unassigned');
    await page.locator('#inv-empty-clear').waitFor();
    await page.locator('[name=search]').fill('');
    assert.deepEqual(await rowIds(),['unknown']);
    await page.locator('#inv-clear-filters').click();
    assert.equal(await area.inputValue(),'');
    assert.deepEqual(await rowIds(),['gauge','other','unknown']);
    console.log('PASS inventory area',width,pt?'pt-BR':'en');
  } finally { await page.close(); }
}
(async()=>{const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{await verify(browser,process.argv[2],1280,false);await verify(browser,process.argv[2],390,true);}finally{await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
