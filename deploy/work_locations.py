"""Fleet references for operational records. The owning service controls record access."""
from __future__ import annotations

import json
import unicodedata


def fold(value):
    value = unicodedata.normalize('NFKD', str(value or '').casefold())
    return ' '.join(''.join(char for char in value if not unicodedata.combining(char)).split())


def catalog(c, actor):
    from . import fleet_access
    user = fleet_access.current(c, actor)
    if not c.execute("SELECT 1 FROM sqlite_master WHERE name='fleet_sites'").fetchone():
        return []
    from .access import effective
    rights=effective(c,user['id'],user['role'])
    operational=('tasks.view','faults.view','maintenance.view','checklists.view','toolbox.view',
                 'handovers.view','logs.view','inventory.view','certificates.view','qshe.view','hr.view_own','it.view_own')
    restricted = fleet_access.restricted(c,user['id']) or (user['role']!='admin' and not any(rights.get(key) for key in operational))
    sites = []
    for row in c.execute('SELECT body FROM fleet_sites'):
        site = json.loads(row[0])
        if restricted and not fleet_access.allowed(c, actor, site['id']):
            continue
        sites.append({key: site.get(key, '') for key in ('id', 'name', 'code', 'kind', 'active')})
    return sorted(sites, key=lambda site: (fold(site['name']), site['id']))


def selection(c, actor, payload, previous=None):
    """Omitted for historical clients. A submitted reference is always checked here."""
    if 'work_site_id' not in payload:
        return previous
    ident = payload['work_site_id']
    sites = catalog(c, actor)
    if ident == '' and not any(site['active'] for site in sites) and not previous:
        return None
    for site in sites:
        if ident == site['id'] and (site['active'] or (previous or {}).get('id') == ident):
            return dict(site)
    from .store import Problem
    raise Problem(422, 'Choose an active ship or base. / Selecione uma embarcação ou base ativa.')


def for_name(c, actor, label):
    if not label:
        return None
    matches = [site for site in catalog(c, actor) if site['name'].casefold() == label.casefold()]
    return matches[0] if len(matches) == 1 else None


class SiteLookup:
    def __init__(self, sites):
        self.by_id = {site['id']: site for site in sites}
        self.by_label = {}
        for site in sites:
            for field in ('name', 'code'):
                key = fold(site[field])
                if key:
                    self.by_label.setdefault(key, set()).add(site['id'])

    def resolve(self, item, *, parent=None, kind=''):
        item = item or {}
        result = []
        def add(ident):
            site = self.by_id.get(ident)
            if site and site not in result:
                result.append(site)

        if kind == 'fleet':
            add(item.get('id'))
        if kind == 'inventory' and item.get('fleet_custody'):
            add(item['fleet_custody'].get('site_id'))
            return result
        add((item.get('vessel_scope') or {}).get('site_id'))
        ref = item.get('work_site') or (item.get('meta') or {}).get('work_site')
        if isinstance(ref, dict):
            add(ref.get('id'))
        if kind == 'manifests':
            add(item.get('origin_id'))
            add(item.get('destination_id'))
        custody = item.get('fleet_custody') or {}
        if isinstance(custody, dict):
            add(custody.get('site_id'))
        add(item.get('site_id'))
        if not result and parent:
            result.extend(self.resolve(parent))
        if not result:
            meta = item.get('meta') or {}
            for value in (meta.get('vessel'), meta.get('site'), item.get('location'),
                          (item.get('edit') or {}).get('location'), (item.get('daily') or {}).get('location')):
                matches = self.by_label.get(fold(value), ())
                if len(matches) == 1:
                    add(next(iter(matches)))
        return result


def pages(fetch, key):
    offset = 0
    while True:
        page = fetch(offset)
        items = page.get(key, [])
        yield from items
        offset += len(items)
        if not items or offset >= page.get('total', offset):
            return
