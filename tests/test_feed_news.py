"""Publish and read team news through the real API of disposable fictional companies."""
from base64 import b64encode
from datetime import date, timedelta
from io import BytesIO
from pathlib import Path
from random import Random
from types import SimpleNamespace
from uuid import uuid4

from PIL import Image
from PIL.PngImagePlugin import PngInfo
import pytest
from starlette.testclient import TestClient

from app import access
from app.server import create_app
from deploy.gate import Gate
from deploy.native_showcase import NativeShowcase


NEWS = '/api/recognition/news'
PASSWORD = 'Fictional-example-only-password'


def session(project, uid):
    accounts = project.app.state.accounts
    with project.store.connection() as db:
        actor = accounts.session_person_in_connection(db, uid)
    token, _ = accounts.issue_session(actor, 'fictional-news-device')
    return {'Authorization': 'Bearer ' + token, 'X-AJ-Hub-ID': project.app.state.config['hub_id']}


def grant_publish(project, uid, enabled):
    policy = access.read(project.store, project.admin, uid)
    rights = dict(policy['permissions'])
    rights['news.publish'] = enabled
    access.save(project.store, project.admin, uid, rights, policy['version'], 'Fictional news team change')


def set_sites(project, uid, sites, mode='project_logistics', version=0):
    payload = dict(user_id=uid, mode=mode, version=version, confirmed=True,
                   grants=[{'site_id': site['id'], 'role': 'viewer'} for site in sites],
                   reason='Fictional crew assignment')
    project.store.fleet.run('set_access', payload, project.admin, str(uuid4()))


def member(project, name, *, role='technician', publish=False, sites=()):
    row = project.app.state.accounts.create('news.' + name, 'Fictional ' + name, PASSWORD, role, project.admin)
    if publish:
        grant_publish(project, row['id'], True)
    if sites:
        set_sites(project, row['id'], sites)
    return row['id'], session(project, row['id'])


@pytest.fixture(scope='module')
def project(tmp_path_factory):
    app = create_app(tmp_path_factory.mktemp('fictional-news-project'))
    app.state.accounts.create('news.admin', 'Fictional manager', PASSWORD, 'admin')
    _, admin = app.state.accounts.login('news.admin', PASSWORD, 'fictional-setup')
    store = app.state.store
    sites = [store.fleet.run('save_site', dict(name=name, kind=kind), admin, str(uuid4()))
             for name, kind in [('Survey North', 'vessel'), ('Coastal Base', 'shore_base')]]
    with TestClient(app) as client:
        result = SimpleNamespace(app=app, client=client, store=store, admin=admin, ship=sites[0], base=sites[1])
        result.manager = session(result, admin['user_id'])
        yield result


def draft(title, *, site=None, image=None):
    return dict(op_id=str(uuid4()), title=title, body='The next shift starts at 07:00.',
                site_id=site['id'] if site else None, image=image)


def publish(project, auth, payload):
    response = project.client.post(NEWS, headers=auth, json=payload)
    assert response.status_code == 200, response.text
    return response.json()['post']


def feed(project, auth, **params):
    response = project.client.get(NEWS, headers=auth, params=params)
    assert response.status_code == 200, response.text
    return response.json()


def image_path(post):
    return f"{NEWS}/{post['id']}/image"


def data_url(content, mime):
    return f"data:{mime};base64,{b64encode(content).decode('ascii')}"


def png(size=(16, 8)):
    metadata = PngInfo()
    metadata.add_text('Comment', 'fictional camera metadata')
    image = Image.frombytes('RGB', size, Random(42).randbytes(size[0] * size[1] * 3))
    output = BytesIO()
    image.save(output, format='PNG', pnginfo=metadata)
    return data_url(output.getvalue(), 'image/png')


def test_only_selected_users_can_publish_and_retries_are_idempotent(project):
    uid, author = member(project, 'editor', role='supervisor')
    _, reader = member(project, 'unselected')
    payload = draft('Company handover next week')
    assert project.client.get(NEWS).status_code == 401
    assert project.client.post(NEWS, json=payload).status_code == 401
    assert project.client.get(NEWS, headers={'Authorization': author['Authorization']}).status_code == 409
    for headers in [author, reader]:
        assert feed(project, headers)['can_publish'] is False
        assert project.client.post(NEWS, headers=headers, json=payload).status_code == 403
    grant_publish(project, uid, True)
    author = session(project, uid)
    assert feed(project, author)['can_publish'] is True
    first = publish(project, author, payload)
    assert (first['author_id'], first['title'], first['body']) == (uid, payload['title'], payload['body'])
    assert not first['site_id'] and not first['has_image']
    assert publish(project, author, payload)['id'] == first['id']
    assert project.client.post(NEWS, headers=author, json={**payload, 'title': 'Different post'}).status_code == 409
    assert [post['id'] for post in feed(project, reader)['posts']].count(first['id']) == 1
    assert project.client.get(image_path(first), headers=reader).status_code == 404
    grant_publish(project, uid, False)
    assert project.client.post(NEWS, headers=author, json=draft('Expired editor session')).status_code in (401, 403)
    assert project.client.post(NEWS, headers=session(project, uid), json=draft('Removed publisher')).status_code == 403


def test_scoped_posts_and_media_follow_current_membership(project):
    uid, author = member(project, 'vessel-editor', publish=True, sites=[project.ship])
    _, ship_crew = member(project, 'ship-crew', sites=[project.ship])
    _, base_crew = member(project, 'base-crew', sites=[project.base])
    _, unassigned = member(project, 'unassigned')
    assert {s['id'] for s in feed(project, author)['sites']} == {project.ship['id']}
    for site_id in [project.base['id'], str(uuid4())]:
        invalid = {**draft('Unassigned audience'), 'site_id': site_id}
        assert project.client.post(NEWS, headers=author, json=invalid).status_code == 422
    image = png((640, 640))
    # Ordinary phone photos exceed both the old 100 KB request guard and the 800 KB avatar guard.
    assert len(image) > 800_000
    payload = draft('North deck briefing', site=project.ship, image=image)
    vessel_news = publish(project, author, payload)
    base_news = publish(project, project.manager, draft('Port briefing', site=project.base))
    company = publish(project, author, draft('Company timetable'))
    assert vessel_news['site_name'] == project.ship['name'] and vessel_news['has_image'] is True
    for auth, vessel_visible, base_visible in [
            (ship_crew, True, False), (base_crew, False, True), (unassigned, False, False),
            (project.manager, True, True)]:
        items = {p['id'] for p in feed(project, auth)['posts']}
        assert company['id'] in items
        assert (vessel_news['id'] in items) == vessel_visible
        assert (base_news['id'] in items) == base_visible
        photo = project.client.get(image_path(vessel_news), headers=auth)
        assert photo.status_code == (200 if vessel_visible else 404)
        if vessel_visible:
            assert photo.headers['content-type'] in ('image/png', 'image/jpeg', 'image/webp')
            assert 'attachment' not in photo.headers.get('content-disposition', '').lower()
            assert 'no-store' in photo.headers['cache-control']
            assert photo.headers['x-content-type-options'] == 'nosniff'
            with Image.open(BytesIO(photo.content)) as shown:
                assert shown.size == (640, 640)
                assert 'fictional camera metadata' not in str(shown.info)
        else:
            assert vessel_news['title'] not in photo.text and photo.headers['content-type'].startswith('application/json')
    assert project.client.get(image_path(vessel_news)).status_code == 401
    assert project.client.get(image_path(vessel_news), headers={**author, 'X-AJ-Hub-ID': str(uuid4())}).status_code == 409
    set_sites(project, uid, [project.base], version=1)
    reassigned = session(project, uid)
    assert vessel_news['id'] not in {p['id'] for p in feed(project, reassigned)['posts']}
    assert project.client.get(image_path(vessel_news), headers=reassigned).status_code == 404
    assert project.client.post(NEWS, headers=reassigned, json=payload).status_code in (403, 404, 422)


def test_current_confirmed_work_rotation_grants_access_and_plans_and_leave_do_not(project):
    now = date.today()
    uid, crew = member(project, 'rotation')
    record = publish(project, project.manager, draft('Rotation-only briefing', site=project.ship, image=png()))
    shift = dict(id='', version=0, user_id=uid, title='Survey rotation', location=project.ship['name'],
                 work_site_id=project.ship['id'], start_on=(now - timedelta(days=2)).isoformat(),
                 end_on=(now + timedelta(days=2)).isoformat(), assignment_type='offshore', status='planned',
                 shift_name='Day shift', start_time='06:00', end_time='18:00', time_zone='UTC')
    for changes, visible in [
            ({}, False), ({'status': 'confirmed'}, True), ({'assignment_type': 'rest'}, False),
            ({'assignment_type': 'onshore', 'end_on': (now - timedelta(days=1)).isoformat()}, False)]:
        shift.update(changes)
        saved = project.store.hr.run('save_shift', shift, project.admin, str(uuid4()))
        shift.update(id=saved['id'], version=saved['version'])
        ids = {post['id'] for post in feed(project, crew)['posts']}
        assert (record['id'] in ids) == visible
        assert project.client.get(image_path(record), headers=crew).status_code == (200 if visible else 404)


def test_restricted_accounts_cannot_read_project_feed_or_company_photos(project):
    news = publish(project, project.manager, draft('Project bulletin', image=png()))
    fleet_uid, _ = member(project, 'fleet-restricted')
    set_sites(project, fleet_uid, [project.ship], mode='vessel_only')
    uid, _ = member(project, 'profile-only')
    policy = access.read(project.store, project.admin, uid)
    access.save(project.store, project.admin, uid, dict.fromkeys(policy['permissions'], False),
                policy['version'], 'Fictional profile-only account')
    shared = project.app.state.accounts.create('guest.demo', 'Shared guest', PASSWORD, 'technician', project.admin)
    for user in [fleet_uid, uid, shared['id']]:
        auth = session(project, user)
        assert project.client.get(NEWS, headers=auth).status_code == 403
        assert project.client.get(image_path(news), headers=auth).status_code == 403
        assert project.client.post(NEWS, headers=auth, json=draft('Restricted writer')).status_code == 403


def test_fleet_only_reader_sees_explicit_site_and_its_image_in_fleet(project):
    path = '/api/fleet/news'
    uid, _ = member(project, 'site-logistics-only')
    now = date.today()
    shift = dict(id='', version=0, user_id=uid, title='Shore duty', location=project.base['name'],
                 work_site_id=project.base['id'], start_on=(now - timedelta(days=1)).isoformat(),
                 end_on=(now + timedelta(days=1)).isoformat(), assignment_type='onshore', status='confirmed',
                 shift_name='Day shift', start_time='06:00', end_time='18:00', time_zone='UTC')
    project.store.hr.run('save_shift', shift, project.admin, str(uuid4()))
    set_sites(project, uid, [project.ship], mode='vessel_only')
    crew = session(project, uid)
    ship = publish(project, project.manager, draft('Vessel-only audience', site=project.ship, image=png()))
    base = publish(project, project.manager, draft('Shore-only audience', site=project.base, image=png()))
    general = publish(project, project.manager, draft('General company audience', image=png()))

    def page(auth, **params):
        response = project.client.get(path, headers=auth, params=params)
        assert response.status_code == 200, response.text
        return response.json()

    def photo(auth, post):
        return project.client.get(f"{path}/{post['id']}/image", headers=auth)

    first = page(crew)
    assert first['can_publish'] is False and first['sites'] == []
    assert ship['id'] in {p['id'] for p in first['posts']}
    assert {p['site_id'] for p in first['posts']} == {project.ship['id']}
    assert page(crew, site_id=project.ship['id'])['posts'] == first['posts']
    assert project.client.get(path, headers=crew, params={'site_id': project.base['id']}).status_code == 404
    assert photo(crew, ship).status_code == 200
    for hidden in (base, general):
        assert photo(crew, hidden).status_code == 404
        assert project.client.get(path, headers=crew, params={'before': hidden['id']}).status_code == 422
    assert project.client.post(path, headers=crew, json=draft('Fleet writer')).status_code in (403, 405)
    assert project.client.get(NEWS, headers=crew).status_code == 403
    assert project.client.get(image_path(ship), headers=crew).status_code == 403

    set_sites(project, uid, [project.base], mode='vessel_only', version=1)
    new_auth = session(project, uid)
    assert {p['site_id'] for p in page(new_auth)['posts']} == {project.base['id']}
    assert photo(new_auth, ship).status_code == 404
    assert photo(new_auth, base).status_code == 200
    assert project.client.get(path, headers=crew).status_code in (401, 403)


def test_invalid_image_and_fields_are_atomic(project):
    payload = draft('Unpublished image submission')
    large_png = png((1536, 1152))
    assert len(large_png.split(',', 1)[1]) > (5 * 1024 * 1024 + 2) // 3 * 4
    animated = BytesIO()
    Image.new('RGB', (10, 10), 'red').save(animated, 'WEBP', save_all=True,
            append_images=[Image.new('RGB', (10, 10), 'blue')], duration=200, loop=0)
    invalid_images = [
        'https://example.test/crew.png', 'data:image/png;base64,broken', data_url(b'not a picture', 'image/png'),
        data_url(b'<svg xmlns="http://www.w3.org/2000/svg"/>', 'image/svg+xml'),
        png().replace('image/png', 'image/jpeg'), data_url(animated.getvalue(), 'image/webp'), large_png,
    ]
    for change in [
            *({'image': image} for image in invalid_images), {'title': '  '}, {'body': '  '},
            {'title': 'x' * 141}, {'body': 'x' * 3001}, {'author_id': str(uuid4())}]:
        rejected = project.client.post(NEWS, headers=project.manager, json={**payload, **change})
        assert rejected.status_code in (413, 422), (list(change), rejected.status_code)
    retry = publish(project, project.manager, payload)
    assert retry['has_image'] is False
    assert sum(p['title'] == payload['title'] for p in feed(project, project.manager)['posts']) == 1


@pytest.mark.parametrize('file_format,mime', [('JPEG', 'image/jpeg'), ('WEBP', 'image/webp')])
def test_static_phone_and_web_images_display_inline(project, file_format, mime):
    binary = BytesIO()
    Image.new('RGB', (64, 32), 'teal').save(binary, file_format)
    image = data_url(binary.getvalue(), mime)
    post = publish(project, project.manager, draft(file_format + ' bulletin photo', image=image))
    photo = project.client.get(image_path(post), headers=project.manager)
    assert photo.status_code == 200 and photo.headers['content-type'].startswith('image/')
    with Image.open(BytesIO(photo.content)) as shown:
        assert shown.size == (64, 32)


def test_pagination_keeps_audience_filter_and_order(project):
    _, crew = member(project, 'pagination-crew', sites=[project.ship])
    records = []
    for index, site in enumerate([None, project.base, project.ship, None, project.base, project.ship]):
        post = publish(project, project.manager, draft('Update ' + str(index), site=site))
        if site != project.base:
            records.append(post['id'])
    first = feed(project, crew, limit=2)
    assert first['next_cursor'] and [p['id'] for p in first['posts']] == records[::-1][:2]
    publish(project, project.manager, draft('New bulletin while reading'))
    second = feed(project, crew, limit=2, before=first['next_cursor'])
    assert [p['id'] for p in second['posts']] == records[::-1][2:]


def test_public_demo_shows_seeded_photo_and_is_read_only():
    gate = Gate('https://demo.example.test', 'fictional-demo-password', b's' * 32, 'guest.demo',
                'fictional-pass', public_entry=True)
    archive = Path(__file__).resolve().parents[1] / 'vendor' / 'FICTIONAL_DEMO.ajproject'
    showcase = NativeShowcase(gate, archive)
    gate.showcase = showcase
    try:
        with TestClient(gate.app(), base_url=gate.origin) as client:
            visit = showcase.admission()
            headers = {'Authorization': 'Bearer ' + visit['token'], 'X-AJ-Hub-ID': visit['hub_id']}
            response = client.get(NEWS, headers=headers)
            assert response.status_code == 200, response.text
            data = response.json()
            assert data['can_publish'] is False and data['sites'] == []
            assert any(not p['site_id'] for p in data['posts'])
            scoped = next(p for p in data['posts'] if p['site_name'] == 'MV Aurora' and p['has_image'])
            assert scoped['author_name'] == 'Safety Officer'
            photo = client.get(image_path(scoped), headers=headers)
            assert photo.status_code == 200 and photo.headers['content-type'].startswith('image/')
            Image.open(BytesIO(photo.content)).verify()
            blocked = client.post(NEWS, headers=headers, json=draft('Shared demo must stay read-only'))
            assert blocked.status_code == 403 and blocked.json()['demo_read_only'] is True
    finally:
        showcase.temp.cleanup()
