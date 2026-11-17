"""Application-only OpenAI environment forwarding. No real credentials/network."""
from __future__ import annotations

import os
from pathlib import Path
import signal
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from deploy import entrypoint as entry, company_entrypoint as company


AI = {'OPENAI_API_KEY': 'Fictional UI143 key #= preserve exactly ',
      'OPENAI_IMPORT_MODEL': 'fictional-test-model'}
FORBIDDEN = {'OPENAI_ORG_ID': 'not-forwarded', 'OPENAI_BASE_URL': 'not-forwarded',
             'COMPANY_SETUP_KEY': 'not-forwarded', 'COMPANY_INITIAL_PASSWORD': 'not-forwarded',
             'EXTRA_PRIVATE_SETTING': 'not-forwarded', 'LD_PRELOAD': 'not-forwarded'}


def test_application_environment_only_copies_explicit_ai_settings(monkeypatch):
    for name, value in {**AI, **FORBIDDEN}.items():
        monkeypatch.setenv(name, value)
    before = {**AI, **FORBIDDEN}
    source = dict(before)
    assert entry.application_environment(source) == {**entry.minimal_environment(), **AI}
    assert source == before
    assert not set(AI) & entry.minimal_environment().keys()
    # Explicit absence must not inherit the supervisor's ambient credentials.
    assert entry.application_environment({}) == entry.minimal_environment()


def test_company_environment_keeps_identity_and_membership_boundaries():
    source = {**AI, **FORBIDDEN, 'WAVELINK_DEPLOYMENT_MODE': 'COMPANY',
              'COMPANY_ID': 'fictional-company', 'COMPANY_NAME': 'Fictional Company',
              'WAVELINK_MEMBERSHIP_MODE': 'OFF', 'MEMBERSHIP_SMTP_PASSWORD': 'not-forwarded'}
    env = company.company_application_environment(source, origin='https://company.example.test')
    assert all(env[name] == value for name, value in AI.items())
    assert not set(FORBIDDEN) & env.keys()
    assert 'MEMBERSHIP_SMTP_PASSWORD' not in env
    assert env['COMPANY_ID'] == source['COMPANY_ID']
    assert env['PUBLIC_URL'] == 'https://company.example.test'
    assert env['WAVELINK_MEMBERSHIP_MODE'] == env['WAVELINK_ALERT_EMAIL'] == 'OFF'


@pytest.mark.parametrize('mode', ['DEMO', 'COMPANY'])
@pytest.mark.parametrize('configured', [False, True])
def test_supervisors_forward_ai_only_to_application(tmp_path, monkeypatch, capsys, mode, configured):
    target = entry if mode == 'DEMO' else company
    mount = tmp_path / 'disk'; mount.mkdir()
    base = tmp_path / 'container'; base.mkdir()
    data = mount / ('wavelink' if mode == 'DEMO' else 'wavelink-company')
    gateway = tmp_path / 'gateway'
    path_type = Path
    gateway_path = '/tmp/wavelink-gateway' if mode == 'DEMO' else '/tmp/wavelink-company-gateway'
    monkeypatch.setattr(target, 'BASE', base)
    monkeypatch.setattr(target, 'MOUNT', mount)
    monkeypatch.setattr(target, 'DATA', data)
    monkeypatch.setattr(target, 'Path', lambda value: gateway if str(value) == gateway_path else path_type(value))
    monkeypatch.setattr(entry, 'mounted', lambda value: value == mount)
    monkeypatch.setattr(target.os, 'geteuid', lambda: 10001, raising=False)
    monkeypatch.setattr(target.os, 'umask', lambda value: 0o077)
    cfg = {'authority': 'company.example.test', 'origin': 'https://company.example.test',
           'config': data / 'hosted.json', 'gate_key': data / 'gate.key'}
    monkeypatch.setattr(target, 'prepare' if mode == 'DEMO' else 'prepare_company', lambda *a, **kw: cfg)
    monkeypatch.setattr(target, 'render' if mode == 'DEMO' else 'render_company', lambda *a, **kw: '# Fictional nginx')
    monkeypatch.setattr(entry, 'wait_ready', lambda *a, **kw: None)
    callbacks = {}; launches = []; checks = []
    monkeypatch.setattr(target.signal, 'signal', lambda sig, callback: callbacks.setdefault(sig, callback))

    class Child:
        stopped = False
        def poll(self): return 0 if self.stopped else None
        def terminate(self): self.stopped = True
        def wait(self, **kw): self.stopped = True; return 0

    def check_gateway(command, **kw):
        assert command[:2] == ['nginx', '-t']
        checks.append(dict(kw['env']))
        return SimpleNamespace(returncode=0, stderr='')

    def start(command, **kw):
        role = ('nginx' if command[0] == 'nginx' else
                'gate' if 'deploy.gate' in command else 'application')
        launches.append((role, dict(kw['env'])))
        if role == 'nginx': callbacks[signal.SIGTERM](signal.SIGTERM, None)
        return Child()

    monkeypatch.setattr(target.subprocess, 'run', check_gateway)
    monkeypatch.setattr(target.subprocess, 'Popen', start)
    source = {**FORBIDDEN, 'WAVELINK_DEPLOYMENT_MODE': mode,
              'COMPANY_ID': 'fictional-company', 'COMPANY_NAME': 'Fictional Company',
              'DEMO_ACCESS_PASSWORD': 'Fictional gate password',
              'DEMO_GUEST_LOGIN': 'fictional-guest', 'DEMO_GUEST_PASSWORD': 'Fictional guest password',
              'MEMBERSHIP_SMTP_PASSWORD': 'not-forwarded'}
    if configured: source.update(AI)
    with patch.dict(os.environ, source, clear=True):
        assert (entry.run() if mode == 'DEMO' else company.run_company()) == 0
    assert [role for role, _ in launches] == (['application', 'gate', 'nginx'] if mode == 'DEMO' else ['application', 'nginx'])
    app = launches[0][1]
    assert {name: app[name] for name in AI if name in app} == (AI if configured else {})
    assert not set(FORBIDDEN) & app.keys()
    assert 'MEMBERSHIP_SMTP_PASSWORD' not in app
    assert not {'DEMO_ACCESS_PASSWORD', 'DEMO_GUEST_PASSWORD'} & app.keys()
    for env in checks + [env for role, env in launches if role != 'application']:
        assert not set(AI) & env.keys()
        assert not set(FORBIDDEN) & env.keys()
    output = capsys.readouterr()
    assert AI['OPENAI_API_KEY'] not in output.out + output.err
