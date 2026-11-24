"""Fictional personnel and service records for the disposable public company."""
from base64 import b64encode
from datetime import date, timedelta
from pathlib import Path
import secrets
from uuid import uuid4

from .demo_management_files import sample_file


def populate(showcase):
    from app import access
    from app.accounts import password_hash
    from app.departments import Departments
    from app.handovers import SECTIONS
    from app.simple_handovers import SimpleHandovers

    from tempfile import gettempdir
    core = showcase.core
    store, accounts = core.state.store, core.state.accounts
    root = Path(showcase.temp.name).resolve()
    if (not showcase.gate.public_entry or root.parent != Path(gettempdir()).resolve()
            or not root.name.startswith('wavelink-public-') or not store.path.resolve().is_relative_to(root / 'company')):
        raise ValueError('Fictional shifts require a disposable public showcase.')
    if hasattr(core.state, 'fictional_seed_result'):
        return core.state.fictional_seed_result
    with store.connection(True) as c:
        c.execute('UPDATE users SET enabled=1,password_hash=?', (password_hash(secrets.token_urlsafe(32)),))
        for login, name in (('demo.admin', 'Demo Manager'), ('demo.shift1', 'Lia Costa'),
                            ('demo.shift2', 'Rafael Lima'), ('demo.logistics', 'Noa Martins')):
            c.execute('UPDATE users SET name=? WHERE login_id=?', (name, login))
        ids = dict(c.execute('SELECT login_id,id FROM users'))

    def actor(login):
        with store.connection() as c:
            return accounts.session_person_in_connection(c, ids[login])

    manager = actor('demo.admin')
    for login in ('demo.shift1', 'demo.shift2', 'demo.logistics'):
        uid = ids[login]
        policy = access.read(store, manager, uid)
        rights = dict(policy['permissions'])
        rights.update({k: True for k in ('hr.view_own', 'hr.documents_submit', 'hr.timesheets_submit',
                                         'hr.expenses_submit', 'it.view_own')})
        if login == 'demo.logistics':
            rights['hr.timesheets_review'] = True
        access.save(store, manager, uid, rights, policy['version'], 'Fictional crew demonstration')

    lia, rafael, noa = (actor('demo.' + name) for name in ('shift1', 'shift2', 'logistics'))
    today = date.today()

    def day(offset):
        return (today + timedelta(days=offset)).isoformat()

    def hr(action, payload, person=manager):
        return store.hr.run(action, payload, person, str(uuid4()))

    def it(action, payload, person=manager):
        return store.it_requests.run(action, payload, person, str(uuid4()))['request']

    def file(key):
        name, _, raw = sample_file(key, 'en')
        return dict(filename=name, data=b64encode(raw).decode())

    dept = Departments(store)
    survey = dept.create('Offshore Survey', 'Aurora survey crew', manager)
    # Fictional members of the disposable showcase's reusable Handover shifts.
    crew = [accounts.create(login, name, secrets.token_urlsafe(32), 'technician', manager)['id']
            for login, name in (('demo.survey.day', 'Mara Brisa'), ('demo.survey.night1', 'Davi Coral'),
                                ('demo.survey.night2', 'Nina Mar'))]
    day_team = [manager['user_id'], rafael['user_id'], crew[0]]
    night_team = [lia['user_id'], crew[1], crew[2]]
    dept.set_members(survey, day_team + night_team, 1, manager, 'Fictional rotation')
    project, vessel = 'Aurora survey', 'MV Aurora'
    aurora = store.fleet.run('save_site', dict(name=vessel,code='AUR',kind='vessel',active=True),manager,str(uuid4()))
    from app.feed_news_backend import publish
    publish(store, manager, dict(op_id=str(uuid4()), site_id=None,
            title='Welcome aboard the Maré Alta demo',
            body='This fictional company feed is where the vessel and shore teams share news. Company updates reach everyone. Vessel updates show the ship they are for.'))
    officer = accounts.create('demo.safety', 'Safety Officer', secrets.token_urlsafe(32), 'technician', manager)
    officer_id = officer['id']
    policy = access.read(store, manager, officer_id)
    rights = dict(policy['permissions'], **{'news.publish': True})
    access.save(store, manager, officer_id, rights, policy['version'], 'Fictional vessel news publisher')
    store.fleet.run('set_access', dict(user_id=officer_id, mode='project_logistics', version=0, confirmed=True,
            grants=[dict(site_id=aurora['id'], role='viewer')], reason='Demonstration vessel assignment'),
            manager, str(uuid4()))
    with store.connection() as c:
        publisher = accounts.session_person_in_connection(c, officer_id)
    drill_photo = Path(__file__).with_name('feed_news_drill.webp').read_bytes()
    publish(store, publisher, dict(op_id=str(uuid4()), site_id=aurora['id'],
            title='Fire alarm drill aboard MV Aurora',
            body='The MV Aurora crew completed a scheduled fire alarm drill during the morning shift. Thank you to everyone who took part on deck and on the bridge.\n\nFictional demo notice · AI-generated photo.',
            image='data:image/webp;base64,' + b64encode(drill_photo).decode('ascii')))
    # Give the preloaded fictional work orders and reports a mix of real demo-directory locations.
    from app import work_locations
    from app.store import pack
    import json
    with store.connection(True) as c:
        available = {site['code']:site for site in work_locations.catalog(c,manager)}
        assigned = [available[code] for code in ('DEMO-MERIDIAN','DEMO-SHORE','DEMO-HORIZON','DEMO-WORKSHOP')]
        for table in ('maintenance_jobs','work_tasks','fault_reports','qshe_reports','asset_certificates'):
            for index,row in enumerate(c.execute('SELECT id,body FROM '+table+' ORDER BY id').fetchall()):
                record=json.loads(row['body'])
                record['work_site']=assigned[index % len(assigned)]
                c.execute('UPDATE '+table+' SET body=? WHERE id=?',(pack(record),row['id']))
    store.tasks.run('create_general', dict(work_site_id=aurora['id'],kind='general', title='Review the Aurora mobilisation checklist',
                    instructions='Confirm the crew transfer and the equipment list for the next shift.',
                    department_id=survey, assignee_ids=[manager['user_id']], priority='high',
                    due_at=day(1)+'T12:00:00Z', confirmed=True), manager, str(uuid4()))
    # Build a fresh fictional order with step-level evidence enabled through the normal routine writer.
    from copy import deepcopy
    with store.connection() as c:
        sample = json.loads(c.execute('SELECT body FROM maintenance_jobs ORDER BY id LIMIT 1').fetchone()[0])
    template = deepcopy(sample['template'])
    template['title'] = 'Training inspection with photo evidence'
    checks = [step for section in template['sections'] for step in section['items']]
    for step, mode in zip(checks, ('optional','required')):
        step['photo_evidence'] = {'mode':mode}
    routine = store.maintenance.run('save_routine', dict(template=template,publish=True,reviewed=True), manager,str(uuid4()))
    store.maintenance.run('create_job', dict(routine_id=routine['id'],revision=routine['revision'],
        work_site_id=aurora['id'],name='Photo evidence training inspection',asset_name='Training sensor rack',
        reference='AUR-PHOTO',assignee_ids=[manager['user_id']],due_at=day(2)+'T12:00:00Z'), manager,str(uuid4()))
    shifts = SimpleHandovers(store)
    def configure(department, location, teams):
        setup = shifts.setup_detail(department, manager)
        if setup['setup']:
            raise ValueError('Expected an unconfigured fictional department.')
        shifts.save_setup(dict(op_id=str(uuid4()), department_id=department, setup_token=setup['setup_token'],
            values=dict(location=location, time_basis='UTC', schedule=dict(format='wavelink-handover-shift-plan-1',
            start_time='06:00', shift_index=0, shifts=[dict(name='Days', minutes=720), dict(name='Nights', minutes=720)]),
            assignments=[dict(user_id=uid, shift_index=index)
                         for index, team in enumerate(teams) for uid in team])), manager)

    def finish(department, location, name, shift_index, person, offset, note, action, filename=None):
        board = shifts.board(department, day(offset), person)
        record = shifts.open(dict(department_id=department, operational_date=day(offset), shift_index=shift_index,
                                  setup_token=board['setup']['setup_token']), person)
        notes = {key:record['edit'][key] for key, _ in SECTIONS}
        notes.update(summary=note, next_actions=action)
        attachments = []
        if filename:
            sheet = '\n'.join((location + ' | ' + name, day(offset), note, action,
                               'Fictional shift record for the Wavelink demo.'))
            attachments.append(dict(id=str(uuid4()), filename=filename, data=b64encode(sheet.encode()).decode()))
        shifts.action(dict(op_id=str(uuid4()), action='finish', target=record['target'], notes=notes,
                           attachments=attachments), person)

    hr_teams = [(survey, available['AUR'], [crew[0]], crew[1:])]
    configure(survey, vessel, (day_team, night_team))
    finish(survey, vessel, 'Offshore Survey', 1, lia, -1, 'Night survey complete. Navigation checks are ready for the day crew.',
           'Review the night navigation check sheet.', 'Night-navigation-checks.txt')
    finish(survey, vessel, 'Offshore Survey', 0, manager, 0, 'Aurora mobilisation complete. The next shift will check survey coverage.',
           'Compare the coverage plot with the planned survey lines.', 'Day-survey-coverage.txt')

    departments = {d['name']: d for d in dept.list(manager)}
    for name, prefix, location, crew_names, publications in (
        ('DEMO Engineering', 'eng', vessel, ('Luca Bay', 'Bia Lake', 'Noel Reef', 'Ida Brook', 'Teo Clay', 'Ana Fern'),
         ((0, -2, 'Port pump vibration readings logged.', 'Compare the readings at operating speed.'),
          (1, -1, 'Spare pump coupling aligned.', 'Check the alignment record before the morning run.'))),
        ('DEMO Logistics', 'log', available['DEMO-SHORE']['name'], ('Isa Moor', 'Oli Pine', 'Luz Glen', 'Ben Lark', 'Mia Dune', 'Leo Elm'),
         ((0, -1, 'Survey spares packed for the launch.', 'Match the sealed cases to the manifest.'),
          (1, 0, 'Two return cases received at the base.', 'Verify the serial numbers before shelving.')))):
        department = departments[name]['id']
        snapshot = dept.details(department, manager)
        members = [m['id'] for m in snapshot['members']]
        team_ids = [accounts.create('demo.' + prefix + str(i), member, secrets.token_urlsafe(32),
                                    'technician', manager)['id'] for i, member in enumerate(crew_names)]
        dept.set_members(department, members + team_ids, snapshot['version'], manager, 'Fictional shift teams')
        site = available['AUR' if prefix == 'eng' else 'DEMO-SHORE']
        hr_teams.append((department, site, team_ids[:3], team_ids[3:]))
        configure(department, location, (team_ids[:3], team_ids[3:]))
        for index, offset, note, action in publications:
            with store.connection() as c:
                author = accounts.session_person_in_connection(c, team_ids[index * 3])
            finish(department, location, name, index, author, offset, note, action)
    timesheet_project = hr('save_timesheet_project', dict(version=0, name=project, active=True,
                                                          approver_ids=[manager['user_id'], noa['user_id']]))
    for department, site, days, nights in hr_teams:
        for shift, people, start, end in (('Days', days, '06:00', '18:00'), ('Nights', nights, '18:00', '06:00')):
            for uid in people:
                hr('save_shift', dict(id='', version=0, user_id=uid, title=shift + ' — ' + site['name'],
                    location=site['name'], work_site_id=site['id'], department_id=department, project=project,
                    assignment_type='onshore' if site['code']=='DEMO-SHORE' else 'offshore',
                    start_on=day(-2), end_on=day(7), shift_name=shift, start_time=start, end_time=end,
                    time_zone='UTC', status='planned', notes='Fictional Aurora survey support rotation'))
    birthdays = core.state.team_birthdays
    for person, offset in ((lia, 0), (rafael, 4)):
        birthday = birthdays.today() + timedelta(days=offset)
        birthdays.save(person, birthday.month, birthday.day, birthdays.mine(person)['version'])
    for i, (person, job, shift) in enumerate(((manager, 'Survey coordinator', 'Days'),
                                              (lia, 'AUV technician', 'Nights'),
                                              (rafael, 'Survey engineer', 'Days'),
                                              (noa, 'Logistics coordinator', 'Days'))):
        user = dict(user_id=person['user_id'], id='', version=0)
        profile = store.recognition.profile(person)
        store.recognition.save_profile(person, dict(version=profile['profile_version'], biography=job+' · '+project,
                                       selected_badge=profile['selected_badge'], avatar_action='keep',avatar=None), str(uuid4()))
        hr('save_person', dict(**user, title=person['name'], job_title=job, admitted_on=day(-410),
                               phone='', emergency_contact='', notes=project))
        hr('save_shift', dict(**user, title=shift + ' · ' + job, location=vessel, project=project,
                              department_id=survey if person != noa else '', start_on=day(-3+i),
                              end_on=day(10+i), shift_name=shift, start_time='18:00' if shift=='Nights' else '06:00',
                              end_time='06:00' if shift=='Nights' else '18:00', time_zone='UTC',
                              status='confirmed', notes='Offshore crew rotation'))
        cert = hr('save_document', dict(**user, type='training', title='Offshore survival training',
                  reference='TRAIN-%02d' % (i+1), issuer='Maré Alta Training', issued_on=day(-310),
                  expiry_mode='dated', expires_on=day(14 if i==0 else 95+i), reminder_days=30, notes='Training example.'))
        hr('add_attachment', dict(id=cert['id'], version=cert['version'], kind='documents', **file('training')))
    for person in (manager, lia):
        trip = hr('save_travel', dict(id='', version=0, user_id=person['user_id'], title='Aurora crew change',
                  mode='flight', origin='Rio de Janeiro', destination='Vitória', depart_on=day(2),
                  return_on=day(16), depart_time='09:30', return_time='17:15', time_zone='America/Sao_Paulo',
                  reference='DEMO-204', accommodation='Shore base', status='confirmed', notes='Mobilisation for Aurora.'))
        hr('add_attachment', dict(id=trip['id'], version=trip['version'], kind='travel', **file('itinerary')))
    hr('save_need', dict(id='', version=0, user_id=manager['user_id'], title='Next offshore rotation',
                         job_title='Survey engineer', project=project, location=vessel, start_on=day(10),
                         end_on=day(24), headcount=1, status='planned', notes='Upcoming crew change.'))
    monday = today-timedelta(days=today.weekday())
    for person in (lia, manager):
        expense = hr('save_expense', dict(id='', version=0, user_id=person['user_id'], title='Transfer to the heliport',
                     date=day(-1), category='travel', merchant='Maré Alta Transfers', amount='48.00', currency='BRL',
                     project=project, description='Crew change transfer', notes=''), person)
        receipt = hr('add_attachment', dict(id=expense['id'], version=expense['version'], kind='expenses', **file('expense')), person)
        hr('submit_expense', dict(id=receipt['id'], version=receipt['version']), person)
        week = hr('save_timesheet_week', dict(week_start=monday.isoformat(), records=[dict(
                    project_id=timesheet_project['project']['id'], version=0, entries=[dict(date=monday.isoformat(),
                    hours='8.00', location=vessel, activity='offshore', notes='Survey shift')], notes='')]), person)
        row = week['records'][0]
        hr('submit_timesheet', dict(id=row['id'], version=row['version']), person)
    for person, title, priority, site in ((manager, 'Survey workstation network port', 'high', aurora),
                                         (lia, 'Offline copy of the mobilisation checklist', 'normal', aurora),
                                         (rafael, 'Printer at the shore base', 'low', available['DEMO-SHORE'])):
        row = it('create', dict(work_site_id=site['id'],title=title, priority=priority, description='Please check this before the next crew change.'), person)
        if person == manager:
            row = it('triage', dict(id=row['id'], version=row['version'], priority=priority, assignee_id=manager['user_id']))
            row = it('transition', dict(id=row['id'], version=row['version'], status='in_progress', comment='Checking the port.'))
            it('add_attachment', dict(id=row['id'], version=row['version'], file_id=str(uuid4()), **file('it-report')))
        else:
            it('comment', dict(id=row['id'], version=row['version'], text='Available for a check after handover.'), person)
    # Create both files through the reviewed import workflow on the fictional company only.
    documents = core.state.document_import
    for kind, filename, title, lines in (
        ('toolbox', 'deck-briefing.txt', 'Deck team briefing', 'Discussion: Confirm the meeting point.\nQuestions: Where is the noticeboard?'),
        ('checklist', 'shift-handover-checklist.txt', 'Shift handover checklist', '# Handover\n- Check the shift log\n- Confirm the next team has the document list'),
    ):
        file = dict(name=filename, data=b64encode((title+'\n'+lines).encode()).decode())
        scan = documents.scan(dict(kind=kind,file=file,language='eng'),manager,None)
        draft = scan['draft']
        draft['title'] = title
        if kind == 'toolbox':
            draft['declaration'] = 'I attended and understood the team briefing.'
        review = dict(kind=kind,source=scan['source'],source_token=scan['source_token'],draft=draft)
        checked = documents.reviewed(review,manager,None)
        documents.reviewed(dict(review,file=file,review_token=checked['review_token'],op_id=str(uuid4()),confirmed=True),
                           manager,None,save=True)
    team = [dict(user_id=p['user_id'], display_name=p['name'], mood=m)
                     for p, m in ((lia, 'happy'), (rafael, 'focused'), (noa, 'calm'))]
    # This in-memory example belongs only to this disposable public company.
    # Keep the real reporting-position table empty and account roles unchanged.
    # Company reporting responsibilities are not security roles. The catalog and
    # formal head designations below belong only to the guarded disposable company.
    new_people = {'opsdirector':'Eva Sol', 'servicesdirector':'Caio Rio', 'opsmgr':'Talia Luz',
                  'itmgr':'Nico Serra', 'finmgr':'Rosa Lago', 'sysadmin':'Ari Monte',
                  'support':'Téo Vale', 'controller':'Iris Prado', 'payables':'Otto Lima'}
    for key, name in new_people.items():
        accounts.create('demo.chart.' + key, name, secrets.token_urlsafe(32), 'technician', manager)
    # key, bilingual display title, fictional login, department, reports to
    outline = [
        ('ceo','CEO','demo.admin','Executive',''),
        ('operations-director','Operations Director / Diretor de Operações','demo.chart.opsdirector','Executive','ceo'),
        ('services-director','Corporate Services Director / Diretor Corporativo','demo.chart.servicesdirector','Executive','ceo'),
        ('operations','Operations Manager / Gerente de Operações','demo.chart.opsmgr','Operations','operations-director'),
        ('offshore','Offshore Supervisor / Supervisor offshore','demo.shift2','Operations','operations'),
        ('chief','Party Chief / Chefe de equipe','demo.shift1','Offshore Survey','offshore'),
        ('survey-tech','Survey Technician / Técnico de levantamento','demo.survey.day','Offshore Survey','chief'),
        ('auv-tech','AUV Technician / Técnico de AUV','demo.survey.night1','Offshore Survey','chief'),
        ('survey-trainee','Trainee','demo.survey.night2','Offshore Survey','survey-tech'),
        ('auv-trainee','Trainee',None,'Offshore Survey','auv-tech'),
        ('it','IT Manager / Gerente de TI','demo.chart.itmgr','IT','services-director'),
        ('systems','Systems Administrator / Analista de sistemas','demo.chart.sysadmin','IT','it'),
        ('support','Service Desk Analyst / Analista de suporte','demo.chart.support','IT','it'),
        ('finance','Finance Manager / Gerente Financeiro','demo.chart.finmgr','Finance','services-director'),
        ('controller','Financial Controller / Controller','demo.chart.controller','Finance','finance'),
        ('payables','Accounts Payable Analyst / Analista de contas a pagar','demo.chart.payables','Finance','finance'),
    ]
    head_logins = {'Executive':'demo.admin', 'Operations':'demo.chart.opsmgr', 'Offshore Survey':'demo.shift1',
                   'IT':'demo.chart.itmgr', 'Finance':'demo.chart.finmgr'}
    with store.connection() as c:
        personnel = {u['login_id']:dict(u) for u in c.execute('SELECT id,login_id,name FROM users WHERE enabled')}
    catalog = {d['name']:d['id'] for d in dept.list(manager)}
    for name, head in head_logins.items():
        if name not in catalog:
            catalog[name] = dept.create(name, 'Fictional demonstration department', manager)
        did = catalog[name]
        details = dept.details(did, manager)
        existing = {m['id'] for m in details['members']}
        members = {personnel[login]['id'] for _,_,login,department,_ in outline if department==name and login}
        if members - existing:
            dept.set_members(did, sorted(existing | members), details['version'], manager, 'Fictional department team')
        dept.set_heads(did, [personnel[head]['id']], dept.details(did, manager)['version'], manager,
                       'Explicit fictional department lead')
    positions = {}
    example = []
    for key,title,login,name,parent in outline:
        positions[key] = str(uuid4())
        person = personnel[login] if login else None
        example.append(dict(id=positions[key], department=catalog[name], dept_name=name,
                            role=key, role_name=title, person=person['id'] if person else None,
                            person_name=person['name'] if person else None,
                            parent=positions[parent] if parent else None))
    core.state.demo_org_example = example
    core.state.fictional_seed_result = manager, team
    return manager, team
