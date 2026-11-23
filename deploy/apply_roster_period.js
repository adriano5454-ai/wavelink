 function locationRosterHtml() {
  return '<details id="hr-location-roster" class="hr-panel"><summary><strong>'+
   E(wtext('Escala por embarcação ou local','Roster by vessel or location'))+'</strong> · '+E(wtext('Dia ou período','Day or date range'))+'</summary>'+
   '<p>'+E(wtext('Consulte as alocações planejadas. Uma escala confirmada não comprova presença.', 'Review scheduled assignments. A confirmed assignment does not establish attendance.'))+'</p>'+
   '<form class="hr-filter-grid">'+field('roster_day',wtext('De','From'),localDay(),'date',10,true)+
   field('roster_until',wtext('Até (opcional, até 93 dias)','To (optional, up to 93 days)'),'','date')+
   field('roster_project',wtext('Número ou nome do projeto (opcional)','Project number or name (optional)'),workspaceFilters.project)+
   '<datalist id="hr-location-projects"></datalist><button class="btn secondary" type="submit">'+E(wtext('Consultar','Show roster'))+'</button></form>'+
   '<section data-location-results aria-live="polite"></section></details>';
 }

 function groupedRoster(ws, start, end) {
  const groups=new Map(), unassigned=[];
  for(const person of ws.roster || []){
   if(person.programming_status==='restricted')continue;
   const rows=(person.assignments || []).filter(r=>['offshore','onshore'].includes(r.assignment_type || 'offshore') &&
    r.status!=='cancelled' && r.start_on<=end && r.end_on>=start).sort((a,b)=>a.start_on.localeCompare(b.start_on)||a.end_on.localeCompare(b.end_on));
   if(!rows.length && person.enabled!==false)unassigned.push(person.name);
   for(const row of rows){
    const place=(row.work_site?.name || row.location || '').trim();
    const key=row.work_site?.id?'site:'+row.work_site.id:'label:'+place.toLowerCase();
    if(!groups.has(key))groups.set(key,{place,people:new Map()});
    const people=groups.get(key).people;
    if(!people.has(person.id))people.set(person.id,{name:person.name,rows:[]});
    people.get(person.id).rows.push(row);
   }
  }
  function allocation(row){
   const offshore=(row.assignment_type || 'offshore')==='offshore';
   const dates=offshore?wtext('Embarque previsto','Planned joining')+' '+date(row.start_on)+' · '+wtext('Desembarque previsto','Planned leaving')+' '+date(row.end_on):
    date(row.start_on)+' – '+date(row.end_on);
   return '<li>'+E(dates)+'<br>'+E([window.AJHRPlanning.stateLabel(row.status),row.shift_name,row.project].filter(Boolean).join(' · '))+'</li>';
  }
  const parts=Array.from(groups.values()).sort((a,b)=>a.place.localeCompare(b.place)).map(group=>
   '<article class="hr-panel"><h3>'+E(group.place || wtext('Local não informado','Location not recorded'))+' ('+group.people.size+')</h3>'+
   Array.from(group.people.values()).sort((a,b)=>a.name.localeCompare(b.name)).map(p=>'<section><strong>'+E(p.name)+'</strong><ul>'+p.rows.map(allocation).join('')+'</ul></section>').join('')+'</article>');
  if(!parts.length)parts.push('<p>'+E(wtext('Nenhuma escala de trabalho nesta consulta.','No work assignments match this query.'))+'</p>');
  if(unassigned.length && !ws.truncated)parts.push('<details><summary>'+E(wtext('Sem escala de trabalho nesta consulta','Without a work assignment in this query'))+' ('+unassigned.length+')</summary><ul>'+unassigned.map(n=>'<li>'+E(n)+'</li>').join('')+'</ul></details>');
  if(ws.truncated)parts.unshift('<p class="notice">'+E(wtext('Resultado parcial. Refine os filtros.','Partial results. Refine the filters.'))+'</p>');
  return parts.join('');
 }
