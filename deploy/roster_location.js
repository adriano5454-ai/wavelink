 function rosterProjectOptions(ws) {
  const codes = new Set();
  for (const person of ws?.roster || []) {
   if (person.programming_status === 'restricted') continue;
   for (const shift of person.assignments || []) if (shift.project) codes.add(shift.project);
  }
  return codes;
 }

 function bindRosterProjects(input, list, ws, context) {
  const codes = rosterProjectOptions(ws);
  const draw = () => list.replaceChildren(...Array.from(codes).sort().map(value => new Option(value)));
  input.setAttribute('list',list.id);
  draw();
  H.api('/api/hr/timesheet-projects',{beforeSend:context.before}).then(data => {
   if (!context.same() || !list.isConnected) return;
   for (const project of data.projects || []) if (project.active && project.name) codes.add(project.name);
   draw();
  }).catch(() => {}); // Free entry and saved assignment codes remain available.
 }

 function locationRosterHtml() {
  return '<details id="hr-location-roster" class="hr-panel"><summary><strong>'+
   E(wtext('Escala por embarcação ou local','Roster by vessel or location'))+'</strong></summary>'+
   '<p>'+E(wtext('Escalas de trabalho na data escolhida. A escala confirmada não comprova presença.', 'Work assignments on the selected date. A confirmed assignment does not establish attendance.'))+'</p>'+
   '<form class="hr-filter-grid">'+field('roster_day',wtext('Data da escala','Roster date'),localDay(),'date',10,true)+
   field('roster_project',wtext('Número ou nome do projeto (opcional)','Project number or name (optional)'),workspaceFilters.project)+
   '<datalist id="hr-location-projects"></datalist><button class="btn secondary" type="submit">'+E(wtext('Consultar','Show roster'))+'</button></form>'+
   '<section data-location-results aria-live="polite"></section></details>';
 }

 function groupedRoster(ws, day) {
  const groups = new Map(), unassigned = [];
  for (const person of ws.roster || []) {
   if (person.programming_status === 'restricted') continue;
   const rows = (person.assignments || []).filter(r => ['offshore','onshore'].includes(r.assignment_type || 'offshore') &&
    r.status !== 'cancelled' && r.start_on <= day && day <= r.end_on);
   if (!rows.length && person.enabled !== false) unassigned.push(person.name);
   for (const row of rows) {
    const place = (row.work_site?.name || row.location || '').trim();
    const key = row.work_site?.id ? 'site:' + row.work_site.id : 'label:' + place.toLowerCase();
    if (!groups.has(key)) groups.set(key,{place,people:new Map()});
    const people = groups.get(key).people;
    if (!people.has(person.id)) people.set(person.id,{name:person.name,assignments:new Set()});
    people.get(person.id).assignments.add([window.AJHRPlanning.stateLabel(row.status),row.shift_name,row.project].filter(Boolean).join(' · '));
   }
  }
  const parts = Array.from(groups.values()).sort((a,b)=>a.place.localeCompare(b.place)).map(group =>
   '<article class="hr-panel"><h3>'+E(group.place || wtext('Local não informado','Location not recorded'))+' ('+group.people.size+')</h3><ul>'+
   Array.from(group.people.values()).sort((a,b)=>a.name.localeCompare(b.name)).map(p=>'<li><strong>'+E(p.name)+'</strong> — '+E([...p.assignments].join(' / '))+'</li>').join('')+'</ul></article>');
  if (!parts.length) parts.push('<p>'+E(wtext('Nenhuma escala de trabalho nesta consulta.','No work assignments match this query.'))+'</p>');
  if (unassigned.length && !ws.truncated) parts.push('<details><summary>'+E(wtext('Sem escala de trabalho nesta consulta','Without a work assignment in this query'))+' ('+unassigned.length+')</summary><ul>'+unassigned.map(n=>'<li>'+E(n)+'</li>').join('')+'</ul></details>');
  if (ws.truncated) parts.unshift('<p class="notice">'+E(wtext('Resultado parcial. Refine os filtros.','Partial results. Refine the filters.'))+'</p>');
  return parts.join('');
 }

 function bindLocationRoster(panel) {
  if (!panel) return;
  const context = capture(), controls = panel.querySelector('form'), output = panel.querySelector('[data-location-results]');
  const day = controls.elements.roster_day, project = controls.elements.roster_project;
  let request = 0, initialized = false;
  async function load() {
   const ticket = ++request, selected = day.value;
   output.replaceChildren();
   if (!selected || !day.validity.valid) return;
   const params = new URLSearchParams({...workspaceFilters,start_on:selected,end_on:selected,
    project:project.value.trim(),user_id:workspaceScope.user_id});
   output.textContent=wtext('Consultando escalas…','Loading assignments…');
   const current=()=>panel.isConnected && context.same() && ticket===request;
   try {
    const data=await H.api('/api/hr/workspace?'+params,{beforeSend:context.before});
    if (current()) output.innerHTML=groupedRoster(data,selected);
   } catch (error) { if (current()) output.textContent=H.message(error); }
  }
  panel.ontoggle=()=>{
   if (!panel.open || initialized) return;
   initialized=true;
   bindRosterProjects(project,panel.querySelector('datalist'),workspace,context);
   load();
  };
  controls.onsubmit=event=>{event.preventDefault();load();};
  day.onchange=load;
  project.onchange=load;
 }
