/* Read-only: all titles, dates and links come from the authorised source snapshot. */
window.AJReadiness=(()=>{
 const permissions=['certificates.view','maintenance.view','hr.view_own','qshe.view'];
 const T=(en,pt)=>window.WavelinkI18n?.locale==='pt-BR'?pt:en;
 const categories={certificates:['Equipment certificates','Certificados de equipamentos'],maintenance:['Maintenance','Manutenção'],crew:['Crew documents','Documentos da equipe'],qshe:['HSE / QSHE','HSE / QSHE']};
 const levels={urgent:['Urgent','Urgente'],review:['Needs review','Revisar'],upcoming:['Due soon','A vencer']};
 const reasons={certificate_expired:['Certificate expired','Certificado vencido'],certificate_due:['Within saved reminder window','Dentro do prazo de alerta'],certificate_not_yet_valid:['Certificate validity has not started','Validade do certificado ainda não iniciada'],certificate_unknown:['Expiry date not recorded','Validade não informada'],maintenance_follow_up:['Follow-up needs review','Acompanhamento precisa de revisão'],maintenance_undated:['Open work order without a due date','Ordem aberta sem prazo'],maintenance_overdue:['Work order overdue','Ordem de serviço atrasada'],maintenance_due:['Work order due within 7 days','Ordem vence em até 7 dias'],crew_expired:['Recorded document expired','Documento registrado vencido'],crew_due:['Within saved reminder window','Dentro do prazo de alerta'],crew_unknown:['Expiry date not recorded','Validade não informada'],qshe_critical:['Open report marked critical','Relato aberto marcado como crítico'],qshe_overdue:['Follow-up or review date passed','Prazo de ação ou revisão vencido'],qshe_open:['Open safety or quality report','Relato de segurança ou qualidade aberto']};
 const el=(tag,label,cls)=>{const n=document.createElement(tag);if(label!==undefined)n.textContent=label;if(cls)n.className=cls;return n;};
 const link=(name,href)=>{const a=el('a',name,'btn secondary');a.href=href;return a;};
 let host,key,load;
 function allowed(can,person){return !!person?.user_id&&person.fleet_mode!=='vessel_only'&&permissions.some(can);}
 function open({root,can,person,api,session,hub}){
  const own=session(),user=person(),canOpen=()=>allowed(can,person());
  if(host?.isConnected&&key===own&&canOpen())return;
  host=el('section',undefined,'wl-readiness');host.id='wl-readiness';key=own;
  const target=host,head=el('header',undefined,'card wl-readiness-head');
  const intro=el('div');intro.append(el('h1',T('Operational readiness','Prontidão operacional')),
   el('p',T('Company records you can access. Review what needs attention and open the source record.','Registros da empresa aos quais você tem acesso. Veja as pendências e abra o registro de origem.')));
  const actions=el('div',undefined,'actions'),refresh=el('button',T('Refresh','Atualizar'),'btn secondary');
  refresh.type='button';actions.append(link(T('All workspaces','Todos os espaços'),'#workspaces'));
  if(canOpen())actions.append(refresh);
  head.append(intro,actions);target.append(head);
  const notice=el('p',T('This view does not check every requirement or authorise sailing or mobilisation. No findings does not mean the operation is cleared.','Esta tela não verifica todos os requisitos nem autoriza navegação ou mobilização. A ausência de pendências não libera a operação.'),'notice wl-readiness-limit');
  target.append(notice);
  const live=el('p','');live.setAttribute('role','status');target.append(live);
  const output=el('div');target.append(output);root.replaceChildren(target);
  const current=()=>target.isConnected&&host===target&&session()===own&&location.hash==='#readiness'&&canOpen();
  if(!canOpen()){live.textContent=T('No readiness source is available to your account.','Nenhuma fonte de prontidão está disponível para sua conta.');return;}
  const joined=a=>T(...a);
  function draw(d){
   output.replaceChildren();
   const summary=el('div',undefined,'wl-readiness-counts');
   for(const [k,l] of Object.entries(levels)){
    const box=el('section',undefined,'card wl-readiness-state');box.dataset.severity=k;
    box.append(el('strong',String(d.counts[k])),el('span',joined(l)));summary.append(box);
   }
   output.append(summary);
   const covered=el('p',undefined,'wl-readiness-sources');const scope={own:['own records','registros próprios'],company:['company register','registro da empresa'],authorised:['authorised reports','relatos autorizados']};
   covered.textContent=T('Sources checked: ','Fontes verificadas: ')+Object.entries(d.sources).map(([k,v])=>joined(categories[k])+' ('+v.records+' · '+joined(scope[v.scope])+')').join(' / ');
   output.append(covered);
   const card=el('section',undefined,'card wl-readiness-list');card.append(el('h2',T('Findings','Pendências')));
   const filters=el('div',undefined,'wl-readiness-filters');
   function select(label, entries){
    const wrap=el('label',label),input=el('select');for(const [value,name] of entries){const option=el('option',name);option.value=value;input.append(option);}
    wrap.append(input);filters.append(wrap);return input;
   }
   const cat=select(T('Source','Fonte'),[['',T('All sources','Todas as fontes')],...Object.keys(d.sources).map(k=>[k,joined(categories[k])])]);
   const lev=select(T('Priority','Prioridade'),[['',T('All priorities','Todas as prioridades')],...Object.entries(levels).map(([k,v])=>[k,joined(v)])]);
   const form=el('label',T('Search records','Buscar registros')),search=el('input');search.type='search';form.append(search);filters.append(form);card.append(filters);
   const list=el('ul',undefined,'wl-readiness-rows'),count=el('p','');count.setAttribute('role','status');card.append(count,list);output.append(card);
   const fold=s=>s.normalize('NFD').replace(/\p{M}/gu,'').toLowerCase();
   function paint(){
    if(!current())return;
    const q=fold(search.value.trim());
    const found=d.items.filter(x=>(!cat.value||x.kind===cat.value)&&(!lev.value||x.severity===lev.value)&&fold(x.title+' '+joined(reasons[x.reason])).includes(q));
    list.replaceChildren();
    for(const x of found){
     const item=el('li',undefined,'wl-readiness-row');item.dataset.severity=x.severity;
     const detail=el('div');detail.append(el('small',joined(categories[x.kind])+' · '+joined(levels[x.severity])),el('h3',x.title),el('p',joined(reasons[x.reason])+ (x.due?' · '+x.due.slice(0,10):'')));
     const a=link(x.kind==='crew'?T('Open HR documents','Abrir documentos no RH'):T('Open record','Abrir registro'),x.href);
     item.append(detail,a); list.append(item);
    }
    count.textContent=found.length?found.length+T(' shown',' exibida(s)'):T('No findings in this view.','Nenhuma pendência nesta visualização.');
    if(d.total>d.items.length)count.textContent+=' · '+T('Only the first 500 findings are shown. Open the source area to review the rest.','Apenas as primeiras 500 pendências são exibidas. Abra a área de origem para conferir as demais.');
   }
   cat.onchange=lev.onchange=search.oninput=paint;paint();
  }
  function valid(data){
   if(!data||data.user_id!==user.user_id||data.hub_id!==hub()||!data.sources||!Array.isArray(data.items)||!Number.isInteger(data.total)||data.items.length>data.total)return false;
   const uuid='[a-f0-9-]{36}',href=new RegExp('^#(?:(?:certificates|maintenance|qshe)/'+uuid+'|hr/(?:me|staff/'+uuid+')/documents)$','i');
   return Object.entries(data.sources).every(([k,v])=>Object.hasOwn(categories,k)&&Number.isInteger(v.records)&&v.records>=0&&['company','own','authorised'].includes(v.scope))&&Object.keys(levels).every(k=>Number.isInteger(data.counts?.[k])&&data.counts[k]>=0)&&data.items.every(x=>Object.hasOwn(data.sources,x.kind)&&Object.hasOwn(levels,x.severity)&&Object.hasOwn(reasons,x.reason)&&typeof x.title==='string'&&typeof x.due==='string'&&href.test(x.href));
  }
  const before=()=>{if(!current())throw Error(T('The account or page changed.','A conta ou a página mudou.'));};
  refresh.onclick=async()=>{
   if(!current()||refresh.disabled)return;
   refresh.disabled=true;output.replaceChildren();live.textContent=T('Checking saved records…','Verificando registros salvos…');
   const ticket={};load=ticket;
   try{
    const data=await api('/api/readiness',{beforeSend:before});
    if(!current()||load!==ticket)return;
    if(!valid(data))throw Error('Invalid readiness response');
    draw(data);live.textContent=T('Last checked: ','Última conferência: ')+new Date(data.as_of).toLocaleString();
   }catch(e){if(current()&&load===ticket){output.replaceChildren();live.textContent=T('Could not verify these records. Refresh to try again.','Não foi possível verificar os registros. Atualize e tente novamente.');}}
   finally{if(current()&&load===ticket)refresh.disabled=false;}
  };
  refresh.click();
 }
 return {open,allowed};
})();
