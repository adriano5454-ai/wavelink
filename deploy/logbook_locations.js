 let logSiteFilter = '';
 const unassignedSite = '__unassigned__';
 const logWords = (en,pt) => WLWorkSites.words(pt,en);
 const unassignedLabel = () => logWords('Unassigned','Sem localização');
 const bookSite = book => book.vessel_scope?.site_id || unassignedSite;
 const bookSiteName = book => book.vessel_scope?.site_name || unassignedLabel();

 function groupedLogbooks(books) {
  const groups = new Map();
  for (const book of books) {
   const id = bookSite(book);
   if (logSiteFilter && logSiteFilter!==id) continue;
   if (!groups.has(id)) groups.set(id,{id,name:bookSiteName(book),books:[]});
   groups.get(id).books.push(book);
  }
  const sorted = [...groups.values()].sort((a,b) => {
   if (a.id===unassignedSite) return 1;
   if (b.id===unassignedSite) return -1;
   return a.name.localeCompare(b.name,document.documentElement.lang);
  });
  if (!sorted.length) return `<p class="log-site-empty" role="status">${logWords('No logbooks at this location.','Nenhum diário nesta localização.')}</p>`;
  return sorted.map(group => `<section class="log-site-group" aria-label="${esc(group.name)}"><h2>${esc(group.name)} <small>(${group.books.length})</small></h2><div class="log-book-grid">${group.books.map(bookCard).join('')}</div></section>`).join('');
 }

 function logSiteBrowser(books, sites) {
  const choices = new Map(sites.filter(site=>site.active).map(site=>[site.id, WLWorkSites.describe(site)]));
  for (const book of books) {
   const id=bookSite(book);
   if (id!==unassignedSite && !choices.has(id)) choices.set(id,bookSiteName(book));
  }
  const options = [...choices].sort((a,b)=>a[1].localeCompare(b[1],document.documentElement.lang));
  options.unshift(['',logWords('All locations','Todas as localizações')]);
  options.push([unassignedSite,unassignedLabel()]);
  if (!options.some(([id])=>id===logSiteFilter)) logSiteFilter='';
  return `<label class="field log-location-filter"><span>${esc(WLWorkSites.label())}</span><select id="logs-location-filter" aria-controls="logs-by-site">${options.map(([id,name])=>`<option value="${esc(id)}" ${id===logSiteFilter?'selected':''}>${esc(name)}</option>`).join('')}</select></label><div id="logs-by-site">${groupedLogbooks(books)}</div>`;
 }

 function bindLogSiteFilter(books) {
  const filter = document.getElementById('logs-location-filter');
  if (!filter) return;
  filter.onchange = () => {
   logSiteFilter=filter.value;
   const container=document.getElementById('logs-by-site');
   AJViewStability.paint(container,groupedLogbooks(books));
  };
 }

 function bookLocationLine(book, allowAssignment=false) {
  const canAssign=allowAssignment && !book.vessel_scope && state.auth?.person?.role==='admin';
  return `<p class="log-site-line">${esc(WLWorkSites.label())} · <strong>${esc(bookSiteName(book))}</strong>${canAssign?` <button type="button" id="log-assign-location" class="btn ghost">${logWords('Assign location','Atribuir localização')}</button>`:''}</p>`;
 }

 function assignLogbookLocation(book) {
  if (book.vessel_scope || state.auth?.person?.role!=='admin') return;
  const title=logWords('Assign location','Atribuir localização');
  modal(title,`<form id="log-site-form"><p><strong>${esc(book.name)}</strong></p><p>${logWords('All existing and future entries inherit this location. The logbook keeps this location once assigned.','Todos os lançamentos atuais e futuros herdam esta localização. O diário mantém a localização após a atribuição.')}</p><div id="log-site-picker"></div><label class="field"><span>${logWords('Reason','Motivo')}</span><input name="reason" required maxlength="1000"></label><p role="status"></p><button type="submit" class="btn">${title}</button></form>`);
  const form=document.getElementById('log-site-form');
  const picker=WLWorkSites.picker(form.querySelector('#log-site-picker'),api);
  const owner=readContext();
  const button=form.querySelector('button[type="submit"]');
  form.onsubmit=async event=>{
   event.preventDefault();
   if (button.disabled || !ownsRead(owner)) return;
   try {
    const siteId=picker.read();
    if (!siteId) {form.querySelector('p[role="status"]').textContent=WLWorkSites.choose();return;}
    const reason=form.elements.reason.value.trim();
    if (!reason) {form.elements.reason.focus();return;}
    button.disabled=true;
    await api('/api/fleet/logs/books/'+encodeURIComponent(book.id)+'/scope',{method:'POST',
     body:{site_id:siteId,version:0,enabled:false,reason,confirmed:true},beforeSend:()=>requireRead(owner)});
    if (!ownsRead(owner)) return;
    dlg.close();
    await open();
   } catch(error) {
    if (ownsRead(owner)) {form.querySelector('p[role="status"]').textContent=error.message;button.disabled=false;}
   }
  };
 }
