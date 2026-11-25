from pathlib import Path
import sys,runpy
BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']
def fieldwork(s):
    s=one(s,'function toolboxHome(data){','let previewScope=crypto.randomUUID(),toolboxPreviewEvents;\n'+(BASE/'toolbox_talk_preview.js').read_text('utf8')+'\n function toolboxHome(data){')
    s=one(s,'if(changed){talkOrigin=null;', 'if(changed){previewScope=crypto.randomUUID();toolboxPreviewEvents?.abort();talkOrigin=null;')
    a=s.index("  document.getElementById('tb-results').addEventListener");b=s.index('  const project=document',a)
    s=s[:a]+'  const updatePreview=mountTalkPreview(data,filteredTalks,words);\n'+s[b:]
    a="AJViewStability.paint(document.getElementById('tb-results'),cards(shown));"
    return one(s,a,a+'updatePreview();')
def transforms():
    return {'app/static/fieldwork.js':fieldwork,'app/static/operations_workspace_ui76.css':lambda s:s+"""
.tb-preview-layout.tb-preview-active{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1rem;align-items:start}
.tb-preview-active #tb-results{grid-template-columns:1fr}
.tb-talk-preview{overflow-wrap:anywhere;min-width:0;max-height:calc(100dvh - 6rem);overflow:auto;position:sticky;top:5rem}
.tb-talk-preview h2{margin-top:0}
#tb-results [aria-current=true]{outline:2px solid currentColor;outline-offset:-2px}
@media(max-width:800px){.tb-preview-layout.tb-preview-active{display:block}.tb-talk-preview[open]{position:fixed;inset:auto 0 0;margin:0;width:100%;max-width:none;box-sizing:border-box;max-height:85dvh;border-radius:1rem 1rem 0 0;background:var(--card,Canvas);color:var(--text,CanvasText)}.tb-talk-preview::backdrop{background:rgb(0 0 0 /.35)}}
"""}
if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='75f342d54e9eeb975dd5ca96f8252ca88ed968eda9cf5a2ef4e3be0a74d25162',overlays=(Path(__file__).name,),previous_cache='ui162-talk-origin',cache='ui162-talk-preview',suffix='talk-preview',scope='Read an authorised toolbox talk preview in its list.')
