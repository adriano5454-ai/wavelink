"""Add local vessel selection to fleet, calendar, IT and HR read models."""


def change(source, old, new, count=1):
    if source.count(old) != count:
        raise ValueError(f"Expected {count} occurrences of {old!r}, found {source.count(old)}")
    return source.replace(old, new)


def fleet(source):
    source = change(source, "select('site-filter',__wl118.t('Site')",
                    "select('site-filter',__wl118.t('Vessel / base')")
    source = change(source, "$('asset-search').oninput=draw;",
                    "$('site-filter').setAttribute('data-page-vessel','');$('asset-search').oninput=draw;")
    source = change(source, "owner,query:'',filter:'all',origin:", "owner,query:'',vessel:'',filter:'all',origin:")
    anchor = "manifestViewState.query,'search')}</div>"
    source = change(source, anchor, anchor + "${WLPageVessels.field(manifestViewState.vessel)}")
    anchor = "$('manifest-search').oninput=draw;"
    source = change(source, anchor, """const vessel=root.querySelector('[data-page-vessel]');
 WLPageVessels.bind(vessel,{sites:dir.sites,value:manifestViewState.vessel,onChange:id=>{
  if(!alive())return;
  manifestViewState.vessel=id;
  draw();
 }});
 """ + anchor)
    source = change(source, "return;$('manifest-search').value='';", "return;manifestViewState.vessel='';vessel.value='';$('manifest-search').value='';")
    anchor = "<div>${select('receiving-site',__wl118.t('Receiving site'),[['',__wl118.t('All receiving sites')],...sites],receivingViewState.site)}</div>"
    source = change(source, anchor, "")
    source = change(source, '<details id="receiving-filters"', anchor + '<details id="receiving-filters"')
    source = change(source, "<summary>Site &amp; condition <span", "<summary>${__wl118.t('Condition')} <span")
    source = change(source, "const sites=[...new Map(items.map(x=>[x.site_id,x.site_name])).entries()];",
                    "const sites=dir.sites.map(site=>[site.id,site.name]);")
    source = change(source, "for(const id of ['receiving-search','receiving-site','receiving-condition'])",
                    "$('receiving-site').setAttribute('data-page-vessel','');\n for(const id of ['receiving-search','receiving-site','receiving-condition'])")
    anchor = "${button('cal-update',__wl118.t('Show dates'),'primary')}"
    source = change(source, anchor, '${WLPageVessels.field()}' + anchor)
    source = change(source, "const load=async()=>{let es=[];if(val('cal-source')", """const vessel=root.querySelector('[data-page-vessel]'),results=$('cal-results');
 let serial=0;
 const load=async()=>{const ticket=++serial,source=val('cal-source');
 const params=new URLSearchParams({start:val('cal-start'),end:val('cal-end'),vessel_id:vessel.value});
 let es=[];if(source""")
    source = change(source, """'/api/fleet/calendar?start='+enc(val('cal-start'))+'&end='+enc(val('cal-end'))""", """'/api/fleet/calendar?'+params""")
    source = change(source, """if(val('cal-source')!=='shipments'){const ls=await api(LOG+'/calendar?start='+enc(val('cal-start'))+'&end='+enc(val('cal-end')))""",
                    """if(source!=='shipments'){const ls=await api(LOG+'/calendar?'+params)""")
    source = change(source, "if(!$('cal-results'))return;$('cal-results').innerHTML=", "if(!results.isConnected||ticket!==serial)return;results.innerHTML=")
    return change(source, "on('cal-update',load);await load();", """WLPageVessels.bind(vessel,{sites:dir.sites,onChange:()=>load().catch(showError)});
 on('cal-update',load);await load();""")


def fleet_calendar(source):
    source = change(source, "def calendar(self,a,start,end):", "def calendar(self,a,start,end,vessel_id=''):")
    anchor = "        for m in self.manifests(a):"
    start = source.index("    def calendar(self,")
    return source[:start] + change(source[start:], anchor, """        from .work_locations import page_vessel_lookup
        with self.store.connection() as c:
            matches=page_vessel_lookup(c,a,vessel_id)
        for m in self.manifests(a):
            if not matches(m,'manifests'):continue""")


def fleet_log_calendar(source):
    source = change(source, "def calendar(self,actor,start,end,site_id=''):", "def calendar(self,actor,start,end,site_id='',vessel_id=''):")
    anchor = "            if site_id and not fleet_access.is_admin(c,actor) and not permissions(c,actor['user_id'],site_id)['logs.view']:"
    start=source.index("    def calendar(self,")
    end=source.find("\n    def ",start+5)
    if end < 0:end=len(source)
    calendar=change(source[start:end],anchor,"""            from .work_locations import page_vessel_lookup
            matches=page_vessel_lookup(c,actor,vessel_id)
""" + anchor)
    calendar=change(calendar,"if not s['site_active'] or (site_id", "if not s['site_active'] or not matches(s) or (site_id")
    return source[:start]+calendar+source[end:]


def manifest_ui(source):
    anchor = "function shipmentMatches(m,s={}){"
    return change(source, anchor, anchor + "\n  if(s.vessel&&s.vessel!==m.origin_id&&s.vessel!==m.destination_id)return false;")


def location_helpers(source):
    return source + '''


def page_vessel_lookup(c, actor, vessel_id):
    """Provide an exact, permission-scoped predicate for paged read models."""
    if not vessel_id:
        return lambda row, kind='': True
    sites = SiteLookup(catalog(c, actor))
    if sites.by_id.get(vessel_id, {}).get('kind') != 'vessel':
        return lambda row, kind='': False

    def matches(row, kind=''):
        if kind == 'manifests':
            return vessel_id in (row.get('origin_id'), row.get('destination_id'))
        meta = row.get('meta') or {}
        ref = row.get('work_site') or meta.get('work_site') or {}
        ident = ref.get('id') or row.get('site_id') or (row.get('vessel_scope') or {}).get('site_id')
        if ident:
            return ident == vessel_id
        if kind == 'travel':
            return any(sites.by_label.get(fold(row.get(key))) == {vessel_id} for key in ('origin', 'destination'))
        if kind == 'timesheets' and any(sites.by_label.get(fold(day.get('location'))) == {vessel_id}
                                        for day in row.get('entries', []) if isinstance(day, dict)):
            return True
        return any(site['id'] == vessel_id for site in sites.resolve(row, kind=kind))
    return matches
'''


def it_api(source):
    source = change(source, "limit: int = 50, person=Depends(logged)", "limit: int = 50, vessel_id: str = '', person=Depends(logged)")
    return change(source, "query, status, priority, offset, limit))", "query, status, priority, offset, limit, vessel_id))")


def it_store(source):
    source = change(source, "priority='', offset=0, limit=50):", "priority='', offset=0, limit=50, vessel_id=''):")
    source = change(source, "return dict(requests=records, total=total,", "return dict(requests=records, filter_location=filter_location, total=total,")
    anchor = "            if status: clauses.append('status=?'); values.append(status)"
    return change(source, anchor, """            filter_location = None
            if vessel_id:
                directory = sites.SiteLookup(sites.catalog(c, actor))
                if directory.by_id.get(vessel_id, {}).get('kind') in ('vessel', 'shore_base'):
                    filter_location = {'id': vessel_id, 'name': directory.by_id[vessel_id]['name']}
                    aliases = {key for key, ids in directory.by_label.items() if ids == {vessel_id}}
                    c.create_function('it_location_alias', 1, lambda text: sites.fold(text) in aliases)
                    # A saved ID always wins, and old names/codes must resolve to exactly one site.
                    clauses.append('''CASE WHEN COALESCE(NULLIF(json_extract(body,'$.work_site.id'),''),
                        NULLIF(json_extract(body,'$.site_id'),'')) IS NOT NULL
                        THEN COALESCE(NULLIF(json_extract(body,'$.work_site.id'),''),json_extract(body,'$.site_id'))=?
                        ELSE it_location_alias(COALESCE(NULLIF(json_extract(body,'$.work_site.name'),''),
                            CASE WHEN json_type(body,'$.work_site')='text' THEN json_extract(body,'$.work_site') END,
                            json_extract(body,'$.location'))) END''')
                    values.append(vessel_id)
                else:
                    clauses.append('0')
""" + anchor)


def it_ui(source):
    source = change(source, "priority:'',offset:0", "priority:'',vessel_id:'',offset:0", 4)
    source = change(source, "function filterSummary(){const labels=[];", """function savedLocationName(row){
  const name=row.work_site?.name||(typeof row.work_site==='string'?row.work_site:row.location);
  return typeof name==='string'?name.trim():'';
 }
 function filterSummary(){const labels=[];
  if(filters.vessel_id && data.filter_location?.id===filters.vessel_id)labels.push(t('Embarcação ou base: ','Vessel or base: ')+data.filter_location.name);
  """)
    source = change(source, "personLabel(row.requester,results.map(r=>r.requester)))+'</small></td>",
                    """personLabel(row.requester,results.map(r=>r.requester)))+'</small>'+(savedLocationName(row)?'<small>'+E(t('Local: ','Location: ')+savedLocationName(row))+'</small>':'')+'</td>""")
    source = change(source, "personLabel(row.requester,[row.requester,row.assignee]))+'</dd><dt>'",
                    """personLabel(row.requester,[row.requester,row.assignee]))+'</dd>'+(savedLocationName(row)?'<dt>'+E(t('Local','Location'))+'</dt><dd>'+E(savedLocationName(row))+'</dd>':'')+'<dt>'""")
    anchor = "function filtersMarkup(){"
    before, rest = source.split(anchor)
    rest = rest.replace("</label><label class=\"field\">", "</label>'+WLPageVessels.field(filters.vessel_id,{includeBases:true})+'<label class=\"field\">", 1)
    source = before + anchor + rest
    anchor = "  if(el('it-filters')){"
    return change(source, anchor, anchor + """
   const f=el('it-filters');
   WLPageVessels.bind(f.querySelector('[data-page-vessel]'),{api:H.api,value:filters.vessel_id,includeBases:true,onChange:id=>{
    if(!f.isConnected||!ready())return;
    filters={...filters,vessel_id:id,query:f.elements.query.value.trim(),status:f.elements.status.value,priority:f.elements.priority.value,offset:0};
    focusResults=true;open(true);
   }});""")


def calendar_api(source):
    source = change(source, "kinds:str='certificates,maintenance,tasks,toolbox',a=Depends(logged)", "kinds:str='certificates,maintenance,tasks,toolbox',vessel_id:str='',a=Depends(logged)")
    return change(source, "else kinds.split(','))", "else kinds.split(','),vessel_id)")


def calendar(source):
    source = change(source, "start, end, kinds=None):", "start, end, kinds=None, vessel_id=''):")
    anchor = "        def add(kind,source_id,"
    source = change(source, anchor, """        from .work_locations import page_vessel_lookup, linked_sites, visible_equipment_positions
        matches = page_vessel_lookup(c, actor, vessel_id)
        def add(record,kind,source_id,""")
    source = change(source, "if start<=d<=end:", "if start<=d<=end and matches(record,kind):")
    for kind in ['certificates','maintenance','tasks','toolbox','checklists','inventory','logs','manifests']:
        old = "add('" + kind + "',"
        source = change(source, old, "add(" + ('m' if kind == 'manifests' else 'b') + ",'" + kind + "',", 2 if kind == 'tasks' else 1)
    for table, kind in [('maintenance_jobs','maintenance'),('asset_certificates','certificate')]:
        anchor = f"            for b in rows(c,'{table}'):"
        source = change(source, anchor, f"""            records=rows(c,'{table}')
            positions=linked_sites(c,actor,'{kind}',records) if vessel_id else {{}}
            for b in records:
                if not b.get('work_site') and positions.get(b['id']):
                    b={{**b,'work_site':positions[b['id']]}}""")
    source = change(source, "            for b in rows(c,'inventory_items'):", """            records=rows(c,'inventory_items')
            positions=visible_equipment_positions(c,actor,[r['id'] for r in records]) if vessel_id else {}
            for b in records:
                if vessel_id:
                    site=positions.get(b['id'])
                    if not site or site['id']!=vessel_id:continue
                    b={**b,'work_site':site}""")
    anchor = """            for r in c.execute("SELECT * FROM ops_log_entries WHERE"""
    source = change(source, anchor, """            from .vessel_logs import require_book, scope
            book_sites={}
""" + anchor)
    anchor = "                add(b,'logs',"
    source = change(source, anchor, """                bid=r['book_id']
                if bid not in book_sites:
                    try:
                        require_book(c,actor,bid)
                    except Problem as exc:
                        if exc.code not in (403,404):raise
                        book_sites[bid]=None
                    else:
                        book_sites[bid]=(scope(c,bid) or {}) if vessel_id else {}
                if book_sites[bid] is None:continue
                if book_sites[bid].get('site_id'):
                    b={**b,'site_id':book_sites[bid]['site_id']}
""" + anchor)
    return source


def calendar_ui(source):
    source = change(source, "day:'',query:'',kinds:", "day:'',query:'',vessel_id:'',kinds:")
    source = change(source, "prefs.month+'|'+[...prefs.kinds]", "prefs.month+'|'+prefs.vessel_id+'|'+[...prefs.kinds]")
    start = source.index('<label class="cal-search">')
    end = source.index('</label>', start) + len('</label>')
    search = source[start:end]
    source = source[:start] + source[end:]
    source = change(source, '<details class="cal-filters"', '<div class="wl-calendar-search-fields">' + search + '${WLPageVessels.field(prefs.vessel_id)}</div><details class="cal-filters"')
    anchor = "  el('calendar-filters').open=prefs.filters;"
    source = change(source, anchor, """  const vessel=host.querySelector('[data-page-vessel]');
  WLPageVessels.bind(vessel,{api,value:prefs.vessel_id,onChange:id=>{
   if(!controlsCurrent())return;
   prefs.vessel_id=id;prefs.day='';reloadSelection();
  }});
""" + anchor)
    source = change(source, "prefs.query='';el('calendar-query').value=''", "prefs.query='';prefs.vessel_id='';vessel.value='';el('calendar-query').value=''")
    return change(source, "{start,end,kinds:requested.join(',')}", "{start,end,kinds:requested.join(','),vessel_id:prefs.vessel_id}")


def hr_api(source):
    source = change(source, "department_id:str='',person=Depends(logged)", "department_id:str='',vessel_id:str='',person=Depends(logged)", 2)
    source = change(source, "department_id=department_id)\n", "department_id=department_id)\n        if vessel_id: scope['vessel_id']=vessel_id\n", 2)
    source = change(source, "def overview(user_id:str='',person=Depends(logged))", "def overview(user_id:str='',vessel_id:str='',person=Depends(logged))")
    source = change(source, "store.hr.overview(person,user_id))", "store.hr.overview(person,user_id,vessel_id))")
    source = change(source, "def review_queue(person=Depends(logged))", "def review_queue(vessel_id:str='',person=Depends(logged))")
    source = change(source, "store.hr.review_queue(person))", "store.hr.review_queue(person,vessel_id))")
    source = change(source, "offset:int=0,limit:int=100,person=Depends(logged))", "offset:int=0,limit:int=100,vessel_id:str='',person=Depends(logged))")
    return change(source, "store.hr.records(person,kind,user_id,offset,limit))", "store.hr.records(person,kind,user_id,offset,limit,vessel_id))")


def hr(source):
    source = change(source, "def workspace(self, actor, start_on, end_on, user_id='', location='', project='', department_id='')", "def workspace(self, actor, start_on, end_on, user_id='', location='', project='', department_id='', vessel_id='')")
    source = change(source, "user_id, location, project, department_id)", "user_id, location, project, department_id, vessel_id)")
    source = change(source, "def records(self, actor, kind, user_id='', offset=0, limit=100)", "def records(self, actor, kind, user_id='', offset=0, limit=100, vessel_id='')")
    source = change(source, "def review_queue(self, actor)", "def review_queue(self, actor, vessel_id='')")
    source = change(source, "def overview(self, actor, user_id='')", "def overview(self, actor, user_id='', vessel_id='')")
    start = source.index('    def records(self,')
    end = source.index('    @staticmethod', source.index('    def overview(',start))
    body = source[start:end]
    body = change(body, 'with self.store.connection() as c:', """with self.store.connection() as c:
            from .work_locations import page_vessel_lookup
            matches = page_vessel_lookup(c, actor, vessel_id)""", 3)
    body = change(body, "            total=len(rows);", """            if vessel_id and kind not in ('people','documents'):
                rows=[r for r in rows if matches(r,kind)]
            total=len(rows);""")
    body = change(body, "if not self._read_allowed(record,user,capabilities): continue", "if not self._read_allowed(record,user,capabilities) or not matches(record,kind): continue")
    body = change(body, "            for kind in KINDS:", "            permitted_timesheets=False\n            for kind in KINDS:")
    body = change(body, "                result[kind] = [self._present", """                if kind=='timesheets': permitted_timesheets=bool(rows)
                if vessel_id and kind not in ('people','documents'):
                    rows=[r for r in rows if matches(r,kind)]
                result[kind] = [self._present""")
    body = change(body, "and not result['timesheets']:", "and not permitted_timesheets:")
    return source[:start]+body+source[end:]


def hr_workspace(source):
    source = change(source, "project='', department_id=''):", "project='', department_id='', vessel_id=''):")
    anchor = '        user,caps=current(c,actor)'
    source = change(source, anchor, anchor + """
        from .work_locations import page_vessel_lookup, catalog
        matches=page_vessel_lookup(c,actor,vessel_id)
        vessel_name=next((s['name'] for s in catalog(c,actor) if s['id']==vessel_id and s['kind']=='vessel'),'') if vessel_id else ''""")
    source = change(source, "            r=json.loads(row[0])", """            r=json.loads(row[0])
            if not matches(r,r['kind']): continue""")
    anchor = "        shifts=[r for r in rows if r['kind']=='shifts']"
    source = change(source, anchor, """        if vessel_id:
            assigned={r['user_id'] for r in rows}
            people=[person for person in people if person['id'] in assigned]
""" + anchor)
    return change(source, "        return {'start_on':start_on,", "        return {'vessel_name':vessel_name,'start_on':start_on,")


def hr_ui(source):
    source = change(source, "#hr-search,#hr-person,", "#hr-search,[data-page-vessel],#hr-person,")
    source = change(source, "start_on:monthStart(),end_on:monthEnd(),location:'',project:'',department_id:''",
                    "start_on:monthStart(),end_on:monthEnd(),location:'',project:'',department_id:'',vessel_id:''", 2)
    anchor = "  el('hr-refresh').onclick="
    source = change(source, anchor, """  if(!['people','documents'].includes(view)){
   const bar=host.querySelector('.hr-toolbar');
   if(['dashboard','calendar','reports'].includes(view))bar.insertAdjacentHTML('beforebegin',WLPageVessels.field(workspaceFilters.vessel_id));
   else bar.querySelector('.actions').insertAdjacentHTML('beforebegin',WLPageVessels.field(workspaceFilters.vessel_id));
   const vessel=host.querySelector('[data-page-vessel]');
   WLPageVessels.bind(vessel,{api:H.api,value:workspaceFilters.vessel_id,onChange:id=>{
    if(!vessel.isConnected||!ready())return;
    workspaceFilters.vessel_id=id;page=0;open(true);
   }});
  }
""" + anchor)
    source = change(source, "encodeURIComponent(id),{beforeSend:c.before}),canReview?H.api('/api/hr/review-queue',", "encodeURIComponent(id)+(queryFilters.vessel_id?'&vessel_id='+encodeURIComponent(queryFilters.vessel_id):''),{beforeSend:c.before}),canReview?H.api('/api/hr/review-queue'+(queryFilters.vessel_id?'?vessel_id='+encodeURIComponent(queryFilters.vessel_id):''),")
    source = change(source, "kind,user_id:id,offset:String(offset),limit:'100'", "kind,user_id:id,offset:String(offset),limit:'100',vessel_id:workspaceFilters.vessel_id||''")
    source = change(source, "view==='calendar'?workspaceFilters:{location:'',project:'',department_id:''}", "view==='calendar'?workspaceFilters:{location:'',project:'',department_id:'',vessel_id:workspaceFilters.vessel_id}")
    source = change(source, "Object.assign(workspaceFilters,{location:'',project:''})", "Object.assign(workspaceFilters,{location:'',project:'',vessel_id:''})")
    source = change(source, "department_id:scope.department_id||'',token:snapshot", "department_id:scope.department_id||'',vessel_id:scope.vessel_id||'',token:snapshot")
    return change(source, "  if(reportKind==='needs')rows.push", "  if(filters.vessel_id)rows.push([wtext('Embarcação','Vessel'),workspace.vessel_name||wtext('Indisponível','Unavailable')]);\n  if(reportKind==='needs')rows.push")


def hr_export(source):
    anchor = "    if kind != \"needs\" and scope[\"department_id\"]:"
    return change(source, anchor, """    if scope.get("vessel_id"):
        qualifiers.append(("Vessel", "Embarcação")[lang] + " · " + (workspace.get("vessel_name") or ("Unavailable", "Indisponível")[lang]))
""" + anchor)


def transforms():
    return {
        'app/static/fleet.js': fleet,
        'app/static/manifest_ui.js': manifest_ui,
        'app/fleet.py': fleet_calendar,
        'app/fleet_api.py': lambda s: change(s,"def calendar(start: str,end: str,a=Depends(logged)): return store.fleet.calendar(a,start,end)",
                                             "def calendar(start: str,end: str,vessel_id:str='',a=Depends(logged)): return store.fleet.calendar(a,start,end,vessel_id)"),
        'app/vessel_logs.py': fleet_log_calendar,
        'app/vessel_logs_api.py': lambda s: change(s,"def calendar(start:str,end:str,site_id:str='',a=Depends(logged)):\n        return store.vessel_logs.calendar(a,start,end,site_id)",
                                                   "def calendar(start:str,end:str,site_id:str='',vessel_id:str='',a=Depends(logged)):\n        return store.vessel_logs.calendar(a,start,end,site_id,vessel_id)"),
        'app/work_locations.py': location_helpers,
        'app/static/it_workspace.js': it_ui,
        'app/it_requests.py': it_store,
        'app/it_requests_api.py': it_api,
        'app/static/project_calendar.js': calendar_ui,
        'app/assets_api.py': calendar_api,
        'app/project_calendar.py': calendar,
        'app/hr.py': hr,
        'app/hr_api.py': hr_api,
        'app/hr_workspace.py': hr_workspace,
        'app/hr_report_export.py': hr_export,
        'app/static/hr_workspace.js': hr_ui,
        'app/static/ui132_visual.css': lambda s: s+'\n.wl-calendar-search-fields{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(13rem,100%),1fr));align-items:end;gap:.75rem;margin-block:.75rem}\n',
    }
