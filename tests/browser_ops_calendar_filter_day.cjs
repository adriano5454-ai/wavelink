const assert = require('node:assert/strict');
const { chromium } = require('playwright-core');

const task = 'Review the Aurora mobilisation checklist';
const calendarResponse = response => new URL(response.url()).pathname === '/api/calendar';

async function readCalendarAfter(page, action) {
  const [response] = await Promise.all([page.waitForResponse(calendarResponse), action()]);
  assert.equal(response.status(), 200);
  const data = await response.json();
  await page.locator('#calendar-workspace[aria-busy="false"] #calendar-board:visible .calendar-day').first().waitFor();
  return data;
}

async function verify(page, origin, width, requestedDate) {
  await page.goto(origin + '/__demo/public?area=hr');
  await page.locator('#hr-section-select').waitFor({ state: 'attached' });
  const link = page.locator('a[data-workspace="calendar"]');
  if (!await link.isVisible()) await page.locator('#shell-toggle').click();
  let data = await readCalendarAfter(page, () => link.click());
  if (!data.events.some(event => event.title === task)) {
    // Demo tasks are due tomorrow, including on the last day of the month.
    data = await readCalendarAfter(page, () => page.locator('#calendar-next').click());
  }
  const due = data.events.find(event => event.title === task);
  assert(due, 'Fictional mobilisation task required in this fixture');
  const date = requestedDate || due.date;
  assert.equal(due.date, date);
  const day = page.locator('.calendar-day[data-calendar-day="' + date + '"]');
  const title = page.locator('#calendar-agenda-title');
  const wholeMonth = page.locator('#calendar-clear-day');
  const vessel = page.locator('[data-page-vessel]');
  const search = page.locator('#calendar-query');
  const tasks = page.locator('[data-cal-kind="tasks"]');
  const aurora = await vessel.locator('option').filter({ hasText: /MV Aurora/ }).first().getAttribute('value');
  await day.click();
  const dateTitle = await title.innerText();
  const trace = {};

  async function checkRows(label, rows, daySelected = true) {
    const actual = await page.locator('#calendar-events article').evaluateAll(articles =>
      articles.map(article => [article.dataset.calAnchor, article.querySelector('time').dateTime.slice(0, 10)]));
    const expected = rows.map(event => ['event:' + event.id, event.date]);
    assert.deepEqual(actual, expected, label);
    assert.equal(await day.getAttribute('aria-pressed'), String(daySelected), label);
    assert.equal(await wholeMonth.isVisible(), daySelected, label);
    assert.equal((await title.innerText()) === dateTitle, daySelected, label);
    const count = (await page.locator('#calendar-result-count').innerText()).match(/\d+/);
    assert.equal(Number(count?.[0]), rows.length, label);
    assert.equal(await page.locator('#calendar-empty').isVisible(), !rows.length, label);
    trace[label] = rows.length;
  }
  const selectedEvents = () => data.events.filter(event => event.date === date);
  await checkRows('all vessels', selectedEvents());
  data = await readCalendarAfter(page, () => vessel.selectOption(aurora));
  const auroraRows = selectedEvents();
  assert(auroraRows.some(event => event.id === due.id));
  await checkRows('Aurora', auroraRows);

  await search.fill('mobilisation');
  await checkRows('search', [due]);
  await page.locator('#calendar-filters > summary').click();
  data = await readCalendarAfter(page, () => tasks.uncheck());
  assert.equal(await search.inputValue(), 'mobilisation');
  await checkRows('tasks off plus search', []);
  await search.fill('');
  await checkRows('tasks off', selectedEvents());

  data = await readCalendarAfter(page, () => tasks.check());
  await checkRows('tasks on', auroraRows);
  data = await readCalendarAfter(page, () => page.locator('#calendar-none').click());
  await checkRows('clear categories', []);
  data = await readCalendarAfter(page, () => page.locator('#calendar-all').click());
  await checkRows('all categories', selectedEvents());
  await search.fill('mobilisation');
  data = await readCalendarAfter(page, () => page.locator('#calendar-reset').click());
  assert.equal(await vessel.inputValue(), '');
  assert.equal(await search.inputValue(), '');
  await checkRows('reset filters', selectedEvents());
  data = await readCalendarAfter(page, () => page.locator('#calendar-refresh').click());
  await checkRows('refresh', selectedEvents());

  // Hold an older Tasks-off GET while a newer Tasks-on read completes.
  // Both use the real local API, and the stale response must leave the day intact.
  let delay, unblock;
  const intercepted = new Promise(resolve => { delay = resolve; });
  const hold = new Promise(resolve => { unblock = resolve; });
  const withoutTasks = request => !(new URL(request.url()).searchParams.get('kinds') || '').split(',').includes('tasks');
  const pattern = '**/api/calendar?*';
  await page.route(pattern, async route => {
    if (withoutTasks(route.request())) { delay(); await hold; }
    await route.continue();
  });
  try {
    await tasks.uncheck();
    await intercepted;
    data = await readCalendarAfter(page, () => tasks.check());
    const older = page.waitForResponse(response => calendarResponse(response) && withoutTasks(response));
    unblock();
    await (await older).finished();
    await page.evaluate(() => new Promise(done => requestAnimationFrame(() => requestAnimationFrame(done))));
    await checkRows('older response last', selectedEvents());
    assert(await tasks.isChecked());
  } finally {
    unblock();
    await page.unroute(pattern);
  }

  // The demo's other due item can fall outside the requested month at month-end.
  const nextDay = new Date(Date.parse(date + 'T12:00:00Z') + 86400000).toISOString().slice(0, 10);
  if (nextDay <= data.end) assert(data.events.some(event => event.date === nextDay), 'Adjacent demo date missing');
  await wholeMonth.click();
  await checkRows('whole month', data.events, false);
  console.log('PASS Operations Calendar', width, date, JSON.stringify(trace));
}

(async () => {
  const origin = new URL(process.argv[2]).origin;
  assert.equal(new URL(origin).hostname, '127.0.0.1');
  const browser = await chromium.launch({ executablePath: process.env.WAVELINK_TEST_CHROMIUM });
  try {
    for (const width of [1360, 389]) {
      const page = await browser.newPage({ viewport: { width, height: 919 }, ignoreHTTPSErrors: true, serviceWorkers: 'block' });
      try {
        await verify(page, origin, width, process.argv[3]);
      } finally {
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
