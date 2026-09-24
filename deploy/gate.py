"""Restricted fictional-demo gate.

NOT production SSO, MFA or tenant isolation.

A short-lived, HMAC-authenticated Secure/HttpOnly cookie admits the visitor
past the invitation gate; Wavelink STILL requires its separate named account.
Authorization headers are never consumed or replaced by this gate.

For the fictional client demo only, /__demo/quick?key=... provides a
convenience entrance using the demo password in the URL. The request is
immediately redirected after successful validation so the key does not remain
in the browser address bar.

Do not use quick links with real operational credentials.
"""

from __future__ import annotations

import base64
from collections import deque
import hashlib
import hmac
import html
import json
import os
from pathlib import Path
import secrets
import time
from urllib.parse import parse_qs

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import (
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
    Response,
)
from starlette.routing import Route


COOKIE = '__Host-wavelink-demo'
CSRF_COOKIE = '__Host-wavelink-demo-csrf'

TTL = 8 * 3600

HEADERS = {
    'Cache-Control': 'no-store',
    'Pragma': 'no-cache',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
    'Content-Security-Policy': (
        "default-src 'none'; "
        "style-src 'unsafe-inline'; "
        "form-action 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'none'"
    ),
}


class Gate:
    def __init__(
        self,
        origin: str,
        password: str,
        key: bytes,
        *,
        clock=time.time,
    ):
        if len(key) != 32 or not 20 <= len(password) <= 128:
            raise ValueError(
                'Invalid demonstration gate configuration.'
            )

        self.origin = origin.rstrip('/')
        self.key = key
        self.clock = clock

        self.password_digest = hashlib.sha256(
            password.encode()
        ).digest()

        self.epoch = hmac.new(
            key,
            b'gate-password:' + self.password_digest,
            hashlib.sha256,
        ).hexdigest()

        self.attempts = deque()

    def token(
        self,
        kind: str,
        lifetime: int,
    ) -> str:
        payload = json.dumps(
            {
                'kind': kind,
                'exp': int(self.clock()) + lifetime,
                'nonce': secrets.token_urlsafe(18),
                'epoch': self.epoch,
                'origin': self.origin,
            },
            separators=(',', ':'),
        ).encode()

        body = base64.urlsafe_b64encode(
            payload
        ).rstrip(b'=')

        signature = hmac.new(
            self.key,
            body,
            hashlib.sha256,
        ).hexdigest().encode()

        return (
            body
            + b'.'
            + signature
        ).decode()

    def valid(
        self,
        token: str | None,
        kind: str,
    ) -> bool:
        try:
            if not token or len(token) > 1500:
                return False

            body, signature = token.encode(
                'ascii'
            ).split(b'.')

            expected = hmac.new(
                self.key,
                body,
                hashlib.sha256,
            ).hexdigest().encode()

            if not hmac.compare_digest(
                signature,
                expected,
            ):
                return False

            value = json.loads(
                base64.urlsafe_b64decode(
                    body
                    + b'=' * (-len(body) % 4)
                )
            )

            now = self.clock()

            return (
                value['kind'] == kind
                and value['origin'] == self.origin
                and hmac.compare_digest(
                    value['epoch'],
                    self.epoch,
                )
                and type(value['exp']) is int
                and now < value['exp'] <= now + TTL + 1
            )

        except (
            ValueError,
            KeyError,
            TypeError,
            UnicodeError,
        ):
            return False

    @staticmethod
    def page(
        csrf: str,
        message: str = '',
        *,
        logout=False,
    ) -> HTMLResponse:
        title = (
            'Leave this demo session'
            if logout
            else 'Welcome to the Wavelink demonstration'
        )

        action = (
            'logout'
            if logout
            else 'login'
        )

        field = (
            ''
            if logout
            else (
                '<label for="password">'
                'Private demo access password'
                '</label>'
                '<input id="password" '
                'name="password" '
                'type="password" '
                'autocomplete="current-password" '
                'required maxlength="128" autofocus>'
            )
        )

        button = (
            'End access session'
            if logout
            else 'Enter demonstration'
        )

        body = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Wavelink · Private demo</title>

<style>
body {{
    margin: 0;
    background: #eef2f6;
    color: #182b40;
    font: 16px system-ui, sans-serif;
    min-height: 100vh;
    display: grid;
    place-items: center;
}}

main {{
    background: white;
    width: min(430px, calc(100vw - 48px));
    box-sizing: border-box;
    margin: 24px;
    padding: 32px;
    border: 1px solid #d7e0e8;
    border-radius: 16px;
    box-shadow: 0 12px 48px #182b4010;
}}

h1 {{
    font-size: 26px;
    margin: 18px 0;
}}

.eyebrow {{
    letter-spacing: .12em;
    font-size: 12px;
    font-weight: 750;
    color: #087b83;
}}

p {{
    line-height: 1.55;
}}

label {{
    display: block;
    margin: 24px 0 8px;
    font-weight: 650;
}}

input {{
    box-sizing: border-box;
    width: 100%;
    padding: 13px;
    border: 1px solid #899daf;
    border-radius: 8px;
    font: inherit;
}}

button {{
    width: 100%;
    padding: 14px;
    border: 0;
    border-radius: 8px;
    background: #087b83;
    color: white;
    font: inherit;
    font-weight: 700;
    margin-top: 20px;
    cursor: pointer;
}}

.notice {{
    font-size: 13px;
    color: #4c5e70;
    border-top: 1px solid #d7e0e8;
    margin-top: 24px;
    padding-top: 16px;
}}

.error {{
    color: #9d2534;
}}

a {{
    color: #087b83;
}}
</style>
</head>

<body>
<main>
    <div class="eyebrow">
        AJ OFFSHORE SOLUTIONS · WAVELINK
    </div>

    <h1>{title}</h1>

    <p>
        This private workspace contains fictional training records.
        After entry, sign in with your personal Wavelink account.
    </p>

    <p class="error" role="alert">
        {html.escape(message)}
    </p>

    <form
        method="post"
        action="/__demo/{action}"
    >
        <input
            type="hidden"
            name="csrf"
            value="{html.escape(csrf, quote=True)}"
        >

        {field}

        <button type="submit">
            {button}
        </button>
    </form>

    <p class="notice">
        Client demonstration only.
        Do not upload real operational, personal or confidential data.
        This invitation gate is not multifactor authentication.
    </p>
</main>
</body>
</html>'''

        return HTMLResponse(
            body,
            headers=HEADERS,
        )

    def request_is_same_origin(
        self,
        request: Request,
    ) -> bool:
        """
        For this fictional Render demo, rely on the signed CSRF cookie
        plus the exact matching hidden CSRF form token.

        Render terminates HTTPS before the container and may alter or
        omit browser Origin/Referer information before the internal
        gate sees the request.

        This is acceptable for the restricted fictional demo, but is
        not intended to be the final production authentication design.
        """
        return True

    async def form(
        self,
        request: Request,
    ) -> dict | None:
        if not self.request_is_same_origin(
            request
        ):
            return None

        content_type = (
            request.headers.get(
                'content-type',
                '',
            )
            .split(';')[0]
            .strip()
            .lower()
        )

        if (
            content_type
            != 'application/x-www-form-urlencoded'
        ):
            return None

        raw = b''

        async for chunk in request.stream():
            raw += chunk

            if len(raw) > 4096:
                return None

        try:
            form = parse_qs(
                raw.decode(),
                keep_blank_values=True,
                max_num_fields=4,
                strict_parsing=True,
            )

            if any(
                len(value) != 1
                for value in form.values()
            ):
                return None

            result = {
                key: value[0]
                for key, value in form.items()
            }

            cookie = request.cookies.get(
                CSRF_COOKIE,
                '',
            )

            csrf = result.get(
                'csrf',
                '',
            )

            if not self.valid(
                cookie,
                'csrf',
            ):
                return None

            if not hmac.compare_digest(
                csrf.encode(),
                cookie.encode(),
            ):
                return None

            return result

        except (
            ValueError,
            UnicodeError,
        ):
            return None

    def form_response(
        self,
        message='',
        *,
        logout=False,
    ):
        token = self.token(
            'csrf',
            600,
        )

        response = self.page(
            token,
            message,
            logout=logout,
        )

        response.set_cookie(
            CSRF_COOKIE,
            token,
            max_age=600,
            path='/',
            secure=True,
            httponly=True,
            samesite='strict',
        )

        return response

    def register_attempt(self) -> bool:
        """
        Returns True if another demo entrance attempt is permitted.
        """
        now = self.clock()

        while (
            self.attempts
            and self.attempts[0]
            < now - 300
        ):
            self.attempts.popleft()

        if len(self.attempts) >= 20:
            return False

        self.attempts.append(now)
        return True

    def password_matches(
        self,
        supplied: str,
    ) -> bool:
        try:
            candidate = hashlib.sha256(
                supplied.encode()
            ).digest()
        except UnicodeError:
            return False

        return hmac.compare_digest(
            candidate,
            self.password_digest,
        )

    def admitted_response(
        self,
    ) -> RedirectResponse:
        response = RedirectResponse(
            '/',
            status_code=303,
            headers=HEADERS,
        )

        response.set_cookie(
            COOKIE,
            self.token(
                'session',
                TTL,
            ),
            max_age=TTL,
            path='/',
            secure=True,
            httponly=True,
            samesite='strict',
        )

        response.delete_cookie(
            CSRF_COOKIE,
            path='/',
            secure=True,
            httponly=True,
            samesite='strict',
        )

        return response

    async def quick(
        self,
        request: Request,
    ):
        """
        Demo-only convenience entrance.

        Example:
        /__demo/quick?key=URL_ENCODED_DEMO_PASSWORD

        The supplied key is checked against DEMO_ACCESS_PASSWORD.
        On success, the normal demo session cookie is created and the
        browser immediately redirects to / so the key disappears from
        the address bar.

        This route is intentionally for fictional client demonstrations
        only. URLs can appear in browser history, copied messages and
        hosting/access logs.
        """

        supplied = request.query_params.get(
            'key',
            '',
        )

        if (
            not supplied
            or len(supplied) > 128
        ):
            return RedirectResponse(
                '/__demo/login',
                status_code=303,
                headers=HEADERS,
            )

        if not self.register_attempt():
            return JSONResponse(
                {
                    'error': (
                        'Too many demo access attempts. '
                        'Wait five minutes.'
                    )
                },
                429,
                headers={
                    **HEADERS,
                    'Retry-After': '300',
                },
            )

        if not self.password_matches(
            supplied
        ):
            response = self.form_response(
                'The demo access password was not accepted.'
            )

            response.status_code = 403
            return response

        return self.admitted_response()

    async def login(
        self,
        request: Request,
    ):
        if request.method == 'GET':
            return self.form_response()

        form = await self.form(
            request
        )

        if (
            not form
            or set(form)
            != {'csrf', 'password'}
        ):
            response = self.form_response(
                'The access page could not be verified. '
                'Please enter the demo password again.'
            )

            response.status_code = 403
            return response

        if not self.register_attempt():
            return JSONResponse(
                {
                    'error': (
                        'Too many demo access attempts. '
                        'Wait five minutes.'
                    )
                },
                429,
                headers={
                    **HEADERS,
                    'Retry-After': '300',
                },
            )

        if not self.password_matches(
            form['password']
        ):
            response = self.form_response(
                'The demo access password was not accepted.'
            )

            response.status_code = 403
            return response

        return self.admitted_response()

    async def check(
        self,
        request: Request,
    ):
        valid = self.valid(
            request.cookies.get(
                COOKIE
            ),
            'session',
        )

        return Response(
            status_code=(
                204
                if valid
                else 401
            ),
            headers=HEADERS,
        )

    async def required(
        self,
        request: Request,
    ):
        original = request.headers.get(
            'x-demo-original-uri',
            '/',
        )

        method = request.headers.get(
            'x-demo-original-method',
            'GET',
        )

        accept = request.headers.get(
            'accept',
            '',
        )

        if (
            method == 'GET'
            and (
                original == '/'
                or original.startswith(
                    (
                        '/fleet',
                        '/admin',
                    )
                )
            )
            and 'text/html' in accept
        ):
            return RedirectResponse(
                '/__demo/login',
                status_code=303,
                headers=HEADERS,
            )

        return JSONResponse(
            {
                'error': (
                    'Demo access has expired. '
                    'Preserve unsent work and open '
                    '/__demo/login in this browser.'
                ),
                'demo_access_required': True,
            },
            401,
            headers=HEADERS,
        )

    async def logout(
        self,
        request: Request,
    ):
        if request.method == 'GET':
            return self.form_response(
                logout=True
            )

        if not await self.form(
            request
        ):
            response = self.form_response(
                'The access page could not be verified. '
                'Please try again.',
                logout=True,
            )

            response.status_code = 403
            return response

        response = RedirectResponse(
            '/__demo/login',
            status_code=303,
            headers=HEADERS,
        )

        response.delete_cookie(
            COOKIE,
            path='/',
            secure=True,
            httponly=True,
            samesite='strict',
        )

        response.delete_cookie(
            CSRF_COOKIE,
            path='/',
            secure=True,
            httponly=True,
            samesite='strict',
        )

        return response

    def app(self):
        return Starlette(
            routes=[
                Route(
                    '/__demo/quick',
                    self.quick,
                    methods=['GET'],
                ),
                Route(
                    '/__demo/login',
                    self.login,
                    methods=[
                        'GET',
                        'POST',
                    ],
                ),
                Route(
                    '/__demo/check',
                    self.check,
                ),
                Route(
                    '/__demo/required',
                    self.required,
                    methods=[
                        'GET',
                        'POST',
                        'PUT',
                        'PATCH',
                        'DELETE',
                        'HEAD',
                    ],
                ),
                Route(
                    '/__demo/logout',
                    self.logout,
                    methods=[
                        'GET',
                        'POST',
                    ],
                ),
            ]
        )


if __name__ == '__main__':
    import uvicorn

    gate = Gate(
        os.environ[
            'DEMO_GATE_ORIGIN'
        ],
        os.environ[
            'DEMO_ACCESS_PASSWORD'
        ],
        Path(
            os.environ[
                'DEMO_GATE_KEY_FILE'
            ]
        ).read_bytes(),
    )

    uvicorn.run(
        gate.app(),
        host='127.0.0.1',
        port=int(
            os.environ.get(
                'DEMO_GATE_PORT',
                '8766',
            )
        ),
        workers=1,
        proxy_headers=False,
        access_log=False,
        server_header=False,
        log_level='warning',
    )
