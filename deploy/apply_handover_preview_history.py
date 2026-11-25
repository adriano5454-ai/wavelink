from pathlib import Path
import runpy
import sys

BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def handovers(s):
    s=one(s,'function mount({api,active,sections,onRead,onEdit})','function mount({api,active,owner,sections,onRead,onEdit})')
    s=one(s,'  let current=null;',"""  let current=null, saved=null, afterBack=null;
  const marker=()=>history.state?.wlJournalPreview;
  const owns=()=>saved && saved.session===owner() && active() && location.hash==='#handovers' && saved.trigger.isConnected;
  function leave(next){
   if(!current?.key || current.key!==marker()){close(true);next?.();return;}
   if(afterBack)return;
   afterBack={next};history.back();
  }
  window.addEventListener('popstate',()=>{
   const pending=afterBack;afterBack=null;
   if(!owns()){saved=null;return;}
   if(marker()===saved.key){
    if(!current)open(saved.trigger,saved.id,saved.revision,true);
   }else if(current?.key===saved.key){
    close(true);
    pending?.next?.();
   }
  });""")
    s=one(s,'async function open(trigger,id,revision){','async function open(trigger,id,revision,replay=false){')
    s=one(s,'const originTop=trigger.getBoundingClientRect().top;close();',"""const replace=current?.key && current.key===marker();
   const originTop=trigger.getBoundingClientRect().top;close();
   let key=null;
   if(revision && location.hash==='#handovers' && (trigger.dataset.hwdOpen===id||trigger.dataset.hwdPublic===id)){
    if(replay){if(!owns()||marker()!==saved.key)return;key=saved.key;}
    else{
     key=crypto.randomUUID();saved={key,trigger,id,revision,session:owner()};
     history[replace?'replaceState':'pushState']({...history.state,wlJournalPreview:key},'');
    }
   }""")
    s=one(s,'const view=current={trigger,list','const view=current={key,trigger,list')
    s=one(s,'back.onclick=()=>close(true);','back.onclick=()=>leave();')
    s=one(s,"e.preventDefault();close(true);","e.preventDefault();leave();")
    s=one(s,'if(valid()){close();run();}','if(valid()){if(key)leave(run);else{close();run();}}')
    s=one(s,'const preview=WLHandoverPreview.mount({','const preview=WLHandoverPreview.mount({\n  owner:scope,')
    return s


def transforms():
    return {'app/static/handovers.js':handovers}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='d6d260a70a954b341e168533581855fd898095838b4e7d9a545ae02b8abcd5ed',overlays=(Path(__file__).name,),previous_cache='ui162-certificate-reset',cache='ui162-handover-preview-history',suffix='handover-preview-history',scope='handover preview history')
