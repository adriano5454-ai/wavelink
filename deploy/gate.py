"""Restricted fictional-demo gate, consolidated from the confirmed chat fixes.

Not production SSO, MFA, per-client invitations or company isolation.
Normal access still requires a separate Wavelink account. The shared quick link
uses the configured guest credentials on the server, then installs the returned
session in the existing browser workspace. No password is embedded in this file.

Query-string links may remain in messages/history/provider logs. Rotate the demo
access password and disable/change the guest account after the presentation.
"""
from __future__ import annotations

import base64
from collections import deque
import hashlib
import hmac
import html
import http.client
import json
import os
from pathlib import Path
import secrets
import time
from urllib.parse import parse_qs

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.routing import Route

COOKIE = '__Host-wavelink-demo'
CSRF_COOKIE = '__Host-wavelink-demo-csrf'
TTL = 8 * 3600
HEADERS = {
    'Cache-Control': 'no-store', 'Pragma': 'no-cache',
    'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer',
    'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
}
BOOT_HEADERS = {
    'Cache-Control': 'no-store', 'Pragma': 'no-cache',
    'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer',
    'X-Frame-Options': 'DENY',
    'Content-Security-Policy': "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none'",
}


class Gate:
    def __init__(self, origin: str, password: str, key: bytes,
                 guest_login: str, guest_password: str, *, clock=time.time):
        if len(key) != 32:
            raise ValueError('Invalid demonstration gate key.')
        if not 20 <= len(password) <= 128:
            raise ValueError('Invalid demonstration access password.')
        if not guest_login.strip():
            raise ValueError('Missing demonstration guest User ID.')
        if not 6 <= len(guest_password) <= 128:
            raise ValueError('Invalid demonstration guest password.')
        self.origin = origin.rstrip('/')
        self.key = key
        self.clock = clock
        # Do not reuse the authentication method name for this string.
        self.guest_login_id = guest_login.strip()
        self.guest_password = guest_password
        self.password_digest = hashlib.sha256(password.encode()).digest()
        self.epoch = hmac.new(key, b'gate-password:' + self.password_digest,
                              hashlib.sha256).hexdigest()
        self.attempts = deque()

    def token(self, kind: str, lifetime: int) -> str:
        payload = json.dumps({
            'kind': kind, 'exp': int(self.clock()) + lifetime,
            'nonce': secrets.token_urlsafe(18), 'epoch': self.epoch,
            'origin': self.origin,
        }, separators=(',', ':')).encode()
        body = base64.urlsafe_b64encode(payload).rstrip(b'=')
        signature = hmac.new(self.key, body, hashlib.sha256).hexdigest().encode()
        return (body + b'.' + signature).decode()

    def valid(self, token: str | None, kind: str) -> bool:
        try:
            if not token or len(token) > 1500:
                return False
            body, signature = token.encode('ascii').split(b'.')
            expected = hmac.new(self.key, body, hashlib.sha256).hexdigest().encode()
            if not hmac.compare_digest(signature, expected):
                return False
            value = json.loads(base64.urlsafe_b64decode(body + b'=' * (-len(body) % 4)))
            now = self.clock()
            return (value['kind'] == kind and value['origin'] == self.origin
                    and hmac.compare_digest(value['epoch'], self.epoch)
                    and type(value['exp']) is int and now < value['exp'] <= now + TTL + 1)
        except (ValueError, KeyError, TypeError, UnicodeError):
            return False

    @staticmethod
    def page(csrf: str, message: str = '', *, logout=False) -> HTMLResponse:
        title = 'Leave this demo session' if logout else 'Welcome to the Wavelink demonstration'
        action = 'logout' if logout else 'login'
        field = '' if logout else (
            '<label for="password">Private demo access password</label>'
            '<input id="password" name="password" type="password" '
            'autocomplete="current-password" required maxlength="128" autofocus>'
        )
        button = 'End access session' if logout else 'Enter demonstration'
        body = f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Wavelink · Private demo</title>
<style>
body {{margin:0;background:#eef2f6;color:#182b40;font:16px system-ui,sans-serif;min-height:100vh;display:grid;place-items:center}}
main {{background:white;width:min(430px,calc(100vw - 48px));box-sizing:border-box;margin:24px;padding:32px;border:1px solid #d7e0e8;border-radius:16px;box-shadow:0 12px 48px #182b4010}}
h1 {{font-size:26px;margin:18px 0}}
.eyebrow {{letter-spacing:.12em;font-size:12px;font-weight:750;color:#087b83}}
p {{line-height:1.55}}
label {{display:block;margin:24px 0 8px;font-weight:650}}
input {{box-sizing:border-box;width:100%;padding:13px;border:1px solid #899daf;border-radius:8px;font:inherit}}
button {{width:100%;padding:14px;border:0;border-radius:8px;background:#087b83;color:white;font:inherit;font-weight:700;margin-top:20px;cursor:pointer}}
.notice {{font-size:13px;color:#4c5e70;border-top:1px solid #d7e0e8;margin-top:24px;padding-top:16px}}
.error {{color:#9d2534}}
</style></head><body><main>
<div class="eyebrow">AJ OFFSHORE SOLUTIONS · WAVELINK</div>
<h1>{title}</h1>
<p>This private workspace contains fictional training records. After entry, sign in with your personal Wavelink account.</p>
<p class="error" role="alert">{html.escape(message)}</p>
<form method="post" action="/__demo/{action}">
<input type="hidden" name="csrf" value="{html.escape(csrf, quote=True)}">
{field}<button type="submit">{button}</button></form>
<p class="notice">Client demonstration only. Do not upload real operational, personal or confidential data.</p>
</main></body></html>'''
        return HTMLResponse(body, headers=HEADERS)

    def request_is_same_origin(self, request: Request) -> bool:
        # Preserve the currently confirmed fictional-demo form behavior:
        # verify the signed Secure/HttpOnly/SameSite CSRF cookie + hidden token.
        # This is NOT evidence that Render removes Origin, nor production SSO.
        return True

    async def form(self, request: Request) -> dict | None:
        if not self.request_is_same_origin(request):
            return None
        content_type = request.headers.get('content-type', '').split(';')[0].strip().lower()
        if content_type != 'application/x-www-form-urlencoded':
            return None
        raw = b''
        async for chunk in request.stream():
            raw += chunk
            if len(raw) > 4096:
                return None
        try:
            form = parse_qs(raw.decode(), keep_blank_values=True, max_num_fields=4,
                            strict_parsing=True)
            if any(len(value) != 1 for value in form.values()):
                return None
            result = {key: value[0] for key, value in form.items()}
            cookie = request.cookies.get(CSRF_COOKIE, '')
            csrf = result.get('csrf', '')
            if not self.valid(cookie, 'csrf'):
                return None
            if not hmac.compare_digest(csrf.encode(), cookie.encode()):
                return None
            return result
        except (ValueError, UnicodeError):
            return None

    def form_response(self, message='', *, logout=False):
        token = self.token('csrf', 600)
        response = self.page(token, message, logout=logout)
        response.set_cookie(CSRF_COOKIE, token, max_age=600, path='/', secure=True,
                            httponly=True, samesite='strict')
        return response

    def register_attempt(self) -> bool:
        now = self.clock()
        while self.attempts and self.attempts[0] < now - 300:
            self.attempts.popleft()
        if len(self.attempts) >= 20:
            return False
        self.attempts.append(now)
        return True

    def password_matches(self, supplied: str) -> bool:
        try:
            candidate = hashlib.sha256(supplied.encode()).digest()
        except UnicodeError:
            return False
        return hmac.compare_digest(candidate, self.password_digest)

    def admitted_response(self) -> RedirectResponse:
        response = RedirectResponse('/', status_code=303, headers=HEADERS)
        response.set_cookie(COOKIE, self.token('session', TTL), max_age=TTL,
                            path='/', secure=True, httponly=True, samesite='strict')
        response.delete_cookie(CSRF_COOKIE, path='/', secure=True,
                               httponly=True, samesite='strict')
        return response

    def authenticate_guest(self) -> dict:
        """Authenticate the configured guest through the loopback Wavelink API.

        The credential itself is not returned to the browser. This does not
        create the guest, change its permissions, or impersonate an administrator.
        """
        device_id = 'demo-guest-' + secrets.token_hex(12)
        payload = json.dumps({'login_id': self.guest_login_id,
                              'password': self.guest_password,
                              'device_id': device_id}).encode()
        con = http.client.HTTPConnection('127.0.0.1', 8765, timeout=10)
        try:
            con.request('POST', '/api/login', body=payload, headers={
                'Host': self.origin.removeprefix('https://'),
                'Content-Type': 'application/json', 'Accept': 'application/json',
                'X-Forwarded-Proto': 'https', 'X-Forwarded-For': '127.0.0.1',
            })
            response = con.getresponse()
            raw = response.read()
        finally:
            con.close()
        if response.status != 200:
            raise RuntimeError('The configured demo guest could not sign in. '
                               'Check that the account exists, is enabled, '
                               'and its Render password matches Wavelink.')
        try:
            data = json.loads(raw.decode())
        except (ValueError, UnicodeError) as exc:
            raise RuntimeError('The Wavelink guest login returned an invalid response.') from exc
        if not (isinstance(data, dict) and isinstance(data.get('token'), str)
                and isinstance(data.get('person'), dict)
                and isinstance(data.get('hub_id'), str)):
            raise RuntimeError('The Wavelink guest login response was incomplete.')
        return data

    @staticmethod
    def bootstrap_page(auth: dict) -> str:
        """Preserve the confirmed guest session handoff and draft/lease checks.

        This is the demonstration handoff, not a replacement for the normal
        account-switch workflow or a promise of durable/offline draft acceptance.
        """
        encoded = json.dumps(auth, separators=(',', ':')).replace(
            '<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
        return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Opening Wavelink…</title>
<style>
body {{margin:0;min-height:100vh;display:grid;place-items:center;background:#eef2f6;color:#182b40;font:16px system-ui,sans-serif}}
main {{width:min(440px,calc(100vw - 48px));background:white;box-sizing:border-box;padding:32px;border:1px solid #d7e0e8;border-radius:16px}}
h1 {{margin-top:0}}#error {{color:#9d2534;white-space:pre-wrap}}
</style></head><body><main><h1>Opening Wavelink…</h1>
<p>Preparing the fictional client workspace.</p><p id="error"></p></main>
<script>
(() => {{
    const auth = {encoded};
    const fail = message => {{
        document.getElementById('error').textContent = message + '\\n\\n'
            + 'Open /__demo/login if you need normal sign-in.';
    }};
    const request = indexedDB.open('pxgeo-dive-check-1', 1);
    request.onupgradeneeded = () => {{
        const db = request.result;
        if (!db.objectStoreNames.contains('state')) db.createObjectStore('state');
    }};
    request.onerror = () => fail('The browser workspace could not be opened.');
    request.onsuccess = () => {{
        const db = request.result;
        const tx = db.transaction('state', 'readwrite');
        const store = tx.objectStore('state');
        const mainReq = store.get('main');
        const leaseReq = store.get('lease');
        let saved = null;
        let lease = null;
        mainReq.onsuccess = () => {{ saved = mainReq.result || null; }};
        leaseReq.onsuccess = () => {{ lease = leaseReq.result || null; }};
        tx.oncomplete = () => {{
            db.close();
            if (lease && Number(lease.expires) > Date.now()) {{
                fail('Another Wavelink tab is already using this browser workspace. '
                     + 'Close it and open the guest link again.');
                return;
            }}
            const hasObjectValues = value => value && typeof value === 'object'
                && Object.keys(value).length > 0;
            const unsent = !!(saved && (
                (Array.isArray(saved.queue) && saved.queue.length)
                || hasObjectValues(saved.drafts) || hasObjectValues(saved.logDrafts)
                || hasObjectValues(saved.fieldworkDrafts) || saved.formDraft));
            const existingUser = saved?.auth?.person?.user_id || '';
            const incomingUser = auth?.person?.user_id || '';
            if (unsent && existingUser && existingUser !== incomingUser) {{
                fail('This browser contains unsent work for another Wavelink account. '
                     + 'Use a private/incognito window for the guest demonstration.');
                return;
            }}
            if (unsent && saved?.hub_id && saved.hub_id !== auth.hub_id) {{
                fail('This browser contains unsent work for another project. '
                     + 'Use a private/incognito window for the guest demonstration.');
                return;
            }}
            const defaults = {{
                hub_id:null, info:null, auth:null, device_id:null, template:null,
                records:[], snapshots:{{}}, queue:[], drafts:{{}}, formDraft:null
            }};
            const next = Object.assign({{}}, defaults, saved || {{}}, {{
                hub_id:auth.hub_id, auth:auth,
                device_id:auth.person.device_id || saved?.device_id || crypto.randomUUID(),
                lastLogin:auth.person.login_id || '', lastName:auth.person.name || ''
            }});
            const write = indexedDB.open('pxgeo-dive-check-1', 1);
            write.onsuccess = () => {{
                const writeDb = write.result;
                const writeTx = writeDb.transaction('state', 'readwrite');
                writeTx.objectStore('state').put(next, 'main');
                writeTx.oncomplete = () => {{ writeDb.close(); location.replace('/#home'); }};
                writeTx.onerror = () => {{
                    writeDb.close(); fail('The guest session could not be saved in this browser.');
                }};
            }};
            write.onerror = () => fail('The browser workspace could not be reopened.');
        }};
    }};
}})();
</script></body></html>'''

    async def quick(self, request: Request):
        supplied = request.query_params.get('key', '')
        if not supplied or len(supplied) > 128:
            return RedirectResponse('/__demo/login', status_code=303, headers=HEADERS)
        if not self.register_attempt():
            return JSONResponse({'error': 'Too many demo access attempts. Wait five minutes.'},
                                429, headers={**HEADERS, 'Retry-After': '300'})
        if not self.password_matches(supplied):
            response = self.form_response('The demo access password was not accepted.')
            response.status_code = 403
            return response
        try:
            auth = self.authenticate_guest()
        except RuntimeError as exc:
            return HTMLResponse('<h1>Guest demonstration unavailable</h1><p>'
                                + html.escape(str(exc)) + '</p>',
                                status_code=503, headers=BOOT_HEADERS)
        response = HTMLResponse(self.bootstrap_page(auth), headers=BOOT_HEADERS)
        response.set_cookie(COOKIE, self.token('session', TTL), max_age=TTL,
                            path='/', secure=True, httponly=True, samesite='strict')
        response.delete_cookie(CSRF_COOKIE, path='/', secure=True,
                               httponly=True, samesite='strict')
        return response

    async def login(self, request: Request):
        if request.method == 'GET':
            return self.form_response()
        form = await self.form(request)
        if not form or set(form) != {'csrf', 'password'}:
            response = self.form_response('The access page could not be verified. '
                                          'Please enter the demo password again.')
            response.status_code = 403
            return response
        if not self.register_attempt():
            return JSONResponse({'error': 'Too many demo access attempts. Wait five minutes.'},
                                429, headers={**HEADERS, 'Retry-After': '300'})
        if not self.password_matches(form['password']):
            response = self.form_response('The demo access password was not accepted.')
            response.status_code = 403
            return response
        return self.admitted_response()

    async def check(self, request: Request):
        valid = self.valid(request.cookies.get(COOKIE), 'session')
        return Response(status_code=204 if valid else 401, headers=HEADERS)

    async def required(self, request: Request):
        original = request.headers.get('x-demo-original-uri', '/')
        method = request.headers.get('x-demo-original-method', 'GET')
        accept = request.headers.get('accept', '')
        if (method == 'GET' and (original == '/' or original.startswith(('/fleet', '/admin')))
                and 'text/html' in accept):
            return RedirectResponse('/__demo/login', status_code=303, headers=HEADERS)
        return JSONResponse({'error': 'Demo access has expired. Open /__demo/login.',
                             'demo_access_required': True}, 401, headers=HEADERS)

    async def logout(self, request: Request):
        if request.method == 'GET':
            return self.form_response(logout=True)
        if not await self.form(request):
            response = self.form_response('The access page could not be verified. '
                                          'Please try again.', logout=True)
            response.status_code = 403
            return response
        response = RedirectResponse('/__demo/login', status_code=303, headers=HEADERS)
        response.delete_cookie(COOKIE, path='/', secure=True, httponly=True, samesite='strict')
        response.delete_cookie(CSRF_COOKIE, path='/', secure=True, httponly=True, samesite='strict')
        return response

    def app(self):
        return Starlette(routes=[
            Route('/__demo/quick', self.quick, methods=['GET']),
            Route('/__demo/login', self.login, methods=['GET', 'POST']),
            Route('/__demo/check', self.check),
            Route('/__demo/required', self.required,
                  methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD']),
            Route('/__demo/logout', self.logout, methods=['GET', 'POST']),
        ])


if __name__ == '__main__':
    import uvicorn
    gate = Gate(os.environ['DEMO_GATE_ORIGIN'], os.environ['DEMO_ACCESS_PASSWORD'],
                Path(os.environ['DEMO_GATE_KEY_FILE']).read_bytes(),
                os.environ['DEMO_GUEST_LOGIN'], os.environ['DEMO_GUEST_PASSWORD'])
    uvicorn.run(gate.app(), host='127.0.0.1',
                port=int(os.environ.get('DEMO_GATE_PORT', '8766')), workers=1,
                proxy_headers=False, access_log=False, server_header=False,
                log_level='warning')
