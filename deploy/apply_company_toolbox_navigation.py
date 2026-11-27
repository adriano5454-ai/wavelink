"""Backport the Toolbox Talks preview and keyboard return to the #69 company release."""
from hashlib import sha256
import json
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
PARENT = "664032a324101447fcdb09e92389c5105e28403da6b4880dd78b244df9e1d979"
RESULT = "e1d08c1b3dc94bbaa581b603b329f025c1cb1f51d8f22f689e8a6e69dc3122fa"
PREVIOUS_CACHE = "ui162-org-dept-leads"
CACHE = "ui162-company-toolbox-navigation"

PREVIEW_CSS = """
.tb-preview-layout.tb-preview-active{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:1rem;align-items:start}
.tb-preview-active #tb-results{grid-template-columns:1fr}
.tb-talk-preview{overflow-wrap:anywhere;min-width:0;max-height:calc(100dvh - 6rem);overflow:auto;position:sticky;top:5rem}
.tb-talk-preview h2{margin-top:0}
#tb-results [aria-current=true]{outline:2px solid currentColor;outline-offset:-2px}
@media(max-width:800px){.tb-preview-layout.tb-preview-active{display:block}.tb-talk-preview[open]{position:fixed;inset:auto 0 0;margin:0;width:100%;max-width:none;box-sizing:border-box;max-height:85dvh;border-radius:1rem 1rem 0 0;background:var(--card,Canvas);color:var(--text,CanvasText)}.tb-talk-preview::backdrop{background:rgb(0 0 0 /.35)}}
"""


def fieldwork(source):
    once = runpy.run_path(str(BASE / "apply_org_dept_leads.py"))["one"]
    source = once(source, "const toolboxStaleControls=new Map();", """const toolboxStaleControls=new Map();let talkOrigin=null;
 function focusTalkRow(row,top){
  row.focus({preventScroll:true});
  window.scrollBy({top:row.getBoundingClientRect().top-top,behavior:'instant'});
 }""")
    source = once(source, "if(changed){toolboxViewKey=key;",
                  "if(changed){previewScope=crypto.randomUUID();toolboxPreviewEvents?.abort();talkOrigin=null;toolboxViewKey=key;")
    anchor = "  // Capture after the first-load shell is mounted."
    source = once(source, anchor, """  const id=route.slice(1).split('/')[1];
  if(id && talkOrigin?.id===id) talkOrigin.restoreRow=true;
""" + anchor)
    source = once(source, "try{const id=route.slice(1).split('/')[1];const data=await api(id?'/api/toolbox/talks/'",
                  "try{const data=await api(id?'/api/toolbox/talks/'")
    anchor = "  try{const data=await api(id?'/api/toolbox/talks/'"
    source = once(source, anchor, """  const activeReadPreview=()=>{
   const entry=window.history.state?.tbPreview;
   if(id||!mounted||!entry||entry.scope!==previewScope)return null;
   const selected=root.querySelector('#tb-results [aria-current="true"]');
   if(selected?.dataset.toolboxId!==entry.id)return null;
   const sheet=root.querySelector('.tb-preview-layout > dialog.tb-talk-preview[open]');
   return ctx.onlyReadPreview(sheet)?entry:null;
  };
  const clearReadPreview=()=>{
   const next={...window.history.state};delete next.tbPreview;
   window.history.replaceState(next,'',location.href);
  };
""" + anchor)
    source = once(source, "   if(!own())return;\n   if(!ctx.pending()){", """   if(!own())return;
   const uninterrupted=ctx.pending();
   const preview=uninterrupted?null:activeReadPreview();
   if(!uninterrupted&&!preview){""")
    anchor = "   toolboxNotice('');if(loading||!mounted||sig!==lastResponse){"
    source = once(source, anchor, """   if(preview){
    if(sig===lastResponse&&!root.querySelector('.tb-stale'))return;
    if(!data.talks.some(talk=>talk.id===preview.id))clearReadPreview();
   }
""" + anchor)
    anchor = "   if(!ctx.pending()){\n    if(!toolboxReadNotice("
    source = once(source, anchor, """   if(denied&&activeReadPreview()){
    clearReadPreview();toolboxNotice(message(e),true);return;
   }
""" + anchor)
    paint = "(id?talkView:toolboxHome)(data);lastResponse=sig;"
    source = once(source, paint, paint + """
    if(id&&talkOrigin?.id===id&&loading){
     const heading=root.querySelector('.fw-heading h1');
     if(heading){heading.tabIndex=-1;heading.style.scrollMarginTop='76px';heading.focus({preventScroll:true});heading.scrollIntoView({block:'start',behavior:'instant'});}
    }else if(!id&&talkOrigin?.restoreRow){
     talkOrigin.restoreRow=false;
     const row=[...root.querySelectorAll('[data-toolbox-id]')].find(a=>a.dataset.toolboxId===talkOrigin.id);
     if(row)focusTalkRow(row,talkOrigin.top);
    }
""")
    anchor = " function toolboxHome(data){"
    preview = (BASE / "toolbox_talk_preview.js").read_text(encoding="utf-8").rstrip("\n")
    source = once(source, anchor, " let previewScope=crypto.randomUUID(),toolboxPreviewEvents;\n"
                  + preview + "\n\n" + anchor)
    source = once(source, "  mountFilters();\n  const project=document.getElementById('tb-project');",
                  "  mountFilters();\n  const updatePreview=mountTalkPreview(data,filteredTalks,words);\n"
                  "  const project=document.getElementById('tb-project');")
    paint = "AJViewStability.paint(document.getElementById('tb-results'),cards(shown));"
    return once(source, paint, paint + "updatePreview();")


def toolbox_context(source):
    once = runpy.run_path(str(BASE / "apply_org_dept_leads.py"))["one"]
    source = once(source,
        "  const pending=()=>current()&&stamp===dialogEpoch()&&wasOpen===dlg.open&&child===observed?.firstElementChild&&!document.querySelector('dialog[open]:not(#dialog)');",
        """  const sameForm=()=>current()&&stamp===dialogEpoch()&&wasOpen===dlg.open&&child===observed?.firstElementChild;
  const pending=()=>sameForm()&&!document.querySelector('dialog[open]:not(#dialog)');
  const onlyReadPreview=sheet=>{
   if(!sheet||dlg.open||!sameForm())return false;
   const open=document.querySelectorAll('dialog[open]:not(#dialog)');
   return open.length===1&&open[0]===sheet;
  };""")
    return once(source, "return {current,pending,before:()=>", "return {current,pending,onlyReadPreview,before:()=>")


def transforms():
    return {
        "app/static/fieldwork.js": fieldwork,
        "app/static/toolbox_ui.js": toolbox_context,
        "app/static/operations_workspace_ui76.css": lambda source: source + PREVIEW_CSS,
    }


def apply(root):
    manifest = root / "RELEASE_FILES.json"
    raw = manifest.read_bytes()
    current = sha256(raw).hexdigest()
    if current == RESULT:
        for name, digest in json.loads(raw)["files"].items():
            if sha256((root / name).read_bytes()).hexdigest() != digest:
                raise ValueError("Unexpected resource: " + name)
        return
    if current != PARENT:
        raise ValueError("Unexpected company release before Toolbox navigation")
    stage = runpy.run_path(str(BASE / "apply_editor_exit.py"))["apply"]
    stage(root, parent=PARENT, overlays=(Path(__file__).name,), previous_cache=PREVIOUS_CACHE,
          cache=CACHE, suffix="company-toolbox-navigation",
          scope="Read authorized Toolbox Talks in context and return to the selected row.")
    if sha256(manifest.read_bytes()).hexdigest() != RESULT:
        raise ValueError("Unexpected release after Toolbox navigation")


if __name__ == "__main__":
    apply(Path(sys.argv[1]))
