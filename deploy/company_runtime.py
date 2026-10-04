"""C01 company-only ASGI boundary; the verified UI97 application is unchanged.

Named-session enforcement covers all ordinary API paths. Isolated QR endpoints
retain their own exact-document grant checks. A pending installation exposes only
its bounded, key-protected first-password-change flow, never a normal session.
"""
from __future__ import annotations
import asyncio
from collections import deque
from contextlib import closing
import hashlib
import hmac
import html
import json
from pathlib import Path
import secrets
import threading
import time
import uuid

from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, FileResponse

from .company_provision import read_marker, verify_activation, activation, ACTIVATION, digest
from .provision import DemoError

ASSETS = Path(__file__).with_name('company_assets')
HEADERS = {'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer',
           'Content-Security-Policy': "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'"}


class SetupError(Exception):
    def __init__(self, code, message): self.code, self.message = code, message


class ActivationService:
    def __init__(self, prepared, record, *, clock=time.time):
        self.prepared, self.record, self.clock = prepared, record, clock
        self.attempts, self.lock = deque(), threading.Lock()

    def authenticate_key(self, value):
        if not isinstance(value, str) or not 32 <= len(value) <= 128 or not secrets.compare_digest(digest(value), self.record['setup_key_sha256']):
            raise SetupError(403, 'First sign-in link is unavailable or invalid. Ask the installation operator.')

    def limit(self):
        now = time.monotonic()
        with self.lock:
            while self.attempts and now-self.attempts[0] > 60: self.attempts.popleft()
            if len(self.attempts) >= 10: raise SetupError(429, 'Too many setup attempts. Wait one minute.')
            self.attempts.append(now)

    def status(self):
        with closing(self.prepared.connect(readonly=True)) as con:
            return verify_activation(con, self.record)

    def outcome(self, secret, request_id):
        self.authenticate_key(secret)
        try:
            if not isinstance(request_id, str) or str(uuid.UUID(request_id)) != request_id: raise ValueError()
        except ValueError:
            raise SetupError(422, 'Invalid setup request identity.') from None
        with closing(self.prepared.connect(readonly=True)) as con:
            done = activation(con, self.record)
        return {'completed': bool(done and done['request_id'] == request_id), 'sign_in_required': True}

    def complete(self, secret, data):
        from app.accounts import normal_login, password_matches, password_hash
        from app.store import pack, utcnow
        self.limit()
        self.authenticate_key(secret)
        keys = {'request_id', 'login_id', 'temporary_password', 'new_password', 'confirm_password'}
        if not isinstance(data, dict) or set(data) != keys or any(not isinstance(v, str) for v in data.values()):
            raise SetupError(422, 'Enter the required first sign-in fields.')
        if len(data['login_id']) > 40 or any(len(data[k]) > 128 for k in ('temporary_password', 'new_password', 'confirm_password')):
            raise SetupError(422, 'One or more first sign-in fields is too long.')
        try:
            if str(uuid.UUID(data['request_id'])) != data['request_id']: raise ValueError()
            login = normal_login(data['login_id'])
        except Exception:
            raise SetupError(422, 'Invalid account or request identity.') from None
        fingerprint = hmac.new(secret.encode(), pack(data).encode(), hashlib.sha256).hexdigest()
        with closing(self.prepared.connect(readonly=True)) as con:
            done = activation(con, self.record)
            if done:
                if done['request_id'] == data['request_id'] and hmac.compare_digest(done['request_fingerprint'], fingerprint):
                    return {'completed': True, 'sign_in_required': True}
                raise SetupError(409, 'First sign-in is already complete. Use the normal account login.')
        if self.clock() >= self.record['setup_expires_epoch']:
            raise SetupError(410, 'The 24-hour first sign-in window expired. Ask the operator; do not reset the project.')
        if login != self.record['admin_login'] or not password_matches(data['temporary_password'], self.record['initial_hash']):
            raise SetupError(403, 'Incorrect initial account or temporary password.')
        password = data['new_password']
        if (not 14 <= len(password) <= 128 or password != password.strip() or any(ord(c) < 32 for c in password)
                or len(set(password)) < 6 or password == secret or password == data['temporary_password']):
            raise SetupError(422, 'Choose a different passphrase of 14-128 characters, with at least six distinct characters and no outer spaces.')
        if password != data['confirm_password']:
            raise SetupError(422, 'The new passphrases do not match.')
        encoded = password_hash(password)
        with closing(self.prepared.connect()) as con:
            con.execute('BEGIN IMMEDIATE')
            try:
                done = activation(con, self.record)
                if done:
                    if done['request_id'] != data['request_id'] or not hmac.compare_digest(done['request_fingerprint'], fingerprint):
                        raise SetupError(409, 'First sign-in was completed elsewhere. Use normal login.')
                else:
                    verify_activation(con, self.record)
                    if self.clock() >= self.record['setup_expires_epoch']:
                        raise SetupError(410, 'The first sign-in window expired. Ask the operator.')
                    now = utcnow()
                    con.execute('UPDATE users SET password_hash=?, credential_version=credential_version+1, updated_at=?, failures=0, locked_until=0 WHERE id=?',
                                (encoded, now, self.record['admin_id']))
                    # No operational accounts exist before activation; remove any
                    # accidentally/offline-created session so only new login works.
                    con.execute('DELETE FROM sessions')
                    con.execute('DELETE FROM participants')
                    detail = {'installation_id': self.record['installation_id'], 'hub_id': self.record['hub_id'],
                              'request_id': data['request_id'], 'request_fingerprint': fingerprint, 'changed_at': now}
                    con.execute('INSERT INTO user_audit(at,actor_id,target_id,action,detail) VALUES(?,?,?,?,?)',
                                (now, self.record['admin_id'], self.record['admin_id'], ACTIVATION, pack(detail)))
                con.commit()
            except BaseException:
                con.rollback()
                raise
        return {'completed': True, 'sign_in_required': True}


class CompanyAccess:
    def __init__(self, app, *, hosted, settings, root):
        self.app, self.hosted, self.settings = app, hosted, settings
        self.record = read_marker(Path(root))
        if self.record['hub_id'] != settings.expected_hub_id:
            raise DemoError('Company wrapper and project identities differ.')
        self.service = None

    def current_service(self):
        prepared = self.hosted.state.prepared
        if not self.hosted.state.serving or not prepared:
            raise DemoError('Company project is not ready.')
        if self.service is None or self.service.prepared is not prepared:
            self.service = ActivationService(prepared, self.record)
        prepared.assert_same_files()
        return self.service

    async def respond(self, response, scope, receive, send):
        for k, v in HEADERS.items(): response.headers[k] = v
        await response(scope, receive, send)

    async def body(self, request):
        if request.headers.get('origin') != self.settings.external_origin:
            raise SetupError(403, 'First sign-in requires this site’s exact browser origin.')
        if request.headers.get('content-type', '').split(';', 1)[0] != 'application/json':
            raise SetupError(415, 'Use the first sign-in form.')
        chunks, total = [], 0
        async for chunk in request.stream():
            total += len(chunk)
            if total > 4096: raise SetupError(413, 'First sign-in request is too large.')
            chunks.append(chunk)
        def unique(pairs):
            d = {}
            for k, v in pairs:
                if k in d: raise ValueError('duplicate')
                d[k] = v
            return d
        try:
            data = json.loads(b''.join(chunks), object_pairs_hook=unique)
        except (ValueError, UnicodeError): raise SetupError(422, 'Invalid first sign-in request.') from None
        return data

    async def __call__(self, scope, receive, send):
        if scope['type'] not in ('http', 'websocket'):
            return await self.app(scope, receive, send)
        path, method = scope.get('path', ''), scope.get('method', '')
        # Health reveals no project content and is needed before external activation.
        if scope['type'] == 'http' and path in ('/healthz', '/readyz') and method in ('GET', 'HEAD'):
            return await self.app(scope, receive, send)
        try:
            service = self.current_service()
            active = await asyncio.to_thread(service.status)
            if path.startswith('/__demo') or path == '/_demo_verify':
                raise SetupError(404, 'No demonstration entry exists on this company service.')
            if scope['type'] == 'websocket':
                if not active or path != '/ws':
                    return await send({'type': 'websocket.close', 'code': 1008})
                # Existing first WebSocket message validates the named session.
                return await self.app(scope, receive, send)
            request = Request(scope, receive)
            if path == '/company-setup/status' and method == 'GET':
                return await self.respond(JSONResponse({'company': self.record['company_name'], 'active': active,
                    'login_id': self.record['admin_login'] if not active else None}), scope, receive, send)
            if path in ('/company-setup/activate', '/company-setup/outcome') and method == 'POST':
                if len(request.headers.getlist('authorization')) != 1:
                    raise SetupError(403, 'Use the private first sign-in link.')
                auth = request.headers.get('authorization', '')
                if not auth.startswith('Bearer '): raise SetupError(403, 'Use the private first sign-in link.')
                data = await self.body(request)
                if path.endswith('/activate'):
                    result = await asyncio.to_thread(service.complete, auth[7:], data)
                else:
                    if not isinstance(data, dict) or set(data) != {'request_id'}:
                        raise SetupError(422, 'Invalid outcome request.')
                    result = await asyncio.to_thread(service.outcome, auth[7:], data['request_id'])
                return await self.respond(JSONResponse(result), scope, receive, send)
            static = {'/company-setup': ('setup.html','text/html'), '/company-setup/': ('setup.html','text/html'),
                      '/company-setup/setup.js': ('setup.js','application/javascript'),
                      '/company-setup/setup.css': ('setup.css','text/css')}
            if path in static and method in ('GET', 'HEAD'):
                filename, media = static[path]
                return await self.respond(FileResponse(ASSETS / filename, media_type=media), scope, receive, send)
            if path == '/company-setup/icon.svg' and method in ('GET', 'HEAD'):
                from app.server import BASE
                return await self.respond(FileResponse(BASE/'static/wavelink-mark.svg',media_type='image/svg+xml'),scope,receive,send)
            if not active:
                if path == '/' and method in ('GET', 'HEAD'):
                    text = (ASSETS/'pending.html').read_text().replace('COMPANY_NAME', html.escape(self.record['company_name']))
                    return await self.respond(Response(text, media_type='text/html'), scope, receive, send)
                raise SetupError(423, 'Company first sign-in is pending. Normal account access is locked.')
            if path.startswith('/company-setup/'):
                raise SetupError(404, 'First sign-in route not found.')
            if path == '/api/join':
                raise SetupError(403, 'Use a named company account. Shared-code entry is disabled.')
            # Public authentication must be reachable before a normal session
            # exists. UI98 adds only exact recovery methods and MFA completion;
            # their own proof/origin/hub/attempt/body checks stay in the core.
            from app.membership_api import PUBLIC_METHODS
            membership_entry = path in PUBLIC_METHODS and method in PUBLIC_METHODS[path]
            from app.password_recovery_api import METHODS as RECOVERY_METHODS
            public_authentication = (path, method) in {
                ('/api/info', 'GET'), ('/api/login', 'POST'), ('/api/login/mfa', 'POST'),
                *RECOVERY_METHODS.items(),
            }
            if path.startswith('/api/') and not public_authentication and not path.startswith('/api/document-sign/') and not membership_entry:
                auth = request.headers.get('authorization', '')
                if len(request.headers.getlist('authorization')) != 1 or not auth.startswith('Bearer '):
                    raise SetupError(401, 'Sign in with your company account.')
                person = await asyncio.to_thread(self.hosted.state.core.state.store.session, auth[7:])
                if not person.get('user_id'):
                    raise SetupError(401, 'Use a named company account, not shared access.')
            async def private_api(message):
                if message['type'] == 'http.response.start' and path.startswith('/api/'):
                    message = dict(message)
                    message['headers'] = [(k,v) for k,v in message.get('headers',[]) if k.lower() != b'cache-control']
                    message['headers'].append((b'cache-control',b'no-store'))
                await send(message)
            return await self.app(scope, receive, private_api)
        except SetupError as exc:
            response = JSONResponse({'error': exc.message}, status_code=exc.code)
        except Exception as exc:
            from app.store import Problem
            if isinstance(exc, Problem): response = JSONResponse({'error': exc.message}, status_code=exc.code)
            else: response = JSONResponse({'error': 'Company storage or setup is unavailable. Contact the operator; no replacement project was created.'}, status_code=503)
        if scope['type'] == 'websocket': return await send({'type':'websocket.close','code':1013})
        return await self.respond(response, scope, receive, send)


def create_company_app(settings, root):
    from app.hosted_runtime import create_hosted_app
    hosted = create_hosted_app(settings)
    # After HostedBoundary (host/origin/proxy validation), before all app routes.
    hosted.user_middleware.append(Middleware(CompanyAccess, hosted=hosted, settings=settings, root=root))
    return hosted


def main():
    import argparse
    import uvicorn
    from app.hosted_config import HostedSettings
    from app.hosted_storage import PreparedProject
    parser = argparse.ArgumentParser(description='C01 company runtime: single named-account project')
    parser.add_argument('--config', required=True, type=Path)
    parser.add_argument('--root', required=True, type=Path)
    args = parser.parse_args()
    settings = HostedSettings.from_file(args.config)
    if settings.project_dir != args.root/'project': raise DemoError('Company runtime project/root mismatch.')
    PreparedProject(settings)
    app = create_company_app(settings, args.root)
    uvicorn.run(app, host=settings.listen_host, port=settings.listen_port, workers=1, reload=False,
                proxy_headers=False, forwarded_allow_ips='', access_log=False, server_header=False,
                limit_concurrency=100, timeout_keep_alive=10, timeout_graceful_shutdown=30, log_level='warning')

if __name__ == '__main__': main()
