from pathlib import Path
import runpy
import sys

BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def controller(s):
    s=one(s,'mount({api,active,owner,sections,onRead,onEdit})','mount({api,active,owner,sections,onRead,onEdit,rememberList})')
    s=one(s,'saved={key,trigger,id,revision,session:owner()};','saved={key,trigger,id,revision,session:owner()};rememberList(trigger,id,revision,originTop,key);')
    s=one(s,'  return {open,close};',"""  function rebind(trigger,id,revision,key){
   if(!active()||!trigger.isConnected||!revision||!key)return;
   saved={trigger,id,revision,key,session:owner()};
   if(marker()===key&&!current)open(trigger,id,revision,true);
  }
  return {open,close,rebind};""")
    s=one(s,"   window.addEventListener('hashchange',e=>{\n     if(location.hash===target", "   if(!target)return;\n   window.addEventListener('hashchange',e=>{\n     if(location.hash===target")
    a=s.index('   const selection=structuredClone(journalSelection);',s.index('function readFromPreview'))
    b=s.index('   markReturn(',a)
    snapshot=s[a:b]
    s=s[:a]+"   const selection=listSelection(trigger,id,top);\n"+s[b:]
    s=one(s,' function readFromPreview(', ' function listSelection(trigger,id,top){\n'+snapshot+'   return selection;\n }\n function readFromPreview(')
    s=one(s,'  owner:scope,',"""  owner:scope,
  rememberList(trigger,id,revision,top,key){
   markReturn({vesselId,selection:listSelection(trigger,id,top),preview:{id,revision,key}},null);
  },""")
    return one(s,'onPreview:preview.open,onSetup:openSimpleSetup','''onPreview:preview.open,onRestorePreview:(trigger,id,revision)=>{
    const old=entry()?.preview;
    if(old?.id===id&&old.revision===revision)preview.rebind(trigger,id,revision,old.key);
   },onSetup:openSimpleSetup''')


def journal(s):
    s=one(s,'onDownload,onPreview,selection','onDownload,onPreview,onRestorePreview,selection')
    return one(s,"if(trigger&&day.open){trigger.focus({preventScroll:true});window.scrollBy({top:trigger.getBoundingClientRect().top-saved.top,behavior:'instant'})}", """if(trigger&&day.open){
       trigger.focus({preventScroll:true});window.scrollBy({top:trigger.getBoundingClientRect().top-saved.top,behavior:'instant'});
       const row=snapshot?.rows.find(r=>r.id===saved.id);
       if(row&&(row.state==='published'||saved.attribute==='data-hwd-public'))onRestorePreview?.(trigger,row.id,row.published_revision);
      }""")


def transforms():
    return {'app/static/handovers.js':controller,'app/static/handover_workspace.js':journal}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='d8c4c941bcb366abf45a76134e898dc3a6f360f3bc76b77452d0962d0e8212a8',overlays=(Path(__file__).name,),previous_cache='ui162-group-manifest-return',cache='ui162-journal-history-return',suffix='journal-history-return',scope='journal history return')
