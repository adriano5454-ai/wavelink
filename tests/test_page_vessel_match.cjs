const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { join } = require('node:path');
const { runInNewContext } = require('node:vm');

const window = {};
const document = { documentElement: { lang: 'en' } };
class Option {
  constructor(text, value) { this.text = text; this.value = value; }
}
runInNewContext(readFileSync(join(__dirname, '../deploy/page_vessel_filter.js'), 'utf8'), { window, document, Option });
const { matches, field, bind } = window.WLPageVessels;
const sites = [
  { id: 'a', kind: 'vessel', name: 'São Miguel', code: 'SHARED' },
  { id: 'b', kind: 'vessel', name: 'Aurora', code: 'B-01' },
  { id: 'c', kind: 'shore_base', name: 'Shore base', code: 'SHARED' },
];

assert.equal(matches({ location: 'SAO MIGUEL' }, 'a', sites), true);
assert.equal(matches({ meta: { vessel: 'b-01' } }, 'b', sites), true);
assert.equal(matches({ location: 'shared' }, 'a', sites), false);
assert.equal(matches({}, '', sites), true);
assert.equal(matches({}, 'a', sites), false);

const record = { work_site: { id: 'b' }, equipment_work_site: { id: 'a' }, location: 'São Miguel' };
assert.equal(matches(record, 'a', sites), false);
assert.equal(matches(record, 'b', sites), true);
assert.equal(matches({ equipment_work_site: { id: 'a' } }, 'a', sites), true);
async function checkDirectory() {
  const select = { isConnected: true, closest: () => null, replaceChildren(...options) { this.options = options; } };
  assert.match(field('', { includeBases: true }), /Vessel or base/);
  await bind(select, { sites, includeBases: true, value: 'c' });
  assert.deepEqual(select.options.map(option => option.value), ['', 'a', 'b', 'c']);
  assert.equal(select.value, 'c');
  assert.equal(select.options[0].text, 'All locations');
  await bind(select, { sites });
  assert.deepEqual(select.options.map(option => option.value), ['', 'a', 'b']);
  document.documentElement.lang = 'pt-BR';
  assert.match(field('', { includeBases: true }), /Embarcação ou base/);
}
checkDirectory().then(() => console.log('Location matching, Fleet ship/base options and translations passed.'));
