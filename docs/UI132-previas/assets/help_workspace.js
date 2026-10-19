/* UI118 localized source */

var __wl118=window.WavelinkI18n||{t:s=>s,markup:s=>s,html:(s,...v)=>s.reduce((a,p,i)=>a+p+(i<v.length?String(v[i]):''),''),template:(s,...v)=>s.reduce((a,p,i)=>a+p+(i<v.length?String(v[i]):''),'')};
/* UI07: public Help navigation only. No auth, database, operational writes or local storage. */
(() => {
  'use strict';
  const query = document.getElementById('help-query');
  const area = document.getElementById('help-group');
  const status = document.getElementById('help-search-status');
  const clear = document.getElementById('help-clear');
  const retry = document.getElementById('help-retry');
  const browser = document.getElementById('help-browser');
  if (!query || !area || !status || !browser) return;
  document.documentElement.classList.add('help-js');
  const rows = [...document.querySelectorAll('[data-topic-row]')];
  const groups = [...document.querySelectorAll('.help-nav-group')];
  const originalOpen = new Map(groups.map(el => [el, el.open]));
  const current = document.body.dataset.helpTopic || '';
  const normal = value => String(value || '').normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const cards = [...document.querySelectorAll('[data-index-topic]')];
  const indexGroups = [...document.querySelectorAll('[data-index-group]')];
  const print = document.getElementById('help-print');
  let catalogue = null, pending = null, failed = false;
  let controller = new AbortController();
  const mobile = window.matchMedia('(max-width:760px)');
  browser.open = !mobile.matches;
  mobile.addEventListener('change', () => { browser.open = !mobile.matches; });
  if (print) { print.hidden = false; print.addEventListener('click', () => window.print()); }

  function snippet(text, words) {
    const source = String(text || '');
    const norm = normal(source);
    let at = words.length ? norm.indexOf(words[0]) : -1;
    at = Math.max(0, at - 35);
    return (at ? '…' : '') + source.slice(at, at + 170).trim() + (source.length > at + 170 ? '…' : '');
  }
  function update() {
    const words = normal(query.value.trim()).split(/\s+/).filter(Boolean);
    const selectedArea = area.value;
    clear.hidden = !words.length && !selectedArea;
    retry.hidden = !failed || !words.length;
    const visible = new Set();
    for (const row of rows) {
      const id = row.dataset.topicRow;
      const group = row.closest('[data-group]');
      const source = catalogue && catalogue.get(id);
      const span = row.querySelector('a > span');
      const base = (span ? span.textContent : '') + ' ' + group.querySelector('summary').textContent;
      const haystack = normal(source ? base + ' ' + source.heading + ' ' + source.text : base);
      const show = (!selectedArea || group.dataset.group === selectedArea) && words.every(word => haystack.includes(word));
      row.hidden = !show;
      const detail = row.querySelector('.help-match');
      detail.hidden = !show || !words.length || !source;
      detail.textContent = show && words.length && source ? snippet(source.text, words) : '';
      if (show) visible.add(id);
    }
    for (const group of groups) {
      const count = [...group.querySelectorAll('[data-topic-row]')].filter(el => !el.hidden).length;
      group.hidden = !count;
      group.querySelector('.help-count').textContent = String(count);
      if (words.length || selectedArea) group.open = count > 0;
      else group.open = originalOpen.get(group);
    }
    for (const card of cards) card.closest('li').hidden = !visible.has(card.dataset.indexTopic);
    for (const group of indexGroups) group.hidden = ![...group.querySelectorAll('[data-index-topic]')].some(a => visible.has(a.dataset.indexTopic));
    const noResults = document.getElementById('help-no-results');
    noResults.hidden = visible.size > 0;
    let text = __wl118.template`${visible.size} of ${rows.length} topics`;
    if (words.length) text += catalogue ? __wl118.t(' · matching guide wording') : failed ? __wl118.t(' · titles only; full-text search unavailable') : __wl118.t(' · checking full guide wording…');
    else text += __wl118.t(' · choose an area or search');
    status.textContent = text;
    const note = document.getElementById('help-index-note');
    if (note) note.textContent = visible.size ? text : __wl118.t('No matching topics. Clear the search or choose another area.');
  }
  async function loadCatalogue() {
    if (catalogue || pending) return pending;
    if (controller.signal.aborted) controller = new AbortController();
    failed = false;
    pending = (async () => {
      try {
        const response = await fetch(window.WavelinkI18n?.locale==='pt-BR'?'/static/pt-BR/help_catalogue.json?v=1.34.19-ui118':'/static/help_catalogue.json?v=1.34.32-c02b893f7650', {credentials:'same-origin', cache:'no-store', signal:controller.signal});
        if (!response.ok) throw new Error('Help catalogue not available');
        const data = await response.json();
        const allowed = new Set(rows.map(el => el.dataset.topicRow));
        if (!data || data.format !== 'wavelink-help-catalogue-1' || !Array.isArray(data.topics) || data.topics.length !== allowed.size) throw new Error('Unexpected help catalogue');
        const loaded = new Map();
        for (const topic of data.topics) {
          if (!topic || !allowed.has(topic.id) || loaded.has(topic.id) || typeof topic.text !== 'string' || topic.text.length > 250000 || typeof topic.heading !== 'string') throw new Error('Invalid help catalogue entry');
          loaded.set(topic.id, topic);
        }
        catalogue = loaded;
      } catch (error) {
        if (error.name !== 'AbortError') failed = true;
      } finally { pending = null; update(); }
    })();
    return pending;
  }
  query.addEventListener('input', () => { update(); if (query.value.trim()) loadCatalogue(); });
  area.addEventListener('change', update);
  clear.addEventListener('click', () => { query.value = ''; area.value = ''; update(); query.focus(); });
  retry.addEventListener('click', () => { loadCatalogue(); update(); });
  for (const group of groups) group.addEventListener('toggle', () => {
    if (!query.value.trim() && !area.value) originalOpen.set(group, group.open);
  });
  window.addEventListener('pagehide', () => controller.abort());
  // Preserve old /help#topic bookmarks. Unknown fragments are never used as URLs.
  if (!current && location.hash) {
    let fragment = '';
    try { fragment = decodeURIComponent(location.hash.slice(1)); } catch (_) { /* invalid bookmark */ }
    if (rows.some(row => row.dataset.topicRow === fragment)) location.replace('/help/topics/' + encodeURIComponent(fragment));
    else if (fragment === 'task-details') location.replace('/static/help_reference.html#task-details');
  }
  update();
})();
