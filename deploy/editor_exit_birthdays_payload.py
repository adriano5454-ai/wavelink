"""Optional day and month shared by an individual with their company's Team."""
from datetime import date, datetime, timedelta, timezone

from . import membership_policy
from .access import effective
from .fleet_access import restricted
from .recognition_moods import company_zone
from .store import Problem


class TeamBirthdays:
    def __init__(self, store, hub_id, company_id, shared_login):
        self.store = store
        self.hub_id = hub_id
        self.zone = company_zone(company_id)
        self.shared_login = shared_login.casefold()
        self.clock = lambda: datetime.now(timezone.utc)
        with store.connection(True) as c:
            c.execute('''CREATE TABLE IF NOT EXISTS team_birthdays(
                hub_id TEXT NOT NULL, user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                month INTEGER, day INTEGER, version INTEGER NOT NULL CHECK(version>0),
                PRIMARY KEY(hub_id,user_id),
                CHECK((month IS NULL AND day IS NULL) OR
                      (month IS NOT NULL AND day IS NOT NULL AND month BETWEEN 1 AND 12 AND
                       day BETWEEN 1 AND CASE WHEN month=2 THEN 29 WHEN month IN (4,6,9,11) THEN 30 ELSE 31 END)))''')
            c.execute('''CREATE INDEX IF NOT EXISTS team_birthdays_calendar
                         ON team_birthdays(hub_id,month,day) WHERE month IS NOT NULL''')

    def today(self):
        return self.clock().astimezone(self.zone).date()

    def _viewer(self, c, actor):
        user = self.store.recognition._person(c, actor)
        if (user['login_id'].casefold() == self.shared_login or restricted(c, user['id'])
                or c.execute('SELECT 1 FROM deleted_users WHERE user_id=?', (user['id'],)).fetchone()
                or not any(effective(c, user['id'], user['role']).values())):
            raise Problem(403, 'Use a personal account with access to the team.')
        return user['id']

    def _mine(self, c, uid):
        row = c.execute('SELECT month,day,version FROM team_birthdays WHERE hub_id=? AND user_id=?',
                        (self.hub_id, uid)).fetchone()
        return dict(row) if row else dict(month=None, day=None, version=0)

    def mine(self, actor):
        with self.store.connection() as c:
            return self._mine(c, self._viewer(c, actor))

    def save(self, actor, month, day, version):
        if type(version) is not int or version < 0:
            raise Problem(422, 'Reload your birthday setting before saving.')
        if month is not None or day is not None:
            try:
                if type(month) is not int or type(day) is not int:
                    raise ValueError()
                date(2000, month, day)  # Recurring February 29 is a valid selection.
            except (ValueError, OverflowError):
                raise Problem(422, 'Choose a valid month and day.') from None
        with self.store.connection(True) as c:
            uid = self._viewer(c, actor)
            current = self._mine(c, uid)
            if current['version'] != version:
                raise Problem(409, 'Your birthday setting changed. Reload it before saving.')
            if (current['month'], current['day']) == (month, day):
                return current
            # Clearing erases the date but retains the revision. An old profile
            # tab cannot silently restore a birthday after consent is withdrawn.
            c.execute('''INSERT INTO team_birthdays(hub_id,user_id,month,day,version) VALUES(?,?,?,?,?)
                ON CONFLICT(hub_id,user_id) DO UPDATE SET
                month=excluded.month, day=excluded.day, version=excluded.version''',
                (self.hub_id, uid, month, day, version + 1))
            return dict(month=month, day=day, version=version + 1)

    def upcoming(self, actor, limit=6, offset=0):
        if type(limit) is not int or not 1 <= limit <= 50 or type(offset) is not int or not 0 <= offset <= 1_000_000:
            raise Problem(422, 'Choose a valid birthday page.')
        today = self.today()
        dates = [today + timedelta(days=n) for n in range(30)]
        values = ','.join(['(?,?,?)'] * len(dates))
        params = [v for n, d in enumerate(dates) for v in (d.month, d.day, n)]
        with self.store.connection() as c:
            self._viewer(c, actor)
            # As in Recognition.directory, managed accounts need current approved
            # membership and a valid saved policy. Evaluate the joins once for the
            # whole window. A missing, malformed, or suspended membership is hidden.
            eligible = f'''WITH upcoming(month,day,days_until) AS (VALUES {values}),
                eligible AS (
                    SELECT u.id AS user_id, u.name, d.month,d.day,d.days_until
                    FROM upcoming d JOIN team_birthdays b ON b.hub_id=? AND b.month=d.month AND b.day=d.day
                    JOIN users u ON u.id=b.user_id
                    LEFT JOIN company_memberships m ON m.user_id=u.id
                    LEFT JOIN account_permissions p ON p.user_id=u.id
                    WHERE u.enabled=1 AND u.login_id<>? COLLATE NOCASE
                    AND NOT EXISTS(SELECT 1 FROM deleted_users x WHERE x.user_id=u.id)
                    AND (u.role='admin' OR NOT EXISTS(SELECT 1 FROM fleet_account_scope f
                        WHERE f.user_id=u.id AND f.mode='vessel_only'))
                    AND (u.membership_required<>1 OR (m.state='approved'
                        AND EXISTS(SELECT 1 FROM company_membership_meta WHERE singleton=1 AND version=?)
                        AND json_type(CASE WHEN json_valid(p.permissions) THEN p.permissions ELSE 'null' END)='object'
                        AND NOT EXISTS(SELECT 1 FROM json_each(
                            CASE WHEN json_valid(p.permissions) THEN p.permissions ELSE 'null' END)
                            WHERE type NOT IN ('true','false'))))
                ), page AS (
                    SELECT * FROM eligible ORDER BY days_until,name COLLATE NOCASE,user_id LIMIT ? OFFSET ?
                )
                SELECT page.*,totals.total FROM (SELECT count(*) AS total FROM eligible) totals
                LEFT JOIN page ON 1 ORDER BY days_until,name COLLATE NOCASE,user_id'''
            rows = c.execute(eligible, (*params, self.hub_id, self.shared_login,
                                        membership_policy.VERSION, limit, offset)).fetchall()
            return dict(total=rows[0]['total'], items=[
                {k: row[k] for k in ('user_id','name','month','day','days_until')}
                for row in rows if row['user_id'] is not None])
