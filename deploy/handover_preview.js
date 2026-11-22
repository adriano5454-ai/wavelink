/* Read one authorised handover beside its saved card. */
window.WLHandoverPreview = (() => {
 'use strict';
 const label=(en,pt)=>window.WavelinkI18n?.locale==='pt-BR'?pt:en;
 const previewLabel=()=>label('Preview handover','Prévia da passagem');
 const element=(tag,value,cls)=>{
  const node=document.createElement(tag);
  if(value)node.textContent=value;
  if(cls)node.className=cls;
  return node;
 };
 function mount({api,active,sections,onRead,onEdit}){
  let current=null;
  function close(restore=false){
   if(!current)return;
   const {trigger,list,layout,panel,observer,files,card}=current;
   current=null;observer.disconnect();files?.dispose();
   trigger.setAttribute('aria-expanded','false');trigger.removeAttribute('aria-controls');
   card.classList.remove('hop-selected');
   if(list.parentElement===layout&&layout.isConnected)layout.replaceWith(list);
   panel.remove();
   if(restore&&trigger.isConnected){trigger.focus({preventScroll:true});trigger.scrollIntoView({block:'nearest'});}
  }
  async function open(trigger,id,revision){
   if(!active()||!trigger?.isConnected||trigger.disabled||trigger.closest('[hidden],[inert]'))return;
   const list=trigger.closest('#hwd-days,.ho-cards,.ho-resume-list,.ho-day-timeline,#sh-saved-notes,#sh-cards,.shw-personal');
   const card=trigger.closest('article,.shw-personal');
   if(!list||!card)return;
   close();
   const layout=element('div','','hop-layout'),panel=element('aside','','hop-panel card');
   panel.id='ho-record-preview';panel.tabIndex=-1;
   panel.setAttribute('aria-label',previewLabel());
   const back=element('button',label('Back to handovers','Voltar às passagens'),'btn secondary');
   back.type='button';back.onclick=()=>close(true);
   const head=element('header','','hop-head'),body=element('div','','hop-body');
   head.append(element('strong',previewLabel()),back);panel.append(head,body);
   list.before(layout);layout.append(list,panel);
   const observer=new MutationObserver(()=>{
    if(current?.panel===panel&&(!trigger.isConnected||!layout.isConnected||trigger.closest('[hidden],[inert],details:not([open])')))close();
   });
   observer.observe(layout.closest('#ho-library'),{childList:true,subtree:true,attributes:true,attributeFilter:['open','hidden','inert']});
   const view=current={trigger,list,layout,panel,observer,card,files:null};
   const valid=()=>current===view&&trigger.isConnected&&panel.isConnected&&active();
   trigger.setAttribute('aria-expanded','true');trigger.setAttribute('aria-controls',panel.id);
   card.classList.add('hop-selected');
   body.setAttribute('role','status');body.textContent=label('Loading handover…','Carregando passagem…');
   panel.onkeydown=e=>{if(e.key==='Escape'){e.preventDefault();close(true);}};
   panel.focus({preventScroll:true});panel.scrollIntoView({block:'nearest'});
   try{
    const url='/api/handovers/'+encodeURIComponent(id)+'/preview'+(revision?'?revision='+encodeURIComponent(revision):'');
    const data=await api(url);
    if(!valid())return;
    if(data.id!==id||data.revision!==revision||!data.edit||!Array.isArray(data.files))throw Error();
    const edit=data.edit;
    body.replaceChildren();body.removeAttribute('role');
    const status=revision?label('Published revision ','Revisão publicada ')+revision:label('Private draft','Rascunho privado');
    body.append(element('span',status+(data.archived?label(' · Archived',' · Arquivada'):''),'hwd-state'),element('h2',edit.title));
    const loc=edit.location||label('Location unassigned','Local não atribuído');
    body.append(element('p',[data.author,loc].filter(Boolean).join(' · '),'hop-context'));
    const dates=[edit.period_start,edit.period_end].filter(Boolean).map(stamp=>{
     const date=stamp.slice(0,10),day=window.WavelinkUX?.date?.(date)||date;
     return day+' '+stamp.slice(11);
    });
    if(dates.length)body.append(element('p',[dates.join(' – '),edit.time_basis].filter(Boolean).join(' · '),'small muted'));
    const actions=element('div','','actions hop-actions');
    function action(caption,run,primary=false){
     const b=element('button',caption,primary?'btn':'btn secondary');b.type='button';
     b.onclick=()=>{if(valid()){close();run();}};actions.append(b);
    }
    action(label('Open full handover','Abrir passagem completa'),()=>onRead(id,revision),!data.can_edit);
    if(data.can_edit)action(label('Edit my notes','Editar minhas notas'),()=>onEdit({id}),true);
    body.append(actions);
    let filled=0;
    for(const [key,caption] of sections()){
     if(!edit[key]?.trim())continue;
     const section=element('section','','hop-note');
     section.append(element('h3',caption),element('p',edit[key]));body.append(section);filled++;
    }
    if(!filled)body.append(element('p',label('No shift notes recorded.','Nenhuma nota de turno registrada.'),'muted'));
    const evidence=element('details','','hop-evidence');
    const evidenceTitle=label('Photos and documents','Fotos e documentos');
    evidence.append(element('summary',evidenceTitle+' ('+data.files.length+')'));
    if(data.files.length){
     const host=element('div');evidence.append(host);
     evidence.ontoggle=()=>{
      if(evidence.open&&valid()&&!view.files){
       view.files=AJHandoverAttachments.mountRead({host,api,id,revision,draft:revision===null,references:data.files,isOwned:valid,isActive:valid});
      }
     };
    }else evidence.append(element('p',label('No files attached.','Nenhum arquivo anexado.'),'small muted'));
    body.append(evidence);
   }catch(error){
    if(current===view&&panel.isConnected){
     body.setAttribute('role','status');body.textContent=label('This handover is unavailable. Refresh the list to check your access and the saved revision.','Esta passagem está indisponível. Atualize a lista para verificar seu acesso e a revisão salva.');
    }
   }
  }
  return {open,close};
 }
 return {mount,label:previewLabel};
})();
