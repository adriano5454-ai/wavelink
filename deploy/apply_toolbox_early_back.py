"""Restore the Toolbox row even if a detail read is still in flight."""
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
replace_once = runpy.run_path(str(BASE / "apply_org_chart_filters.py"))["replace_once"]


def fieldwork(source):
    # Back can return to the list before the detail request resolves or fails.
    source = replace_once(source,
        "  // Capture after the first-load shell is mounted. A later dialog must not make",
        """  const id=route.slice(1).split('/')[1];
  if(id && talkOrigin?.id===id) talkOrigin.restoreRow=true;
  // Capture after the first-load shell is mounted. A later dialog must not make""")
    source = replace_once(source, "try{const id=route.slice(1).split('/')[1];const data=await api(id?'/api/toolbox/talks/'",
                          "try{const data=await api(id?'/api/toolbox/talks/'")
    source = replace_once(source, "talkOrigin={id,top,atList:true}", "talkOrigin={id,top,restoreRow:true}")
    source = replace_once(source, "if(id&&talkOrigin?.id===id&&talkOrigin.atList){\n     talkOrigin.atList=false;",
                          "if(id&&talkOrigin?.id===id&&loading){")
    return replace_once(source, "else if(!id&&talkOrigin&&!talkOrigin.atList){\n     talkOrigin.atList=true;",
                        "else if(!id&&talkOrigin?.restoreRow){\n     talkOrigin.restoreRow=false;")


def transforms():
    return {"app/static/fieldwork.js": fieldwork}


if __name__ == "__main__":
    apply = runpy.run_path(str(BASE / "apply_editor_exit.py"))["apply"]
    apply(Path(sys.argv[1]), parent="ac2ba948e02a7dcb8d6b08049ef9638b660998ab9ecc92affe85c139fd2dada2",
          overlays=(Path(__file__).name,), previous_cache="ui162-checklist-preview-sections",
          cache="ui162-toolbox-early-back", suffix="toolbox-early-back",
          scope="Restore the Toolbox list opener and scroll when leaving a pending detail read.")
