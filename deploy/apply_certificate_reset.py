from pathlib import Path
import runpy
import sys

BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']

def transforms():
    # The shared painter preserves form values. Reconcile all controls with the
    # catalogue preferences after painting, including an intentional reset.
    return {'app/static/certificate_workspace.js':lambda s:one(s,
        "const q=root.querySelector('[name=certsearch]');q.oninput",
        """const q=root.querySelector('[name=certsearch]');
  if(q.value!==prefs.q)q.value=prefs.q;
  root.querySelector('[name=certcontact]').value=prefs.contact;
  const vesselFilter=root.querySelector('[data-page-vessel]');if(vesselFilter)vesselFilter.value=prefs.vessel;
  q.oninput""")}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='2be630681f8e3d27084fce39d06369f1ee664e5756daa288e187238022117ab9',overlays=(Path(__file__).name,),previous_cache='ui162-receiving-manifest-return',cache='ui162-certificate-reset',suffix='certificate-reset',scope='certificate reset')
