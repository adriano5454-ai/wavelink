"""Fictional personnel and service records for the disposable public company."""
from base64 import b64encode
from datetime import date, timedelta
import secrets
from uuid import uuid4

from .demo_management_files import sample_file


def populate(core):
    from app import access
    from app.accounts import password_hash
    from app.departments import Departments
    from app.handovers import SECTIONS
    from app.simple_handovers import SimpleHandovers

    store, accounts = core.state.store, core.state.accounts
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
    dept.set_members(survey, [p['user_id'] for p in (lia, rafael, manager)], 1, manager, 'Fictional rotation')
    project, vessel = 'Aurora survey', 'MV Aurora'
    aurora = store.fleet.run('save_site', dict(name=vessel,code='AUR',kind='vessel',active=True),manager,str(uuid4()))
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
    setup = shifts.setup_detail(survey, manager)
    shifts.save_setup(dict(op_id=str(uuid4()), department_id=survey, setup_token=setup['setup_token'], values=dict(
        location=vessel, time_basis='UTC', schedule=dict(format='wavelink-handover-shift-plan-1',
        start_time='06:00', shift_index=0, shifts=[dict(name='Days',minutes=720),dict(name='Nights',minutes=720)]),
        assignments=[dict(user_id=manager['user_id'],shift_index=0),dict(user_id=lia['user_id'],shift_index=1)])), manager)
    for shift_index, person, offset, note in ((1,lia,-1,'Night survey complete. Navigation checks are ready for the day crew.'),
                                              (0,manager,0,'Aurora mobilisation complete. The next shift will check survey coverage.')):
        board = shifts.board(survey, day(offset), person)
        record = shifts.open(dict(department_id=survey,operational_date=day(offset),shift_index=shift_index,
                                  setup_token=board['setup']['setup_token']), person)
        notes = {key:record['edit'][key] for key, _ in SECTIONS}
        notes['summary'] = note
        notes['next_actions'] = ('Review the night navigation check sheet.' if shift_index
                                 else 'Compare the coverage plot with the planned survey lines.')
        filename = 'Night-navigation-checks.txt' if shift_index else 'Day-survey-coverage.txt'
        sheet = '\n'.join(('MV Aurora | Offshore Survey', day(offset), note, notes['next_actions'],
                           'Fictional shift record for the Wavelink demo.'))
        evidence = dict(id=str(uuid4()), filename=filename, data=b64encode(sheet.encode()).decode())
        shifts.action(dict(op_id=str(uuid4()),action='finish',target=record['target'],notes=notes,
                           attachments=[evidence]),person)
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
    timesheet_project = hr('save_timesheet_project', dict(version=0, name=project, active=True,
                                                          approver_ids=[manager['user_id'], noa['user_id']]))
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
    return manager, [dict(user_id=p['user_id'], display_name=p['name'], mood=m)
                     for p, m in ((lia, 'happy'), (rafael, 'focused'), (noa, 'calm'))]
