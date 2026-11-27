"""Return focus when browser Back reuses the mounted Toolbox results."""
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
replace_once = runpy.run_path(str(BASE / "apply_org_chart_filters.py"))["replace_once"]


def fieldwork(source):
    source = replace_once(source, " function toolboxNotice(text,denied=false){", """ function focusTalkRow(row,top){
  row.focus({preventScroll:true});
  window.scrollBy({top:row.getBoundingClientRect().top-top,behavior:'instant'});
 }
 function toolboxNotice(text,denied=false){""")
    source = replace_once(source,
        "if(row){row.focus({preventScroll:true});window.scrollBy({top:row.getBoundingClientRect().top-talkOrigin.top,behavior:'instant'});}",
        "if(row)focusTalkRow(row,talkOrigin.top);")
    source = replace_once(source,
        "if(restore&&visible()&&row){row.focus({preventScroll:true});window.scrollBy({top:row.getBoundingClientRect().top-top,behavior:'instant'});}",
        "if(restore&&visible()&&row)focusTalkRow(row,top);")
    return replace_once(source,
        " function sync(){if(!visible()){dismiss();return}const entry=window.history.state?.tbPreview;if(entry?.scope===previewScope&&link(entry.id))show(entry.id,false);else dismiss(true);}",
        """ function sync(event){
  if(!visible()){dismiss();return;}
  const entry=window.history.state?.tbPreview;
  if(entry?.scope===previewScope&&link(entry.id)){show(entry.id,false);return;}
  if(event?.type==='popstate'&&!activeId&&talkOrigin?.restoreRow){
   // Back can return before the detail route replaces this list.
   const row=link(talkOrigin.id);
   talkOrigin.restoreRow=false;
   if(row&&(document.activeElement===document.body||document.activeElement===row))focusTalkRow(row,talkOrigin.top);
  }else dismiss(true);
 }""")


def transforms():
    return {"app/static/fieldwork.js": fieldwork}


if __name__ == "__main__":
    apply = runpy.run_path(str(BASE / "apply_editor_exit.py"))["apply"]
    apply(Path(sys.argv[1]), parent="8bdf4de94325c2bafcc1dc57467318eed92c2f9549d133e0913cac0335602db4",
          overlays=(Path(__file__).name,), previous_cache="ui162-demo-outlines",
          cache="ui162-toolbox-retained-row", suffix="toolbox-retained-row",
          scope="Restore the originating Toolbox row when Back reuses the mounted list.")
