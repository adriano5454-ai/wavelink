"""Consumption posting is a separate, per-vessel grant."""
from . import fleet_access as access
from .fleet_tank_readings import vessel
from .store import Problem

def ensure(c):
    c.execute("""CREATE TABLE IF NOT EXISTS fleet_consumption_grants (
        user_id TEXT NOT NULL, site_id TEXT NOT NULL, PRIMARY KEY(user_id,site_id))""")

def allowed(c,a,sid):
    if not access.allowed(c,a,sid):
        return False
    if access.is_admin(c,a):
        return True
    return c.execute('SELECT 1 FROM fleet_consumption_grants WHERE user_id=? AND site_id=?',
                     (a['user_id'],sid)).fetchone() is not None

def require(c,a,sid):
    s = vessel(c,a,sid)
    if not allowed(c,a,sid):
        raise Problem(403,'You can view this vessel, but do not have permission to post consumption.')
    return s
