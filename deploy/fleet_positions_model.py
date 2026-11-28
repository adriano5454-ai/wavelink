"""Manual reported positions only. One company's SQLite per hub. Append-only revisions."""
import math
from datetime import datetime, timezone
from . import fleet_access as access
from .fieldwork_common import text,version
from .store import Problem,utcnow

def ensure(c):
    c.execute("""CREATE TABLE IF NOT EXISTS fleet_position_reports(site_id TEXT NOT NULL, revision INTEGER NOT NULL, lat REAL NOT NULL, lon REAL NOT NULL, observed TEXT NOT NULL, source TEXT NOT NULL, reporter TEXT NOT NULL, recorded TEXT NOT NULL, PRIMARY KEY(site_id,revision))""")

def latest(c,sid):
    row=c.execute("SELECT revision,lat,lon,observed,source FROM fleet_position_reports WHERE site_id=? ORDER BY revision DESC LIMIT 1",(sid,)).fetchone()
    return dict(row) if row else None

def read(fleet,a):
    from .fleet import _all
    with fleet.store.connection() as c:
        user=fleet._person(c,a)
        return {'admin':user['role']=='admin','sites':[dict(id=s['id'],name=s['name'],version=s['version'],position=latest(c,s['id'])) for s in sorted(_all(c,'fleet_sites'),key=lambda s:s['name'].casefold()) if s['kind']=='vessel' and s['active'] and access.allowed(c,a,s['id'])]}

def save(c,p,a):
    from .fleet import _get
    access.require_admin(c,a)
    s=_get(c,'fleet_sites',p.get('id'))
    if not s['active'] or s['kind']!='vessel':raise Problem(422,'Select an active vessel.')
    version(s,p.get('version'))
    old=latest(c,s['id'])
    if type(p.get('revision')) is not int or p['revision']!=(old or {}).get('revision',0):raise Problem(409,'Position changed. Reload the map.')
    lat,lon=p.get('lat'),p.get('lon')
    if any(type(v) not in (int,float) or not -m<=v<=m for v,m in [(lat,90),(lon,180)]):raise Problem(422,'Invalid latitude or longitude.')
    try:
        raw=p['observed']
        if not isinstance(raw,str) or len(raw) not in (17,20) or not raw.endswith('Z'):raise ValueError
        at=datetime.strptime(raw,'%Y-%m-%dT%H:%MZ' if len(raw)==17 else '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        if at>datetime.now(timezone.utc):raise ValueError
    except (ValueError,KeyError,TypeError):raise Problem(422,'Enter a valid UTC observation time, not in the future.')
    stamp=at.strftime('%Y-%m-%dT%H:%M:%SZ')
    if old and stamp<old['observed']:raise Problem(409,'An older observation cannot replace the latest position.')
    source=text(p.get('source',''),'Position source',120,True)
    c.execute('INSERT INTO fleet_position_reports VALUES (?,?,?,?,?,?,?,?)',(s['id'],p['revision']+1,lat,lon,stamp,source,a['user_id'],utcnow()))
    return 'site',s['id']
