"""Preserve the scoped list, report and read-only history in the QSHE workspace."""
from pathlib import Path
import runpy

BASE = Path(__file__).resolve().parent
one = runpy.run_path(str(BASE / 'apply_org_chart_filters.py'))['replace_once']


def qshe(source):
    source = one(source, ' function syncSession(){', """ const visits=new Map();
 let visitOwner='';
 function entry(){
  if(visitOwner!==scope()){visits.clear();visitOwner=scope();}
  return visits.get(history.state?.wlQsheVisit);
 }
 function saveVisit(view,id,focusId,push=false){
  entry();
  const key=(!push&&entry()?history.state.wlQsheVisit:null)||crypto.randomUUID();
  if(!visits.has(key)&&visits.size>=64)visits.delete(visits.keys().next().value);
  visits.set(key,{view,id,focusId,status,query,category,assignment,vesselId,offset});
  history[push?'pushState':'replaceState']({...history.state,wlQsheVisit:key},'');
 }
 function focusControl(control){
  if(!control?.isConnected)return;
  if(control.tagName==='H2')control.tabIndex=-1;
  control.focus({preventScroll:true});
  const box=control.getBoundingClientRect();
  if(box.top<72||box.bottom>innerHeight){control.style.scrollMarginTop='80px';control.scrollIntoView({block:'start',behavior:'instant'});}
 }
 function openRow(id){
  if(!allowed()||form)return;
  saveVisit(selected?'report':'list',selected,id);saveVisit('report',id,null,true);
  select(id,true);
 }
 window.addEventListener('popstate',()=>{
  const saved=entry();
  if(!saved||!allowed()||form||!handles(location.hash)||document.querySelector('dialog[open]'))return;
  if(!el('qs-workspace'))return;
  mountedRoute='';open();
 });
 function syncSession(){""")
    source = one(source, "b.onclick=()=>select(b.dataset.qsId)", "b.onclick=()=>openRow(b.dataset.qsId)")
    source = one(source, "  context=scope();mountedRoute=location.hash;", """  const visit=entry();
  if(visit){
   ({status,query,category,assignment,vesselId,offset}=visit);
   selected=visit.id;
  }
  context=scope();mountedRoute=location.hash;""")
    source = one(source, "   if(selected)await select(selected);\n  }catch", """   if(selected)await select(selected,true);
   else if(visit?.focusId)focusControl([...el('qs-list').querySelectorAll('[data-qs-id]')].find(b=>b.dataset.qsId===visit.focusId));
  }catch""")
    source = one(source, ' async function select(id){',' async function select(id,focus=false){')
    source = one(source, "report.'));detail(f);}", """report.'));detail(f);
   const saved=entry();
   if(saved?.view==='history'&&saved.id===id)await historyView(f,true);
   else if(focus)focusControl(saved?.focusId==='history'?el('qs-history'):el('qs-detail').querySelector('h2'));
  }""")
    source = one(source, "el('qs-history').onclick=()=>historyView(f.id);", """el('qs-history').onclick=()=>{
   if(!allowed()||form||selected!==f.id)return;
   saveVisit('report',f.id,'history');saveVisit('history',f.id,null,true);historyView(f,true);
  };""")
    source = one(source,"async function historyView(id){const g=", "async function historyView(f,focus){const id=f.id,g=")
    source = one(source,"el('qs-return').onclick=()=>select(id);", """const heading=el('qs-detail').querySelector('h2');
  const identity=document.createElement('p');identity.textContent=f.reference+' / '+words('REVISÃO SALVA','SAVED REVISION')+' '+f.version;
  heading.before(identity);heading.append(document.createTextNode(' — '+f.title));
  el('qs-return').onclick=()=>{if(!form&&allowed()&&entry()?.id===id&&entry().view==='history')history.back();};
  if(focus)focusControl(heading);""")
    return source


def transforms():
    return {'app/static/qshe_reports.js': qshe}
