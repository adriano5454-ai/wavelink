"""Use the tested neutral outlines in authenticated private company workspaces."""
from pathlib import Path
import runpy,sys
BASE=Path(__file__).resolve().parent
PARENT='d3db7a7ef2d3b1d88ddb31cd5ec247dcf7b691aae74120e5f24d3065256f17f9'
def app(s):
    mark="    document.body?.classList?.toggle('wl-public-demo', workspaceReady && window.WavelinkNativeDemo?.active() === true);"
    assert s.count(mark)==1
    return s.replace(mark,mark+"""
    const companyAccount = Boolean(workspaceReady && !workspaceIssue && !mismatch && !storageFailed && !disposed
        && state.info?.workspace_brand?.id && state.auth?.person?.user_id && state.auth.token && !state.publicDemoUserId
        && state.hub_id && state.hub_id === state.info.hub_id && state.hub_id === state.auth.hub_id);
    document.body?.classList?.toggle('wl-company-account', companyAccount);""")
def colors(s):
    assert s.count('.wl-public-demo #app')==2
    return s.replace('.wl-public-demo #app',':is(.wl-public-demo,.wl-company-account) #app')
def transforms():
    return {'app/static/app.js':app,'app/static/visual_ui124.css':colors}
if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent=PARENT,overlays=(Path(__file__).name,),
        previous_cache='ui162-original-job-source',cache='ui162-company-neutral-edges',suffix='company-neutral-edges',
        scope='Apply the same neutral UI edges to authenticated company accounts without changing permissions.')
