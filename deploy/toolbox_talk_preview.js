function mountTalkPreview(data, filteredTalks, words){
 const list=document.getElementById('tb-results'), layout=document.createElement('div');
 layout.className='tb-preview-layout';list.before(layout);layout.append(list);
 const mobile=matchMedia('(max-width:800px)'),owner=AJToolboxUI.key(), token=state.auth?.token;
 let panel=null,activeId=null,top=0;
 const visible=()=>layout.isConnected&&location.hash==='#toolbox'&&owner===AJToolboxUI.key()&&token===state.auth?.token&&permission('toolbox.view')&&!root.querySelector('.tb-stale');
 const link=id=>[...list.querySelectorAll('[data-toolbox-id]')].find(a=>a.dataset.toolboxId===id);
 const dismiss=(restore=false)=>{
  const row=link(activeId);row?.removeAttribute('aria-current');panel?.remove();panel=null;layout.classList.remove('tb-preview-active');
  if(restore&&visible()&&row){row.focus({preventScroll:true});window.scrollBy({top:row.getBoundingClientRect().top-top,behavior:'instant'});}
  activeId=null;
 };
 function show(id,action){
  const row=link(id),r=filteredTalks().find(item=>item.id===id);
  if(!visible()||!row||!r)return;
  const first=!panel,same=id===activeId,offset=same?top:row.getBoundingClientRect().top;
  dismiss();activeId=id;top=offset;
  if(action){const entry={...window.history.state,tbPreview:{id,scope:previewScope}};
   if(first&&!window.history.state?.tbPreview)window.history.pushState(entry,'',location.href);else window.history.replaceState(entry,'',location.href);}
  row.setAttribute('aria-current','true');layout.classList.add('tb-preview-active');
  panel=document.createElement(mobile.matches?'dialog':'section');panel.className='tb-talk-preview card';panel.setAttribute('aria-labelledby','tb-preview-title');layout.append(panel);
  const text=(tag,value)=>{const node=document.createElement(tag);node.textContent=value;panel.append(node);return node;};
  const title=text('h2',r.meta.work_description);title.id='tb-preview-title';title.tabIndex=-1;
  const close=text('button',words('Close','Fechar'));close.type='button';close.className='btn secondary';close.onclick=()=>window.history.back();
  const facts=document.createElement('dl');facts.className='fw-details';panel.append(facts);
  function fact(label,value){if(!value)return;const k=document.createElement('dt'),v=document.createElement('dd');k.textContent=label;v.textContent=value;facts.append(k,v);}
  fact(words('Status','Status'),__wl118.status(r.status));fact(words('Briefing form','Formulário da reunião'),r.template?.definition?.name);fact(words('Form reference','Referência do formulário'),r.template?.definition?.code);
  fact(words('Vessel or site','Embarcação ou local'),r.work_site?.name||r.meta.site);fact(words('Project','Projeto'),r.meta.project_number);
  fact(words('Briefing date','Data da reunião'),r.meta.event_utc);fact(words('JSA reference','Referência da análise de risco'),r.meta.jsa);
  const controls=(r.template?.definition?.prompts||[]).filter(prompt=>r.discussed?.[prompt.id]&&prompt.text);
  if(controls.length){text('h3',words('Items discussed','Itens discutidos'));const ul=document.createElement('ul');panel.append(ul);for(const prompt of controls){const li=document.createElement('li');li.textContent=prompt.text;ul.append(li);}}
  if(r.attendees&&r.acknowledgements)text('p',words('Acknowledged','Ciência registrada')+': '+Object.keys(r.acknowledgements).length+'/'+r.attendees.length+' · '+words('Guests','Visitantes')+': '+Object.keys(r.guest_acknowledgements||{}).length+'/'+(r.guests||[]).length);
  const full=text('a',words('Open full toolbox talk','Abrir diálogo de segurança completo'));full.className='btn';full.href=row.href;
  full.onclick=e=>{if(e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;e.preventDefault();if(!visible()||!link(id))return;talkOrigin={id,top,atList:true};dismiss();location.replace(full.href);};
  if(mobile.matches){panel.addEventListener('cancel',e=>{e.preventDefault();window.history.back()});panel.showModal();}
  title.focus({preventScroll:true});
  if(!mobile.matches){const bounds=title.getBoundingClientRect();if(bounds.top<64||bounds.bottom>innerHeight)title.scrollIntoView({block:'center',behavior:'instant'});}
 }
 function sync(){if(!visible()){dismiss();return}const entry=window.history.state?.tbPreview;if(entry?.scope===previewScope&&link(entry.id))show(entry.id,false);else dismiss(true);}
 list.addEventListener('click',e=>{const a=e.target.closest('a[data-toolbox-id][href]');if(!a||e.defaultPrevented||e.button||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey||!visible())return;e.preventDefault();show(a.dataset.toolboxId,true);});
 toolboxPreviewEvents?.abort();toolboxPreviewEvents=new AbortController();const opts={signal:toolboxPreviewEvents.signal};
 window.addEventListener('popstate',sync,opts);mobile.addEventListener('change',()=>{if(activeId)show(activeId,false)},opts);
 window.addEventListener('keydown',e=>{if(visible()&&panel&&e.key==='Escape'&&!mobile.matches){e.preventDefault();window.history.back();}},opts);
 sync();
 return ()=>{if(activeId&&!link(activeId)){dismiss();if(window.history.state?.tbPreview?.scope===previewScope)window.history.back();}};
}
