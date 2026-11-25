from pathlib import Path
import runpy
import sys
BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def calendar(s):
    s=one(s,' function setText(el,text)',(BASE/'calendar_task_preview.js').read_text('utf8')+'\n function setText(el,text)')
    s=one(s,"if(e.kind!=='checklists'){location.hash", "if(e.kind==='tasks'){showTask(e,target);return;}\n  if(e.kind!=='checklists'){location.hash")
    s=one(s,'window.scrollTo(0,el?', 'if(origin&&history.state?.calTaskOrigin===origin.marker&&anchor()){focusEvent();return;}\n   window.scrollTo(0,el?')
    s=one(s,'return {open,syncSession,phaseOf,range,validate,href}', 'return {open,syncSession,phaseOf,range,validate,href,taskTitle}')
    return one(s,'if(next!==owner){owner=next;', 'if(next!==owner||cred!==credential){preview?.remove();preview=null;origin=null;}\n  if(next!==owner){owner=next;')

def tasks(s):
    a="const nav=root.querySelector('.gt-detail-nav'),route=location.hash,viewOwner=root.firstElementChild;"
    return one(s,a,a+"\n  window.AJCalendar?.taskTitle(t.id,root.querySelector('h1'));")

def transforms():
    return {'app/static/project_calendar.js':calendar,'app/static/general_tasks.js':tasks,'app/static/project_calendar.css':lambda s:s+"""
.cal-task-preview{box-sizing:border-box;position:fixed;inset:0 0 0 auto;margin:0;width:min(30rem,100%);height:100dvh;max-height:100dvh;max-width:100%;border:1px solid var(--line);background:var(--card,Canvas);color:inherit;padding:1.25rem;overflow:auto}
.cal-task-preview h2{margin-top:0;overflow-wrap:anywhere}.cal-task-preview .btn{margin:.5rem .5rem 0 0}
.cal-task-preview::backdrop{background:rgb(0 0 0 / .35)}
@media(max-width:700px){.cal-task-preview{inset:auto 0 0;width:100%;height:auto;max-height:80dvh;border-radius:1rem 1rem 0 0;padding-bottom:max(1rem,env(safe-area-inset-bottom))}}
"""}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='473491814e2e3f224b2435632a1b14c55bf29e955708a8a3c55aa5069ff2bfb3',overlays=(Path(__file__).name,),previous_cache='ui162-employee-selection-feedback',cache='ui162-calendar-task-preview',suffix='calendar-task-preview',scope='Preview calendar tasks and return to their exact event.')
