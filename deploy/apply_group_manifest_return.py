from pathlib import Path
import runpy
import sys

BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def fleet(s):
    start=s.index("  $('receiving-results').querySelectorAll('[data-receiving-row] a[href^=")
    end=s.index("  root.querySelectorAll('[data-receiving-open]')",start)
    s=s[:start]+s[end:]
    s=one(s," $('receiving-site').setAttribute('data-page-vessel','');",""" $('receiving-workspace').addEventListener('click',e=>{
  const link=e.target.closest('a[href^="#manifest/"]');
  if(!link||!viewAlive()||e.defaultPrevented||e.button||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;
  const detail=$('receiving-detail').contains(link);
  const row=detail?receivingViewState.selected:link.closest('[data-receiving-row]')?.dataset.receivingRow;
  if(row)receivingOrigin={owner,manifest:link.hash.slice('#manifest/'.length),row,detail,
   list:$('receiving-results').scrollTop,page:window.scrollY,parent:embedded?window.parent.scrollY:0};
 });
 $('receiving-site').setAttribute('data-page-vessel','');""")
    return one(s,"const link=[...$('receiving-results').querySelectorAll('[data-receiving-row] a')]", """const link=origin.detail
   ? receivingViewState.selected===origin.row && [...$('receiving-detail').querySelectorAll('a')].find(a=>a.hash==='#manifest/'+origin.manifest)
   : [...$('receiving-results').querySelectorAll('[data-receiving-row] a')]""")


def transforms():
    return {'app/static/fleet.js':fleet}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='0204cd1064ea8adf84364d62eb2abb9f96ade5992522ba37ff139f3ab70c6a20',overlays=(Path(__file__).name,),previous_cache='ui162-workspace-query-return',cache='ui162-group-manifest-return',suffix='group-manifest-return',scope='group manifest return')
