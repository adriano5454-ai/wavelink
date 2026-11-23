from pathlib import Path
import runpy
import sys


def workspace(source):
    start = source.index(' function locationRosterHtml()')
    end = source.index(' function bindLocationRoster(panel)', start)
    source = source[:start] + Path(__file__).with_suffix('.js').read_text(encoding='utf-8') + '\n' + source[end:]
    pairs = [
        ('const ticket = ++request, selected = day.value;', 'const ticket = ++request, selected = day.value, until = controls.elements.roster_until.value || selected;'),
        ('   const params = new URLSearchParams({...workspaceFilters,start_on:selected,end_on:selected,', """   if(until<selected || (Date.parse(until)-Date.parse(selected))/86400000>92){
    output.textContent=wtext('Escolha de 1 a 93 dias, com fim igual ou posterior ao início.','Choose 1 to 93 days, ending on or after the start date.');
    return;
   }
   const params = new URLSearchParams({...workspaceFilters,start_on:selected,end_on:until,"""),
        ('groupedRoster(data,selected)', 'groupedRoster(data,selected,until)'),
        ('  day.onchange=load;', '  day.onchange=load;\n  controls.elements.roster_until.onchange=load;'),
    ]
    for old, new in pairs:
        if source.count(old) != 1:
            raise ValueError('Unexpected roster source: ' + old)
        source = source.replace(old,new)
    return source


def transforms():
    return {'app/static/hr_workspace.js': workspace}


if __name__=='__main__':
    apply=runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]),parent='032a3c192d54f115771ae54ded1d9a3ed6ae01e5031bdf218bbd337c7d7d3d19',overlays=(Path(__file__).name,),previous_cache='ui162-hr-mobile-day-count',cache='ui162-roster-period',suffix='roster-period',scope='Read-only roster by vessel or location over a selected date range.')
