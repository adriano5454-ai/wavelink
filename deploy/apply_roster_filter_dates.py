"""Carry the open roster query through a vessel-triggered, permission-checked HR refresh."""
import runpy
from pathlib import Path

BASE = Path(__file__).resolve().parent
one = runpy.run_path(str(BASE / 'apply_org_chart_filters.py'))['replace_once']


def workspace(source):
    source = one(source, 'workspaceFilters.vessel_id=id;page=0;open(true);', """const panel=view==='calendar'?el('hr-location-roster'):null;
    const fields=panel?.querySelector('form')?.elements;
    const roster=fields?{open:panel.open,from:fields.roster_day.value,until:fields.roster_until.value,project:fields.roster_project.value}:null;
    if(roster?.open)panel.querySelector('[data-location-results]').textContent=wtext('Consultando escalas.','Loading assignments.');
    workspaceFilters.vessel_id=id;page=0;open(true,false,roster);""")
    source = one(source, 'async function open(force=false,planningOnly=false){',
                 'async function open(force=false,planningOnly=false,roster=null){')
    return one(source, '   renderOverview();\n   if(createDocument){', """   renderOverview();
   if(roster&&view==='calendar'){
    const panel=el('hr-location-roster'),fields=panel?.querySelector('form')?.elements;
    if(fields){
     fields.roster_day.value=roster.from;
     fields.roster_until.value=roster.until;
     fields.roster_project.value=roster.project;
     panel.open=roster.open;
    }
   }
   if(createDocument){""")


def transforms():
    return {'app/static/hr_workspace.js': workspace}
