from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError(old)
    return source.replace(old, new)


def chart(source):
    source = replace_once(source, 'function drawOrgTree(container,data,edit,decorate){',
                          (BASE/'org_chart_filters.js').read_text('utf8') +
                          'function paintOrgTree(container,data,edit,decorate,matches=null){')
    source = replace_once(source, 'const groups=new Map();\n for(const p of data.positions)',
                          'const folds=matches?new Set():folded;\n const groups=new Map();\n for(const p of data.positions)')
    source = replace_once(source, 'if(folded.has(parent))folded.delete(parent);else folded.add(parent)',
                          'if(folds.has(parent))folds.delete(parent);else folds.add(parent)')
    source = replace_once(source, 'list.hidden=folded.has(parent)', 'list.hidden=folds.has(parent)')
    return replace_once(source, 'card.append(link);if(decorate)', """card.append(link);
     if(matches&&!matches.has(r.id)){const context=el('small',text('Linha de reporte','Reporting line'));context.className='org-context';card.append(context)}
     const branch=String(r.vessel_id||r.department||'');
     item.dataset.tone=String(Array.from(branch).reduce((sum,c)=>sum+c.charCodeAt(0),0)%4);
     if(decorate)""")


def transforms():
    return {'app/static/hr_workspace.js':chart,
            'app/static/ui132_visual.css':lambda s:s+'\n'+(BASE/'org_chart_filters.css').read_text('utf8')}


if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='664032a324101447fcdb09e92389c5105e28403da6b4880dd78b244df9e1d979',
        overlays=(Path(__file__).name,),previous_cache='ui162-org-dept-leads',cache='ui162-org-chart-filters',
        suffix='org-chart-filters',scope='Search visible reporting positions and filter by department, vessel and vacancy.')
