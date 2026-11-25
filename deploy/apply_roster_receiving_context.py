from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
one = runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def roster(s):
    a=s.index(' function bindLocationRoster(panel)')
    b=s.index(' let mobileDay=',a)
    body=s[a:b]
    body=one(body,'const context = capture(), controls','const mounted = capture(), controls')
    body=one(body,'const ticket = ++request, selected',"""if (!mounted.same() || H.dialog.open || form || !panel.isConnected) return;
   const context = capture();
   const ticket = ++request, selected""")
    body=one(body,'panel.isConnected && context.same()', 'panel.isConnected && context.pending()')
    body=one(body,"panel.querySelector('datalist'),workspace,context","panel.querySelector('datalist'),workspace,mounted")
    return s[:a]+body+s[b:]

def fleet(s):
    a="""__wl118.markup('<a href="#receiving" class="btn">Receiving &amp; placement</a>')"""
    s=one(s,a,'__wl118.html`<a href="#receiving" data-receiving-site="${E(s.id)}" class="btn">Receiving &amp; placement</a>`')
    a=" on('add-site',()=>siteForm());"
    s=one(s,a,a+"""
 root.querySelectorAll('[data-receiving-site]').forEach(link=>link.onclick=e=>{
  if(e.defaultPrevented||e.button||e.ctrlKey||e.metaKey||e.altKey||e.shiftKey||dia.open||modalSaving||fleetJournal.activeCount())return;
  const site=link.dataset.receivingSite;
  if(sites.some(s=>s.id===site))receivingViewState=freshReceivingState(saveSession(),site);
 });""")
    a="let receivingViewState={owner:'',query:'',site:'',condition:'all',selected:'',detail:false,filtersOpen:false,listScroll:0,pageScroll:0,parentScroll:0};"
    s=one(s,a,"""function freshReceivingState(owner='',site=''){
 return {owner,query:'',site,condition:'all',selected:'',detail:false,filtersOpen:false,listScroll:0,pageScroll:0,parentScroll:0};
}
let receivingViewState=freshReceivingState();""")
    return one(s,"receivingViewState={owner,query:'',site:'',condition:'all',selected:'',detail:false,filtersOpen:false,listScroll:0,pageScroll:0,parentScroll:0};","receivingViewState=freshReceivingState(owner);")

def transforms():
    return {'app/static/hr_workspace.js':roster,'app/static/fleet.js':fleet}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='7d5affad0a14bc2a38b74feb2d25a6878e6872700c05067faa6f1228034b501b',overlays=(Path(__file__).name,),previous_cache='ui162-talk-preview',cache='ui162-roster-receiving-context',suffix='roster-receiving-context',scope='Retain the authorised roster after record close and open receiving for the chosen site.')
