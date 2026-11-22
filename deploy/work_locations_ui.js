/* Shared controls for fleet locations. Each open form reads its current project. */
(() => {
 'use strict';
 const words = (pt, en) => window.WavelinkUX?.text(pt, en) || (document.documentElement.lang.startsWith('pt') ? pt : en);
 const label = () => words('Embarcação ou base', 'Ship or base');
 const choose = () => words('Selecione uma localização', 'Choose a location');
 const types = {vessel:['Embarcação','Vessel'],shore_base:['Base','Shore base'],warehouse:['Armazém','Warehouse'],workshop:['Oficina','Workshop']};
 const describe = site => [site.name,site.code,types[site.kind] && words(...types[site.kind])].filter(Boolean).join(' · ');
 const active = sites => sites.filter(site => site.active);
 function options(sites, current='') {
  return sites.filter(site => site.active || site.id === current).map(site => [site.id,describe(site)]);
 }
 function picker(host, api, {value='', initialName='', byName=false, required=true, legacy=false, onPick, all=false}={}) {
  const select=document.createElement('select'), title=document.createElement('span'), box=document.createElement('label');
  box.className='field wl-work-site';title.textContent=label();if(!byName)select.name='work_site_id';
  const message=document.createElement('small');message.setAttribute('role','status');
  const retry=document.createElement('button');retry.type='button';retry.className='btn secondary';
  retry.textContent=words('Tentar novamente','Retry');retry.hidden=true;
  box.append(title,select,message,retry);host.append(box);
  let sites=[], loaded=false, epoch=0;
  async function load(){
   const call=++epoch;loaded=false;select.disabled=true;retry.hidden=true;
   message.textContent=words('Carregando localizações…','Loading locations…');
   try{
    const data=await api('/api/fleet/work-locations');
    if(call!==epoch||!box.isConnected)return;
    if(!Array.isArray(data?.sites))throw Error(words('Lista indisponível.','Locations unavailable.'));
    sites=data.sites;
    const available=all?sites:sites.filter(site=>site.active || legacy && (site.id===value || byName && site.name===initialName));
    const initial=available.find(site=>site.id===value) || (initialName&&available.find(site=>site.name===initialName));
    select.replaceChildren(new Option(all?words('Todas as localizações','All locations'):choose(),''));
    for(const site of available) select.add(new Option(describe(site),site.id));
    if(byName && legacy && initialName && !initial)select.add(new Option(initialName,'__historical__'));
    select.value=initial?.id || (byName && legacy && initialName?'__historical__':'');
    select.disabled=!available.length;select.required=required&&!!available.length;
    loaded=true;message.textContent=available.length?'':words('Nenhuma embarcação ou base cadastrada.','No ships or bases have been added.');
    if(initial)onPick?.(initial);
   }catch(error){
    if(call!==epoch||!box.isConnected)return;
    message.textContent=error.message||words('Não foi possível carregar as localizações.','Could not load locations.');retry.hidden=false;
   }
  }
  select.onchange=()=>{value=select.value;const site=sites.find(s=>s.id===value);onPick?.(site || (value==='__historical__'?{name:initialName}:null));};
  retry.onclick=load;load();
  return {box,select,read(){
   if(!loaded)throw Error(words('Carregue a lista de localizações antes de salvar.','Load the location list before saving.'));
   if(select.required&&!select.value){select.focus();throw Error(choose());}
   return select.value;
  }};
 }
 function nameField(input, api, legacy=false, value=''){
  if(!input||input.readOnly||input.disabled)return;
  const wrap=input.closest('label');if(!wrap)return;
  const host=document.createElement('div');wrap.after(host);
  const current=input.value;
  const control=picker(host,api,{byName:true,initialName:current,legacy,value,onPick:site=>{
   if(input.value===(site?.name||''))return;input.value=site?.name||'';input.dispatchEvent(new Event('input',{bubbles:true}));
  }});
  // Existing workflows store a printable location. A project with no sites can still use its original field.
  const sync=()=>{const hasChoices=control.select.options.length>1;
   wrap.classList.toggle('wl-original-site-field',hasChoices);wrap.hidden=hasChoices;if(hasChoices&&!control.select.value && !legacy)input.value='';
  };
  new MutationObserver(sync).observe(control.select,{childList:true,attributes:true,attributeFilter:['disabled']});
  return control;
 }
 function fw(f,kind,context,restore,api){
  const uses=['General task','Verification task','Maintenance work order','Asset maintenance order','Toolbox talk','Certificate draft','Inventory item','Stocktake'];
  if(!uses.includes(kind))return null;
  const original=context.record || context.item || context.certificate || context.corrective_fault || {};
  const host=document.createElement('div');f.querySelector('#fw-local-state').after(host);
  const siteInput=kind==='Toolbox talk'? f.elements.site:null;
  const control=picker(host,api,{value:restore?.values?.work_site_id || original.work_site?.id || '',
   initialName:siteInput?.value||'',legacy:!!(context.record||context.item||context.certificate),
   onPick:site=>{if(siteInput&&site){siteInput.value=site.name;siteInput.dispatchEvent(new Event('input',{bubbles:true}));}}});
  if(siteInput){
   const sync=()=>{if(control.select.options.length>1){siteInput.required=false;siteInput.closest('label').classList.add('wl-original-site-field');siteInput.closest('label').hidden=true;}};
   new MutationObserver(sync).observe(control.select,{childList:true});
  }
  return control;
 }
 function body(control){
  if(!control)return {};
  const id=control.read();
  return id==='__historical__'||!id&&!control.select.required?{}:{work_site_id:id};
 }
 window.WLWorkSites=Object.freeze({body,words,label,choose,describe,options,active,picker,nameField,fw});
})();
