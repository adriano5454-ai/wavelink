'use strict';

const assert = require('node:assert/strict');
const path = require('node:path');
const { chromium } = require('playwright-core');

// Exercise the ordinary workspace pages of the isolated demonstration company.
// The test uses displayed records and the native responses delivered to this session.
const lists = [
  {route:'tasks', endpoint:'/api/tasks', key:'tasks', rows:'[data-task-id]', id:'data-task-id',
    search:'[name=task-query]', word:r=>r.title, reset:'#task-reset'},
  {route:'maintenance', endpoint:'/api/maintenance', key:'jobs', rows:'article[data-mw-order]', id:'data-mw-order',
    search:'#mw-search', word:r=>r.reference||r.name, reset:'#mw-clear'},
  {route:'faults', endpoint:'/api/faults', key:'items', rows:'[data-fr-id]', id:'data-fr-id',
    search:'#fr-query', word:r=>r.reference, submit:'#fr-filters [type=submit]'},
  {route:'qshe', endpoint:'/api/qshe', key:'items', rows:'[data-qs-id]', id:'data-qs-id',
    search:'#qs-query', word:r=>r.reference, submit:'#qs-filters [type=submit]'},
  {route:'checklists', endpoint:'/api/records', rows:'article[data-cw-card]', id:'data-cw-card',
    search:'#checklist-search', word:r=>r.meta?.dive_number||r.id, reset:'#cw-clear'},
  {route:'certificates', endpoint:'/api/certificates', rows:'[data-cert-preview]', id:'data-cert-preview',
    search:'[name=certsearch]', word:r=>r.number||r.title, reset:'#cert-reset'},
  {route:'toolbox', endpoint:'/api/toolbox', key:'talks', rows:'[data-toolbox-id]', id:'data-toolbox-id',
    search:'#tb-query', word:r=>r.meta?.work_scope||r.meta?.site||r.meta?.vessel},
  {route:'logs', endpoint:'/api/logs/books', rows:'.log-book-card', search:'#logs-page-query',
    vessel:'#logs-location-filter', word:r=>r.name||r.title},
  {route:'it', endpoint:'/api/it/workspace', key:'requests', rows:'a.it-request-link',
    search:'#it-filters [name=query]', word:r=>r.title, submit:'#it-filters [type=submit]'},
];

async function route(page, hash) {
  const nav=page.locator('a[href="#'+hash+'"]:visible').first();
  if(await nav.count()){
    await nav.click();
    return;
  }
  const title=page.locator('main h1:visible').first();
  if(await title.count()) await title.click();
  const url = new URL(page.url());
  url.hash = hash;
  await page.goto(url.href);
}

async function recordIds(page, desc) {
  return page.locator(desc.rows + ':visible').evaluateAll((rows, attr) => rows.map(el =>
    attr ? el.getAttribute(attr) : (el.matches('a') ? el : el.querySelector('a')).hash.split('/').pop()), desc.id);
}

async function expectIds(page, desc, ids, message) {
  try {
    await page.waitForFunction(({selector,attr,wanted})=>{
      const ids = [...document.querySelectorAll(selector)].filter(el=>el.getClientRects().length).map(el=>
        attr ? el.getAttribute(attr) : (el.matches('a') ? el : el.querySelector('a')).hash.split('/').pop());
      return JSON.stringify(ids.sort())===JSON.stringify(wanted);
    }, {selector:desc.rows,attr:desc.id,wanted:[...ids].sort()},{timeout:9000});
  } catch(error) {
    assert.deepEqual((await recordIds(page,desc)).sort(),[...ids].sort(),message);
    throw error;
  }
}

async function typeQuery(page, desc, query) {
  await page.locator(desc.search).fill(query);
  if(desc.submit) await page.locator(desc.submit).click();
}

function siteFor(record, options) {
  const id = record.work_site?.id || record.meta?.work_site?.id || record.vessel_scope?.site_id;
  if(id) return options.find(o=>o.id===id);
  const labels=[record.meta?.vessel, record.meta?.site,record.location].filter(Boolean);
  return options.find(o=>labels.some(label=>o.label===label || o.label.startsWith(label+' · ')));
}

async function checkItLocations(page,desc,language) {
  const responseFor=path=>page.waitForResponse(r=>new URL(r.url()).pathname===path&&r.request().method()==='GET');
  const mine=responseFor(desc.endpoint);
  const directory=responseFor('/api/fleet/work-locations');
  await route(page,desc.route);
  const mineData=await (await mine).json();
  const sites=(await (await directory).json()).sites;
  const form=page.locator('#it-filters');
  const location=form.locator('[data-page-vessel]');
  assert.equal(await form.locator('.wl-page-vessel label>span').innerText(),language==='pt'?'Embarcação ou base':'Vessel or base');
  await location.locator('option').filter({hasText:'DEMO Meridian'}).waitFor({state:'attached'});
  const options=await location.locator('option').evaluateAll(nodes=>nodes.map(n=>({id:n.value,text:n.textContent})));
  assert.equal(options[0].text,language==='pt'?'Todas as localizações':'All locations');
  assert.deepEqual(options.slice(1).map(o=>o.id).sort(),sites.filter(s=>['vessel','shore_base'].includes(s.kind)).map(s=>s.id).sort());
  const box=await location.boundingBox();
  assert.ok(box&&box.width>0&&box.x>=0&&box.x+box.width<=page.viewportSize().width+1);
  const ship=sites.find(s=>s.code==='AUR');
  const base=sites.find(s=>s.kind==='shore_base'&&s.name==='DEMO Shore Base');
  assert.ok(ship&&base,'The Fleet directory includes a vessel and a base');
  const queue=responseFor(desc.endpoint);
  await page.locator('[data-it-view=queue]').click();
  const rows=(await (await queue).json()).requests;
  const workstation=rows.find(r=>r.work_site?.id===ship.id&&/network port/i.test(r.title));
  const printer=rows.find(r=>r.work_site?.id===base.id&&/printer/i.test(r.title));
  assert.ok(workstation&&printer,'Both located IT requests are present in the service queue');
  assert.ok(mineData.requests.some(r=>r.id===workstation.id));
  assert.ok(!mineData.requests.some(r=>r.id===printer.id));
  const query=form.locator('[name=query]'),status=form.locator('[name=status]'),priority=form.locator('[name=priority]');
  async function apply(action,wanted,expectedLocation) {
    const request=responseFor(desc.endpoint);
    await action();
    const response=await request;
    const payload=await response.json();
    assert.equal(new URL(response.url()).searchParams.get('vessel_id')||'',expectedLocation);
    assert.deepEqual(payload.requests.map(r=>r.id).sort(),[...wanted].sort());
    await expectIds(page,desc,wanted,'IT results reflect the selected location and filters');
    await page.waitForFunction(id=>document.querySelector('#it-filters [data-page-vessel]')?.value===id,expectedLocation);
  }
  const submit=()=>form.locator('[type=submit]').click();
  await query.fill('network port');
  await priority.selectOption(workstation.priority);
  await status.selectOption(workstation.status);
  await apply(()=>location.selectOption(ship.id),[workstation.id],ship.id);
  if(process.env.WAVELINK_SCREENSHOT_DIR){
    await form.scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(process.env.WAVELINK_SCREENSHOT_DIR,'Wavelink-IT-location-search-'+language+'.png')});
  }
  const different=async(control,value)=>control.locator('option').evaluateAll((els,original)=>els.find(e=>e.value&&e.value!==original).value,value);
  await status.selectOption(await different(status,workstation.status));
  await apply(submit,[],ship.id);
  await status.selectOption(workstation.status);
  await priority.selectOption(await different(priority,workstation.priority));
  await apply(submit,[],ship.id);
  await status.selectOption(printer.status);
  await priority.selectOption(printer.priority);
  await apply(()=>location.selectOption(base.id),[],base.id);
  assert.equal(await query.inputValue(),'network port');
  await query.fill('printer');
  await apply(submit,[printer.id],base.id);
  await apply(()=>location.selectOption(ship.id),[],ship.id);
  await apply(()=>page.locator('#it-clear').click(),rows.map(r=>r.id),'');
  for(const control of [query,status,priority]) assert.equal(await control.inputValue(),'');
  console.log(language+' IT: Aurora workstation and Shore Base printer confirmed with keyword, status, priority, and reset');
}

async function verifyRegister(page, desc, language) {
  if(desc.route==='it')return checkItLocations(page,desc,language);
  const response = page.waitForResponse(r=>new URL(r.url()).pathname===desc.endpoint && r.request().method()==='GET');
  await route(page,desc.route);
  let body=await (await response).json();
  if(desc.route==='tasks') {
    const all=page.locator('button[data-task-view=all]');
    if(await all.getAttribute('aria-pressed')!=='true'){
      const loaded=page.waitForResponse(r=>new URL(r.url()).pathname===desc.endpoint&&r.request().method()==='GET');
      await all.click();
      body=await (await loaded).json();
      await page.locator('button[data-task-view=all][aria-pressed=true]').waitFor();
    }
  }
  const data=desc.key?body[desc.key]:body;
  const vessel=page.locator(desc.vessel||'main select[data-page-vessel]').first();
  await vessel.waitFor();
  await vessel.locator('option').filter({hasText:'DEMO Meridian'}).waitFor({state:'attached'});
  assert.equal(await page.locator('#wl-search-dialog:visible').count(),0);
  const opts=await vessel.locator('option').evaluateAll(nodes=>nodes.map(el=>({id:el.value,label:el.textContent.trim()})));
  const active=opts.filter(o=>o.id&&!o.id.startsWith('__'));
  if(!desc.vessel) {
    assert.match(opts[0].label,language==='pt'?/Todas as embarcações/i:/All vessels/i);
    assert.equal(opts.some(o=>/Shore Base|DEMO Workshop/i.test(o.label)),false,'Only Fleet vessels appear on '+desc.route);
  }
  await vessel.waitFor();
  const box=await vessel.evaluate(el=>{const r=el.getBoundingClientRect();return {left:r.left,right:r.right,width:r.width,viewport:innerWidth};});
  assert.ok(box.width>0&&box.left>=-1&&box.right<=box.viewport+1,desc.route+' picker fits the viewport '+JSON.stringify(box));
  await page.locator(desc.rows+':visible').first().waitFor();
  const initial=await recordIds(page,desc);
  const rows=data.filter(r=>initial.includes(r.id));
  assert.equal(rows.length,initial.length,desc.route+' rendered rows belong to the native response');
  const located=rows.filter(r=>siteFor(r,active));
  assert.ok(located.length,desc.route+' demo has at least one record located on a vessel: '+JSON.stringify({initial,sites:active.map(o=>o.label),reported:rows.map(r=>r.work_site?.name||r.meta?.site)}));
  const chosen=siteFor(located[0],active);
  const aboard=located.filter(r=>siteFor(r,active).id===chosen.id);
  await vessel.selectOption(chosen.id);
  await expectIds(page,desc,aboard.map(r=>r.id),desc.route+' shows precisely the selected vessel');
  if(desc.route==='tasks'||desc.route==='maintenance'){
    const refresh=page.locator('#op-refresh');
    const loaded=page.waitForResponse(r=>new URL(r.url()).pathname===desc.endpoint&&r.request().method()==='GET');
    await refresh.click();
    await loaded;
    await expectIds(page,desc,aboard.map(r=>r.id),desc.route+' refresh preserves vessel');
    assert.equal(await vessel.inputValue(),chosen.id);
  }
  if(desc.route==='maintenance'&&process.env.WAVELINK_SCREENSHOT_DIR) {
    await typeQuery(page,desc,'inspection');
    await expectIds(page,desc,aboard.filter(r=>(r.name||r.title||'').toLowerCase().includes('inspection')).map(r=>r.id),'matching maintenance inspection');
    await vessel.scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join(process.env.WAVELINK_SCREENSHOT_DIR,'Wavelink-maintenance-vessel-search-'+language+'.png')});
  }
  const term=desc.word(aboard[0]);
  assert.ok(term,desc.route+' has a native searchable term');
  await typeQuery(page,desc,term);
  await page.locator(desc.rows+':visible').first().waitFor();
  const both=await recordIds(page,desc);
  assert.ok(both.includes(aboard[0].id),desc.route+' includes matching ship and text');
  assert.ok(both.every(id=>aboard.some(r=>r.id===id)));
  await typeQuery(page,desc,'wv-no-record-matches-Q7J');
  await expectIds(page,desc,[],desc.route+' combines the vessel with an empty text result');
  assert.equal(await vessel.inputValue(),chosen.id);
  await typeQuery(page,desc,'');
  const alternate=active.find(o=>o.id!==chosen.id);
  await vessel.selectOption(alternate.id);
  await expectIds(page,desc,located.filter(r=>siteFor(r,active).id===alternate.id).map(r=>r.id),desc.route+' second vessel');
  await vessel.selectOption('');
  await expectIds(page,desc,initial,desc.route+' all vessels restores the local list');
  console.log(language+' '+desc.route+' '+chosen.label+': '+aboard.length+'/'+initial.length+' visible; text and vessel intersect');
}

async function checkHandover(page) {
  await route(page,'handovers');
  const picker=page.locator('main select[data-page-vessel]').first();
  await picker.locator('option').filter({hasText:'MV Aurora'}).waitFor({state:'attached'});
  const opt=async name=>picker.locator('option').filter({hasText:name}).first().getAttribute('value');
  const days=page.locator('#hwd-days .hwd-day');
  await days.first().waitFor();
  const initial=await days.count();
  await picker.selectOption(await opt('DEMO Horizon'));
  await days.first().waitFor({state:'hidden'});
  await picker.selectOption(await opt('MV Aurora'));
  await days.first().waitFor();
  assert.equal(await days.count(),initial,'Both demo handover days belong to MV Aurora');
  await page.locator('#ho-more > summary').click();
  const cards=page.locator('#ho-rows .ho-card:visible');
  await cards.first().waitFor();
  const firstTitle=await cards.first().locator('h2').innerText();
  await page.locator('#ho-search').fill(firstTitle);
  await cards.filter({hasText:firstTitle}).first().waitFor();
  await picker.selectOption(await opt('DEMO Horizon'));
  await cards.first().waitFor({state:'hidden'});
  assert.equal(await page.locator('#ho-search').inputValue(),firstTitle);
  console.log('handovers MV Aurora '+initial+' displayed days; DEMO Horizon 0');
}

async function checkCalendar(page) {
  await route(page,'calendar');
  const picker=page.locator('main select[data-page-vessel]').first();
  const ship=picker.locator('option').filter({hasText:'MV Aurora'});
  await ship.waitFor({state:'attached'});
  await picker.selectOption(await ship.getAttribute('value'));
  await page.locator('#calendar-agenda-view').click();
  const events=page.locator('#calendar-events a[data-calendar-source]:visible');
  const expected=events.filter({hasText:/Aurora mobilisation checklist|Photo evidence training inspection/i}).first();
  await expected.waitFor();
  const search=page.locator('#calendar-query');
  if(!(await search.isVisible())) await search.locator('xpath=ancestor::details[1]/summary').click();
  await search.fill('wv-no-record-matches-Q7J');
  await expected.waitFor({state:'hidden'});
  await search.fill('Aurora mobilisation');
  await events.filter({hasText:/Aurora mobilisation/i}).first().waitFor();
  await picker.selectOption(await picker.locator('option').filter({hasText:'DEMO Horizon'}).getAttribute('value'));
  await events.filter({hasText:/Aurora mobilisation/i}).first().waitFor({state:'hidden'});
  console.log('calendar MV Aurora mobilisation search intersects the selected vessel');
}

async function verify(browser,entry,language,width) {
  const context=await browser.newContext({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
  try {
    const page=await context.newPage();
    page.setDefaultTimeout(15000);
    const errors=[];
    page.on('pageerror',err=>errors.push(err.message));
    await page.goto(entry);
    await page.locator('#wl-global-search-trigger:visible').waitFor({timeout:60000});
    if(language==='pt'){
      await route(page,'profile');
      await page.locator('#wl-language-select').selectOption('pt-BR');
      await page.locator('#profile-language button').click();
      await page.locator('html[lang="pt-BR"] #wl-language-select').waitFor();
    }
    const only=process.env.WAVELINK_TEST_PAGES?.split(',');
    for(const desc of lists.filter(d=>!only||only.includes(d.route))){
      try{await verifyRegister(page,desc,language);}catch(error){
        const heading=await page.locator('main h1').allTextContents();
        throw new Error(language+' '+desc.route+' '+page.url()+' '+heading.join(' / ')+' '+errors.join(', ')+': '+error.message,{cause:error});
      }
    }
    if(!only||only.includes('handovers'))await checkHandover(page);
    if(!only||only.includes('calendar'))await checkCalendar(page);
    assert.deepEqual(errors,[]);
  }finally{await context.close();}
}

(async()=>{
  const entry=new URL(process.argv[2]);
  assert.equal(entry.hostname,'127.0.0.1','Use a disposable local demonstration');
  const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
  try{
    await verify(browser,entry.href,'en',1360);
    await verify(browser,entry.href,'pt',390);
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
