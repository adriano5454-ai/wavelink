from pathlib import Path
import runpy
import sys

BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def transforms():
    # Keep filters with the account-scoped directory. The existing session
    # check resets them on account changes; only the mount expires on exit.
    return {'app/static/home_workspace.js':lambda s:one(s,
        "generation++;inflight=null;query='';group='all';",
        "generation++;inflight=null;")}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='89962d3945fdb683267de07e15bb9de8f9e6f5ba72c78d2446e8d7089da1ddd3',overlays=(Path(__file__).name,),previous_cache='ui162-handover-preview-history',cache='ui162-workspace-query-return',suffix='workspace-query-return',scope='workspace query return')
