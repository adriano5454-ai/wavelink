"""Read-only crew examples for NativeShowcase's disposable company."""
from datetime import date, timedelta
from pathlib import Path
from tempfile import gettempdir
from uuid import NAMESPACE_URL, uuid5


def fixture_id(key):
    return str(uuid5(NAMESPACE_URL, 'urn:wavelink:public-crew:v1:' + key))


# Each row is a fictional crew member and their inclusive assignment legs.
CREW = (
    ('Mira Vale', 'Hydrographer', [('DEMO-MERIDIAN', 'DEMO-101', -3, 3), ('DEMO-HORIZON', 'DEMO-101', 4, 11)]),
    ('Idris Fen', 'ROV pilot', [('DEMO-HORIZON', 'DEMO-202', -2, 4), ('AUR', 'DEMO-202', 5, 12)]),
    ('Nila Arden', 'Survey engineer', [('DEMO-MERIDIAN', 'DEMO-101', -4, 9)]),
    ('Oren North', 'Sonar operator', [('DEMO-MERIDIAN', 'DEMO-303', -1, 10)]),
    ('Vera Brook', 'Deck supervisor', [('DEMO-MERIDIAN', 'DEMO-303', 1, 12)]),
    ('Sol Marin', 'ROV supervisor', [('DEMO-HORIZON', 'DEMO-202', -3, 9)]),
    ('Ivo Moss', 'Geophysicist', [('DEMO-HORIZON', 'DEMO-101', -1, 11)]),
    ('Tess Reed', 'Marine electrician', [('AUR', 'DEMO-202', -2, 8)]),
    ('Lena Cove', 'Survey technician', [('AUR', 'DEMO-303', 0, 10)]),
    ('Rui Dale', 'Deck technician', [('AUR', 'DEMO-303', 2, 12)]),
    ('Pia Shore', 'Logistics planner', [('DEMO-SHORE', 'DEMO-101', -4, 10)]),
    ('Cleo Finch', 'Equipment coordinator', [('DEMO-SHORE', 'DEMO-303', -2, 11)]),
)


def populate_crew(showcase):
    from app import work_locations
    from app.hr import identity
    from app.store import utcnow

    store = showcase.core.state.store
    temp = Path(showcase.temp.name).resolve()
    company = temp / 'company'
    if (not showcase.gate.public_entry or temp.parent != Path(gettempdir()).resolve()
            or not temp.name.startswith('wavelink-public-')
            or not store.path.resolve().is_relative_to(company)):
        raise ValueError('Crew fixtures require the disposable public showcase.')
    actor = showcase.manager
    today = date.today()
    projects = {}
    for code in sorted({code for _, _, legs in CREW for _, code, _, _ in legs}):
        result = store.hr.run('save_timesheet_project', dict(version=0, name=code, active=True,
                              approver_ids=[actor['user_id']]), actor, fixture_id('project/' + code))
        projects[code] = result['project']['id']
    with store.connection(True) as c:
        sites = {s['code']:s for s in work_locations.catalog(c, actor) if s['active']}
        manager = c.execute('SELECT * FROM users WHERE id=?', (actor['user_id'],)).fetchone()
        for name, role, legs in CREW:
            uid = fixture_id(name)
            # Canonical HR records reference users. These roster-only identities are
            # disabled at insertion, with no password, email, invitation or session.
            c.execute("""INSERT INTO users(id,login_id,name,role,enabled,password_hash,created_at,updated_at)
                         VALUES(?,?,?,'technician',0,'',?,?) ON CONFLICT(id) DO NOTHING""",
                      (uid, 'roster:' + uid, name, utcnow(), utcnow()))
            for site_code, project, begin, end in legs:
                record_id = fixture_id(name + '/' + site_code)
                if c.execute('SELECT 1 FROM hr_records WHERE id=?', (record_id,)).fetchone():
                    continue
                site = sites[site_code]
                payload = dict(title=role, location=site['name'], project=project, shift_name=role,
                               assignment_type='onshore' if site_code=='DEMO-SHORE' else 'offshore',
                               start_on=(today+timedelta(days=begin)).isoformat(),
                               end_on=(today+timedelta(days=end)).isoformat(), status='planned',
                               time_zone='UTC', start_time='06:00', end_time='18:00')
                values = store.hr._values(c, 'shifts', payload, None)
                record = dict(values, id=record_id, kind='shifts', version=1, user_id=uid,
                              user_name=name, work_site=site, roster_project_id=projects[project],
                              created_at=utcnow(), created_by=identity(manager), attachments=[])
                store.hr._commit_record(c, record, manager, 'seed_demo_shift', None)
