async function mountPositions(container){
 const live=()=>current()&&container.isConnected&&view==='org';
 const t=orgText, text=(en,pt)=>t(pt,en);
 const make=(tag,value)=>{const e=document.createElement(tag);if(value!==undefined)e.textContent=value;return e};
 const button=(label,act)=>{const b=make('button',label);b.type='button';b.className='btn secondary';b.onclick=act;return b};
 let data, busy=false;
 const status=make('p');status.setAttribute('role','status');
 const body=make('div');container.append(status,body);
 const error=e=>{if(live())status.textContent=e.message};
 async function read(){
   try{const next=await H.api('/api/hr/org-positions');if(live()){data=next;draw()}}catch(e){error(e)}
 }
 function draw(){
   body.replaceChildren();status.textContent='';
   if(!data.positions.length&&!data.editor)return;
   body.append(make('h2',text('Reporting positions','Posições e subordinação')));
   if(data.editor){
     body.append(button(text('Add position','Adicionar posição'),()=>edit(null)));
     body.append(make('p',text('Assign existing department members. Review access separately in People & access.','Atribua membros do departamento. Revise os acessos separadamente em Pessoas e acessos.')));
   }
   const groups=new Map();
   for(const r of data.positions){if(!groups.has(r.department))groups.set(r.department,[]);groups.get(r.department).push(r)}
   for(const rows of groups.values()){
     const section=make('section');body.append(section);section.append(make('h3',rows[0].dept_name));
     const children=new Map();for(const r of rows){if(!children.has(r.parent))children.set(r.parent,[]);children.get(r.parent).push(r)}
     const stack=(children.get(null)||[]).slice().reverse().map(r=>[r,0]);
     while(stack.length){const [r,depth]=stack.pop();const line=make('div');line.className='hr-position-row';line.style.marginInlineStart=Math.min(3,depth)*0.8+'rem';
       const title=r.role_name+' · '+(r.person_name||text('Vacant','Vaga'));
       line.append(make('strong',title));if(r.parent){const parent=rows.find(x=>x.id===r.parent);line.append(make('small',text('Reports to: ','Reporta a: ')+parent.role_name+(parent.person_name?' · '+parent.person_name:'')))}
       if(data.editor){line.append(button(text('Edit position','Editar posição'),()=>edit(r)));line.draggable=true;
         line.ondragstart=e=>e.dataTransfer.setData('text/x-wavelink-position',r.id);
         line.ondragover=e=>e.preventDefault();line.ondrop=e=>{e.preventDefault();const src=rows.find(x=>x.id===e.dataTransfer.getData('text/x-wavelink-position'));if(src&&src.id!==r.id)edit(src,r.id)};
       }section.append(line);for(const child of (children.get(r.id)||[]).slice().reverse())stack.push([child,depth+1]);
     }
   }
 }
 function edit(row,to){
   body.replaceChildren();status.textContent='';const form=make('form');form.className='hr-position-form';body.append(form);
   const select=(label)=>{const l=make('label',label),s=make('select');l.append(s);form.append(l);return s};
   const fill=(s,list,first,value)=>{s.replaceChildren(new Option(first,''));for(const x of list)s.add(new Option(x.name,x.id));s.value=value||''};
   const input=label=>{const l=make('label',label),i=make('input');i.maxLength=100;l.append(i);form.append(l);return i};
   const dept=select(text('Department','Departamento'));fill(dept,data.departments,text('New department','Novo departamento'),row?.department||data.departments[0]?.id);
   const dn=input(text('New department name','Nome do novo departamento'));
   const role=select(text('Role','Cargo'));fill(role,data.roles,text('New role','Novo cargo'),row?.role);
   const rn=input(text('New role name','Nome do novo cargo'));
   const parent=select(text('Reports to','Reporta a')),person=select(text('Person','Pessoa'));
   function options(){dn.parentElement.hidden=!!dept.value;rn.parentElement.hidden=!!role.value;
     fill(parent,data.positions.filter(p=>p.department===dept.value&&p.id!==row?.id).map(p=>({id:p.id,name:p.role_name+' · '+(p.person_name||text('Vacant','Vaga'))})),text('Top level','Nível superior'),to??row?.parent);
     fill(person,data.people.filter(p=>p.departments.includes(dept.value)),text('Vacant','Vaga'),row?.person);
   }options();dept.onchange=options;role.onchange=()=>{rn.parentElement.hidden=!!role.value};
   const submit=make('button',text('Save position','Salvar posição'));submit.className='btn';form.append(submit,button(text('Cancel','Cancelar'),draw));
   form.onsubmit=async e=>{e.preventDefault();if(busy||!live())return;busy=true;for(const c of form.elements)c.disabled=true;
     try{const next=await H.api('/api/hr/org-positions',{method:'POST',body:{revision:data.revision,id:row?.id||'',department:dept.value,new_department:dept.value?'':dn.value.trim(),role:role.value,new_role:role.value?'':rn.value.trim(),parent:parent.value,person:person.value},beforeSend:()=>{if(!live())throw Error(text('Chart closed','Organograma fechado'))}});
       if(live()){data=next;draw()}
     }catch(err){error(err);if(live())for(const c of form.elements)c.disabled=false}finally{busy=false}
   };dept.focus()
 }
 await read();
}
