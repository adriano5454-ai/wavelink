 const directoryButtons=[];
 function start(row,to,context={}){
   if(!live()||busy||container.querySelector('form'))return;
   editing=true;draw();edit(row,to,context);
 }
 function directoryActions(){
   if(!data.editor||directoryButtons.length)return;
   const cards=container.parentElement.querySelectorAll('.hr-org-unit');
   for(const card of cards){
     const department=data.departments.find(d=>d.name===card.querySelector('h3').textContent);
     if(!department)continue;
     const actions=make('div');actions.className='actions org-unit-actions';
     for(const [label,kind] of [[text('Add area leader','Adicionar líder da área'),'leader'],[text('Add person to chart','Adicionar pessoa ao organograma'),'member']]){
       const control=button(label,()=>start(null,null,{department:department.id,kind}));
       actions.append(control);directoryButtons.push(control);
     }
     card.querySelector('h3').after(actions);
   }
 }
 function cardActions(card,r){
   const menu=make('details');menu.className='org-card-actions';const summary=make('summary',text('Actions','Ações'));menu.append(summary);card.append(menu);
   const context={department:r.department,target:r};
   menu.append(button(text('Add position above','Adicionar cargo acima'),()=>start(null,r.parent,{...context,kind:'above'})),
     button(text('Add position below','Adicionar cargo abaixo'),()=>start(null,r.id,{...context,kind:'below'})),
     button(text('Assign or change person','Atribuir ou trocar pessoa'),()=>start(r,undefined,{...context,kind:'assign'})),
     button(text('Edit position','Editar posição'),()=>start(r)));
   card.draggable=true;
   card.ondragstart=e=>{if(e.target.closest('a,button,summary')){e.preventDefault();return}e.dataTransfer.setData('text/x-wavelink-position',r.id)};
   card.ondragover=e=>e.preventDefault();
   card.ondrop=e=>{e.preventDefault();const src=data.positions.find(x=>x.department===r.department&&x.id===e.dataTransfer.getData('text/x-wavelink-position'));if(src&&src.id!==r.id)start(src,r.id)};
 }
 function draw(){
   container.querySelector('.hr-position-form')?.remove();body.inert=false;
   for(const b of directoryButtons)b.disabled=false;
   status.textContent='';directoryActions();drawOrgTree(body,data,()=>{editing=true;draw()},editing?cardActions:null);
   if(editing){
     const controls=make('div');controls.className='actions';
     controls.append(button(text('View chart','Ver organograma'),()=>{editing=false;draw()}),button(text('Add position','Adicionar posição'),()=>start(null)));
     body.prepend(controls);
   }
 }
