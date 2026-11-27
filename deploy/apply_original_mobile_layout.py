"""Keep Original Files filters and library folders in reach on narrow screens."""
from pathlib import Path
import runpy,sys
BASE=Path(__file__).resolve().parent
PARENT='c7c815d74e33faee600130d2739eb818db582d6efb2288219e59a75f59724162'
def once(s,a,b):
    if s.count(a)!=1: raise ValueError(a)
    return s.replace(a,b,1)
def browse(s):
    s=once(s,'folderOpen:window.innerWidth>800','folderOpen:true')
    s=once(s,"    const available = new Set", """    const grouped=node('div','wf-workspace-folders'), library=node('div','wf-library-folders');
    if(window.matchMedia('(max-width:800px)').matches)nav.append(library,grouped);else nav.append(grouped,library);
    const available = new Set""")
    i=s.index("    if (available.size) {")
    j=s.index("    function disclosure(",i)
    s=s[:i]+s[i:j].replace('nav.append(', 'grouped.append(').replace('folderButton(nav,','folderButton(grouped,')+s[j:]
    i=s.index("    nav.append(node('h3','wf-nav-label',t('Library folders'")
    j=s.index("    const main=node('section','wf-main')",i)
    s=s[:i]+s[i:j].replace('nav.append(', 'library.append(').replace('folderButton(nav,','folderButton(library,').replace('branch(null,nav);','branch(null,library);')+s[j:]
    return s
def css(s):
    return s+'''
/* Keep filters in normal page flow, never as a clipped mobile flyout. */
.wf-library-folders,.wf-workspace-folders{display:grid;gap:.14rem;min-width:0}
.wf-workspace-folders:empty{display:none}
@media(max-width:800px){
 #original-library .wf-sidebar>summary{box-sizing:border-box;min-height:44px;padding:.65rem .5rem}
 #original-library .wf-folder-list{max-height:min(14rem,40vh)}
 #original-library .wf-tools{display:grid;grid-template-columns:minmax(0,1fr);align-items:stretch}
 #original-library .wf-tools>*{min-width:0;max-width:100%;margin-inline:0;box-sizing:border-box}
 #original-library .wf-tools :is(input,select){box-sizing:border-box;max-width:100%;min-width:0}
 #original-library .wf-filter>summary{box-sizing:border-box;min-height:44px;overflow-wrap:anywhere;background:#f7fafb;border-color:#788f9b}
 #original-library .wf-filter-body{position:static;box-sizing:border-box;width:100%;min-width:0;max-width:none;margin-top:.35rem;padding:.65rem;box-shadow:none}
 #original-library .wf-filter-body .wf-select{display:grid;grid-template-columns:minmax(0,1fr)}
 #original-library .wf-filter-body select{width:100%;min-height:44px}
}
'''
def transforms():
    return {'app/static/original_library.js':browse,'app/static/workspace_original_files.css':css}
if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent=PARENT,overlays=(Path(__file__).name,),
        previous_cache='ui162-company-neutral-edges',cache='ui162-original-mobile-layout',suffix='original-mobile-layout',
        scope='Show the original-file folders and keep filters in view on phones.')
