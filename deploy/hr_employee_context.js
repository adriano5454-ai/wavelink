const employeeRecords=/^#hr\/staff\/([0-9a-f-]{36})\/(documents|assignments|timesheets|expenses)$/;
let employeeReturn=null, returningToEmployee=false;
const employeeMemberships=new WeakMap();
function employeeDepartments(person){
 let memberships=employeeMemberships.get(directory);
 if(!memberships){
   memberships=new Map();
   for(const unit of directory.org_chart?.units||[]){
     if(!unit.name)continue;
     for(const member of [...unit.people,...unit.heads]){
       if(!member.profile_id)continue;
       if(!memberships.has(member.profile_id))memberships.set(member.profile_id,[]);
       memberships.get(member.profile_id).push(unit.name);
     }
   }
   employeeMemberships.set(directory,memberships);
 }
 return memberships.get(person.id)||(workspace?.people?.find(p=>p.id===person.id)?.departments||[]).map(d=>d.name);
}
function bindEmployeePanel(panel){
 bindRecordActions(panel);
 panel.querySelector('[data-hr-cert-create]')?.addEventListener('click',()=>{if(ready())beginForm('documents',null,'save')});
 panel.querySelector('#hr-person-edit')?.addEventListener('click',()=>{if(ready())beginForm('people',overview.people?.[0]||null,'save')});
 panel.querySelectorAll('[data-hr-jump]').forEach((button,index)=>button.onclick=()=>{
   if(!ready()||reading)return;
   employeeReturn={direct:true,id:overview.person.id,hash:location.hash,tab:button.dataset.hrJump,index,search:peopleSearch,
     list:host.querySelector('.hr-person-list').scrollTop,y:window.scrollY,detail:panel.scrollTop};
   query='';page=0;location.hash='#hr/staff/'+overview.person.id+'/'+button.dataset.hrJump;
 });
}
function employeeSectionRoute(tab){
 const route=location.hash.match(employeeRecords);
 if(!route||tab===route[2])return false;
 if(['documents','assignments','timesheets','expenses'].includes(tab)){
   if(employeeReturn)employeeReturn.direct=false;
   query='';page=0;location.hash='#hr/staff/'+route[1]+'/'+tab;return true;
 }
 if(tab==='people'){
   host.querySelector('.hr-employee-context button')?.click();return true;
 }
 // Other HR sections retain their existing employee scope and original URL format.
 lastHash='#hr/staff/'+route[1];history.replaceState(history.state,'',lastHash);
 host.dataset.hrRoute=lastHash;employeeReturn=null;return false;
}
function recordContext(){
 const route=location.hash.match(employeeRecords);
 if(!route||view!==route[2]||overview.person.id!==route[1])return;
 const header=document.createElement('div');header.className='hr-employee-context';
 const name=document.createElement('strong');name.textContent=overview.person.name;
 const back=document.createElement('button');back.type='button';back.className='btn secondary';back.textContent=wtext('Voltar ao perfil','Back to employee profile');
 back.onclick=()=>{if(!ready())return;view='people';
   if(employeeReturn?.direct&&employeeReturn.id===route[1]&&employeeReturn.tab===route[2])history.back();
   else location.hash=employeeReturn?.id===route[1]?employeeReturn.hash:'#hr/staff/'+route[1];
 };
 header.append(name,back);host.querySelector('.hr-tabs').after(header);
}
function restoreEmployee(){
 const r=employeeReturn;
 if(!returningToEmployee||view!=='people'||!r||r.hash!==location.hash||overview.person.id!==r.id)return;
 const panel=host.querySelector('.hr-person-layout > section'),list=host.querySelector('.hr-person-list');
 if(!panel||!list)return;
 returningToEmployee=false;list.scrollTop=r.list;panel.scrollTop=r.detail;
 panel.querySelectorAll('[data-hr-jump]')[r.index]?.focus({preventScroll:true});
 window.scrollTo({top:r.y,behavior:'instant'});
}
function replaceEmployeePanel(layout){
 const temp=document.createElement('div');temp.innerHTML=AJInterface.markup(peopleHtml());
 const oldList=layout.querySelector('.hr-person-list'),nextList=temp.querySelector('.hr-person-list');
 // Rebuild the full view if permissions or the authorized roster changed.
 const signature=list=>Array.from(list.children,li=>[li.dataset.personSearch,li.firstElementChild.dataset.hrPersonLink,li.hidden]);
 if(JSON.stringify(signature(oldList))!==JSON.stringify(signature(nextList)))return false;
 const selected=overview.person.id;
 oldList.querySelectorAll('[data-hr-person-link]').forEach(b=>b.setAttribute('aria-current',String(b.dataset.hrPersonLink===selected)));
 const panel=temp.querySelector('.hr-person-layout > section');
 layout.querySelector(':scope > section').replaceWith(panel);bindEmployeePanel(panel);
 const picker=el('hr-person');picker.innerHTML=employeeOptions();
 status('');return true;
}
