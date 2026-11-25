from pathlib import Path
import runpy
import sys

BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def directory(s):
    s=one(s,"let generation=0,inflight=null","let liveMount=()=>false,generation=0,inflight=null")
    s=one(s,'   const safe=()=>current()', '   liveMount=current;\n   const safe=()=>current()')
    return one(s,'  return {draw};','  return {draw,isMounted:()=>liveMount()};')


def transforms():
    return {'app/static/home_workspace.js':directory,
            'app/static/app.js':lambda s:one(s,"if(root.firstElementChild?.dataset.stableView===pageKey('workspaces')","if(homeWorkspace.isMounted()&&root.firstElementChild?.dataset.stableView===pageKey('workspaces')")}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='4063c1959eac0ecbe50a6ad399bb7959d9806ee7ad38b554d394caaa018039b3',overlays=(Path(__file__).name,),previous_cache='ui162-checklist-guest-reader',cache='ui162-workspace-search-return',suffix='workspace-search-return',scope='workspace search return')
