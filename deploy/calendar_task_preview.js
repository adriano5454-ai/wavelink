 let preview=null,origin=null,positionedRoute='';
 window.addEventListener('hashchange',()=>{if(location.hash==='#calendar')positionedRoute='';else if(preview){preview.remove();preview=null;}});
 function anchor(){
  if(!origin||origin.owner!==account()||origin.token!==token()||origin.key!==key())return null;
  const container=node?.querySelector(origin.agenda?'#calendar-events':'#calendar-grid');
  return [...container?.querySelectorAll('[data-calendar-source]')||[]].find(a=>a.dataset.calendarSource===origin.id);
 }
 function focusEvent(){
  const a=anchor();if(!a||!here())return;
  a.focus({preventScroll:true});window.scrollBy({top:a.getBoundingClientRect().top-origin.top,behavior:'instant'});
 }
 function showTask(e,target,forward=false){
  if(!snapshot||blocked||stale||busyPage())return;
  if(!forward){
   origin={owner:account(),token:token(),key:key(),id:e.id,route:href(e),agenda:!!target.closest('#calendar-events'),top:target.getBoundingClientRect().top,marker:crypto.randomUUID()};
   history.replaceState({...history.state,calTaskOrigin:origin.marker},'');
   history.pushState({...history.state,calTaskPreview:origin.marker},'',location.href);
  }
  const d=document.createElement('dialog');preview=d;d.className='cal-task-preview';d.setAttribute('aria-labelledby','cal-preview-title');
  const h=document.createElement('h2');h.id='cal-preview-title';h.textContent=e.title;
  const p=document.createElement('p');p.textContent=[detailLabel(e),dateLabel(e.date),e.all_day?__wl118.t('Date only'):e.when.slice(11,16)+' UTC',pretty(e.status)].join(' · ');
  const close=document.createElement('button');close.className='btn secondary';close.textContent=__wl118.t('Close');close.type='button';close.onclick=()=>history.back();
  const open=document.createElement('a');open.className='btn';open.href=href(e);open.textContent=window.WavelinkUX.text('Abrir tarefa completa','Open full task');
  open.onclick=ev=>{if(ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey)return;ev.preventDefault();
   if(!here()||!anchor()||!snapshot?.events.includes(e)||blocked||stale)return;
   d.close();d.remove();preview=null;location.replace(open.href);
  };
  d.addEventListener('cancel',ev=>{ev.preventDefault();close.click()});
  d.append(h,p,close,open);node.append(d);d.showModal();close.focus({preventScroll:true});
 }
 window.addEventListener('popstate',()=>{
  if(preview){preview.close();preview.remove();preview=null;if(here())requestAnimationFrame(focusEvent);return;}
  const a=anchor();if(here()&&a&&origin.marker===history.state?.calTaskPreview){
   const e=snapshot?.events.find(row=>row.id===origin.id);if(e)showTask(e,a,true);
  }
 });
 function taskTitle(id,heading){
  if(!heading||positionedRoute===location.hash||origin?.route!==location.hash||origin.route!=='#tasks/'+id||origin.owner!==account()||origin.token!==token())return;
  positionedRoute=location.hash;heading.tabIndex=-1;heading.style.scrollMarginTop='76px';heading.focus({preventScroll:true});heading.scrollIntoView({block:'start',behavior:'instant'});
 }
