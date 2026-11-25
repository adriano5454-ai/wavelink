from pathlib import Path
import runpy
import sys

BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def fleet(s):
    s=one(s,'function beginPage(key){fleetNews.dispose();',"""function beginPage(key){
 if(receivingOrigin && key!=='receiving' && key!=='manifest/'+receivingOrigin.manifest)receivingOrigin=null;
 fleetNews.dispose();""")
    s=one(s,'let receivingRead=0,','let receivingOrigin=null;\nlet receivingRead=0,')
    s=one(s,"async function showReceiving(){beginPage('receiving');","""async function showReceiving(){
 const origin=receivingOrigin && lastViewKey==='manifest/'+receivingOrigin.manifest ? receivingOrigin : null;
 receivingOrigin=null;beginPage('receiving');""")
    marker="   root.querySelectorAll('[data-receiving-open]')"
    marker=marker.strip()
    s=one(s,marker,"""$('receiving-results').querySelectorAll('[data-receiving-row] a[href^="#manifest/"]').forEach(link=>{
   link.onclick=e=>{
    if(!viewAlive()||e.defaultPrevented||e.button||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;
    receivingOrigin={owner,manifest:link.hash.slice('#manifest/'.length),row:link.closest('[data-receiving-row]').dataset.receivingRow,
     list:$('receiving-results').scrollTop,page:window.scrollY,parent:embedded?window.parent.scrollY:0};
   };
  });
  """+marker)
    anchor="draw();$('receiving-results').scrollTop=receivingViewState.listScroll;"
    return one(s,anchor,anchor+"""
 if(origin && origin.owner===owner){
  const link=[...$('receiving-results').querySelectorAll('[data-receiving-row] a')].find(a=>
   a.closest('[data-receiving-row]').dataset.receivingRow===origin.row && a.hash==='#manifest/'+origin.manifest);
  if(link)requestAnimationFrame(()=>{
   if(!viewAlive()||!link.isConnected)return;
   $('receiving-results').scrollTop=origin.list;
   window.scrollTo({top:origin.page,behavior:'instant'});
   if(embedded)window.parent.scrollTo({top:origin.parent,behavior:'instant'});
   link.focus({preventScroll:true});
  });
 }""")


def transforms():
    return {'app/static/fleet.js':fleet}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='7c98e9006c80ce8dca10c2e71dd345a564bb402bc2d9264805dcdf6618b983b0',overlays=(Path(__file__).name,),previous_cache='ui162-workspace-search-return',cache='ui162-receiving-manifest-return',suffix='receiving-manifest-return',scope='receiving manifest return')
