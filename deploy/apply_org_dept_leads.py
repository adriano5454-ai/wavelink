from pathlib import Path
import runpy
import sys
BASE=Path(__file__).parent

def one(s,old,new):
    if s.count(old)!=1:
        raise ValueError(old)
    return s.replace(old,new)

def ui(s):
    s=one(s,"for(const p of data.positions){if(!groups.has(p.department))groups.set(p.department,[]);groups.get(p.department).push(p)}",
          "for(const p of data.positions){const group=data.example?'showcase':p.department;if(!groups.has(group))groups.set(group,[]);groups.get(group).push(p)}")
    s=one(s,"section.setAttribute('aria-label',rows[0].dept_name);","const heading=data.example?'Maré Alta Surveys · Demo':rows[0].dept_name;section.setAttribute('aria-label',heading);")
    s=one(s,"section.append(el('h3',rows[0].dept_name))","section.append(el('h3',heading))")
    s=one(s,"card.append(el('strong',r.role_name));","card.append(el('strong',r.role_name));if(data.example)card.append(el('small',r.dept_name));")
    s=one(s,"text('Add area leader','Adicionar líder da área')","text('Add top-level position','Adicionar cargo no nível superior')")
    s=one(s,"orgText('Liderança não definida','Leadership not defined')","orgText('Sem chefia formal cadastrada','No formal department head designated')")
    s=one(s,"orgText('Liderança','Leadership')","orgText('Chefia formal','Formal department head')")
    return one(s,"card.querySelector('h3').after(actions);","""const designation=make('a',text('Manage formal department heads','Gerenciar chefias formais'));
     designation.className='btn secondary';designation.href='#admin/departments';
     designation.title=text('Choose this department in Administration to review its formal designation.','Escolha este departamento na Administração para revisar a designação formal.');
     actions.append(designation);card.querySelector('h3').after(actions);""")

def transforms():
    return {'app/static/hr_workspace.js':ui}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='f60a10e240eb0e16b9d23051230b7e4a93b289157d5911a81af6346da971bc4d',overlays=(Path(__file__).name,),previous_cache='ui162-org-card-actions',cache='ui162-org-dept-leads',suffix='org-dept-leads',scope='Identify formal department heads separately from chart positions and group the public company example.')
