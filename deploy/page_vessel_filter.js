/* Register filters use the Fleet sites visible to the signed-in user. */
(() => {
 'use strict';
 const controls = new WeakMap();
 const indexes = new WeakMap();
 const pending = new WeakMap();
 const words = (pt,en) => window.WavelinkUX?.text(pt,en) ||
  (document.documentElement.lang.toLowerCase().startsWith('pt') ? pt : en);
 const fold = value => String(value || '').normalize('NFKD').replace(/\p{M}/gu,'')
  .toLowerCase().trim().replace(/\s+/gu,' ');
 const escape = value => String(value).replace(/[&<>"']/g, c =>
  ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const label = includeBases => includeBases ? words('Embarcação ou base','Vessel or base') : words('Embarcação','Vessel');
 const all = includeBases => includeBases ? words('Todas as localizações','All locations') : words('Todas as embarcações','All vessels');

 function field(value='',{includeBases=false}={}) {
  const loading = value ? `<option value="${escape(value)}" selected>${words('Carregando…','Loading…')}</option>` : '';
  return `<div class="wl-page-vessel"><label><span>${label(includeBases)}</span><select name="page_vessel" data-page-vessel disabled><option value="">${all(includeBases)}</option>${loading}</select></label><span class="wl-page-vessel-status" role="status" hidden></span><button type="button" class="btn secondary wl-page-vessel-retry" hidden>${words('Tentar novamente','Retry')}</button></div>`;
 }

 function catalogue(api) {
  const owner = window.AJInventoryWorkspace?.key?.();
  const current = pending.get(api);
  if (owner && current?.owner === owner) return current.promise;
  const promise = Promise.resolve().then(() => api('/api/fleet/work-locations')).then(data => {
   if (!Array.isArray(data?.sites)) throw Error('Invalid Fleet directory');
   return data.sites;
  });
  if (owner) {
   pending.set(api,{owner,promise});
   const release = () => { if (pending.get(api)?.promise === promise) pending.delete(api); };
   promise.then(release,release);
  }
  return promise;
 }

 async function bind(select,{api,sites,value='',onChange,includeBases=false}={}) {
  if (!select) return false;
  const state = {sites:[]};
  controls.set(select,state);
  const box = select.closest('.wl-page-vessel');
  const status = box?.querySelector('.wl-page-vessel-status');
  const retry = box?.querySelector('.wl-page-vessel-retry');
  const current = () => select.isConnected && controls.get(select) === state;
  select.disabled = true;
  select.onchange = () => { if (current()) onChange?.(select.value); };
  try {
   const items = sites ?? await catalogue(api);
   if (!current()) return false;
   if (!Array.isArray(items)) throw Error('Invalid Fleet directory');
   state.sites = items;
   const options = [new Option(all(includeBases),'')];
   for (const site of items.filter(site => site.kind === 'vessel' || (includeBases && site.kind === 'shore_base'))) {
    const text = [site.name, site.code, site.active === false ? words('Inativa','Inactive') : ''].filter(Boolean).join(' · ');
    options.push(new Option(text,site.id));
   }
   select.replaceChildren(...options);
   select.value = options.some(option => option.value === value) ? value : '';
   select.disabled = options.length === 1;
   if (status) {
    status.textContent = select.disabled ? (includeBases ? words('Nenhuma embarcação ou base disponível.','No vessels or bases available.') : words('Nenhuma embarcação disponível.','No vessels available.')) : '';
    status.hidden = !select.disabled;
   }
   if (retry) retry.hidden = true;
   if (value && !select.value) onChange?.('');
   return true;
  } catch {
   if (!current()) return false;
   if (status) {
    status.textContent = includeBases ? words('Não foi possível carregar as localizações.','Could not load locations.') : words('Não foi possível carregar as embarcações.','Could not load vessels.');
    status.hidden = false;
   }
   if (retry) {
    retry.hidden = false;
    retry.onclick = () => bind(select,{api,sites,value,onChange,includeBases});
   }
   return false;
  }
 }

 function aliasIndex(sites) {
  if (indexes.has(sites)) return indexes.get(sites);
  const result = new Map();
  for (const site of sites) {
   for (const alias of [site.name,site.code].map(fold).filter(Boolean)) {
    if (result.has(alias) && result.get(alias) !== site.id) result.set(alias,null);
    else result.set(alias,site.id);
   }
  }
  indexes.set(sites,result);
  return result;
 }

 function matches(record,id,selectOrSites) {
  if (!id) return true;
  if (!record) return false;
  const saved = record.work_site?.id || record.meta?.work_site?.id || record.vessel_scope?.site_id ||
   record.work_site_id || record.site_id || record.vessel_id || record.equipment_work_site?.id;
  if (saved) return saved === id;
  const sites = Array.isArray(selectOrSites) ? selectOrSites : controls.get(selectOrSites)?.sites;
  if (!sites?.length) return false;
  const aliases = aliasIndex(sites);
  return [record.meta?.vessel,record.meta?.site,record.location,record.daily?.location,record.edit?.location]
   .some(value => typeof value === 'string' && aliases.get(fold(value)) === id);
 }
 window.WLPageVessels = Object.freeze({field,bind,matches});
})();
