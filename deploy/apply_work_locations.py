"""Apply fleet-backed locations to native record writers, forms and authorised search."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
PARENT = '125b943635134f55791ec9db24c9ddaa6459dfef9fe6b8fe54522094eaac2b57'


def once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected parent near ' + old[:90])
    return source.replace(old, new)


def apply(root):
    receipt = root / 'RELEASE_FILES.json'
    if sha256(receipt.read_bytes()).hexdigest() != PARENT:
        raise ValueError('Unexpected runtime before work locations')
    manifest = json.loads(receipt.read_bytes())
    changed = {}
    def edit(path, fn):
        data = changed.get(path)
        if data is None:
            data = (root / path).read_bytes()
            if sha256(data).hexdigest() != manifest['files'][path]:
                raise ValueError('File changed before work locations: ' + path)
        source = data.decode().replace('\r\n', '\n')
        try:
            result = fn(source)
        except ValueError as err:
            raise ValueError(path + ': ' + str(err)) from err
        changed[path] = (result.replace('\n','\r\n') if b'\r\n' in data else result).encode()
    def patch(name, *pairs):
        def transform(s):
            for before, after in pairs:
                s = once(s, before, after)
            return s
        edit('app/' + name, transform)
    def native(name, *pairs):
        def transform(s):
            first = re.search(r'^from [.]', s, re.M)
            if not first:
                raise ValueError('Missing native imports')
            return s[:first.start()] + 'from . import work_locations as sites\n' + s[first.start():]
        edit('app/'+name, transform)
        patch(name, *pairs)

    changed['app/work_locations.py'] = (BASE/'work_locations.py').read_bytes().replace(b'\r\n',b'\n')
    native('general_tasks.py',
           ("allowed = {'kind','title','instructions'", "allowed = {'work_site_id','kind','title','instructions'"),
           ("        checklist = self._new_checklist(c, p.get('checklist'), a)", "        t['work_site'] = sites.selection(c,a,p)\n        checklist = self._new_checklist(c, p.get('checklist'), a)"))
    native('work_tasks.py', ("        t['count_id']=s['id']", "        t['work_site']=sites.selection(c,a,p)\n        t['count_id']=s['id']"))
    patch('fault_task_creation.py',
          ("        t = self.store.tasks.do_create_general(c, p['task'], a)", """        task = dict(p['task'])
        if 'work_site_id' not in task and f.get('work_site'):
            task['work_site_id'] = f['work_site']['id']
        t = self.store.tasks.do_create_general(c, task, a)"""))
    for module, table in [('fault_reports.py','fault_reports'), ('qshe_reports.py','qshe_reports')]:
        def reports(s):
            s = s.replace("check_fields(p,{'title','description'", "check_fields(p,{'work_site_id','title','description'")
            s = once(s,"check_fields(p,{'id','version','title','description'", "check_fields(p,{'id','version','work_site_id','title','description'")
            s = once(s,"        c.execute('INSERT INTO "+table+" VALUES", "        f['work_site']=sites.selection(c,a,p)\n        c.execute('INSERT INTO "+table+" VALUES")
            s = once(s,"        f.update(fields)", "        f['work_site']=sites.selection(c,a,p,f.get('work_site'))\n        f.update(fields)")
            s = once(s,"for k in ('id','version','reference','title','status','priority','department_name'", "for k in ('work_site','id','version','reference','title','status','priority','department_name'")
            s = once(s,'return dict(departments=departments,users=users,priorities=PRIORITIES', 'return dict(sites=sites.catalog(c,a),departments=departments,users=users,priorities=PRIORITIES')
            return s
        native(module)
        edit('app/'+module,reports)
    native('maintenance.py', ("        if 'recurrence' in p:j['recurrence']", "        j['work_site']=sites.selection(c,a,p)\n        if 'recurrence' in p:j['recurrence']"))
    patch('maintenance_cycles.py', ("            put(c, 'maintenance_jobs', planned,", "            planned['work_site'] = j.get('work_site')\n            put(c, 'maintenance_jobs', planned,"))
    native('toolbox.py', ("        self.apply_content(c,r,p)\n        put(c,'toolbox_talks'", "        r['work_site']=sites.selection(c,a,p)\n        self.apply_content(c,r,p)\n        put(c,'toolbox_talks'"),
           ("        changed=any(r.get", "        changed=r.get('work_site')!=before.get('work_site') or any(r.get"))
    native('inventory.py', ("        item.update(clean)\n        if iid:touch", "        item['work_site']=sites.selection(c,a,p,item.get('work_site'))\n        item.update(clean)\n        if iid:touch"),
           ("        put(c,'inventory_counts',s,b['id'],True)", "        s['work_site']=sites.selection(c,a,p)\n        put(c,'inventory_counts',s,b['id'],True)"))
    native('certificates.py', ("        note=text(p.get('reason',''),'Correction note", "        if 'work_site_id' in p:values['work_site']=sites.selection(c,a,p,b.get('work_site'))\n        note=text(p.get('reason',''),'Correction note"),
           ("        put(c,'asset_certificates',b,b['family_id'],True)", "        b['work_site']=old.get('work_site')\n        put(c,'asset_certificates',b,b['family_id'],True)"))
    native('it_requests.py', ("fields(payload, allowed[action], allowed[action])", "fields(payload, allowed[action] | ({'work_site_id'} if action == 'create' else set()), allowed[action])"),
           ("                record = dict(id=str(uuid.uuid4()), version=1, title=", "                record = dict(id=str(uuid.uuid4()), work_site=sites.selection(c,actor,payload), version=1, title="))
    patch('server.py', ("class NewDive(Strict):", "class NewDive(Strict):\n    work_site_id: str | None = Field(default=None, max_length=36)"),
          ("class EditMeta(Strict):", "class EditMeta(Strict):\n    work_site_id: str | None = Field(default=None, max_length=36)"),
          ("payload.live_mode, payload.recognition_points)", "payload.live_mode, payload.recognition_points, payload.work_site_id)"),
          ("payload.meta.model_dump(), payload.version, a)", "payload.meta.model_dump(), payload.version, a, payload.work_site_id)"))
    native('store.py',
           ("live_mode: bool = False, recognition_points: int = 1) -> dict:", "live_mode: bool = False, recognition_points: int = 1, work_site_id: str | None = None) -> dict:"),
           ("                if rec['meta'] != meta or", "                if work_site_id and (rec.get('work_site') or {}).get('id') != work_site_id:\n                    raise Problem(409, 'This checklist ID already uses another location.')\n                if rec['meta'] != meta or"),
           ("            for p in rec['phases']:\n                rec['items'][p] =", "            rec['work_site']=sites.selection(con,actor,{'work_site_id':work_site_id}) if work_site_id is not None else None\n            for p in rec['phases']:\n                rec['items'][p] ="),
           ("return [dict(id=r['id'], meta=r['meta'], created_at=", "return [dict(id=r['id'], work_site=r.get('work_site'), meta=r['meta'], created_at="),
           ("def update_meta(self, rid: str, meta: dict, version: int, actor: dict):", "def update_meta(self, rid: str, meta: dict, version: int, actor: dict, work_site_id=None):"),
           ("            rec['meta'] = meta", """            if work_site_id is not None:
                rec['work_site']=sites.selection(con,actor,{'work_site_id':work_site_id},rec.get('work_site'))
            elif rec['meta'].get('vessel') != meta.get('vessel'):
                rec.pop('work_site',None)
            rec['meta'] = meta"""))
    for module, insertion, row in [('handovers.py',"                con.execute('INSERT INTO handover_records", 'rec'),
                                   ('daily_handovers.py',"            con.execute('INSERT INTO handover_records", 'record'),
                                   ('simple_handovers.py',"                con.execute('INSERT INTO handover_records", 'rec')]:
        indent=insertion[:len(insertion)-len(insertion.lstrip())]
        native(module,(insertion,indent+row+"['work_site']=sites.for_name(con,actor,("+row+".get('draft') or {}).get('location'))\n"+insertion))
    patch('handovers.py', ("                    time_basis=edit['time_basis'] if edit else '',", "                    work_site=rec.get('work_site'), location=edit.get('location','') if edit else '',\n                    time_basis=edit['time_basis'] if edit else '',"))
    patch('work_tasks.py',("name=title,item_ids=ids,scope_mode=mode,recognition_points=p.get", "name=title,item_ids=ids,scope_mode=mode,**({'work_site_id':p['work_site_id']} if 'work_site_id' in p else {}),recognition_points=p.get"))
    patch('handovers.py',("                        rec['draft'] = edit; rec['kind'] = edit['kind']", """                        if (rec.get('draft') or {}).get('location') != edit.get('location'):
                            rec['work_site']=sites.for_name(con,actor,edit.get('location'))
                        rec['draft'] = edit; rec['kind'] = edit['kind']"""),
          ("work_site=rec.get('work_site'), location=edit.get('location','') if edit else '',","work_site=rec.get('work_site') if edit and (rec.get('work_site') or {}).get('name')==edit.get('location') else None, location=edit.get('location','') if edit else '',"))
    patch('toolbox.py',("        self.apply_content(c,r,p)\n        changed=", "        if 'work_site_id' in p:r['work_site']=sites.selection(c,a,p,r.get('work_site'))\n        self.apply_content(c,r,p)\n        changed="))
    native('action_center_api.py',
           ("    @app.get('/api/search')", """    @app.get('/api/fleet/work-locations')
    def locations(a=Depends(logged)):
        with store.connection() as c:
            return {'sites': sites.catalog(c,a)}

    @app.get('/api/search')"""),
           ("limit: int = 30, a=Depends(logged)", "limit: int = 30, site_id: str = '', offset: int = 0, a=Depends(logged)"),
           ("store.global_search.search(a, q, kinds, limit)", "store.global_search.search(a, q, kinds, limit, site_id, offset)"))
    native('action_center.py',
       ("'logs', 'faults', 'qshe', 'fleet', 'manifests',", "'logs', 'faults', 'qshe', 'fleet', 'manifests', 'it',"),
       ("    return ' '.join(str(value or '').casefold().split())", "    return sites.fold(value)"),
       ("query: str, kinds: str = '', limit: int = 30) -> dict:", "query: str, kinds: str = '', limit: int = 30, site_id: str = '', offset: int = 0) -> dict:"),
       ("        if len(query) < 2:", "        if type(offset) is not int or not 0 <= offset <= 1_000_000:\n            raise Problem(422, 'Invalid result page.')\n        if len(query) < 2 and not site_id:"),
       ("        results: list[dict] = []", """            lookup = sites.SiteLookup(sites.catalog(c, actor))
            if site_id and site_id not in lookup.by_id:
                raise Problem(404, 'Location unavailable.')
        query_names_site = any(token in name for name in lookup.by_label for token in _tokens(query))
        source_query = '' if site_id or query_names_site else query
        results: list[dict] = []"""),
       ("*, updated_at: object = '', keywords: object = '') -> None:", "*, updated_at: object = '', keywords: object = '', record=None, parent=None) -> None:"),
       ("            match = _score(query, str(title or ''), str(subtitle or ''), str(keywords or ''))", """            locations = lookup.resolve(record, parent=parent, kind=kind) if record else []
            if site_id and all(site['id'] != site_id for site in locations):
                return
            names = ' '.join(site['name'] + ' ' + site['code'] for site in locations)
            match = _score(query, str(title or ''), str(subtitle or ''), str(keywords or '')+' '+names) if query else (0,0)"""),
       ("                _rank=match[0], _distance=match[1],", "                locations=locations, _rank=match[0], _distance=match[1],"),
       ("            if kind not in requested or", "            if kind=='people' and site_id:return\n            if kind not in requested or"),
       ("for item in self.store.logs.entries(book['id'], actor, q=query, limit=min(20, limit), offset=0).get('entries', []):",
        "for item in sites.pages(lambda start: self.store.logs.entries(book['id'],actor,q=source_query,limit=200,offset=start),'entries'):"),
       ("for item in self.store.faults.catalog(actor, status='all', query=query)['items']:", "for item in sites.pages(lambda start: self.store.faults.catalog(actor,status='all',query=source_query,offset=start),'items'):"),
       ("for item in self.store.qshe.catalog(actor, status='all', query=query)['items']:", "for item in sites.pages(lambda start: self.store.qshe.catalog(actor,status='all',query=source_query,offset=start),'items'):"),
       ("        def fleet_rows():", """        def it_rows():
            view = 'queue' if user['role']=='admin' or permissions.get('it.manage') else 'mine'
            for row in sites.pages(lambda start: self.store.it_requests.workspace(actor,view=view,offset=start,limit=100),'requests'):
                add('it',row['id'],row['title'],row.get('description'),row['status'],_href('it/requests',row['id']),
                    record=row,updated_at=row.get('updated_at'),keywords=row.get('priority',''))
        run('it', 'it.view_own', it_rows)

        def fleet_rows():"""),
       ("        items = results[:limit]", "        items = results[offset:offset+limit]"),
       ("total_returned=len(items), has_more=authorised_total > limit,", "total_returned=len(items), total=authorised_total, offset=offset, has_more=authorised_total > offset+limit,"),
       ("'fleet':'Fleet sites','manifests':'Manifests',", "'fleet':'Fleet sites','manifests':'Manifests','it':'IT requests',"))
    def search_sources(s):
        # Each record passed here has already cleared its owning module's read check.
        for var, kind, dest in [('item','tasks','item'),('item','maintenance','item'),('item','checklists','item'),
              ('item','handovers','item'),('item','toolbox','item'),('item','inventory','item'),
              ('item','certificates','item'),('book','logs','book'),('item','logs','item, parent=book'),
              ('site','fleet','site'),('item','faults','item'),('item','qshe','item'),('item','manifests','item')]:
            start=s.index("add('"+kind+"', "+var+"['id']")
            # Insert a keyword just before updated_at/keywords, after the six positional arguments.
            pos=re.search(r'(?<!\w)(updated_at|keywords)=',s[start:])
            at=start+pos.start()
            s=s[:at]+'record='+dest+', '+s[at:]
        return s
    edit('app/action_center.py',search_sources)
    native('hr.py',
       ("strict_fields(payload,SAVE_FIELDS[kind],{'id','version','user_id','title'})", "strict_fields(payload,SAVE_FIELDS[kind] | ({'work_site_id'} if kind in ('shifts','needs','travel','expenses','timesheets') else set()),{'id','version','user_id','title'})"),
       ("                values=self._values(c,kind,payload,record)", """                values=self._values(c,kind,payload,record)
                if 'work_site_id' in payload:
                    values['work_site']=sites.selection(c,actor,payload,(record or {}).get('work_site'))
                elif kind in ('needs','shifts') and (not record or record.get('location')!=values.get('location')):
                    values['work_site']=sites.for_name(c,actor,values.get('location'))"""))
    patch('action_center.py',
       ("'manifests', 'it',", "'manifests', 'it', 'hr',"),
       ("        def it_rows():", """        def hr_rows():
            directory=self.store.hr.directory(actor)
            for kind,cap in [('shifts','hr.shifts_manage'),('needs','hr.shifts_manage'),('travel','hr.travel_manage'),('expenses','hr.expenses_review'),('timesheets','hr.timesheets_review')]:
                people=directory['users'] if permissions.get(cap) else [user]
                for person in people:
                    for row in sites.pages(lambda start: self.store.hr.records(actor,kind,person['id'],offset=start,limit=100),'items'):
                        if not lookup.resolve(row):
                            continue
                        add('hr',row['id'],row.get('title'),row.get('location') or row.get('project'),row.get('status'),
                            _href('hr/record/'+kind,row['id']),record=row,updated_at=row.get('updated_at'))
        if site_id or query_names_site or 'hr' in kinds.split(','):
            run('hr','hr.view_own',hr_rows)

        def it_rows():"""),
       ("'manifests':'Manifests','it':'IT requests',", "'manifests':'Manifests','it':'IT requests','hr':'HR',"))
    patch('action_center.py',("        authorised_total = len(results)", """        if site_id and not query and len(requested)>1:
            from collections import deque
            groups = {}
            for result in results:
                groups.setdefault(result['kind'],deque()).append(result)
            results = []
            while groups:
                for key in list(groups):
                    results.append(groups[key].popleft())
                    if not groups[key]:
                        del groups[key]
        authorised_total = len(results)"""))
    patch('action_center.py', ('                for item in self.store.inventory.get(book[\'id\'], actor).get(\'items\', []):', """                catalogue=self.store.inventory.get(book['id'],actor)
                for count in catalogue.get('counts',[]):
                    add('inventory',count['id'],count.get('name'),book.get('name'),count.get('status'),
                        _href('inventory/count',count['id']),record=count,updated_at=count.get('updated_at'))
                for item in catalogue.get('items',[]):"""))
    def js(name,*pairs):
        patch('static/'+name, *pairs)
    js('fieldwork.js',
       ("    const acceptanceForm=kind==='Task acceptance';".strip(), "const locationField=WLWorkSites.fw(f,kind,context,restore,api);\n  const acceptanceForm=kind==='Task acceptance';"),
       ("const payload=payloadFn(new FormData(f),f);const text=", "const siteId=locationField?.read();const payload=payloadFn(new FormData(f),f);if(locationField)(payload.task||payload).work_site_id=siteId;const text="))
    for file in ('fault_reports.js','qshe_reports.js'):
        js(file, ("if(['create','triage'].includes(action))directory=await api(", "if(['create','amend','triage'].includes(action))directory=await api("),
           ("   if(action==='create')Object.assign(payload", "   if(['create','amend'].includes(action))payload.work_site_id=row?.work_site?.id||'';\n   if(action==='create')Object.assign(payload"),
           ("<h2>${E(f.title)}</h2>", "<h2>${E(f.title)}</h2>${f.work_site?.name?'<p>'+E(WLWorkSites.label())+' · '+E(f.work_site.name)+'</p>':''}"))
    js('report_forms.js',
       ("if(q==='qs')fields+=select('category'", """fields+=select('work_site_id',WLWorkSites.label(),[['',WLWorkSites.choose()],...WLWorkSites.options(f.directory.sites||[],p.work_site_id)]);
   if(q==='qs')fields+=select('category'"""),
       ("__wl118.t('Vessel / site / area (label only)')","WLWorkSites.words('Área específica (opcional)','Specific area (optional)')"),
       ("  if($('evidence-files'))", "  if($('work_site_id'))$('work_site_id').required=WLWorkSites.active(f.directory.sites||[]).length>0;\n  if($('evidence-files'))"))
    js('app.js',
       ("    const form=$('#meta-form');","""    const form=$('#meta-form');
    const siteInput=form.elements.vessel;
    const locationField=WLWorkSites.nameField(siteInput,api,!!existing,existing?.work_site?.id||(!existing&&d.vessel===state.formDraft?.vessel?state.formDraftSite:'')||'');
    if(locationField)locationField.select.addEventListener('change',()=>{if(!existing)state.formDraftSite=locationField.select.value;});"""),
       ("body:{version:existing.meta_version,meta:data()}", "body:{version:existing.meta_version,meta:data(),...WLWorkSites.body(locationField)}"),
       ("body:{id,meta:data(),template_id:t.id", "body:{id,meta:data(),...WLWorkSites.body(locationField),template_id:t.id"))
    js('simple_handovers.js',("  $('#sh-pattern').value=v.schedule", "  if(canSchedule)WLWorkSites.nameField($('#sh-location'),api,!!data.setup);\n  $('#sh-pattern').value=v.schedule"))
    js('handovers.js',("   if(f.data?.daily){el('ho-edit-kind')", "   if(!f.data?.daily)WLWorkSites.nameField(el('ho-location'),api,!!f.data);\n   if(f.data?.daily){el('ho-edit-kind')"))
    js('it_workspace.js',
       ("action==='create'?{title:'',description:'',priority:'normal'}","action==='create'?{title:'',description:'',priority:'normal',work_site_id:''}"),
       ("  if(f.action==='triage')el('it-assignee-search')", """  if(f.action==='create'){
   const host=document.createElement('div');f.node.querySelector('.it-form-fields').append(host);
   f.locationField=WLWorkSites.picker(host,H.api,{value:f.values.work_site_id, onPick:site=>{f.values.work_site_id=site?.id||'';}});
  }
  if(f.action==='triage')el('it-assignee-search')"""),
       ("  const values=copy(f.values);","  if(f.action==='create')f.values.work_site_id=f.locationField.read();\n  const values=copy(f.values);"))
    js('maintenance_workspace.js',
       ("[j.id,j.name,j.reference,j.asset_name,j.instructions", "[j.id,j.name,j.reference,j.asset_name,j.work_site?.name,j.work_site?.code,j.instructions"),
       ("</p><small>${E(j.reference ||", "</p>${j.work_site?.name?'<small>'+E(j.work_site.name)+'</small>':''}<small>${E(j.reference ||"),
       ("<h2>Instructions</h2><dl class=\"mw-facts\">", "<h2>Instructions</h2><dl class=\"mw-facts\">${j.work_site?.name?'<dt>'+E(WLWorkSites.label())+'</dt><dd>'+E(j.work_site.name)+'</dd>':''}"))
    js('task_workspace.js',("[t.id,t.title,t.department_name,", "[t.id,t.title,t.department_name,t.work_site?.name,t.work_site?.code,"))
    js('general_tasks.js', ("${facts}<h2>Instructions</h2>", "${facts}${t.work_site?.name?'<p>'+E(WLWorkSites.label())+' · '+E(t.work_site.name)+'</p>':''}<h2>Instructions</h2>"))
    js('action_center_ui82.js',
       ("['fleet',__wl118.t('Fleet sites')],['manifests',__wl118.t('Manifests')]", "['fleet',__wl118.t('Fleet sites')],['manifests',__wl118.t('Manifests')],['it',__wl118.t('IT requests')]"),
       ("  const owner=state.session,input=byId('wl-search-input');", """  const site=byId('wl-search-site'), selected=site.value,session=state.session;
  site.disabled=true;
  state.H.api('/api/fleet/work-locations',{beforeSend:guard(session)}).then(data=>{
   if(!owns(session)||!dialog.open)return;
   site.replaceChildren(new Option(WLWorkSites.words('Todas as localizações','All locations'),''));
   for(const item of data.sites)site.add(new Option(WLWorkSites.describe(item),item.id));
   site.value=selected;site.disabled=false;
  }).catch(err=>{if(owns(session)&&dialog.open)text(byId('wl-search-status'),message(err));});
  const owner=state.session,input=byId('wl-search-input');"""),
       ("  byId('wl-search-kind')?.addEventListener('change'", "  byId('wl-search-site')?.addEventListener('change',()=>runSearch(true));\n  byId('wl-search-kind')?.addEventListener('change'"),
       ("searchInput.value='';state.searchSequence++;", "searchInput.value='';byId('wl-search-site').value='';state.searchSequence++;"),
       ("if(input.value.trim().length>=2)runSearch(true);", "if(input.value.trim().length>=2||site.value)runSearch(true);"),
       ("if(q.length<2){emptySearch();", "if(q.length<2&&!byId('wl-search-site').value){emptySearch();"),
       ("if(q.length<2){state.searchSequence++;", "if(q.length<2&&!byId('wl-search-site').value){state.searchSequence++;"),
       ("async function runSearch(immediate){", "async function runSearch(immediate,offset=0){"),
       ("const params=new URLSearchParams({q,limit:'40'});", "const params=new URLSearchParams({q,limit:'40',offset:String(offset)});const site=byId('wl-search-site').value;if(site)params.set('site_id',site);"),
       ("    if(item.subtitle)copy.append", "    if(item.locations?.length)copy.append(node('span','wl-location-result',item.locations.map(x=>x.name).join(' · ')));\n    if(item.subtitle)copy.append"),
       ("  if(data.has_more)results.append(node('p','wl82-scope-note',__wl118.t('Up to 40 results are shown. Refine the phrase or choose a workspace to find other matches.')));", """  if(data.offset||data.has_more){
   const nav=node('nav','wl82-results-pages');nav.setAttribute('aria-label',WLWorkSites.words('Páginas de resultados','Result pages'));
   const previous=node('button','btn secondary',WLWorkSites.words('Anterior','Previous')), next=node('button','btn secondary',WLWorkSites.words('Próxima','Next'));
   for(const b of [previous,next])b.type='button';
   previous.disabled=!data.offset;next.disabled=!data.has_more;
   previous.onclick=()=>runSearch(true,Math.max(0,data.offset-40));next.onclick=()=>runSearch(true,data.offset+40);
   nav.append(previous,node('span','',(data.offset+1)+'–'+(data.offset+items.length)+' / '+data.total),next);results.append(nav);
  }"""),
       ("'wl-search-input','wl-search-kind','wl-action-category'", "'wl-search-input','wl-search-kind','wl-search-site','wl-action-category'"),
       ("text(byId('wl-search-status'),__wl118.t('Enter at least two characters.'));", "text(byId('wl-search-status'),WLWorkSites.words('Escolha uma localização ou digite pelo menos duas letras.','Choose a location or type at least two characters.'));"))
    css='\n.wl82-search-options{display:flex;align-items:center;gap:.5rem;flex-wrap:wrap}.wl82-search-options select{max-width:100%}.wl82-results-pages{display:flex;justify-content:center;align-items:center;gap:1rem;margin:.7rem 0}.wl-location-result{color:var(--accent,#087e83)}.wl-work-site{margin:.6rem 0}.wl-work-site small:empty{display:none}\n'
    edit('app/static/action_center_ui82.css',lambda s:s+css)
    edit('app/static/action_center_ui82.js', lambda s:(BASE/'work_locations_ui.js').read_text('utf-8')+'\n'+s)
    js('hr_workspace.js',
       ("  f.node=el('hr-form');if(f.node.elements.decision)", """  f.node=el('hr-form');
  f.workLocation=null;
  if(f.mode==='save'&&['shifts','needs','travel','expenses','timesheets'].includes(f.kind)){
   if(f.node.elements.location)f.workLocation=WLWorkSites.nameField(f.node.elements.location,H.api,!!f.row,f.values.work_site_id||f.row?.work_site?.id||'');
   else {const host=document.createElement('div');f.node.querySelector('button[type="submit"]')?.closest('.actions')?.before(host);
    if(!host.isConnected)f.node.append(host);
    f.workLocation=WLWorkSites.picker(host,H.api,{value:f.values.work_site_id||f.row?.work_site?.id||'',required:false});}
  }
  if(f.node.elements.decision)"""),
       (" const newProfileDocument=", " const searchRecord=/^#hr\\/record\\/(shifts|needs|travel|expenses|timesheets)\\/([0-9a-f-]{36})$/;\n const newProfileDocument="),
       ("||newProfileDocument.test(hash);", "||newProfileDocument.test(hash)||searchRecord.test(hash);"),
       ("   const createDocument=newProfileDocument.test(hash);", """   const linked=hash.match(searchRecord);
   if(linked){
    const [_,kind,rid]=linked;
    const record=checkedRecord(await H.api('/api/hr/'+kind+'/'+rid,{beforeSend:c.before}),kind,rid);
    if(!c.pending())return;
    lastHash='#hr';history.replaceState(history.state,'',lastHash);host.dataset.hrRoute=lastHash;
    renderOverview();showRecord(kind,record);return;
   }
   const createDocument=newProfileDocument.test(hash);"""))
    js('action_center_ui82.js',("['manifests',__wl118.t('Manifests')],['it',__wl118.t('IT requests')]", "['manifests',__wl118.t('Manifests')],['it',__wl118.t('IT requests')],['hr',WLWorkSites.words('RH','HR')]"))
    js('hr_workspace.js',("const p=copy(v);delete p.decision;", "const p=copy(v);delete p.work_site_id;if(f.workLocation)Object.assign(p,WLWorkSites.body(f.workLocation));delete p.decision;"))
    js('action_center_ui82.js',("const dialog=byId('wl-search-dialog');if(!dialogOpen", "const dialog=byId('wl-search-dialog');if(dialog)dialog.dataset.wlManagedClose='true';if(!dialogOpen"))
    js('inventory_workspace.js',
          ("  const setupValues=()=>['name','scope_mode'", """  const locationHost=document.createElement('div');f.querySelector('[name="name"]').closest('label').after(locationHost);
  const workLocation=WLWorkSites.picker(locationHost,api);
  const setupValues=()=>['work_site_id','name','scope_mode'"""),
          ("if(!request){const d=new FormData(f),mode=d.get('scope_mode');request={list_id:b.id,", "if(!request){let site;try{site=workLocation.read();}catch(e){F().showError(e);return;}const d=new FormData(f),mode=d.get('scope_mode');request={work_site_id:site,list_id:b.id,"))
    js('maintenance_workspace.js',("card.querySelector('[data-mw-select]')?.click();", "card.querySelector('[data-mw-open]')?.click();"))
    js('maintenance_workspace.js',('class="mw-order-title" data-mw-select="${E(j.id)}" aria-controls="mw-selected" aria-pressed="${j.id===prefs.selected}" aria-label="View summary: ${E(j.name)}"', 'class="mw-order-title" data-mw-open="${E(j.id)}"'),('<button type="button" class="btn secondary mw-open-direct"', '<button type="button" class="btn secondary" data-mw-select="${E(j.id)}" aria-controls="mw-selected" aria-pressed="${j.id===prefs.selected}">${E(WLWorkSites.words("Resumo","Summary"))}</button><button type="button" class="btn secondary mw-open-direct"'))
    js('operations.js',("<div class=\"actions\">${j.can_work&&j.status==='open'?", """<p class="small">${E(WLWorkSites.words('Evidência fotográfica','Photo evidence'))} · ${E(__wl118.t(({off:'Off',optional:'Optional',required:'Required'})[s.definition.photo_evidence?.mode]||'Off'))}</p><div class="actions">${j.can_work&&j.status==='open'?"""))
    edit('app/static/action_center_ui82.js',lambda s:s+'\n'+(BASE/'record_cards.js').read_text('utf-8'))
    edit('app/static/action_center_ui82.css',lambda s:s+'\n:is(article.ho-card,article.hr-record,article.ux-roster-card,.maintenance-step,article[data-cw-card],article[data-home-workspace],.home-work-row,.ph-row,.ph-shift-card,.hwd-record,.ho-day-entry,.sh-record,.sh-resume,.ha-card,.log-mobile-entry,.log-entry,article[data-shipment-card],tr:has(.it-request-link),tr[data-stock-row],.tw47-stock-item):has(:is(a[href],button):not(:disabled)){cursor:pointer}\n.wl-original-site-field[hidden]{display:none!important}\n')
    static='app/static/'
    hashes={name[len(static):]:sha256(data).hexdigest()[:12] for name,data in changed.items() if name.startswith(static)}
    def refs(source):
        for name,digest in hashes.items():
            pattern=r'(/static/'+re.escape(name)+r'\?v=[\d.]+-)[0-9a-f]{12}'
            source,count=re.subn(pattern,lambda m:m[1]+digest,source)
            if count!=1:raise ValueError('Unexpected asset references: '+name+' '+str(count))
        return source
    for page,pt in [('index.html',False),('pt-BR/index.html',True)]:
        def page_update(s):
            field=('<label for="wl-search-site">'+('Embarcação ou base' if pt else 'Ship or base')+
                   '</label><select id="wl-search-site"><option value="">'+('Todas as localizações' if pt else 'All locations')+'</option></select>')
            anchor='<span aria-live="polite" id="wl-search-status"' if pt else '<span id="wl-search-status"'
            return once(refs(s),anchor,field+anchor).replace(' minlength="2"','',1)
        edit(static+page,page_update)
    edit(static+'sw.js',lambda s:once(refs(s),'ui162-20261122-crew-lists','ui162-20261122-work-locations-1'))
    variant=manifest['variant']+'-work-locations'
    info=json.loads((root/'UI_PATCH.json').read_bytes())
    info.update(patch_id=variant,parent_patch_id=manifest['variant'],parent_manifest_sha256=PARENT,
                scope='Fleet locations on work records, location search and record-card navigation.')
    changed['UI_PATCH.json']=(json.dumps(info,indent=2)+'\n').encode()
    for name,data in changed.items():
        (root/name).write_bytes(data)
        manifest['files'][name]=sha256(data).hexdigest()
    manifest['variant']=variant
    receipt.write_bytes((json.dumps(manifest,indent=2)+'\n').encode())
    print(variant,sha256(receipt.read_bytes()).hexdigest())


if __name__=='__main__':
    apply(Path(sys.argv[1]))
