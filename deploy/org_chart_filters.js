let filterOwner, chartFilters;
function drawOrgTree(host,data,edit,decorate){
 const owner=identity();
 if(filterOwner!==owner){filterOwner=owner;chartFilters={}}
 if(decorate||!data.positions.length){paintOrgTree(host,data,edit,decorate);return}
 host.replaceChildren();
 const controls=document.createElement('div'), results=document.createElement('div'), count=document.createElement('p');
 controls.className='org-filter-controls';count.setAttribute('role','status');
 host.append(controls,count,results);
 const fields={}, text=orgText;
 function field(key,label,options){
   const wrapper=document.createElement('label'), input=document.createElement(options?'select':'input');
   wrapper.textContent=label;wrapper.append(input);controls.append(wrapper);fields[key]=input;
   if(options){
     for(const [id,name] of options)input.add(new Option(name,id));
   }else{input.type='search'}
   input.value=chartFilters[key]||'';
   chartFilters[key]=input.value;
   input.addEventListener(options?'change':'input',()=>{chartFilters[key]=input.value;refresh()});
 }
 const rows=data.positions, byId=new Map(rows.map(r=>[r.id,r]));
 const options=(key,label)=>Array.from(new Map(rows.filter(r=>r[key]).map(r=>[r[key],r[label]||r[key]]))).sort((a,b)=>a[1].localeCompare(b[1]));
 const all=['',text('Todos','All')];
 field('query',text('Buscar nome ou cargo','Search name or role'));
 field('department',text('Departamento','Department'),[all,...options('department','dept_name')]);
 const vessels=options('vessel_id','vessel_name');
 if(vessels.length)field('vessel',text('Embarcação','Vessel'),[all,...vessels]);else delete chartFilters.vessel;
 field('status',text('Situação do cargo','Position status'),[all,['filled',text('Ocupado','Filled')],['vacant',text('Vago','Vacant')]]);
 const clear=document.createElement('button');clear.type='button';clear.className='btn secondary';clear.textContent=text('Limpar filtros','Clear filters');controls.append(clear);
 clear.onclick=()=>{chartFilters={};Object.values(fields).forEach(input=>input.value='');refresh();fields.query.focus()};
 const plain=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 function refresh(){
   const f=chartFilters, terms=plain(f.query).trim().split(/\s+/).filter(Boolean);
   const active=Boolean(terms.length||f.department||f.vessel||f.status);
   const matches=new Set(), visible=new Set();
   for(const row of rows){
     if(f.department&&row.department!==f.department||f.vessel&&row.vessel_id!==f.vessel||f.status&&(row.person?'filled':'vacant')!==f.status)continue;
     const name=plain([row.role_name,row.person_name].join(' '));
     if(!terms.every(term=>name.includes(term)))continue;
     matches.add(row.id);
     for(let r=row;r&&!visible.has(r.id);r=byId.get(r.parent))visible.add(r.id);
   }
   count.textContent=text('Cargos encontrados','Matching positions')+' · '+matches.size;
   clear.disabled=!active;
   if(!matches.size){results.textContent=text('Nenhum cargo corresponde aos filtros.','No positions match these filters.');return}
   paintOrgTree(results,{...data,positions:rows.filter(r=>visible.has(r.id))},edit,decorate,active?matches:null);
 }
 refresh();
}
