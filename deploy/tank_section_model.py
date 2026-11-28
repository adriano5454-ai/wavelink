from datetime import datetime,timezone
import re
from . import fleet_access as access
from .fieldwork_common import base,text,version
from .store import Problem

KINDS={'fresh_water','diesel','fuel_oil','other_fuel'}
METHODS={'gauge','sounding','manual'}

def ensure(c):
    c.execute("""CREATE TABLE IF NOT EXISTS fleet_tank_readings (
        id TEXT PRIMARY KEY,site_id TEXT NOT NULL,tank TEXT NOT NULL,tank_key TEXT NOT NULL,
        contents TEXT NOT NULL,quantity REAL NOT NULL,unit TEXT NOT NULL,method TEXT NOT NULL,
        observed TEXT NOT NULL,recorded TEXT NOT NULL,reporter TEXT NOT NULL)""")
    c.execute('CREATE INDEX IF NOT EXISTS tank_readings_site_time ON fleet_tank_readings(site_id,observed DESC,recorded DESC,id DESC)')

def vessel(c,a,sid,action='view'):
    from .fleet import _get
    access.require_site(c,a,sid,action)
    s=_get(c,'fleet_sites',sid)
    if not s['active'] or s['kind']!='vessel':raise Problem(404,'Active vessel not available.')
    return s

def read(fleet,a,sid='',readonly=False):
    from .fleet import _all
    with fleet.store.connection() as c:
        fleet._person(c,a)
        sites=[dict(id=s['id'],name=s['name'],version=s['version']) for s in sorted(_all(c,'fleet_sites'),key=lambda s:s['name'].casefold()) if s['kind']=='vessel' and s['active'] and access.allowed(c,a,s['id'])]
        if not sid:return {'sites':sites}
        vessel(c,a,sid)
        cols='id,tank,contents,quantity,unit,method,observed'
        order='observed DESC, recorded DESC, id DESC'
        history=[dict(r) for r in c.execute(f'SELECT {cols} FROM fleet_tank_readings WHERE site_id=? ORDER BY {order} LIMIT 101',(sid,))]
        latest=[dict(r) for r in c.execute(f"""SELECT {cols} FROM (SELECT *,ROW_NUMBER() OVER(PARTITION BY tank_key ORDER BY {order}) AS rank FROM fleet_tank_readings WHERE site_id=?) WHERE rank=1 ORDER BY tank_key""",(sid,))]
        return {'sites':sites,'latest':latest,'history':history[:100],'more':len(history)>100,'can_record':not readonly and access.allowed(c,a,sid,'prepare')}

def result(c,a,rid):
    row=c.execute('SELECT id,site_id FROM fleet_tank_readings WHERE id=?',(rid,)).fetchone()
    if not row:raise Problem(404,'Reading not available.')
    vessel(c,a,row['site_id'],'prepare')
    return {'id':rid,'saved':True}

def save(c,p,a):
    s=vessel(c,a,p.get('site_id'),'prepare')
    version(s,p.get('version'))
    tank=text(p.get('tank',''),'Tank',80,True)
    kind,unit,method=(p.get(k) for k in ('contents','unit','method'))
    if kind not in tuple(KINDS) or method not in tuple(METHODS) or unit not in ('L','m3','kg','t') or (kind=='fresh_water' and unit not in ('L','m3')):
        raise Problem(422,'Choose compatible contents, unit and measurement method.')
    q=p.get('quantity')
    if type(q) not in (int,float) or not 0<=q<=1_000_000_000:raise Problem(422,'Enter a finite nonnegative quantity up to one billion.')
    stamp=p.get('observed')
    if not isinstance(stamp,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z',stamp):raise Problem(422,'Enter UTC measurement time.')
    try:
        when=datetime.fromisoformat(stamp)
        if when>datetime.now(timezone.utc):raise ValueError
    except ValueError:raise Problem(422,'Enter valid UTC measurement time, not in the future.')
    rid=base(a)['id']
    c.execute('INSERT INTO fleet_tank_readings VALUES (?,?,?,?,?,?,?,?,?,?,?)',(rid,s['id'],tank,tank.casefold(),kind,q,unit,method,when.isoformat(timespec='seconds').replace('+00:00','Z'),datetime.now(timezone.utc).isoformat(),a['user_id']))
    return 'tank_reading',rid
