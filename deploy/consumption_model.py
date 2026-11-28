"""Daily vessel-wide stock-balance estimates, separate from tank soundings."""
from datetime import date, datetime, timezone
from decimal import Decimal
import math
from .fieldwork_common import base, version
from .fleet_tank_readings import KINDS
from . import fleet_consumption_access as access
from .store import Problem

FIELDS = ('opening', 'closing', 'received', 'produced', 'transfer_in', 'transfer_out', 'other_out')
UNITS = {'fresh_water':'m3', 'diesel':'L', 'fuel_oil':'L', 'other_fuel':'L'}

def ensure(c):
    c.execute("""CREATE TABLE IF NOT EXISTS fleet_consumption (
        id TEXT PRIMARY KEY, site_id TEXT NOT NULL, day TEXT NOT NULL,
        contents TEXT NOT NULL, unit TEXT NOT NULL, opening REAL NOT NULL, closing REAL NOT NULL,
        received REAL NOT NULL, produced REAL NOT NULL, transfer_in REAL NOT NULL,
        transfer_out REAL NOT NULL, other_out REAL NOT NULL, used REAL NOT NULL,
        reporter TEXT NOT NULL, recorded TEXT NOT NULL, UNIQUE(site_id,day,contents))""")
    c.execute('CREATE INDEX IF NOT EXISTS consumption_site_kind_day ON fleet_consumption(site_id,contents,day DESC)')

def daily(c, sid):
    cols = ','.join(('id','day','contents','unit',*FIELDS,'used'))
    return {kind:[dict(r) for r in c.execute(
        f'SELECT {cols} FROM fleet_consumption WHERE site_id=? AND contents=? ORDER BY day DESC LIMIT 30',
        (sid,kind))] for kind in sorted(KINDS)}

def result(c, a, rid):
    r = c.execute('SELECT site_id,used,unit FROM fleet_consumption WHERE id=?',(rid,)).fetchone()
    if not r:
        raise Problem(404,'Consumption entry not available.')
    access.require(c,a,r['site_id'])
    return dict(id=rid,saved=True,used=r['used'],unit=r['unit'])

def save(c,p,a):
    s = access.require(c,a,p.get('site_id'))
    version(s,p.get('version'))
    kind = p.get('contents')
    if not isinstance(kind,str) or kind not in UNITS or p.get('unit') != UNITS[kind]:
        raise Problem(422,'Choose a contents type and use its displayed unit.')
    stamp = p.get('day')
    try:
        day = date.fromisoformat(stamp)
        if day.isoformat() != stamp or not date(2000,1,1) <= day < datetime.now(timezone.utc).date():
            raise ValueError
    except (TypeError, ValueError):
        raise Problem(422,'Enter a completed UTC day.')
    amounts = []
    for key in FIELDS:
        q = p.get(key)
        if type(q) not in (int,float) or not 0 <= q <= 1_000_000_000 or not math.isfinite(q):
            raise Problem(422,'Enter a nonnegative quantity up to one billion in each field.')
        amount = Decimal(str(q))
        if amount != amount.quantize(Decimal('.001')):
            raise Problem(422,'Use no more than three decimal places.')
        amounts.append(amount)
    opening,closing,received,produced,transfer_in,transfer_out,other_out = amounts
    if kind != 'fresh_water' and produced:
        raise Problem(422,'Onboard production is only supported for fresh water.')
    used = opening + received + produced + transfer_in - transfer_out - other_out - closing
    if used < 0:
        raise Problem(422,'The balance is negative. Check the stocks and movements.')
    if c.execute('SELECT 1 FROM fleet_consumption WHERE site_id=? AND day=? AND contents=?',
                 (s['id'],stamp,kind)).fetchone():
        raise Problem(409,'A balance already exists for this vessel, date and contents.')
    rid = base(a)['id']
    c.execute('INSERT INTO fleet_consumption VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
              (rid,s['id'],stamp,kind,UNITS[kind],*map(float,amounts),float(used),
               a['user_id'],datetime.now(timezone.utc).isoformat()))
    return 'consumption',rid
