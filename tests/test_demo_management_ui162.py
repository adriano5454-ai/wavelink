"""Public management examples and the normal visitor's links into Wavelink."""
from html.parser import HTMLParser
from io import BytesIO
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4
from zipfile import ZipFile

import pytest
from starlette.testclient import TestClient

from deploy.demo_management import BASE
from deploy.demo_management_data import ADMIN_SECTIONS, AREAS, BY_RECORD
from deploy.demo_management_files import SAMPLE_FILES
from deploy.gate import Gate, PUBLIC_COOKIE


class Page(HTMLParser):
    def __init__(self, body):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.forms = []
        self.feed(body)

    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        if tag == 'a':
            self.links.append(fields['href'])
        if tag == 'form':
            self.forms.append(fields.get('method', 'get').lower())

    def details(self):
        result = set()
        for link in self.links:
            url = urlsplit(link)
            params = parse_qs(url.query)
            if url.path == BASE and 'record' in params:
                result.add((params['area'][0], params['record'][0]))
        return result


@pytest.fixture
def demo(monkeypatch):
    gate = Gate('https://demo.example.test', 'Private demo test entry password',
                b'd' * 32, 'visitor', 'Fictional visitor password', public_entry=True)
    def no_account_required():
        pytest.fail('The read-only management examples should never open a Wavelink account.')
    monkeypatch.setattr(gate, 'authenticate_guest', no_account_required)
    return gate, TestClient(gate.app(), base_url='https://demo.example.test')


@pytest.mark.parametrize(('locale','heading'), [
    ('en', 'Management preview'), ('pt', 'Visão de gestão'),
])
def test_direct_public_entry_and_language(demo, locale, heading):
    _, browser = demo
    res = browser.get(BASE, params={'lang': locale})
    assert res.status_code == 200
    assert heading in res.text and 'Maré Alta Surveys' in res.text
    assert res.headers['Content-Language'] == ('en' if locale == 'en' else 'pt-BR')
    assert res.headers['Cache-Control'] == 'no-store' and 'set-cookie' not in res.headers
    page = Page(res.text)
    assert '/__demo/public' in page.links
    assert all(not urlsplit(link).netloc for link in page.links)
    assert all(any(parse_qs(urlsplit(link).query).get('area') == [a.key] for link in page.links) for a in AREAS)
    assert ('personnel','lia') in page.details() and ('it','ticket-018') in page.details()


def test_browser_language_and_switch_preserve_record(demo):
    _, browser = demo
    response = browser.get(BASE + '?area=access&record=lia', headers={'Accept-Language':'pt-BR, en;q=0.5'})
    assert response.headers['Content-Language'] == 'pt-BR'
    assert 'Acesso aprovado' in response.text
    switch = next(link for link in Page(response.text).links if 'lang=en' in link)
    eng = browser.get(switch)
    assert eng.status_code == 200
    assert 'Access approved' in eng.text and 'Field team member' in eng.text


def test_each_area_record_and_cross_reference_opens(demo):
    _, browser = demo
    for area in AREAS:
        res = browser.get(BASE, params={'area': area.key, 'lang':'pt'})
        assert res.status_code == 200 and area.title[1] in res.text
        page = Page(res.text)
        assert page.details().issuperset({(area.key,r.key) for r in area.records})
        assert set(page.forms).issubset({'get'})
        for row in area.records:
            detail = browser.get(BASE, params={'area':area.key,'record':row.key,'lang':'pt'})
            assert detail.status_code == 200
            assert row.title[1] in detail.text
            assert set(row.related).issubset(Page(detail.text).details())
            assert all(target in BY_RECORD for target in row.related)


def test_employee_journey_includes_access_travel_document_and_hours(demo):
    _, browser = demo
    profile = browser.get(BASE + '?area=personnel&record=lia&lang=pt')
    links = Page(profile.text).details()
    assert {('access','lia'),('personnel','survival'),('travel','lia-flight'),('time','lia-week')} <= links
    assert 'Curso de sobrevivência' in profile.text


def test_search_with_and_without_matches(demo):
    _, browser = demo
    hit = browser.get(BASE, params={'area':'inventory','lang':'pt','q':'velocidade'})
    assert ('inventory','sv204') in Page(hit.text).details()
    miss = browser.get(BASE, params={'area':'inventory','lang':'pt','q':'nenhum resultado semelhante'})
    assert 'Nenhum registro encontrado' in miss.text
    assert 'Limpar busca' in miss.text


def test_live_links_use_guest_scope_and_current_workspace(demo):
    gate, browser = demo
    workspace = str(uuid4())
    params = dict(lang='en', area='inventory', workspace=workspace, open='inventory,tasks')
    anonymous = browser.get(BASE, params=params)
    assert not any('browser_workspace=' in link for link in Page(anonymous.text).links)
    browser.cookies.set(PUBLIC_COOKIE, gate.token('public-session', 600), domain='demo.example.test',path='/')
    active = browser.get(BASE, params=params)
    links = Page(active.text).links
    expected = '/?browser_workspace=' + workspace + '&public_demo=1'
    assert expected + '#home' in links and expected + '#inventory' in links
    area = next(link for link in links if 'record=sv204' in link)
    assert expected + '#inventory' in Page(browser.get(area).text).links
    assert expected + '#inventory' not in Page(browser.get(BASE, params={**params, 'open':'tasks'}).text).links
    assert not any('browser_workspace=' in u for u in Page(browser.get(BASE, params={**params,'workspace':'unknown'}).text).links)


def test_preview_is_public_demo_only_and_has_no_write_route(demo):
    gate, browser = demo
    assert browser.post(BASE, data={'area':'access','record':'lia'}).status_code == 405
    assert browser.get(BASE+'?area=unknown').status_code == 404
    assert browser.get(BASE+'?area=personnel&record=unknown').status_code == 404
    gate.public_entry = False
    assert browser.get(BASE).status_code == 404
    assert browser.get(BASE+'?area=personnel&record=lia').status_code == 404


@pytest.mark.parametrize('lang,hr,it', [('en','Human resources (HR)','IT requests'),
                                       ('pt','Recursos humanos (RH)','Solicitações de TI')])
def test_guest_workspaces_have_shell_navigation_and_sample_details(demo, lang, hr, it):
    gate, browser = demo
    path = BASE + '/workspace'
    def workspace(area, **params):
        return browser.get(path, params={'lang': lang, 'area': area, **params})
    home = workspace('hr')
    assert home.status_code == 200 and '<h1>' + hr + '</h1>' in home.text
    links = Page(home.text).links
    assert links == ['#workspaces'] + ['#demo/' + area for area in
                                      ('personnel', 'schedule', 'travel', 'time', 'expenses', 'alerts')]
    assert '#demo/hr' in Page(workspace('schedule').text).links
    queue = workspace('it')
    assert '<h1>' + it + '</h1>' in queue.text
    assert '#demo/it/ticket-018' in Page(queue.text).links
    detail = workspace('it', record='ticket-018')
    assert '#demo/it' in Page(detail.text).links
    assert any(link.startswith(BASE + '/files/') for link in Page(detail.text).links)
    admin = workspace('admin')
    assert len([link for link in Page(admin.text).links if 'from=admin' in link]) >= 8
    assert browser.post(path, data={'area':'it'}).status_code == 405
    gate.public_entry = False
    assert workspace('hr').status_code == 404


@pytest.mark.parametrize('language', ['en', 'pt'])
def test_admin_menu_and_review_queue(demo, language):
    _, browser = demo
    main = Page(browser.get(BASE, params={'lang': language}).text)
    admin = next(href for href in main.links if parse_qs(urlsplit(href).query).get('area') == ['admin'])
    result = browser.get(admin)
    assert result.status_code == 200
    page = Page(result.text)
    assert {tab for tab, _, _, _ in ADMIN_SECTIONS} == {
        'users', 'departments', 'records', 'imports', 'company', 'templates', 'logbooks', 'fleet'
    }
    for _, labels, area, record in ADMIN_SECTIONS:
        assert labels[language == 'pt'].replace('&', '&amp;') in result.text
        target = next(link for link in page.links if parse_qs(urlsplit(link).query) == {
            'lang': [language], 'area': [area], 'from': ['admin'], **({'record': [record]} if record else {})
        })
        opened = browser.get(target)
        assert opened.status_code == 200
        assert any(parse_qs(urlsplit(link).query).get('area') == ['admin'] for link in Page(opened.text).links)
    assert {('access', 'request'), ('expenses', 'taxi'), ('it', 'ticket-018')} <= page.details()


@pytest.mark.parametrize('language', ['en', 'pt'])
def test_sample_documents_open_from_records(demo, language):
    _, browser = demo
    found = set()
    for (area, key), record in BY_RECORD.items():
        names = {value[0] for _, value in record.fields if value[0] in SAMPLE_FILES}
        if not names:
            continue
        page = Page(browser.get(BASE, params={'area': area, 'record': key, 'lang': language}).text)
        for filename in names:
            url = f"{BASE}/files/{SAMPLE_FILES[filename]}?lang={language}"
            assert url in page.links
            response = browser.get(url)
            assert response.status_code == 200
            assert filename in response.headers['Content-Disposition']
            if filename.endswith('.pdf'):
                assert response.content.startswith(b'%PDF-') and response.content.rstrip().endswith(b'%%EOF')
            else:
                with ZipFile(BytesIO(response.content)) as book:
                    assert 'xl/workbook.xml' in book.namelist()
                    assert b'FIC-SV-0204' in book.read('xl/worksheets/sheet1.xml')
            found.add(filename)
    assert found == set(SAMPLE_FILES)


def test_sample_documents_require_public_demo_and_have_no_write_action(demo):
    gate, browser = demo
    assert browser.get(BASE + '/files/missing').status_code == 404
    assert browser.post(BASE + '/files/manifest').status_code == 405
    gate.public_entry = False
    assert browser.get(BASE + '?area=admin').status_code == 404
    assert browser.get(BASE + '/files/training').status_code == 404
