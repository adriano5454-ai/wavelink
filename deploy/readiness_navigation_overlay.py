"""Show authorised readiness in the main sidebar and chart exact per-source counts."""
from pathlib import Path

BASE=Path(__file__).resolve().parent

def once(s,a,b):
    if s.count(a)!=1:
        raise ValueError(a)
    return s.replace(a,b,1)

def shell(s,pt=False):
    mark='<a data-workspace="qshe" href="#qshe">' if pt else '<a href="#qshe" data-workspace="qshe" >'
    label='Prontidão operacional' if pt else 'Operational readiness'
    tag=(f'<a href="#readiness" data-workspace="readiness" id="nav-readiness" hidden>'
         '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 4v16h16M8 15v-4m5 4V7m5 8V4"/></svg>'
         f'<span>{label}</span></a>\n')
    return once(s,mark,tag+mark)

def router(s):
    s=once(s,"hash.startsWith('#qshe')?'qshe':","hash==='#readiness'?'readiness':hash.startsWith('#qshe')?'qshe':")
    old="else if(a.dataset.workspace==='it')a.hidden="
    return once(s,old,"else if(a.dataset.workspace==='readiness')a.hidden=!window.AJReadiness?.allowed(canUse,state.auth?.person);"+old)

def data(s):
    old="    out.sort(key="
    return once(s,old,"    for kind in sources:\n        sources[kind]['findings']={key:0 for key in SEVERITY}\n    for record in out:\n        sources[record['kind']]['findings'][record['severity']]+=1\n"+old)

def page(s):
    s=once(s," function open({root", (BASE/'readiness_source_chart.js').read_text(encoding='utf8')+" function open({root")
    s=once(s,'   output.append(covered);',
           "   output.append(readinessSourceChart(d,{el,T,joined,categories,levels,scope}),covered);")
    old="Number.isInteger(v.records)&&v.records>=0&&"
    return once(s,old, old+"Object.keys(levels).every(k=>Number.isInteger(v.findings?.[k])&&v.findings[k]>=0)&&Object.keys(levels).reduce((n,k)=>n+v.findings[k],0)<=v.records&&")

def transforms():
    p='app/static/'
    return {'app/readiness.py':data,p+'app.js':router,
        p+'index.html':shell,p+'pt-BR/index.html':lambda s:shell(s,True),p+'readiness_workspace.js':page,
        p+'readiness_workspace.css':lambda s:s+'\n'+(BASE/'readiness_source_chart.css').read_text(encoding='utf8')}

