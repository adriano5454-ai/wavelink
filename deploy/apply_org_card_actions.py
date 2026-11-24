from pathlib import Path
import runpy
import sys
BASE=Path(__file__).parent
def one(s,a,b):
    if s.count(a)!=1:raise ValueError(a)
    return s.replace(a,b)

def backend(s):
    s=one(s,"    if not isinstance(p,dict) or set(p)!=keys", """    above = p.get('insert_above','') if isinstance(p,dict) else ''
    if isinstance(p,dict) and 'insert_above' in p:
        keys.add('insert_above')
    if not isinstance(p,dict) or set(p)!=keys""")
    s=one(s,"        if bool(dept)==", """        if above:
            child=c.execute('SELECT * FROM hr_org_positions WHERE id=?',(above,)).fetchone()
            if old or not child or child['department']!=dept or child['parent']!=parent:
                raise Problem(409,'Choose a current position in this department.')
        if bool(dept)==""")
    return one(s,"        return snapshot(c,actor,False)", """        if above:
            c.execute('UPDATE hr_org_positions SET parent=?,version=version+1 WHERE id=?',(pos,above))
            membership_policy.audit(c,user['id'],above,'org_position_saved',dict(parent=pos,previous_parent=parent))
        return snapshot(c,actor,False)""")

def ui(s):
    s=one(s,'function drawOrgTree(container,data,edit){','function drawOrgTree(container,data,edit,decorate){')
    s=one(s,'if(data.editor)container.append(btn','if(data.editor&&!decorate)container.append(btn')
    s=one(s,'card.append(link);nodes.set','card.append(link);if(decorate)decorate(card,r);nodes.set')
    a=s.index(' function draw(){',s.index('async function mountPositions'));b=s.index(' function edit(row,to){',a)
    s=s[:a]+(BASE/'org_card_actions.js').read_text(encoding='utf8')+s[b:]
    s=one(s,"function edit(row,to){","function edit(row,to,context={}){")
    s=one(s,"body.replaceChildren();status.textContent='';const form=make('form');form.className='hr-position-form';body.append(form);","""body.inert=true;for(const b of directoryButtons)b.disabled=true;
   status.textContent='';const form=make('form');form.className='hr-position-form';body.before(form);
   const messages={
     leader:text('Add a top-level position for this area. Existing reporting lines and access stay the same.','Adicione uma posição no nível superior desta área. Os vínculos existentes e os acessos permanecem iguais.'),
     above:text('Insert directly above the selected position. Only that position changes supervisor.','Insira diretamente acima do cargo selecionado. Somente esse cargo muda de superior.'),
     below:text('Add a position reporting to the selected position.','Adicione um cargo subordinado à posição selecionada.'),
     member:text('Choose an unplaced member and a role for their new position.','Escolha um membro sem posição e um cargo para ele.'),
     assign:text('Choose an eligible member or leave this position vacant.','Escolha um membro elegível ou deixe a posição vaga.')
   };if(context.kind)form.append(make('p',messages[context.kind]+(context.target?' · '+context.target.role_name+' · '+(context.target.person_name||text('Vacant','Vaga')):'')));""")
    s=one(s,"row?.department||data.departments","context.department||row?.department||data.departments")
    s=one(s,"data.people.filter(p=>p.departments.includes(dept.value))","data.people.filter(p=>p.departments.includes(dept.value)&&!data.positions.some(pos=>pos.department===dept.value&&pos.person===p.id&&pos.id!==row?.id))")
    s=one(s,"}options();dept.onchange=options;", """}options();
   dept.disabled=!!context.department;
   parent.disabled=['above','below','leader','assign'].includes(context.kind);
   role.disabled=context.kind==='assign';person.required=context.kind==='member';
   dept.onchange=options;""")
    s=one(s,"for(const c of form.elements)c.disabled=true;","const enabled=Array.from(form.elements).filter(c=>!c.disabled);for(const c of enabled)c.disabled=true;")
    s=one(s,"if(live())for(const c of form.elements)c.disabled=false","if(live())for(const c of enabled)c.disabled=false")
    s=one(s,"body:{revision:data.revision,id:row?.id||'',department:dept.value","body:{...(context.kind==='above'?{insert_above:context.target.id}:{}),revision:data.revision,id:row?.id||'',department:dept.value")
    return one(s,"};dept.focus()","};(context.kind==='assign'?person:context.department?role:dept).focus()")

def transforms():
    return {'app/org_positions.py':backend,'app/static/hr_workspace.js':ui,'app/static/ui132_visual.css':lambda s:s+"""
.org-card-actions{max-width:100%;text-align:start}.org-card-actions summary{cursor:pointer;padding:.45rem}
.org-card-actions button{display:block;width:100%;white-space:normal;margin:.25rem 0}.org-unit-actions{margin:.5rem 0;flex-wrap:wrap}
"""}
if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='37e49a802024f2bc5e60ea66f742dea07ed637beb6140d2d63674f080a715e09',overlays=(Path(__file__).name,),previous_cache='ui162-demo-org-example',cache='ui162-org-card-actions',suffix='org-card-actions',scope='Contextual organization chart editing and atomic insertion above a position.')
