'use strict';
// Run against a public demo deployment with playwright-core and Chromium installed.
// node tests/browser_demo_navigation.cjs https://demo.example.com
const assert = require('node:assert/strict');
const {chromium} = require('playwright-core');

async function verifyHRLayout(page, expectedColumns) {
  const sections = page.locator('[data-demo-workspace] .section-grid');
  await sections.waitFor();
  const layout = await sections.evaluate(grid => {
    const links = [...grid.querySelectorAll('li > a')];
    return {
      grid: getComputedStyle(grid).display,
      cards: links.length,
      columns: new Set(links.map(link => Math.round(link.getBoundingClientRect().left))).size,
      separated: links.every(link => {
        const title = link.querySelector('.entry-title').getBoundingClientRect();
        const note = link.querySelector('small').getBoundingClientRect();
        return note.top > title.bottom && link.getBoundingClientRect().height >= 44;
      }),
      overflow: document.documentElement.scrollWidth > innerWidth + 1
    };
  });
  assert.deepEqual(layout, {grid: 'grid', cards: 6, columns: expectedColumns,
                            separated: true, overflow: false});
}

async function verify() {
  const origin = new URL(process.argv[2]).origin;
  const browser = await chromium.launch({executablePath: process.env.WAVELINK_TEST_CHROMIUM});
  try {
    for (const width of [1360, 390]) {
      const context = await browser.newContext({viewport: {width, height: 850}});
      const page = await context.newPage();
      await page.goto(origin + '/__demo/public');
      const home = page.locator('.ux-workspace-shortcuts');
      await home.locator('a[href="#demo/hr"]').waitFor();
      await home.locator('a[href="#demo/it"]').waitFor();
      const workspace = new URL(page.url());
      workspace.hash = 'workspaces';
      await page.goto(workspace.href);
      await page.locator('#home-hr').waitFor();
      const cards = page.locator('[data-home-workspace]');
      assert.deepEqual(await cards.evaluateAll(rows => rows.slice(0, 2).map(row => row.dataset.homeWorkspace)), ['hr', 'it']);
      if (width > 600) {
        await page.locator('#nav-hr[href="#demo/hr"]').waitFor();
        await page.locator('#nav-it[href="#demo/it"]').waitFor();
      }
      await page.locator('#home-hr').click();
      await verifyHRLayout(page, width > 600 ? 3 : 1);
      await page.locator('a[href="#demo/schedule"]').click();
      await page.locator('a[href="#demo/schedule/aurora"]').click();
      await page.locator('[data-demo-request]').getByRole('heading', {level: 1, name: /Aurora/}).waitFor();
      await page.locator('[data-demo-request] a[href="#workspaces"]').click();
      await page.locator('#home-it').click();
      await page.locator('a[href="#demo/it/ticket-018"]').click();
      await page.locator('[data-demo-request] a[href^="/__demo/management/files/"]').waitFor();
      const recordLayout = await page.locator('[data-demo-workspace] .details').evaluate(div => getComputedStyle(div).display);
      assert.equal(recordLayout, 'grid');
      await page.reload();
      await page.locator('[data-demo-request]').getByRole('heading', {level: 1, name: /018/}).waitFor();
      assert.equal(new URL(page.url()).search, workspace.search);
      await context.close();
    }
  } finally {
    await browser.close();
  }
}
if (require.main === module) verify().catch(error => { console.error(error); process.exitCode = 1; });
module.exports = {verifyHRLayout};
