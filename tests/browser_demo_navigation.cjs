'use strict';
const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');

async function verify(origin, options = {}) {
  const browser = await chromium.launch(options.launch || {executablePath:process.env.WAVELINK_TEST_CHROMIUM});
  try {
    for (const width of [1360,390]) {
      const ctx = await browser.newContext({viewport:{width,height:900},ignoreHTTPSErrors:!!options.local});
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.stack || e.message));
      page.setDefaultTimeout(16000);
      try {
        await page.goto(origin+'/__demo/public');
        const home=page.locator('#personal-home');
        await home.locator('#wl-mood-editor:visible').waitFor();
        const faces=home.locator('.wl-mood-face');
        assert.ok(await faces.count()>=5);
        assert.equal(await home.locator('input[name="wl-team-mood"]').count(),5);
        await home.getByText('Happy',{exact:true}).first().click();
        await home.locator('#wl-mood-share').click();
        await home.locator('#wl-mood-remove:visible').waitFor();
        const url=new URL(page.url());
        async function open(hash) { const target=new URL(url); target.hash=hash; await page.goto(target.href); }
        await open('team');
        await page.locator('#wl-team-moods #wl-mood-remove:visible').waitFor();
        assert.equal(await page.locator('input[value="happy"]').isChecked(),true);
        await page.reload();
        await page.locator('#wl-team-moods #wl-mood-remove:visible').waitFor();
        await page.locator('#wl-mood-remove').click();
        await page.getByText('Your mood was removed.').waitFor();
        await open('workspaces');
        await page.locator('#home-hr').waitFor();
        const keys=await page.locator('[data-home-workspace]').evaluateAll(nodes=>nodes.map(n=>n.dataset.homeWorkspace));
        const expected=['hr','it','handovers','tasks','checklists','logs','calendar','inventory','maintenance','certificates','fleet','shipments','receiving','faults','toolbox','qshe','originals','builders','members','admin'];
        assert.deepEqual([...keys].sort(),expected.sort());
        await page.locator('#home-hr').click();
        const hr=page.locator('#hr-workspace');
        await hr.locator('[data-hr-tab="calendar"]').waitFor({state:'attached'});
        if(width>600) await hr.locator('[data-hr-tab="calendar"]:visible').click();
        else await hr.locator('#hr-section-select').selectOption('calendar');
        await hr.getByText('Offshore Survey',{exact:true}).first().waitFor({state:'attached'});
        assert.ok((await hr.innerText()).includes('MV Aurora'));
        if(options.proof)await page.screenshot({path:options.proof+'/native-hr-'+width+'.jpg',type:'jpeg'});
        if(width>600)await hr.locator('[data-hr-tab="people"]:visible').click();
        else await hr.locator('#hr-section-select').selectOption('people');
        await hr.getByText('Lia Costa',{exact:false}).first().waitFor({state:'attached'});
        await open('it');
        const it=page.locator('#it-workspace');
        await it.locator('[data-it-view="queue"]').click();
        await it.locator('.it-request-link').filter({hasText:'Survey workstation'}).click();
        await it.getByText('PORTA-REDE-EXEMPLO.pdf',{exact:false}).first().waitFor({state:'attached'});
        await open('admin');
        const sections=page.locator('.admin-hub-card[href^="#admin/"]');
        await sections.first().waitFor();
        assert.equal(await sections.count(),8);
        for(const key of ['departments','records','imports','company','templates','logbooks','fleet','users']){
          await page.locator('.admin-hub-card[href="#admin/'+key+'"]').click();
          await page.waitForFunction(k=>location.hash==='#admin/'+k,key);
          await open('admin');
          await sections.first().waitFor();
        }
        await open('home');
        await home.locator('#wl-mood-editor:visible').waitFor();
        assert.equal(await home.locator('#wl-mood-remove').isVisible(),false);
        if(options.proof)await page.screenshot({path:options.proof+'/native-home-'+width+'.jpg',type:'jpeg'});
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1),false);
        assert.deepEqual(errors,[]);
        console.log(width+'px: 20 native workspaces, 8 administrative sections, HR calendar and directory, IT case, and private mood check-in');
      } catch(e) {
        console.error('Current route',new URL(page.url()).hash,'UI', (await page.locator('body').innerText()).slice(-2500),'errors',errors);
        throw e;
      } finally { await ctx.close(); }
    }
  } finally {await browser.close();}
}
if(require.main===module)verify(new URL(process.argv[2]).origin).catch(e=>{console.error(e);process.exitCode=1;});
module.exports={verify};
