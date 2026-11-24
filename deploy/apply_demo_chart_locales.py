"""Localize only the public showcase's example positions and directory labels."""
import runpy
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
replace = runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']


def chart(source):
    source = replace(source, 'function renderOrg(){', """const demoChartLabels=new Map(Object.entries({
 'Executive':'Diretoria','Operations':'Operações','Offshore Survey':'Levantamento offshore',
 'Meridian Survey Team':'Equipe de levantamento Meridian','IT':'TI','Finance':'Finanças',
 'DEMO Survey':'Levantamento DEMO','DEMO Engineering':'Engenharia DEMO','DEMO Logistics':'Logística DEMO',
 'Survey coordinator':'Coordenação de levantamento','AUV technician':'Técnico de AUV',
 'Survey engineer':'Engenheiro de levantamento','Logistics coordinator':'Coordenação de logística'
}));
function demoChartLabel(value){
 return orgText(demoChartLabels.get(value)||value,value);
}
function renderOrg(){
 const label=value=>window.WavelinkNativeDemo?.active()?demoChartLabel(value):value;""")
    source = replace(source, "const heading=unit.name||orgText(", "const heading=label(unit.name)||orgText(")
    source = replace(source, "'<small>'+E(person.title)+'</small>'", "'<small>'+E(label(person.title))+'</small>'")
    return replace(source, ' const owner=identity();\n if(filterOwner', """ if(data.example){
   data={...data,positions:data.positions.map(row=>({...row,
     role_name:row.demo_titles?orgText(row.demo_titles.pt,row.demo_titles.en):row.role_name,
     dept_name:demoChartLabel(row.dept_name)}))};
 }
 const owner=identity();
 if(filterOwner""")


def transforms():
    return {'app/static/hr_workspace.js':chart}


if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='d55cb83c9d27a299f18772cb0bc4d483cd81dc7f3c9218b540f612da8cde0109',
        overlays=(Path(__file__).name,),previous_cache='ui162-org-chart-filters',cache='ui162-demo-chart-locales',
        suffix='demo-chart-locales',scope='Display fictional organization chart labels in the selected language.')
