'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');

async function visit(page, view) {
  const url = new URL(page.url());
  url.hash = view;
  await page.goto(url.href);
}
async function start(browser, width, url) {
  const context = await browser.newContext({viewport:{width,height:900},ignoreHTTPSErrors:true,serviceWorkers:'block'});
  const page = await context.newPage();
  await page.goto(url);
  await page.locator('#wl-global-search-trigger:visible').waitFor({timeout:60000});
  return {context,page};
}
function recordPath(id) {return '/api/records/'+id;}

async function checkNative(browser,width,url) {
  const {context,page} = await start(browser,width,url);
  try {
    const writes = [], errors = [];
    page.on('request', req => {if(req.method()==='POST'&&new URL(req.url()).pathname.startsWith('/api/records/'))writes.push(req.url());});
    page.on('pageerror',err=>errors.push(err.message));
    await visit(page,'checklists');
    const row = page.locator('article[data-cw-card]').first();
    await row.waitFor();
    const id = await row.getAttribute('data-cw-card');
    const name = await row.locator('.cw-record-name').innerText();
    const receipt = page.waitForResponse(r=>new URL(r.url()).pathname===recordPath(id)&&r.request().method()==='GET');
    await row.locator('.cw-type').click();
    const saved = await (await receipt).json();
    const panel = page.locator('#checklist-inspector');
    const list = panel.locator('.cw-item-list');
    await list.waitFor();
    assert.equal(new URL(page.url()).hash,'#checklists');
    assert.equal(await panel.locator('h2').innerText(),name);
    const phases = ['pre','post'].filter(p=>saved.phases[p]);
    const stage = phases.find(p=>!saved.phases[p].final)||phases[0];
    const definition = saved.template.sections.filter(s=>s.id!=='winch'||saved.meta.include_winch).flatMap(s=>s.items).find(i=>i.phases.includes(stage));
    assert.ok((await list.innerText()).includes(definition.text));
    if(width>850){
      const left = await row.boundingBox(), right = await panel.boundingBox();
      assert.ok(right.x>=left.x+left.width, 'details appear to the right of the list');
    }else assert.equal(await row.isVisible(),false);
    assert.deepEqual(writes,[], 'previewing must not join or change a checklist');
    await panel.locator('#cw-back-list').click();
    assert.equal(await row.locator('.cw-record-name').evaluate(el=>el===document.activeElement),true);
    await row.locator('.cw-record-name').press('Enter');
    await list.waitFor();
    if(await page.evaluate(()=>window.WavelinkNativeDemo.active())){
      await panel.locator('[data-cw-read-stage]').first().click();
      await page.waitForFunction(()=>document.activeElement.id==='cw-preview-items');
      assert.equal(new URL(page.url()).hash,'#checklists');
      assert.deepEqual(writes,[]);
    }else{
    await panel.locator('a[data-cw-open]').first().click();
    await page.waitForURL(u=>u.hash===`#dive/${id}/${stage}`);
    await page.locator('#checklist-stage-workspace').waitFor();
    }
    assert.deepEqual(errors,[]);
    console.log(width+'px checklist body, keyboard selection, saved items, back and explicit stage passed');
  }finally{await context.close();}
}

async function checkSwitchAndPaging(browser,width,url) {
  const {context,page}=await start(browser,width,url);
  try {
    const menu=page.locator('#workspace-nav a[data-workspace="checklists"]');
    if(!await menu.isVisible())await page.locator('#shell-toggle').click();
    await menu.click();
    const row=page.locator('article[data-cw-card]').first();
    const id=await row.getAttribute('data-cw-card');
    const path=recordPath(id);
    const received=page.waitForResponse(response=>new URL(response.url()).pathname===path);
    await row.locator('.cw-record-name').click();
    const original=await (await received).json();
    await page.locator('#cw-preview-items .cw-item-list').waitFor();
    await page.locator('#cw-back-list').click();
    let mode='long', release, began;
    const started=new Promise(resolve=>{began=resolve;});
    const delayed=new Promise(resolve=>{release=resolve;});
    await page.route(u=>u.pathname===path,async route=>{
      if(mode==='denied'){await route.fulfill({status:403,contentType:'application/json',body:'{"detail":"Unavailable"}'});return;}
      const saved=structuredClone(original);
      if(mode==='slow'){began();await delayed;}
      const section=saved.template.sections.find(s=>s.items.length&&s.id!=='winch');
      const model=section.items[0];
      const stage='pre';
      const alternate='post';
      saved.phases[alternate] ||= {version:1,final:null};
      saved.items[alternate] ||= {};
      const extra=Array.from({length:19},(_,i)=>({...model,id:'preview-'+i,number:String(i<6?i+1:i-5).padStart(2,'0'),text:'Inspection item '+(i+1),phases:[stage]}));
      const other={...model,id:'other-stage',number:'A',text:'Alternate stage check',phases:[alternate]};
      saved.template.sections=[
        {...section,id:'deck',title:'Deck & safety',short:'Deck',items:extra.slice(0,6)},
        {...section,id:'winch',title:'Excluded winch',items:[{...model,id:'winch-check',phases:[stage]}]},
        {...section,id:'subsea',title:'',short:'Subsea checks',items:extra.slice(6)},
        {...section,id:'other',title:'',short:'',items:[other]}
      ];
      saved.meta.include_winch=false;
      if(mode==='empty')saved.template.sections=[];
      saved.items[stage]={};
      extra.forEach((item,i)=>{saved.items[stage][item.id]={status:i===0?'issue':'pending'};});
      saved.items[alternate][other.id]={status:'complete'};
      await route.fulfill({json:saved});
    });
    await row.locator('.cw-record-name').click();
    const panel=page.locator('#checklist-inspector');
    await panel.getByText('Inspection item 1',{exact:true}).waitFor();
    assert.equal(await panel.locator('.cw-item-list li').count(),8);
    const headings=panel.locator('#cw-preview-items').getByRole('heading',{level:4});
    assert.deepEqual(await headings.allTextContents(),['Deck & safety','Subsea checks'],
      'The preview must distinguish two sections whose saved numbers restart.');
    const deck=panel.getByRole('list',{name:'Deck & safety',exact:true});
    const subsea=panel.getByRole('list',{name:'Subsea checks',exact:true});
    assert.equal(await deck.getByRole('listitem').count(),6);
    assert.equal(await subsea.getByRole('listitem').count(),2);
    assert.deepEqual(await panel.locator('.cw-item-number').allTextContents(),['01','02','03','04','05','06','01','02']);
    await panel.locator('#cw-items-next').click();
    await panel.getByText('Inspection item 9',{exact:true}).waitFor();
    assert.deepEqual(await headings.allTextContents(),['Subsea checks']);
    assert.equal(await subsea.getByRole('listitem').count(),8);
    assert.deepEqual(await panel.locator('.cw-item-number').allTextContents(),['03','04','05','06','07','08','09','10']);
    assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
    await panel.locator('#cw-preview-phase').selectOption('post');
    assert.equal(await headings.count(),0,'A legacy section without a label should still display its items.');
    await panel.getByText('Alternate stage check',{exact:true}).waitFor();
    assert.equal(await panel.locator('.cw-item-status').innerText(),'Completed');
    await panel.locator('#cw-back-list').click();
    mode='empty';
    await row.locator('.cw-record-name').click();
    await panel.getByText('This stage has no items.',{exact:true}).waitFor();
    assert.equal(await headings.count(),0);
    await panel.locator('#cw-back-list').click();
    mode='slow';
    await row.locator('.cw-record-name').click();await started;
    await panel.locator('#cw-back-list').click();
    release();
    await page.getByRole('heading',{name:'Select a checklist',includeHidden:true}).waitFor({state:'attached'});
    await row.locator('.cw-record-name').waitFor();
    assert.equal(await row.locator('.cw-record-name').evaluate(el=>el===document.activeElement),true);
    mode='denied';
    await row.locator('.cw-record-name').click();
    await panel.getByRole('heading',{name:'Checklist unavailable'}).waitFor();
    assert.equal(await panel.locator('.cw-item-list,[data-cw-open]').count(),0);
    console.log('Item pagination, phase selection, late reads and unavailable record passed');
  }finally{await context.close();}
}

async function checkCardLayouts(browser,width,url) {
  const {context,page} = await start(browser,width,url);
  const problems=[];
  const routes = [
    ['home','.ph-row'], ['home','.ph-shift-card'], ['home','#recognition-home .wl-feed-card'],
    ['workspaces','.home-destination'], ['tasks','.tw110-row'], ['checklists','.cw-record'],
    ['maintenance','.mw-order'], ['handovers','.hwd-record'], ['fleet','.fleet77-site-grid article'],
    ['inventory','.iw162-inventory-row'], ['toolbox','.fw-card'], ['original-files','.wf-row.of-file'],
    ['faults','.fr-row'], ['qshe','.qs-row'], ['logs','.log-book-card'], ['team','.wl-feed-card'],
    ['builders','.sb-card'], ['certificates','.certificate-card'], ['calendar','.calendar-agenda-row'],
    ['admin','.admin-hub-card']
  ];
  if(width<=760)routes.push(['it','.it-table tbody tr']);
  try {
    for(const [route,selector] of routes) {
      if(new URL(page.url()).hash!=='#'+route)await visit(page,route);
      const target=route==='fleet'?page.frameLocator('#fleet-workspace-frame'):page;
      const card=target.locator(selector+':visible').first();
      await card.waitFor({timeout:8000});
      const layout=await target.locator(selector+':visible').evaluateAll(cards=>{
        const viewport=document.documentElement.clientWidth;
        return cards.map(card=>{
          const rect=card.getBoundingClientRect(),css=getComputedStyle(card);
          return {left:rect.left,right:rect.right,viewport,width:rect.width,height:rect.height,
            clipped:css.overflowY!=='visible'&&card.scrollHeight>card.clientHeight+2};
        });
      });
      for(const [index,box] of layout.entries()){
        const name=`${width}px ${route} ${selector} [${index}]`;
        if(box.width<=0||box.height<=0||box.left< -1||box.right>box.viewport+1)problems.push(`${name} extends outside its viewport`);
        if(box.clipped)problems.push(`${name} clips its contents or requires internal scrolling`);
      }
      if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1))problems.push(`${width}px ${route} overflows horizontally`);
    }
    console.log(`${width}px checked ${routes.length} lists for clipped content and viewport overflow: ${problems.length} problems`);
    return problems;
  }finally{await context.close();}
}

async function main(){
  const browser=await chromium.launch({executablePath:process.env.WAVELINK_TEST_CHROMIUM});
  try{
    const url=process.argv[2];
    for(const width of [1360,390])await checkNative(browser,width,url);
    for(const width of [1360,389])await checkSwitchAndPaging(browser,width,url);
    const problems=[];
    for(const width of [1360,1024,390,320])problems.push(...await checkCardLayouts(browser,width,url));
    assert.deepEqual(problems,[]);
  }finally{await browser.close();}
}
main().catch(error=>{console.error(error);process.exitCode=1;});
