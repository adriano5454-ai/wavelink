"""Integrate the Fleet vessel selector with the operational registers."""


def replace(source, original, updated, count=1):
    found = source.count(original)
    if found != count:
        raise RuntimeError(f"Vessel filter integration expected {count} occurrence(s) of {original!r}, found {found}")
    return source.replace(original, updated)


def task_workspace(source):
    source = replace(source, 'select[name="task-status"]\'', 'select[name="task-status"],select[data-page-vessel]\'')
    source = replace(source, '  const matches=t=>', """  const vessels=window.WLPageVessels;
  const vesselMatches=t=>!filter.vessel || vessels.matches(t,filter.vessel,root.querySelector('[data-page-vessel]'));
  const matches=t=>""")
    source = replace(source, '.includes(q)&&status&&(filter.kind', '.includes(q)&&vesselMatches(t)&&status&&(filter.kind')
    source = replace(source, '}<details id="task-filter-options"', '}${vessels?.field(filter.vessel)||\'\'}<details id="task-filter-options"')
    source = replace(source, '${tasks.length} available in this access scope', '${tasks.filter(vesselMatches).length} available in this access scope')
    source = replace(source, "Object.assign(filter,{query:'',kind:", "Object.assign(filter,{vessel:'',query:'',kind:")
    source = replace(source, "  draw();paintPreview();if(previewId)select(previewId);", """  const selector=view.querySelector('[data-page-vessel]');
  if(selector)vessels.bind(selector,{api,value:filter.vessel,onChange(id){
   if(!safe()){selector.value=filter.vessel||'';return;}
   filter.vessel=id;listScroll=0;scroll.scrollTop=0;draw();
  }}).then(ready=>{if(ready&&filter.vessel&&current())draw();});
  draw();paintPreview();if(previewId)select(previewId);""")
    return source


def operations(source):
    return replace(source, "{query:'',kind:'all',status:'open',expanded:false,reviewOnly:false}",
                   "{vessel:'',query:'',kind:'all',status:'open',expanded:false,reviewOnly:false}", 2)


def maintenance(source):
    source = replace(source, "({orderPage:0,query:", "({orderPage:0,vessel:'',query:")
    source = replace(source, "prefs.view!=='open'||prefs.routine||", "prefs.view!=='open'||prefs.vessel||prefs.routine||")
    source = replace(source, "</label>${button('mw-filters'", "</label>${window.WLPageVessels?.field(prefs.vessel)||''}${button('mw-filters'")
    source = replace(source, '<span>${jobs.filter(j=>matches(j,id,ctx.now())).length}</span>', '<span></span>')
    source = replace(source, "views.map(([id,label])=>[id,label+' ('+jobs.filter(j=>matches(j,id,ctx.now())).length+')'])", "views")
    source = replace(source, "      click('mw-clear',", """      const selector=ctx.root.querySelector('[data-page-vessel]');
      if(selector)window.WLPageVessels.bind(selector,{api,value:prefs.vessel,onChange(id){
        if(!safe(selector)){selector.value=prefs.vessel;return;}
        prefs.vessel=id;prefs.orderPage=0;prefs.scroll=0;drawRows();
      }}).then(ready=>{if(ready&&prefs.vessel&&selector.isConnected&&active())drawRows();});
      click('mw-clear',""")
    source = replace(source, "const rows=filtered(data.jobs||[],prefs,ctx.now(),ctx.userId());", """const selector=ctx.root.querySelector('[data-page-vessel]');
      const jobs=(data.jobs||[]).filter(job=>!prefs.vessel || window.WLPageVessels.matches(job,prefs.vessel,selector));
      const rows=filtered(jobs,prefs,ctx.now(),ctx.userId());
      for(const [id,label] of views){
        const count=jobs.filter(job=>matches(job,id,ctx.now())).length;
        const badge=ctx.root.querySelector('[data-mw-view="'+id+'"] span'),option=el('mw-show').querySelector('option[value="'+id+'"]');
        if(badge)badge.textContent=count;
        if(option)option.textContent=label+' ('+count+')';
      }""")
    source = replace(source, "(data.jobs||[]).length", "jobs.length", 3)
    return source


def checklist(source):
    source = replace(source, "{query:'',type:'',view:'open',sort:'updated'", "{vessel:'',query:'',type:'',view:'open',sort:'updated'", 2)
    source = replace(source, "if (prefs.type || prefs.view", "if (prefs.vessel || prefs.type || prefs.view")
    source = replace(source, "    function readyToNavigate()", """    const vesselRecords=()=>allowed().filter(row=>!prefs.vessel || window.WLPageVessels.matches(row,prefs.vessel,root.querySelector('[data-page-vessel]')));
    function readyToNavigate()""")
    source = replace(source, '</label><button type="button" class="btn secondary" id="cw-filter-toggle"',
                     '</label>${window.WLPageVessels?.field(prefs.vessel)||\'\'}<button type="button" class="btn secondary" id="cw-filter-toggle"')
    source = replace(source, "const records = allowed(), rows", "const records = vesselRecords(), rows")
    source = replace(source, "if (!filtered(allowed(),prefs)", "if (!filtered(vesselRecords(),prefs)")
    source = replace(source, ":records.length?__wl118.t('No matching checklists')", ":prefs.vessel||records.length?__wl118.t('No matching checklists')")
    source = replace(source, "${records.length?__wl118.t('Clear or change", "${prefs.vessel||records.length?__wl118.t('Clear or change")
    source = replace(source, "    function bind() {", """    function bind() {
      const selector=root.querySelector('[data-page-vessel]');
      if(selector)window.WLPageVessels.bind(selector,{api,value:prefs.vessel,onChange(id){
        if(!readyToNavigate()){selector.value=prefs.vessel;return;}
        prefs.vessel=id;prefs.listScroll=0;update();
      }}).then(ready=>{if(ready&&prefs.vessel&&selector.isConnected&&active())update();});""")
    return source


def handovers(source):
    source = replace(source, ' let filters=', """ let vesselId='';
 const appliesToVessel=row=>!vesselId||window.WLPageVessels.matches(row,vesselId,el('ho-vessel-filter')?.querySelector('select'));
 const vesselRows=()=>!vesselId?rows:rows.filter(appliesToVessel);
 let filters=""")
    source = replace(source, 'function reset(){preview.close();', "function reset(){vesselId='';preview.close();")
    source = replace(source, '</nav><section id="ho-days-panel">',
                     '</nav><div id="ho-vessel-filter">${window.WLPageVessels?.field(vesselId)||\'\'}</div><section id="ho-days-panel">')
    source = replace(source, "  el('ho-search').oninput=", """  const selector=el('ho-vessel-filter').querySelector('select');
  if(selector)window.WLPageVessels.bind(selector,{api,value:vesselId,onChange(id){
   if(!allowed()||editor||document.querySelector('dialog[open]')){selector.value=vesselId;return;}
   preview.close();vesselId=id;journalSelection={vessel_id:id};setJournalTab(journalTab);
  }}).then(ready=>{
   if(!ready||!vesselId||!directory||!selector.isConnected||editor)return;
   if(journalTab==='incoming')paintIncoming(directory.actor_id);
   if(journalTab==='drafts')paintSavedDrafts();
   if(journalTab==='days'&&el('ho-more').open)paintRows();
  });
  el('ho-search').oninput=""")
    source = replace(source, "el('ho-search').value='';el('ho-kind').value='';",
                     "vesselId='';if(selector)selector.value='';journalSelection={};el('ho-search').value='';el('ho-kind').value='';")
    source = replace(source, "  const more=el('ho-more');", """  const vesselField=el('ho-vessel-filter');
  if(vesselField)vesselField.hidden=!['days','drafts','incoming'].includes(journalTab);
  const more=el('ho-more');""")
    source = replace(source, 'selection:journalSelection,preferredDepartment:', 'selection:Object.assign(journalSelection,{vessel_id:vesselId}),preferredDepartment:')
    source = replace(source, 'mountInbox({host,rows,actor:', 'mountInbox({host,rows:vesselRows(),actor:')
    source = replace(source, 'list=rows.filter(r=>(!filters.kind', 'list=vesselRows().filter(r=>(!filters.kind')
    source = replace(source, 'drafts=rows.filter(x=>x.mine', 'drafts=vesselRows().filter(x=>x.mine')
    source = replace(source, "host.hidden=false;dailyReset();dayFilters.date=dayFilters.date||todayLocal();",
                     """host.hidden=false;dailyReset();dayFilters.date=dayFilters.date||todayLocal();
  const locations=directory.daily.locations.filter(location=>appliesToVessel({location}));
  if(vesselId&&!appliesToVessel({location:dayFilters.location}))dayFilters.location=locations[0]||'';""")
    source = replace(source, '${directory.daily.locations.map(v=>', '${locations.map(v=>')
    source = replace(source, "  if(!wanted.date||!wanted.location.trim()||!wanted.department){", """  if(vesselId&&wanted.location.trim()&&!appliesToVessel({location:wanted.location})){
   host.textContent=window.WavelinkUX.text('Escolha um local da embarcação selecionada.','Choose a location for the selected vessel.');
   return;
  }
  if(!wanted.date||!wanted.location.trim()||!wanted.department){""")
    return source


def handover_workspace(source):
    source = replace(source, "Object.keys(r.selection).length!==4||['subject_key','date_from','date_to','include_archived'].some",
                     "Object.keys(r.selection).length!==(selection.vessel_id?5:4)||['subject_key','date_from','date_to','include_archived',...(selection.vessel_id?['vessel_id']:[])].some")
    source = replace(source, "include_archived:!!selection.include_archived});",
                     "include_archived:!!selection.include_archived,...(selection.vessel_id?{vessel_id:selection.vessel_id}:{})});")
    source = replace(source, "'/api/handovers/overview/subjects?include_archived='+!!selection.include_archived",
                     "'/api/handovers/overview/subjects?include_archived='+!!selection.include_archived+(selection.vessel_id?'&vessel_id='+encodeURIComponent(selection.vessel_id):'')")
    source = replace(source, "d?.format!==FORMAT||d.actor_id!==actor||!Array.isArray(d.subjects)",
                     "d?.format!==FORMAT||d.actor_id!==actor||(d.vessel_id||'')!==(selection.vessel_id||'')||!Array.isArray(d.subjects)")
    return source


def handovers_api(source):
    boundary = source.index("    @app.get('/api/handovers/overview/subjects')")
    head, tail = source[:boundary], source[boundary:]
    tail = replace(tail, "include_archived: bool = False, auth=Depends(credentials))", "include_archived: bool = False, vessel_id: str = '', auth=Depends(credentials))", 3)
    tail = replace(tail, "overview_service.catalog(*auth, include_archived=include_archived)",
                   "overview_service.catalog(*auth, include_archived=include_archived, vessel_id=vessel_id)")
    tail = replace(tail, "date_to=date_to, include_archived=include_archived)", "date_to=date_to, include_archived=include_archived, vessel_id=vessel_id)", 2)
    return head + tail


def handover_overview(source):
    source = replace(source, "or set(value) != {'subject_key'", "or set(value) - {'vessel_id'} != {'subject_key'")
    source = replace(source, "    return dict(subject_key=key,", """    vessel_id = value.get('vessel_id', '')
    if not isinstance(vessel_id, str) or len(vessel_id) > 200:
        raise Problem(422, 'Choose a vessel from Ships and bases.')
    return dict(**({'vessel_id': vessel_id} if vessel_id else {}), subject_key=key,""")
    source = replace(source, "def _collect(self, con, person, include_archived):", """def _collect(self, con, person, include_archived, actor, vessel_id=''):
        from .work_locations import SiteLookup, catalog
        lookup = SiteLookup(catalog(con, actor)) if vessel_id else None

        def matches_vessel(location, ref=None):
            if not lookup:
                return True
            if ref and ref.get('name') == location and ref.get('id'):
                site = lookup.by_id.get(ref['id'])
                return bool(site and site['kind'] == 'vessel' and site['id'] == vessel_id)
            return any(site['id'] == vessel_id and site['kind'] == 'vessel'
                       for site in lookup.resolve({'location': location}))
""")
    source = replace(source, "            if cfg:\n                g = group", "            if cfg and matches_vessel(cfg['values']['location']):\n                g = group")
    source = replace(source, "            day = daily['operational_date']", """            if not matches_vessel(location, rec.get('work_site')):
                continue
            day = daily['operational_date']""")
    source = replace(source, "def catalog(self, actor, token=None, *, include_archived=False):",
                     "def catalog(self, actor, token=None, *, include_archived=False, vessel_id=''):")
    source = replace(source, "self._collect(con, person, include_archived)", "self._collect(con, person, include_archived, actor, vessel_id)")
    source = replace(source, "return dict(format=FORMAT, actor_id=person['id'], include_archived=",
                     "return dict(**({'vessel_id': vessel_id} if vessel_id else {}), format=FORMAT, actor_id=person['id'], include_archived=")
    source = replace(source, "self._collect(con, person, chosen['include_archived'])",
                     "self._collect(con, person, chosen['include_archived'], actor, chosen.get('vessel_id', ''))")
    return source


def transforms():
    return {
        'app/static/task_workspace.js': task_workspace,
        'app/static/operations.js': operations,
        'app/static/maintenance_workspace.js': maintenance,
        'app/static/checklist_workspace.js': checklist,
        'app/static/handovers.js': handovers,
        'app/static/handover_workspace.js': handover_workspace,
        'app/handovers_api.py': handovers_api,
        'app/handover_overview.py': handover_overview,
    }
