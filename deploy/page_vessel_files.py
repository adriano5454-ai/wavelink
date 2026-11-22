"""Add authorised vessel membership to originals and their workspace folders."""


def once(source, before, after):
    if source.count(before) != 1:
        raise ValueError('Unexpected original files source near ' + before[:90])
    return source.replace(before, after)


PROJECT = '''
        from . import work_locations
        directory = work_locations.catalog(c, actor)
        lookup = work_locations.SiteLookup(directory)
        vessel_ids = {site['id'] for site in directory if site['kind'] == 'vessel'}

        def project(*args, owner=None, kind='', equipment=(), **kwargs):
            file = present(*args, **kwargs)
            owner = owner or {}
            saved = owner.get('work_site') or (owner.get('meta') or {}).get('work_site')
            if saved and saved.get('id'):
                # Never substitute a different legacy label for a saved site.
                ids = {saved['id']}
            else:
                ids = {site['id'] for site in lookup.resolve(owner, kind=kind)}
            file['vessel_ids'] = sorted(vessel_ids & ids)
            if not ids and equipment:
                file['_equipment'] = [iid for iid in equipment if iid]
            return file

        rows = list(chain(private_files(c, store, actor, caps, project),
                          operational_files(c, store, actor, caps, originals, project)))
        ids = {iid for row in rows for iid in row.get('_equipment', ())}
        positions = work_locations.visible_equipment_positions(c, actor, ids)
        items = {}
        for row in rows:
            equipment = row.pop('_equipment', ())
            if equipment:
                positions_for_file = {(positions.get(iid) or {}).get('id') for iid in equipment}
                if len(positions_for_file) == 1 and positions_for_file <= vessel_ids:
                    row['vessel_ids'] = list(positions_for_file)
            key = (row['group'], row['url'])
            if key in items:
                row['vessel_ids'] = sorted(set(row['vessel_ids']) | set(items[key]['vessel_ids']))
            items[key] = row
'''


def catalogue(source):
    changes = [
        ('def private_files(c, store, actor, caps):', 'def private_files(c, store, actor, caps, present):'),
        ('def operational_files(c, store, actor, caps, originals):',
         'def operational_files(c, store, actor, caps, originals, present):'),
        ("'#hr/staff/'+employee_id, archived=", "'#hr/staff/'+employee_id, owner=rec, archived="),
        ("'#it/requests/'+rec['id'], at=", "'#it/requests/'+rec['id'], owner=rec, at="),
        ("'#qshe/'+rec['id'], archived=", "'#qshe/'+rec['id'], owner=rec, archived="),
        ('context._authored_handovers(c, author, actor, caps)', 'context._authored_handovers(c, author, actor, caps, include_location=True)'),
        ("route, archived=doc.get('archived')", "route, owner=doc['location_record'], archived=doc.get('archived')"),
        ("'#certificates/'+rec['id'], archived=", "'#certificates/'+rec['id'], owner=rec, equipment=rec.get('asset_ids', ()), archived="),
        ("'#asset/'+item['id'], archived=", "'#asset/'+item['id'], equipment=[item['id']], archived="),
        ("'#fleet/manifest/'+mid)", "'#fleet/manifest/'+mid, owner=manifest, kind='manifests')"),
        ('def referenced(group, template, route):', 'def referenced(group, template, route, owner, equipment):'),
        ("at=doc['imported_at'], linked=doc['id'])", "at=doc['imported_at'], linked=doc['id'], owner=owner, equipment=equipment)"),
        ("archived=ref['archived'], at=ref['imported_at'])", "archived=ref['archived'], at=ref['imported_at'], owner=record)"),
        ("file, url, route, at=record.get(", "file, url, route, owner=record, at=record.get("),
        ("yield from referenced('maintenance', job['template'], route)",
         "equipment = [(job.get('asset') or {}).get('id')]\n            yield from referenced('maintenance', job['template'], route, job, equipment)"),
        ("route, at=job.get('updated_at',''))", "route, owner=job, equipment=equipment, at=job.get('updated_at',''))"),
        ('from .vessel_logs import require_book', 'from .vessel_logs import require_book, scope'),
        ("for img in _body(ref['body']).get('images',[]):", "book_site = scope(c, ref['book_id'])\n            for img in _body(ref['body']).get('images',[]):"),
        ("'#logs/'+ref['book_id'], at=", "'#logs/'+ref['book_id'], owner=book_site, at="),
        ("""        items = {}
        for row in chain(private_files(c, store, actor, caps), operational_files(c, store, actor, caps, originals)):
            items[row['group'], row['url']] = row
""", PROJECT.lstrip('\n')),
        ("items[group,url] = present(group, file['title'], file, url, import_route(group,file['record_id']))",
         """rid = file['record_id']
                entry = present(group, file['title'], file, url, import_route(group, rid))
                entry['vessel_ids'] = []
                if group == 'logbook':
                    from .vessel_logs import require_book, scope
                    if authorised(require_book, c, actor, rid):
                        site_id = (scope(c, rid) or {}).get('site_id')
                        if site_id in vessel_ids:
                            entry['vessel_ids'] = [site_id]
                elif group == 'inventory' and caps.get('inventory.view'):
                    from .inventory import positioned_items
                    entries = positioned_items(c, rid, lookup)
                    entry['vessel_ids'] = sorted({item['vessel_id'] for item in entries if not item['archived']} & vessel_ids)
                items[group,url] = entry"""),
        ('workspace_imports=destinations)', "workspace_imports=destinations,\n                    vessels=[site for site in directory if site['kind'] == 'vessel'])"),
    ]
    for before, after in changes:
        source = once(source, before, after)
    return source


def handovers(source):
    source = once(source, '_authored_handovers(self,c,user_id,actor,permissions):',
                  '_authored_handovers(self,c,user_id,actor,permissions,*,include_location=False):')
    return once(source, "author_id=user_id,reference='',files=[file_ref(f) for f in attachments],sources=[],folder=None))",
                """author_id=user_id,reference='',files=[file_ref(f) for f in attachments],sources=[],folder=None))
                if include_location:
                    label = edit.get('location', '')
                    saved = record.get('work_site') or {}
                    documents[-1]['location_record'] = {'location': label, 'work_site': saved if saved.get('name') == label else None}""")


def browser(source):
    changes = [
        ('const workspaceFiles=data.workspace_files||[];', '''const vesselNames=new Map((data.vessels||[]).map(v=>[v.id,[v.name,v.code].filter(Boolean).join(' ')]));
    if(ui.vessel&&!vesselNames.has(ui.vessel)){ui.vessel='';ui.page=0;selected.clear();}
    const workspaceFiles=(data.workspace_files||[]).filter(f=>!ui.vessel||f.vessel_ids?.includes(ui.vessel));'''),
        ('{...d,groups:[]}', '{...d,groups:[],vessel_ids:[]}'),
        ('if (native) { if (!native.groups.includes(file.group)) native.groups.push(file.group); continue; }',
         '''if (native) {
        if (!native.groups.includes(file.group)) native.groups.push(file.group);
        for(const id of file.vessel_ids||[])if(!native.vessel_ids.includes(id))native.vessel_ids.push(id);
        continue;
      }'''),
        ('docs.filter(d=>h.archived||!d.archived)', 'docs.filter(d=>(h.archived||!d.archived)&&(!ui.vessel||d.groups.length>0))'),
        ('...workspaceFiles.map(d=>d.group)', '...(data.workspace_files||[]).map(d=>d.group)'),
        ('tools.append(searchwrap);', '''tools.append(searchwrap);
    const vesselTemplate=document.createElement('template');
    vesselTemplate.innerHTML=window.WLPageVessels.field(ui.vessel);
    const vesselField=vesselTemplate.content.firstElementChild;
    tools.append(vesselField);'''),
        ('layout.append(sidebar,main);shell.append(layout);', '''layout.append(sidebar,main);shell.append(layout);
    const vesselControl=vesselField.querySelector('[data-page-vessel]');
    window.WLPageVessels.bind(vesselControl,{sites:data.vessels||[],value:ui.vessel||'',onChange:id=>{
      const refocus=document.activeElement===vesselControl;
      ui.vessel=id;ui.page=0;selected.clear();h.redraw();
      if(refocus)shell.querySelector('[data-page-vessel]')?.focus({preventScroll:true});
    }});'''),
        ('d.folder_path,d.employee_name,...d.groups.map(groupPath)',
         "d.folder_path,d.employee_name,...(d.vessel_ids||[]).filter(id=>!ui.vessel||id===ui.vessel).map(id=>vesselNames.get(id)),...d.groups.map(groupPath)"),
        ("'',q?t('No matching files'", "'',(q||ui.type||ui.vessel)?t('No matching files'"),
        ("if(q||ui.type)empty.append", "if(q||ui.type||ui.vessel)empty.append"),
        ("ui.type='';subtype.querySelector('select').value='';reset();", "ui.type='';ui.vessel='';ui.page=0;selected.clear();h.redraw();"),
        ('folderId:folder,\n     setQuery:', 'folderId:folder,redraw:draw,\n     setQuery:'),
    ]
    for before, after in changes:
        source = once(source, before, after)
    return source


def transforms():
    return {'app/library_workspace_files.py': catalogue, 'app/context_documents.py': handovers,
            'app/static/original_library.js': browser}
