"""Disposable localization checks; no network, live company or SMTP writes."""
from __future__ import annotations
import asyncio
import hashlib
import json
import os
from pathlib import Path
import uuid

import pytest
from fastapi.testclient import TestClient

from app.localization import (PT_BR, company_locale, marker_locale, locale_bootstrap,
                              localized_send, translate_message)
from app.hosted_config import HostedSettings
from app.hosted_storage import PreparedProject
from deploy.company_provision import prepare_company, read_marker
from deploy.company_runtime import create_company_app, ActivationService
from deploy.company_localization import localized_asset
from deploy.company_entrypoint import company_application_environment

SOURCE = Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()


@pytest.mark.parametrize('env,expected', [
    ({}, 'en'),
    ({'COMPANY_ID': 'corcovado'}, 'en'),
    ({'WAVELINK_DEPLOYMENT_MODE': 'DEMO', 'COMPANY_ID': 'corcovado'}, 'en'),
    ({'WAVELINK_DEPLOYMENT_MODE': 'COMPANY', 'COMPANY_ID': 'sulmara'}, 'en'),
    ({'WAVELINK_DEPLOYMENT_MODE': 'COMPANY', 'COMPANY_ID': 'fictional-company', 'LANG': 'pt_BR.UTF-8'}, 'en'),
    ({'WAVELINK_DEPLOYMENT_MODE': 'COMPANY', 'COMPANY_ID': 'corcovado'}, PT_BR),
    ({'WAVELINK_DEPLOYMENT_MODE': 'COMPANY', 'COMPANY_ID': 'Corcovado'}, 'en'),
])
def test_locale_is_fixed_by_exact_deployment_identity(env, expected):
    assert company_locale(env) == expected


def test_child_environment_preserves_company_locale_without_extra_operator_settings():
    source = {'WAVELINK_DEPLOYMENT_MODE': 'COMPANY', 'COMPANY_ID': 'corcovado', 'COMPANY_NAME': 'Corcovado',
              'WAVELINK_LOCALE': 'en', 'LANG': 'en_US.UTF-8'}
    env = company_application_environment(source, origin='https://corcovado.example.test')
    assert company_locale(env) == PT_BR
    assert 'WAVELINK_LOCALE' not in env
    assert marker_locale({'company_id': 'corcovado'}) == PT_BR
    assert marker_locale({'company_id': 'sulmara', 'ui_locale': PT_BR}) == 'en'
    bootstrap = locale_bootstrap(PT_BR)
    assert '"pt-BR"' in bootstrap and 'writable:false' in bootstrap
    assert '"en"' in locale_bootstrap('injected-value')


def test_only_reviewed_messages_are_translated():
    message = 'Incorrect email/User ID or password, or the account is disabled.'
    assert translate_message(message, PT_BR) == 'E-mail, usuário ou senha incorretos, ou a conta está desativada.'
    assert translate_message(message, 'en') == message
    assert translate_message('Customer document: '+message, PT_BR) == 'Customer document: '+message
    assert translate_message({'error': message}, PT_BR) == {'error': message}


def response_messages(payload, *, path='/api/info', locale=PT_BR, status=200):
    messages = []
    async def send(message): messages.append(message)
    async def execute():
        raw = json.dumps(payload).encode()
        forward = localized_send(send, path=path, locale=locale)
        await forward({'type': 'http.response.start', 'status': status, 'headers': [(b'content-type', b'application/json'), (b'content-length', str(len(raw)).encode())]})
        await forward({'type': 'http.response.body', 'body': raw[:10], 'more_body': True})
        await forward({'type': 'http.response.body', 'body': raw[10:]})
    asyncio.run(execute())
    return messages


def test_json_translation_preserves_user_values_and_protocol_codes():
    source = {'error': 'Sign in again.', 'name': 'Sign in again.', 'hub_id': 'unchanged-id',
              'records': [{'message': 'Sign in again.'}], 'defaults': {'company': 'Sulmara'}}
    messages = response_messages(source, path='/api/example', status=401)
    result = json.loads(messages[-1]['body'])
    assert result == {**source, 'error': 'Entre novamente.'}
    assert dict(messages[0]['headers'])[b'content-language'] == b'pt-BR'
    assert dict(messages[0]['headers'])[b'content-length'] == str(len(messages[-1]['body'])).encode()
    english = response_messages(source, locale='en', status=401)
    assert json.loads(b''.join(message.get('body', b'') for message in english[1:])) == source
    info = json.loads(response_messages({'defaults': source['defaults']})[-1]['body'])
    assert info == {'defaults': source['defaults'], 'ui_locale': PT_BR}


def test_english_and_binary_pass_through_without_body_changes():
    async def check(locale, content_type):
        messages = []
        async def send(message): messages.append(message)
        forward = localized_send(send, path='/api/export', locale=locale)
        header = {'type': 'http.response.start', 'status': 200, 'headers': [(b'content-type', content_type)]}
        body = {'type': 'http.response.body', 'body': b'Sign in again.\x00\xff'}
        await forward(header); await forward(body)
        assert messages[-1] == body
        if locale == 'en': assert messages[0] == header
    asyncio.run(check('en', b'application/json'))
    asyncio.run(check(PT_BR, b'application/pdf'))


def test_gateway_static_translation_does_not_change_english_assets():
    assets = Path(__file__).resolve().parents[1] / 'deploy/company_assets'
    for name in ('setup.html', 'setup.js', 'pending.html'):
        original = (assets/name).read_text()
        assert localized_asset(original, 'en') == original
        translated = localized_asset(original, PT_BR)
        assert translated != original
        assert 'support@mywavelink.com' in translated if name.endswith('.html') else True
    assert 'lang="pt-BR"' in localized_asset((assets/'setup.html').read_text(), PT_BR)


@pytest.fixture
def company(tmp_path, monkeypatch):
    env = dict(WAVELINK_DEPLOYMENT_MODE='COMPANY', COMPANY_ID='corcovado', COMPANY_NAME='Corcovado',
               PUBLIC_URL='https://corcovado.example.test', INITIALISE_COMPANY='YES_FIRST_DEPLOY_ONLY',
               COMPANY_ADMIN_LOGIN='admin', COMPANY_INITIAL_PASSWORD='initial12',
               COMPANY_SETUP_KEY='Fictional-Corcovado-only-setup-key-0123456789')
    for key, value in env.items(): monkeypatch.setenv(key, value)
    root = tmp_path/'corcovado'
    cfg = prepare_company(root, SOURCE, env)
    settings = HostedSettings.from_file(cfg['config'], environ={})
    return root, cfg, settings, env


def client_for(company):
    root, cfg, settings, env = company
    return TestClient(create_company_app(settings, root), base_url=settings.external_origin,
                      headers={'Host': settings.authority, 'X-Forwarded-Proto': 'https',
                               'X-Forwarded-For': '192.0.2.15', 'Origin': settings.external_origin},
                      client=('127.0.0.1', 1234))


def test_pending_company_gateway_is_portuguese_and_read_only(company):
    root, cfg, settings, env = company
    original_db = hashlib.sha256((root/'project/dives.sqlite3').read_bytes()).hexdigest()
    with client_for(company) as client:
        page = client.get('/')
        assert 'Primeiro acesso pendente' in page.text and 'lang="pt-BR"' in page.text
        assert 'Corcovado' in page.text
        script = client.get('/company-setup/setup.js')
        assert 'Salvando a nova senha' in script.text
        assert 'request_id' in script.text and 'temporary_password' in script.text
        bootstrap = client.get('/static/workspace-locale.js?company=sulmara&lang=en', headers={'Accept-Language': 'en-US'})
        assert '"pt-BR"' in bootstrap.text and bootstrap.headers['cache-control'] == 'no-store'
        locked = client.get('/api/info')
        assert locked.status_code == 423
        assert 'primeiro acesso da empresa' in locked.json()['error']
    assert hashlib.sha256((root/'project/dives.sqlite3').read_bytes()).hexdigest() == original_db


def test_active_company_bootstrap_and_login_errors_are_portuguese(company):
    root, cfg, settings, env = company
    service = ActivationService(PreparedProject(settings), read_marker(root))
    password = 'Fictional permanent password 012345.'
    service.complete(env['COMPANY_SETUP_KEY'], dict(request_id=str(uuid.uuid4()), login_id='admin',
                     temporary_password=env['COMPANY_INITIAL_PASSWORD'], new_password=password, confirm_password=password))
    with client_for(company) as client:
        info = client.get('/api/info').json()
        assert info['ui_locale'] == PT_BR and info['hub_id'] == cfg['hub_id']
        assert info['defaults'] == {}  # Anonymous bootstrap still discloses no project data.
        wrong = client.post('/api/login', json={'login_id': 'admin', 'password': 'wrong', 'device_id': 'corcovado-test-device'})
        assert wrong.status_code == 403
        assert wrong.json()['error'] == 'E-mail, usuário ou senha incorretos, ou a conta está desativada.'
        missing = client.get('/api/records')
        assert missing.status_code == 401 and missing.json()['error'] == 'Entre com sua conta da empresa.'
        login = client.post('/api/login', json={'login_id': 'admin', 'password': password, 'device_id': 'corcovado-test-device'})
        assert login.status_code == 200 and login.json()['token']


def test_only_reviewed_static_html_paths_can_select_variants(tmp_path):
    from app.localization import localized_html_path
    root = tmp_path/'static'
    (root/'pt-BR/help_topics').mkdir(parents=True)
    (root/'help_topics').mkdir()
    for name in ('index.html', 'password_recovery.html', 'membership_entry.html', 'document_join.html', 'fleet.html', 'help_topics/start.html', 'unexpected.html'):
        (root/name).write_text('<html lang="en">Original</html>')
        (root/'pt-BR'/name).write_text('<html lang="pt-BR">Português</html>')
    for route, name in [('/', 'index.html'), ('/static/index.html', 'index.html'),
                        ('/reset-password/', 'password_recovery.html'), ('/join-team', 'membership_entry.html'),
                        ('/sign', 'document_join.html'), ('/fleet', 'fleet.html'),
                        ('/help/topics/start', 'help_topics/start.html'), ('/static/help_topics/start.html', 'help_topics/start.html')]:
        assert localized_html_path(route, root, PT_BR) == root/'pt-BR'/name
        assert localized_html_path(route, root, 'en') is None
    for route in ('/api/files/index.html', '/static/../index.html', '/static/pt-BR/index.html',
                  '/static//index.html', '/static/unexpected.html', '/static/help_topics/unknown.html',
                  '/help/topics/start/../../index', '/static/foo/index.html', '/static/index.html/extra'):
        assert localized_html_path(route, root, PT_BR) is None, route
    (root/'pt-BR/index.html').unlink()
    assert localized_html_path('/', root, PT_BR) is None
    (root/'pt-BR/index.html').symlink_to(root/'password_recovery.html')
    assert localized_html_path('/', root, PT_BR) is None


def test_hr_and_common_literal_errors_have_reviewed_translations():
    import ast
    from app.localization import MESSAGES_PT_BR
    modules = ('hr', 'hr_api', 'fieldwork_common', 'access', 'accounts', 'browser_admin',
               'browser_admin_api', 'company_membership', 'membership_api', 'user_lifecycle',
               'departments', 'fleet_access', 'task_access', 'access_review', 'assets_api',
               'account_security', 'account_security_api', 'company_roles', 'store',
               'project_presence', 'email_alerts_api', 'operations_api', 'membership_mail', 'email_alerts')
    for module in modules:
        for node in ast.walk(ast.parse((SOURCE/'app'/(module+'.py')).read_text())):
            if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                    and node.func.id in ('Problem', 'HTTPException') and len(node.args) > 1
                    and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str)):
                message = node.args[1].value
                assert message in MESSAGES_PT_BR, (module, message)
                assert translate_message(message, 'en') == message


def test_hr_field_errors_preserve_raw_service_behavior():
    from app.hr import decimal_value, clock, choice
    from app.store import Problem
    cases = [
        (lambda: decimal_value('2,50', 'Amount'), 'Amount must be a decimal string with at most two decimal places.', 'Informe valor como número decimal, com no máximo duas casas decimais.'),
        (lambda: clock('25:00', 'depart time'), 'depart time must use HH:MM.', 'Informe horário de partida no formato HH:MM.'),
        (lambda: choice('invalid', ('flight', 'vessel'), 'travel mode'), 'Choose a valid travel mode.', 'Escolha um valor válido para meio de transporte.'),
    ]
    for call, english, portuguese in cases:
        with pytest.raises(Problem) as caught:
            call()
        assert caught.value.code == 422 and caught.value.message == english
        assert translate_message(caught.value.message, PT_BR) == portuguese
        assert translate_message(caught.value.message, 'en') == english
    assert translate_message('CustomerField must use HH:MM.', PT_BR) == 'CustomerField must use HH:MM.'


def test_validation_translation_retains_machine_codes_and_supplied_values():
    from app.localization import localized_validation_detail
    source = [{'type': 'int_parsing', 'loc': ['query', 'limit'], 'msg': 'Input should be a valid integer, unable to parse string as an integer', 'input': 'User supplied text'},
              {'type': 'string_too_long', 'loc': ['body', 'title'], 'msg': 'String should have at most 240 characters', 'input': 'Sign in again.', 'ctx': {'max_length': 240}},
              {'type': 'custom_unknown', 'loc': ['body', 'name'], 'msg': 'Customer authored validation', 'input': 'Sign in again.'}]
    translated = localized_validation_detail(source, PT_BR)
    assert translated[0] == {**source[0], 'msg': 'Informe um número inteiro válido.'}
    assert translated[1] == {**source[1], 'msg': 'Use no máximo 240 caracteres.'}
    assert translated[2] == source[2]
    assert localized_validation_detail(source, 'en') is source
    assert localized_validation_detail('Not Found', PT_BR) == 'Página não encontrada.'
    assert localized_validation_detail('Customer authored message', PT_BR) == 'Customer authored message'
    assert source[0]['msg'].startswith('Input should')
    messages = response_messages({'detail': source}, path='/api/hr/records', status=422)
    assert json.loads(messages[-1]['body'])['detail'] == translated


def test_private_hr_http_errors_are_portuguese_and_bad_forms_write_nothing(company):
    root, cfg, settings, env = company
    record = read_marker(root)
    password = 'Fictional permanent password 012345.'
    ActivationService(PreparedProject(settings), record).complete(env['COMPANY_SETUP_KEY'], dict(
        request_id=str(uuid.uuid4()), login_id='admin', temporary_password=env['COMPANY_INITIAL_PASSWORD'],
        new_password=password, confirm_password=password))
    with client_for(company) as client:
        token = client.post('/api/login', json={'login_id': 'admin', 'password': password, 'device_id': 'hr-locale-test-device'}).json()['token']
        headers = {'Authorization': 'Bearer '+token, 'X-AJ-Hub-ID': cfg['hub_id']}
        malformed_query = client.get('/api/hr/records?kind=expenses&limit=wrong', headers=headers)
        assert malformed_query.status_code == 422
        detail = malformed_query.json()['detail'][0]
        assert detail['type'] == 'int_parsing' and detail['input'] == 'wrong'
        assert detail['msg'] == 'Informe um número inteiro válido.'
        fields = dict(id='', version=0, user_id=record['admin_id'], title='Despesa de teste',
                      date='2026-10-17', category='travel', merchant='Loja de teste', amount='12.50',
                      currency='brl', project='Projeto de teste', description='Texto informado pelo usuário', notes='')
        invalid = client.post('/api/hr/action', headers=headers, json={'action': 'save_expense', 'payload': fields, 'op_id': str(uuid.uuid4())})
        assert invalid.status_code == 422
        assert invalid.json()['error'] == 'Use um código de moeda com três letras maiúsculas.'
        fields['currency'] = 'BRL'
        fields['amount'] = '12,50'
        invalid_amount = client.post('/api/hr/action', headers=headers, json={'action': 'save_expense', 'payload': fields, 'op_id': str(uuid.uuid4())})
        assert invalid_amount.status_code == 422
        assert invalid_amount.json()['error'] == 'Informe valor como número decimal, com no máximo duas casas decimais.'
        records = client.get('/api/hr/records?kind=expenses', headers=headers)
        assert records.status_code == 200 and records.json()['items'] == []
