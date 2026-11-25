from pathlib import Path
import runpy
import sys
BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def toolbox(s):
    s=one(s,"const toolboxStaleControls=new Map();","const toolboxStaleControls=new Map();let talkOrigin=null;")
    s=one(s,"if(changed){toolboxViewKey=key;","if(changed){talkOrigin=null;toolboxViewKey=key;")
    s=one(s,"  mountFilters();","""  mountFilters();
  document.getElementById('tb-results').addEventListener('click',ev=>{
   const a=ev.target.closest('a[data-toolbox-id][href]');
   if(a&&!ev.defaultPrevented&&!ev.button&&!ev.ctrlKey&&!ev.metaKey&&!ev.altKey&&!ev.shiftKey)
    talkOrigin={id:a.dataset.toolboxId,top:a.getBoundingClientRect().top,atList:true};
  });""")
    a="(id?talkView:toolboxHome)(data);lastResponse=sig;"
    return one(s,a,a+"""
    if(id&&talkOrigin?.id===id&&talkOrigin.atList){
     talkOrigin.atList=false;
     const heading=root.querySelector('.fw-heading h1');
     if(heading){heading.tabIndex=-1;heading.style.scrollMarginTop='76px';heading.focus({preventScroll:true});heading.scrollIntoView({block:'start',behavior:'instant'});}
    }else if(!id&&talkOrigin&&!talkOrigin.atList){
     talkOrigin.atList=true;
     const row=[...root.querySelectorAll('[data-toolbox-id]')].find(a=>a.dataset.toolboxId===talkOrigin.id);
     if(row){row.focus({preventScroll:true});window.scrollBy({top:row.getBoundingClientRect().top-talkOrigin.top,behavior:'instant'});}
    }
""")

def transforms():
    return {'app/static/fieldwork.js':toolbox}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='cff2db677d4c4c03d94e08e9b7fcf8fdcb2fccda7e0d4e00c6399cbb0c2e57bb',overlays=(Path(__file__).name,),previous_cache='ui162-calendar-task-preview',cache='ui162-talk-origin',suffix='talk-origin',scope='Restore the toolbox talk heading and list focus.')
