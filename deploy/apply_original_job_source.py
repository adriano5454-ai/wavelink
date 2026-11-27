"""Keep the source record attached to the same job and vessel as each reference."""
from pathlib import Path
import runpy, sys
BASE=Path(__file__).resolve().parent
PARENT='b094a34a9b2bf4a06fbb16e121c8f5f3a0f7a1f3222d2013d3b082b9082c4cea'
def once(s,a,b):
    assert s.count(a)==1,a
    return s.replace(a,b,1)
def backend(s):
    return once(s,"vessel_ids=list(row['vessel_ids']))]","vessel_ids=list(row['vessel_ids']), record=row['record'])]")
def frontend(s):
    s=once(s,"    const jobsFor=d=>[...new Set((d.jobSources||[]).filter(f=>!ui.group||groupMatches(f.group)).flatMap(f=>(f.job_contexts||[]).filter(ctx=>!ui.vessel||ctx.vessel_ids.includes(ui.vessel)).flatMap(ctx=>ctx.references)))];",
"""    const contextsFor=d=>(d.jobSources||[]).filter(f=>!ui.group||groupMatches(f.group)).flatMap(f=>(f.job_contexts||[]).filter(ctx=>!ui.vessel||ctx.vessel_ids.includes(ui.vessel)).map(ctx=>({...ctx,group:f.group})));
    const jobsFor=d=>[...new Set(contextsFor(d).flatMap(ctx=>ctx.references))];""")
    mark="        if(d.workspace&&d.record){"
    i=s.index(mark)
    j=s.index("        menu.append(button(t('Download original'",i)
    return s[:i]+"""        if(ui.job){
          const origins=new Map();
          for(const ctx of contextsFor(d))if(ctx.record&&ctx.references.some(ref=>fold(ref)===ui.job))origins.set(ctx.record,ctx);
          let index=0;
          for(const origin of origins.values()){
            index++;
            const label=t('Open source record','Abrir registro de origem')+(origins.size>1?' '+index:'');
            const link=node('a','wf-text-button',label);link.href=origin.record;
            link.onclick=e=>{if(d.workspace&&!e.ctrlKey&&!e.metaKey&&!e.shiftKey&&!e.altKey&&e.button===0)h.rememberSource({...d,record:origin.record},row)};
            menu.append(link);
          }
        }else """+s[i+8:j]+s[j:]
def transforms():
    return {'app/library_workspace_files.py':backend,'app/static/original_library.js':frontend}
if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent=PARENT,overlays=(Path(__file__).name,),
        previous_cache='ui162-original-job-filter',cache='ui162-original-job-source',suffix='original-job-source',
        scope='Open the source record associated with the selected job and vessel for shared originals.')
