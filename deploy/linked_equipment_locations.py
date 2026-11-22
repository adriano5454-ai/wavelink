"""Add permission-checked equipment locations to the native record writers and pickers."""


def replace(source, before, after):
    if source.count(before) != 1:
        raise ValueError('Unexpected equipment location integration point: '+before)
    return source.replace(before, after)


HELPERS = '''

def attach_equipment_sites(c, actor, options):
    """Add current location to already authorised equipment choices."""
    from .inventory import equipment_sites
    positions = equipment_sites(c, actor, [item['id'] for item in options]) if options else {}
    for item in options:
        item['work_site'] = positions.get(item['id'])


def common_equipment_site(positions, ids):
    if not ids:
        return None
    first = positions.get(ids[0])
    if first and first['active'] and all(positions.get(iid) == first for iid in ids):
        return first
    return None


def visible_equipment_positions(c, actor, ids):
    from .access import effective
    from .fleet_access import current
    from .inventory import equipment_sites
    if not ids:
        return {}
    user = current(c, actor)
    if not effective(c, user['id'], user['role']).get('inventory.view'):
        return {}
    return equipment_sites(c, actor, ids)


def linked_sites(c, actor, kind, records):
    """Resolve only records the caller has already checked for source access."""
    site_by_id = {site['id']: site for site in catalog(c, actor)}
    ids_by_record = {}
    result = {}
    for record in records:
        rid = record['id']
        if kind != 'asset' and record.get('work_site'):
            site = site_by_id.get(record['work_site']['id'])
            result[rid] = site if site and site['active'] else None
        elif kind == 'asset':
            ids_by_record[rid] = [rid]
        elif kind == 'maintenance':
            asset = record.get('asset') or {}
            ids_by_record[rid] = [asset['id']] if asset.get('id') else []
        elif kind == 'certificate':
            ids_by_record[rid] = record.get('asset_ids', [])
    ids = {iid for asset_ids in ids_by_record.values() for iid in asset_ids}
    positions = visible_equipment_positions(c, actor, ids)
    for rid, asset_ids in ids_by_record.items():
        result[rid] = common_equipment_site(positions, asset_ids)
    return result


def equipment_selection(c, actor, payload, ids=(), *, link=None, previous=None):
    """Freeze one location at write time. An explicit location takes precedence."""
    if 'work_site_id' in payload:
        return selection(c, actor, payload, previous)
    if previous and 'equipment_site_hint' not in payload:
        return previous
    candidate = None
    if link:
        from .general_tasks import _link_record
        source = _link_record(c, link['kind'], link['id'], actor)
        candidate = linked_sites(c, actor, link['kind'], [source]).get(source['id'])
    elif ids:
        candidate = common_equipment_site(visible_equipment_positions(c, actor, ids), ids)
    if 'equipment_site_hint' in payload and (not candidate or candidate['id'] != payload['equipment_site_hint']):
        from .store import Problem
        raise Problem(409, 'Equipment location changed. Refresh and review the ship or base. / '
                           'O local do equipamento mudou. Atualize e confira a embarcação ou base.')
    return candidate
'''


def tasks(source):
    source = replace(source, "            found = []\n            active_lists",
                     "            found = []\n            sources = {}\n            active_lists")
    source = replace(source, '                found.append(link_summary(c, ref, actor))',
                     "                found.append(link_summary(c, ref, actor))\n                sources[b['id']] = b")
    source = replace(source, '            return dict(items=found[:100], total=len(found), truncated=len(found) > 100)', '''            page = found[:100]
            positions = sites.linked_sites(c, actor, kind, [sources[item['id']] for item in page])
            for item in page:
                item['work_site'] = positions.get(item['id'])
            return dict(items=page, total=len(found), truncated=len(found) > 100)''')
    source = replace(source, "allowed = {'work_site_id','kind'", "allowed = {'equipment_site_hint','work_site_id','kind'")
    return replace(source, "t['work_site'] = sites.selection(c,a,p)", "t['work_site'] = sites.equipment_selection(c, a, p, link=link)")


def stock_tasks(source):
    source = replace(source, '            return dict(departments=deps,users=users if can_create else [],inventories=inv',
                     "            sites.attach_equipment_sites(c, actor, [item for book in inv for item in book['items']])\n"
                     '            return dict(departments=deps,users=users if can_create else [],inventories=inv')
    source = replace(source, "**({'work_site_id':p['work_site_id']} if 'work_site_id' in p else {})",
                     "**{k:p[k] for k in ('work_site_id','equipment_site_hint') if k in p}")
    return replace(source, "t['work_site']=sites.selection(c,a,p)", "t['work_site']=stored.get('work_site')")


def reports(source):
    source = replace(source, "check_fields(p,{'work_site_id','title'", "check_fields(p,{'equipment_site_hint','work_site_id','title'")
    source = replace(source, "check_fields(p,{'id','version','work_site_id','title'", "check_fields(p,{'id','version','equipment_site_hint','work_site_id','title'")
    source = replace(source, "f['work_site']=sites.selection(c,a,p)\n",
                     "f['work_site']=sites.equipment_selection(c, a, p, [f['asset_link']['id']] if f.get('asset_link') else [])\n")
    source = replace(source, '            return dict(items=result[:100],total=len(result),truncated=len(result)>100)',
                     """            page = result[:100]
            if kind == 'asset':
                sites.attach_equipment_sites(c, a, page)
            return dict(items=page,total=len(result),truncated=len(result)>100)""")
    source = replace(source, "        f['work_site']=sites.selection(c,a,p,f.get('work_site'))\n", '')
    return replace(source, '        if all(f.get(k)==v for k,v in fields.items()):',
                   """        if 'work_site_id' in p or 'equipment_site_hint' in p:
            fields['work_site'] = sites.equipment_selection(c, a, p, [f['asset_link']['id']] if f.get('asset_link') else [], previous=f.get('work_site'))
        if all(f.get(k)==v for k,v in fields.items()):""")


def certificates(source):
    source = replace(source, "            return dict(**d,items=sorted(items,key=lambda x:x['name'].casefold()))",
                     "            sites.attach_equipment_sites(c, actor, items)\n            return dict(**d,items=sorted(items,key=lambda x:x['name'].casefold()))")
    return replace(source, "        if 'work_site_id' in p:values['work_site']=sites.selection(c,a,p,b.get('work_site'))",
                   """        if not cid or 'work_site_id' in p or 'equipment_site_hint' in p or set(values['asset_ids']) != set(b.get('asset_ids', [])):
            values['work_site'] = sites.equipment_selection(c, a, p, values['asset_ids'], previous=b.get('work_site'))""")


def assets(source):
    source = replace(source, '            return dict(directory=directory(c), inventories=[',
                     '            result = dict(directory=directory(c), inventories=[')
    source = replace(source, '    def get(self, item_id, actor):',
                     """            from .work_locations import attach_equipment_sites
            attach_equipment_sites(c, actor, [item for book in result['inventories'] for item in book['items']])
            return result

    def get(self, item_id, actor):""")
    return replace(source, '            item = annotate(c,[item])[0]',
                   """            item = annotate(c,[item])[0]
            from .inventory import equipment_sites
            item['equipment_work_site'] = equipment_sites(c, actor, [item_id]).get(item_id)""")


def maintenance(source):
    return replace(source, "j['work_site']=sites.selection(c,a,p)",
                   """j['work_site']=sites.equipment_selection(c, a, p, [asset['id']] if asset else [])
        if asset and 'work_site_id' not in p:
            j['equipment_site_derived'] = True""")


def maintenance_cycles(source):
    return replace(source, "            planned['work_site'] = j.get('work_site')",
                   """            if j.get('equipment_site_derived') and linked:
                from .work_locations import equipment_selection
                planned['work_site'] = equipment_selection(c, a, {}, [linked['id']])
                planned['equipment_site_derived'] = True
            else:
                planned['work_site'] = j.get('work_site')""")


def transforms():
    return {
        'app/work_locations.py': lambda s: s + HELPERS,
        'app/general_tasks.py': tasks,
        'app/work_tasks.py': stock_tasks,
        'app/inventory.py': lambda s: replace(s, "s['work_site']=sites.selection(c,a,p)", "s['work_site']=sites.equipment_selection(c, a, p, [x['id'] for x in items])"),
        'app/assets.py': assets,
        'app/fault_reports.py': reports,
        'app/qshe_reports.py': reports,
        'app/certificates.py': certificates,
        'app/maintenance.py': maintenance,
        'app/maintenance_cycles.py': maintenance_cycles,
        'app/fault_task_creation.py': lambda s: replace(s, "if 'work_site_id' not in task and f.get('work_site'):",
            "if 'work_site_id' not in task and 'equipment_site_hint' not in task and f.get('work_site'):"),
    }
