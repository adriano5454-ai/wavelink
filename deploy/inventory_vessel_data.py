"""Add inventory vessel read models to the packaged runtime."""


def replace_one(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected inventory source near ' + old[:70])
    return source.replace(old, new)


POSITION = '''
    def inventory_position(self, item, containers=()):
        """Resolve the current site. A shipment in transit has no current site."""
        lineage = (item, *containers)  # nearest container first
        for row in lineage:
            custody = row.get('fleet_custody')
            if custody:
                if custody.get('state') == 'in_transit':
                    return None
                return self.by_id.get(custody.get('site_id'))
        for row in lineage:
            ref = row.get('work_site') or (row.get('meta') or {}).get('work_site') or {}
            ident = ref.get('id') or row.get('site_id')
            if ident:
                return self.by_id.get(ident)
        for row in lineage:
            matched = self.resolve(row)
            if matched:
                return matched[0]
        return None
'''


def work_locations(source):
    source = replace_one(source, '    def resolve(self, item,', POSITION + '\n    def resolve(self, item,')
    return replace_one(source, """        if kind == 'inventory' and item.get('fleet_custody'):
            add(item['fleet_custody'].get('site_id'))
            return result""", """        if kind == 'inventory':
            if 'inventory_site_id' in item:
                add(item['inventory_site_id'])
            else:
                site = self.inventory_position(item)
                if site:
                    add(site['id'])
            return result""")


READ_ITEMS = '''
def positioned_items(c, list_id, lookup, *, item_ids=None):
    """Read one list, or specific items and their ancestors, including custody."""
    from .inventory_boxes import MAX_DEPTH
    has_custody = c.execute("SELECT 1 FROM sqlite_master WHERE name='fleet_custody'").fetchone()
    join = 'LEFT JOIN fleet_custody AS custody ON custody.item_id=item.id' if has_custody else ''
    custody_column = 'custody.body' if has_custody else 'NULL'
    prefix = ''
    where = 'WHERE item.parent_id=?'
    params = (list_id,)
    if item_ids is not None:
        params = (*item_ids, MAX_DEPTH)
        marks = ','.join('?' for _ in item_ids)
        prefix = f"""WITH RECURSIVE ancestry(id, list_id, container, depth) AS (
            SELECT id, parent_id, json_extract(body, '$.container_id'), 0
              FROM inventory_items WHERE id IN ({marks})
            UNION
            SELECT parent.id, parent.parent_id, json_extract(parent.body, '$.container_id'), a.depth + 1
              FROM inventory_items AS parent JOIN ancestry AS a
                ON parent.id=a.container AND parent.parent_id=a.list_id
             WHERE a.depth < ?
        )"""
        where = 'WHERE item.id IN (SELECT id FROM ancestry)'
    items = []
    for body, custody_body in c.execute(
            f'{prefix} SELECT item.body, {custody_column} FROM inventory_items AS item {join} {where}', params):
        item = json.loads(body)
        if custody_body:
            custody = json.loads(custody_body)
            site = lookup.by_id.get(custody.get('site_id'), {})
            item['fleet_custody'] = dict(custody, site_name=site.get('name', ''))
        items.append(item)
    by_id = {item['id']: item for item in items}
    for item in items:
        containers = []
        parent = by_id.get(item.get('container_id'))
        seen = {item['id']}
        while (parent and parent.get('list_id') == item.get('list_id')
               and parent['id'] not in seen and len(containers) < MAX_DEPTH):
            containers.append(parent)
            seen.add(parent['id'])
            parent = by_id.get(parent.get('container_id'))
        site = lookup.inventory_position(item, containers)
        item['equipment_work_site'] = site
        item['inventory_site_id'] = site['id'] if site else ''
        item['vessel_id'] = site['id'] if site and site['kind'] == 'vessel' else ''
        item.setdefault('part_number', '')
    return items


def equipment_sites(c, actor, item_ids):
    """Resolve equipment already authorised by the caller to current, visible Fleet sites."""
    ids = list(dict.fromkeys(item_ids))
    if not ids:
        return {}
    lookup = sites.SiteLookup(sites.catalog(c, actor))
    result = {}
    for start in range(0, len(ids), 250):
        batch = ids[start:start+250]
        wanted = set(batch)
        for item in positioned_items(c, None, lookup, item_ids=batch):
            if item['id'] in wanted:
                result[item['id']] = lookup.by_id.get(item['inventory_site_id'])
    return result
'''


def inventory(source):
    source = replace_one(source, 'class Inventory(CategoriesMixin,BoxesMixin,Service):',
                         READ_ITEMS + '\n\nclass Inventory(CategoriesMixin,BoxesMixin,Service):')
    source = replace_one(source, '    def list(self,actor):', '    def list(self,actor,*,include_vessels=False):')
    source = replace_one(source, """            result=[]
            for b in rows(c,'inventory_lists'):
                items=rows(c,'inventory_items',b['id'])
                result.append(dict(b,category_summary=""", """            from collections import Counter
            result=[]
            catalog = sites.catalog(c, actor) if include_vessels else []
            lookup = sites.SiteLookup(catalog) if include_vessels else None
            for b in rows(c,'inventory_lists'):
                if include_vessels:
                    items = positioned_items(c, b['id'], lookup)
                    b['vessel_counts'] = dict(Counter(x['vessel_id'] for x in items if x['vessel_id'] and not x['archived']))
                else:
                    items = rows(c, 'inventory_items', b['id'])
                result.append(dict(b,category_summary=""")
    source = replace_one(source, '            return result\n    def get(self,bid,actor):', """            if include_vessels:
                return dict(lists=result, vessels=[s for s in catalog if s['kind']=='vessel'])
            return result
    def get(self,bid,actor):""")
    return replace_one(source, """            from .fleet import annotate
            return dict(b,items=annotate(c,decorate([dict(x,part_number=x.get('part_number','')) for x in rows(c,'inventory_items',bid)])),counts=""", """            catalog = sites.catalog(c, actor)
            items = positioned_items(c, bid, sites.SiteLookup(catalog))
            return dict(b,vessels=[s for s in catalog if s['kind']=='vessel'],items=decorate(items),counts=""")


def fieldwork_api(source):
    return replace_one(source, '    def inventories(a=Depends(logged)):return store.inventory.list(a)',
                       '    def inventories(include_vessels:bool=False,a=Depends(logged)):\n'
                       '        return store.inventory.list(a, include_vessels=include_vessels)')


def transforms():
    return {'app/inventory.py': inventory, 'app/fieldwork_api.py': fieldwork_api,
            'app/work_locations.py': work_locations}
