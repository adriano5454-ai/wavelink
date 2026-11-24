"""Keep names and selectors legible in the Handover shift setup."""
from pathlib import Path
import runpy
import sys


def transforms():
    return {'app/static/ui132_visual.css': lambda s: s + """
#sh-setup-fields{min-inline-size:0}
#sh-setup-people .sh-person{display:grid;grid-template-columns:minmax(0,1fr) minmax(9rem,14rem);align-items:center;gap:.75rem}
#sh-setup-people .sh-person>span{min-width:0;overflow-wrap:anywhere}
#sh-setup-people .sh-person small{display:block}
#sh-setup-people .sh-person select{box-sizing:border-box;width:100%;min-width:0;max-width:100%}
@media(max-width:600px){#sh-setup-people .sh-person{grid-template-columns:minmax(0,1fr);gap:.35rem}}
"""}


if __name__ == '__main__':
    apply = runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]), parent='11c373e030ab1cd9d9a7a07368b244bebcf56c85da0fb75ef372579c4f3dbaf8',
          overlays=(Path(__file__).name,), previous_cache='ui162-handover-reader',
          cache='ui162-handover-shifts', suffix='handover-shifts', scope='Improve Handover shift assignment rows.')
