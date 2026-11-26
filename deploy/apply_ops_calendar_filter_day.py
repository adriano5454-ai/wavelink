from pathlib import Path
import runpy

BASE = Path(__file__).resolve().parent
replace_once = runpy.run_path(str(BASE / 'apply_org_chart_filters.py'))['replace_once']


def preserve_day(source):
    # A vessel/category reload still checks access and replaces the returned
    # month. Only the date controls change the selected day within that month.
    for assignment in (
        'prefs.vessel_id=id;',
        'prefs.kinds=[...s];',
        'prefs.kinds=[...snapshot.available_types];',
        'prefs.kinds=[];',
        'prefs.kinds=defaults.filter(k=>!snapshot||snapshot.available_types.includes(k));',
    ):
        source = replace_once(source, assignment + "prefs.day='';", assignment)
    return source


def transforms():
    return {'app/static/project_calendar.js': preserve_day}
