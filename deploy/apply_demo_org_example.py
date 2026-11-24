from pathlib import Path
import runpy
import sys

BASE=Path(__file__).parent

def replace(s,old,new):
    if s.count(old)!=1:
        raise ValueError('Unexpected organogram source')
    return s.replace(old,new)

def api(s):
    old="return response(org_positions.snapshot(c,person,getattr(request.state,'public_demo_read_only',False)))"
    return replace(s,old,"""public = getattr(request.state,'public_demo_read_only',False)
            chart = org_positions.snapshot(c,person,public)
            if public and not chart['positions'] and getattr(app.state,'demo_org_example',None):
                chart.update(positions=app.state.demo_org_example, example=True)
            return response(chart)""")

def ui(s):
    old="container.append(el('p',text('Nenhuma posição visível na estrutura. Consulte os departamentos abaixo.','No reporting positions visible. Browse the departments below.')));return;"
    new="""container.append(el('p',data.editor
     ?text('Para montar o organograma, abra Editar estrutura, adicione a primeira posição no nível superior e escolha Reporta a nas posições subordinadas.','To build your chart, open Edit structure, add the first position at the top level, then choose Reports to for subordinate positions.')
     :text('Nenhuma posição visível. Consulte o diretório abaixo ou peça ao responsável pelo RH para configurar a estrutura.','No reporting positions visible. Browse the directory below or ask your HR administrator to set up the structure.')));return;"""
    s=replace(s,old,new)
    return replace(s," const groups=new Map();\n for(const p of data.positions)", " if(data.example)container.append(el('p',text('Estrutura fictícia de exemplo','Fictional reporting structure')));\n const groups=new Map();\n for(const p of data.positions)")

def transforms():
    return {'app/hr_api.py':api,'app/static/hr_workspace.js':ui}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='ba6f46a61218fc82432337c7827add1e9cb0c98354910476f12ee41d5c9c8d50',overlays=(Path(__file__).name,),previous_cache='ui162-hr-org-tree',cache='ui162-demo-org-example',suffix='demo-org-example',scope='Display an isolated fictional hierarchy in the public demo and clarify empty private charts.')
