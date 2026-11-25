from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
one = runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

# Store only an opaque key in browser history. Each module keeps its own session-bound UI state.
def memory(field, owner):
    return """const returnEntries=new Map();let returnOwner;
 function entry(){
   if(returnOwner!==OWNER){returnEntries.clear();returnOwner=OWNER}
   return returnEntries.get(window.history.state?.FIELD);
 }
 function markReturn(value,target){
   entry();
   const key=crypto.randomUUID(), source=location.hash;
   if(returnEntries.size>=32)returnEntries.delete(returnEntries.keys().next().value);
   returnEntries.set(key,{...value,source,target});
   function mark(){window.history.replaceState({...window.history.state,FIELD:key},'')}
   mark();
   window.addEventListener('hashchange',e=>{
     if(location.hash===target&&new URL(e.oldURL).hash===source&&returnOwner===OWNER)mark();
   },{once:true,capture:true});
 }
""".replace('FIELD',field).replace('OWNER',owner)


def handovers(s):
    s=one(s,"const view=current={trigger,list,layout,panel,observer,card,files:null};",
          "const view=current={trigger,list,layout,panel,observer,card,files:null,originTop};")
    s=one(s,'   close();\n   const layout=', '   const originTop=trigger.getBoundingClientRect().top;close();\n   const layout=')
    s=one(s,"trigger.focus({preventScroll:true});trigger.scrollIntoView({block:'nearest'});",
          "trigger.focus({preventScroll:true});window.scrollBy({top:trigger.getBoundingClientRect().top-originTop,behavior:'instant'});")
    s=one(s,'observer,files,card}=current','observer,files,card,originTop}=current')
    s=one(s,'()=>onRead(id,revision)', '()=>onRead(id,revision,trigger,originTop)')
    s=one(s,' const preview=WLHandoverPreview.mount(',memory('wlHandoverReturn','scope()')+"""
 function readFromPreview(id,revision,trigger,top){
   if(!trigger.dataset.hwdOpen&&!trigger.dataset.hwdPublic)return showDetail(id,revision);
   if(!revision)return showDetail(id,revision);
   const target='#handover/'+encodeURIComponent(id)+'/'+revision;
   const selection=structuredClone(journalSelection);
   selection.returnRow={id,top,day:trigger.closest('[data-hwd-day]')?.dataset.hwdDay,
     attribute:trigger.hasAttribute('data-hwd-public')?'data-hwd-public':'data-hwd-open'};
   markReturn({vesselId,selection},target);location.hash=target;
 }
 function backFromReader(){
   if(entry()?.target===location.hash){window.history.back();return}
   if(location.hash.startsWith('#handover/')){location.hash='#handovers';return}
   load(true);
 }
 const preview=WLHandoverPreview.mount(""")
    s=one(s,'onRead:(id,revision)=>showDetail(id,revision)','onRead:readFromPreview')
    s=one(s,"reset();if(location.hash==='#handovers/mine')","""reset();const previous=entry();
  if(previous?.source===location.hash){vesselId=previous.vesselId;journalSelection=structuredClone(previous.selection)}
  if(location.hash==='#handovers/mine')""")
    s=one(s,"if(readViewLive(c))load(true);};};","if(readViewLive(c))backFromReader();};};")
    return one(s,"el('ho-back').onclick=()=>load(true);","el('ho-back').onclick=backFromReader;")


def journal(s):
    a="window.scrollTo({top:anchor?window.scrollY+anchor.getBoundingClientRect().top-memory.top:memory.y,left:memory.x,behavior:'instant'});"
    return one(s,a,a+"""
    const saved=selection.returnRow;delete selection.returnRow;
    if(saved){
      const day=host.querySelector('[data-hwd-day="'+CSS.escape(saved.day)+'"]');
      const trigger=day?.querySelector('['+saved.attribute+'="'+CSS.escape(saved.id)+'"]');
      if(trigger&&day.open){trigger.focus({preventScroll:true});window.scrollBy({top:trigger.getBoundingClientRect().top-saved.top,behavior:'instant'})}
    }""")


def files(s):
    s=one(s,' function create(c){',' let sourceBack=()=>null;\n function create(c){\n'+memory('wlFileSourceReturn','c.session()')+"""
  sourceBack=()=>{const saved=entry();return saved?.target===location.hash&&c.can('originals.view')?()=>window.history.back():null};
""")
    s=one(s,' return {create};',' return {create,sourceReturn:()=>sourceBack()};')
    s=one(s,'link.href=d.record;menu.append(link);',"""link.href=d.record;
          link.onclick=e=>{if(!e.ctrlKey&&!e.metaKey&&!e.shiftKey&&!e.altKey&&e.button===0)h.rememberSource(d,row)};
          menu.append(link);""")
    s=one(s,'setQuery:value=>{query=value;}',"""rememberSource:(d,row)=>{
       scope();markReturn({folder,query,archived,ui:{group:browseUi.group,type:browseUi.type,sort:browseUi.sort,
         vessel:browseUi.vessel,page:browseUi.page,filters:browseUi.filters,folderOpen:browseUi.folderOpen},
         expanded:[...expandedFolders],id:d.id,top:row.getBoundingClientRect().top},d.record);
     },setQuery:value=>{query=value;}""")
    return one(s,'   await load();if(initialRevision&&active()&&data)',"""   const saved=entry();
   if(saved?.source===location.hash&&!initialRevision){
     folder=saved.folder;query=saved.query;archived=saved.archived;Object.assign(browseUi,saved.ui);
     for(const id of saved.expanded)expandedFolders.add(id);
   }
   await load();
   if(active()&&data&&saved?.source===location.hash&&!initialRevision){
     const row=shell.querySelector('[data-document-id="'+CSS.escape(saved.id)+'"]');
     if(row){const menu=row.querySelector('.wf-more');menu.open=true;
       const origin=[...menu.querySelectorAll('a')].find(a=>a.hash===saved.target);
       if(origin){origin.focus({preventScroll:true});window.scrollBy({top:row.getBoundingClientRect().top-saved.top,behavior:'instant'})}}
   }
   if(initialRevision&&active()&&data)""")


def certificates(s):
    s=one(s,"const header=B('cert-all'", """const sourceBack=window.AJOriginalLibrary?.sourceReturn?.();
  const header=(sourceBack?B('cert-back-source',window.WavelinkUX.text('Voltar aos arquivos originais','Back to Original Files')):'')+B('cert-all'""")
    return one(s,"page(shell(c.title,header,body));","page(shell(c.title,header,body));if(sourceBack)F().click('cert-back-source',sourceBack);")


def employees(s):
    s=one(s,'function restoreEmployee(){',"""function revealMobileEmployee(){
 if(!window.matchMedia('(max-width:700px)').matches)return;
 const title=host?.querySelector('.ux-profile-hero h2');if(!title)return;
 const bounds=title.getBoundingClientRect(),margin=8;
 let inset=0;
 for(let node=document.elementFromPoint(innerWidth/2,1);node;node=node.parentElement){
   if(['sticky','fixed'].includes(getComputedStyle(node).position)){
     const box=node.getBoundingClientRect();if(box.top<=1&&box.bottom<innerHeight/2)inset=Math.max(inset,box.bottom);
   }
 }
 if(bounds.top<inset+margin)window.scrollBy({top:bounds.top-inset-margin,behavior:'instant'});
 else if(bounds.bottom>innerHeight-margin)window.scrollBy({top:bounds.bottom-innerHeight+margin,behavior:'instant'});
}
function restoreEmployee(){""")
    s=one(s,"window.scrollTo({top:r.y,behavior:'instant'});","window.scrollTo({top:r.y,behavior:'instant'});revealMobileEmployee();")
    return one(s," status('');return true;\n}",""" if(oldList.contains(document.activeElement)){
   oldList.querySelector('[aria-current="true"]')?.focus({preventScroll:true});
 }
 status('');revealMobileEmployee();return true;
}""")


def transforms():
    return {'app/static/handovers.js':handovers,'app/static/handover_workspace.js':journal,
            'app/static/original_library.js':files,'app/static/certificate_workspace.js':certificates,'app/static/hr_workspace.js':employees}


if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='17ca31b65afc49bbf29ddf22fe8c7848721590c32dca33fcd23c2571cb390fd1',
        overlays=(Path(__file__).name,),previous_cache='ui162-employee-context',cache='ui162-handover-files-return',
        suffix='handover-files-return',scope='Restore exact journal and original file source navigation context.')
