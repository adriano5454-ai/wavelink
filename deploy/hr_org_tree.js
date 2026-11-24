let treeOwner='', folded=new Set(), returnLink=null;
function drawOrgTree(container,data,edit){
 if(treeOwner!==identity()){treeOwner=identity();folded.clear();returnLink=null}
 const text=orgText, el=(tag,value)=>{const e=document.createElement(tag);if(value!==undefined)e.textContent=value;return e};
 const btn=(label,fn)=>{const b=el('button',label);b.type='button';b.className='btn secondary';b.onclick=fn;return b};
 const persons=new Set(directory.org_chart.units.flatMap(u=>[...u.people,...u.heads]).map(p=>p.profile_id).filter(Boolean));
 container.replaceChildren();
 if(data.editor)container.append(btn(text('Editar estrutura','Edit structure'),edit));
 if(!data.positions.length){
   container.append(el('p',text('Nenhuma posição visível na estrutura. Consulte os departamentos abaixo.','No reporting positions visible. Browse the departments below.')));return;
 }
 const groups=new Map();
 for(const p of data.positions){if(!groups.has(p.department))groups.set(p.department,[]);groups.get(p.department).push(p)}
 for(const rows of groups.values()){
   const section=el('section');section.className='org-tree';section.tabIndex=0;section.setAttribute('aria-label',rows[0].dept_name);
   section.append(el('h3',rows[0].dept_name));container.append(section);
   const nodes=new Map(),children=new Map();
   for(const r of rows){
     const item=el('li'),card=el('div');card.className='org-node';item.append(card);
     card.append(el('strong',r.role_name));
     const link=persons.has(r.person)?el('a',r.person_name):el('span',r.person_name||text('Vaga','Vacant'));
     if(link.tagName==='A'){link.href='#profile/'+encodeURIComponent(r.person);link.dataset.orgPosition=r.id;
       link.onclick=()=>{returnLink={id:r.id,left:section.scrollLeft}}}
     card.append(link);nodes.set(r.id,item);
     if(!children.has(r.parent))children.set(r.parent,[]);children.get(r.parent).push(r);
   }
   for(const [parent,subordinates] of children){
     const list=el('ul');for(const r of subordinates)list.append(nodes.get(r.id));
     if(!parent){list.className='org-roots';section.append(list);continue}
     const item=nodes.get(parent);item.append(list);list.id='org-reports-'+parent;
     const toggle=btn('',()=>{if(folded.has(parent))folded.delete(parent);else folded.add(parent);sync()});
     const sync=()=>{list.hidden=folded.has(parent);toggle.setAttribute('aria-expanded',String(!list.hidden));
       toggle.textContent=(list.hidden?text('Expandir','Expand'):text('Recolher','Collapse'))+' ('+subordinates.length+')';
       toggle.setAttribute('aria-label',toggle.textContent+' · '+item.firstChild.firstChild.textContent)};
     toggle.setAttribute('aria-controls',list.id);item.firstChild.append(toggle);sync();
   }
   if(returnLink){const a=section.querySelector('[data-org-position="'+CSS.escape(returnLink.id)+'"]');
     if(a){section.scrollLeft=returnLink.left;a.focus();returnLink=null}}
 }
}
