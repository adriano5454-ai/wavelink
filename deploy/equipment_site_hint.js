 const equipmentControls=new WeakMap();

 function prepareEquipmentSite(select,{selected='',hint='',onUpdate}={}){
  if(!select || equipmentControls.has(select))return;
  const notice=document.createElement('small');
  notice.setAttribute('role','status');
  notice.className='small muted';
  notice.hidden=true;
  select.closest('label').append(notice);
  const state={manual:!!selected&&!hint,inferred:hint,links:null,notice,onUpdate};
  equipmentControls.set(select,state);
  select.addEventListener('change',()=>{
   state.manual=!!select.value;
   state.inferred='';
   refreshEquipmentSite(select);
   onUpdate?.();
  });
 }

 function refreshEquipmentSite(select){
  const state=equipmentControls.get(select);
  if(!state || !state.links || !select.options.length)return;
  const links=state.links;
  const first=links[0];
  const single=first?.active && links.every(site=>site?.active && site.id===first.id);
  const match=single && [...select.options].some(option=>option.value===first.id);
  let message='';
  if(!state.manual){
   const value=match?first.id:'';
   const changed=select.value!==value || state.inferred!==value;
   select.value=value;
   state.inferred=value;
   if(changed)state.onUpdate?.();
   if(match)message=words('Localização preenchida pelo vínculo.','Location filled from the linked record.');
   else if(links.length)message=words('O vínculo não indica uma única localização ativa. Selecione a embarcação ou base.','The linked records do not identify one current location. Choose the ship or base.');
  }else if(match && select.value!==first.id){
   message=words('Localização do vínculo: ','Linked location: ')+first.name+'.';
  }
  if(state.notice.textContent!==message)state.notice.textContent=message;
  state.notice.hidden=!message;
 }

 function equipmentSites(select,sites){
  if(!select)return;
  prepareEquipmentSite(select,{selected:select.value});
  equipmentControls.get(select).links=sites;
  refreshEquipmentSite(select);
 }

 function equipmentHint(select){
  const state=equipmentControls.get(select);
  return state && !state.manual && state.inferred===select.value ? state.inferred : '';
 }

 function equipmentBody(select,id){
  const hint=equipmentHint(select);
  return hint?{equipment_site_hint:hint}:{work_site_id:id};
 }
