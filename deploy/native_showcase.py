"""The public visitor uses the product's real application on an isolated fictional project."""
import asyncio
from datetime import datetime, time as midnight, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
import secrets
import tempfile
import threading
import time
from uuid import NAMESPACE_URL, uuid5

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from starlette.websockets import WebSocketDisconnect

from .provision import SEED_SHA256
from .showcase_seed import populate

PREFIX = 'wlshow.'
READ_ONLY = 'This public demo is read-only. You can explore the form and its fictional records.'
MODULES = frozenset(('action-centre admin approval-directory approvals assets attention builders calendar certificates '
                     'context-documents deleted-records email-alerts faults fleet handovers home hr info inventory it '
                     'logs maintenance me memberships original-documents presence qshe recognition records search '
                     'tasks template templates toolbox verification').split())


def reply(data, status=200):
    return JSONResponse(data, status_code=status, headers={'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff'})


class NativeShowcase:
    def __init__(self, gate, archive):
        from app.project_transfer import import_project
        from app.server import create_app, load_config
        if sha256(archive.read_bytes()).hexdigest() != SEED_SHA256:
            raise ValueError('Unexpected public showcase fixture.')
        self.gate = gate
        self.temp = tempfile.TemporaryDirectory(prefix='wavelink-public-')
        project = Path(self.temp.name) / 'company'
        import_project(archive, project, 'Maré Alta Surveys')
        config = load_config(project)
        config['hub_id'] = str(uuid5(NAMESPACE_URL, gate.origin + '/__demo/native'))
        config['allow_legacy_codes'] = False
        self.core = create_app(project, prepared_config=config)
        self.hub_id = config['hub_id']
        self.manager, self.team = populate(self.core)
        from .showcase_crew import populate_crew
        populate_crew(self)
        self.lock = threading.Lock()
        self.reader = ''
        self.issued = 0.
        with self.core.state.store.connection(True) as c:
            c.execute('CREATE TABLE showcase_visit_state (visit TEXT PRIMARY KEY, expires INTEGER, day TEXT, mood TEXT, revoked INTEGER)')

    def admission(self):
        # This token has no authority in either the staff demo or a company installation.
        token = PREFIX + self.gate.token('native-visit', 8 * 3600)
        return dict(token=token, hub_id=self.hub_id, person={**self.manager, 'device_id': 'demo-'+secrets.token_hex(10)})

    async def portuguese(self, request):
        from .gate import PUBLIC_COOKIE
        from app.server import BASE
        embedded = request.url.path.endswith('/fleet')
        if (not self.gate.valid(request.cookies.get(PUBLIC_COOKIE), 'public-session') or
                not embedded and (request.query_params.get('public_demo') != '1' or not request.query_params.get('browser_workspace'))):
            return RedirectResponse('/__demo/public', status_code=303)
        page = (BASE/'static'/'pt-BR'/('fleet.html' if embedded else 'index.html')).read_text('utf-8')
        return HTMLResponse(page.replace('/static/workspace-locale.js','/__demo/native/locale-pt.js'),
            headers={'Cache-Control':'no-store', 'Content-Language':'pt-BR',
                     'Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; "
                       "img-src 'self' data: blob:; connect-src 'self'; worker-src 'self' blob:; "
                       "object-src 'none'; base-uri 'self'; frame-ancestors "+("'self'" if embedded else "'none'")})

    async def portuguese_locale(self, request):
        from app.localization import locale_bootstrap
        return Response(locale_bootstrap('pt-BR'),media_type='application/javascript',
                        headers={'Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'})

    def visit(self, token):
        if not self.gate.public_entry or not token.startswith(PREFIX) or not self.gate.valid(token[len(PREFIX):], 'native-visit'):
            return None
        visit = sha256(token.encode()).hexdigest()
        with self.core.state.store.connection() as c:
            row = c.execute('SELECT revoked FROM showcase_visit_state WHERE visit=?', (visit,)).fetchone()
        return visit if not row or not row[0] else None

    def reader_token(self):
        # Only the internal application ever sees this credential. Native APIs still perform
        # their normal account, project, source-record and attachment checks.
        with self.lock:
            if not self.reader or time.monotonic() - self.issued > 3600:
                self.reader, _ = self.core.state.accounts.issue_session(self.manager, 'fictional-read-service')
                self.issued = time.monotonic()
            return self.reader

    def visit_state(self, visit, day, *, write=False, mood=None, revoke=False):
        with self.core.state.store.connection(write) as c:
            if write:
                now = int(self.gate.clock())
                c.execute('DELETE FROM showcase_visit_state WHERE expires<?', (now,))
                c.execute('INSERT INTO showcase_visit_state VALUES(?,?,?,?,?) ON CONFLICT(visit) DO UPDATE SET '
                          'day=excluded.day,mood=excluded.mood,revoked=MAX(revoked,excluded.revoked)',
                          (visit, now+8*3600, day, mood, int(revoke)))
            row = c.execute('SELECT mood FROM showcase_visit_state WHERE visit=? AND day=? AND revoked=0',
                            (visit, day)).fetchone()
            return row[0] if row else None

    async def moods(self, req, visit):
        now = datetime.now(timezone.utc)
        day = now.date().isoformat()
        expires = datetime.combine(now.date()+timedelta(days=1), midnight.min, timezone.utc).isoformat()
        if req.method == 'POST':
            if req.headers.get('x-wavelink-mood-day') != day:
                return reply({'error':'A new day has started. Refresh the mood check-in.', 'mood_day_changed':True}, 409)
            raw = bytearray()
            async for chunk in req.stream():
                if len(chunk)+len(raw)>128:
                    return reply({'error':'Choose one of the five moods.'}, 422)
                raw.extend(chunk)
            try:
                value = json.loads(raw)
                if not isinstance(value,dict) or set(value)!={'mood'} or value['mood'] not in (None,'happy','calm','focused','tired','difficult'):
                    raise ValueError
            except (ValueError, UnicodeError):
                return reply({'error':'Choose one of the five moods.'}, 422)
            mine = await asyncio.to_thread(self.visit_state, visit, day, write=True, mood=value['mood'])
        else:
            mine = await asyncio.to_thread(self.visit_state, visit, day)
        entries = list(self.team)
        if mine:
            entries.append(dict(user_id=self.manager['user_id'], display_name=self.manager['name'], mood=mine))
        return reply(dict(day=day, expires_at=expires, mine=mine, items=entries))

    async def websocket(self, ws):
        if ws.headers.get('origin') != self.gate.origin:
            return await ws.close(code=1008)
        await ws.accept()
        try:
            first = await asyncio.wait_for(ws.receive_json(), 10)
            token = first.get('token') if isinstance(first, dict) else None
            if not isinstance(token, str) or not await asyncio.to_thread(self.visit, token):
                return await ws.close(code=1008)
            await ws.send_json({'type': 'connected'})
            while (await asyncio.wait_for(ws.receive_json(), 75)).get('type') == 'ping':
                if not await asyncio.to_thread(self.visit, token):
                    return await ws.close(code=1008)
                await ws.send_json({'type': 'pong'})
        except (WebSocketDisconnect, asyncio.TimeoutError, ValueError, AttributeError, RuntimeError):
            return

    async def __call__(self, scope, receive, send):
        req = Request(scope, receive)
        headers = req.headers
        auth = headers.getlist('authorization')
        visit = await asyncio.to_thread(self.visit, auth[0][7:]) if len(auth)==1 and auth[0].startswith('Bearer ') else None
        path = scope['path']
        method = req.method
        if not visit:
            result = reply({'error':'Open the public demo to start a visit.'}, 401)
        elif headers.get('origin') not in (None, self.gate.origin):
            result = reply({'error':'Open this action in your public demo visit.'}, 403)
        elif headers.get('x-aj-hub-id') not in (None, self.hub_id):
            result = reply({'error':'The demo workspace changed.', 'hub_changed':True, 'hub_id':self.hub_id}, 409)
        elif path=='/api/logout' and method=='POST':
            await asyncio.to_thread(self.visit_state, visit, '', write=True, revoke=True)
            result = reply({'ok':True})
        elif path=='/api/recognition/moods' and method in ('GET','POST'):
            result = await self.moods(req, visit)
        elif path=='/api/info' and method in ('GET','HEAD'):
            from app import __version__
            result = reply(dict(name='Wavelink', project_name='Maré Alta Surveys', hub_id=self.hub_id,
                                version=__version__, login_mode='accounts', defaults={}, template_id=None,
                                template_revision=None, capabilities={'fleet':True}, lan_addresses=[],
                                phone_url=self.gate.origin+'/', port=443, https=True, deployment_mode='public_showcase',
                                workspace_brand={'id':'public-demo','name':'Maré Alta Surveys · Demo'}))
        elif not (method in ('GET','HEAD') or (method=='POST' and path in (
                '/api/presence/heartbeat','/api/handovers/simple/open','/api/verification/lookup'))) or not (
                (path.startswith('/api/') and path.split('/')[2] in MODULES) or
                path in ('/api/backup/summary','/api/security/status','/api/security/sessions','/api/membership-entry/info')):
            result = reply({'error':READ_ONLY, 'demo_read_only':True}, 403)
        else:
            # Drop caller credentials and routing hints before entering the isolated app.
            passed = [(k,v) for k,v in scope['headers'] if k in (b'accept',b'accept-language',b'x-aj-hub-id',
                      b'if-none-match',b'range',b'content-type',b'content-length')]
            passed.extend([(b'host',self.gate.origin.removeprefix('https://').encode()),
                           (b'authorization',('Bearer '+await asyncio.to_thread(self.reader_token)).encode())])
            async def private(message):
                if message['type']=='http.response.start':
                    message = {**message,'headers':[(k,v) for k,v in message['headers'] if k.lower() not in (b'cache-control',b'set-cookie')]+[(b'cache-control',b'no-store')]}
                await send(message)
            from app.localization import localized_send
            from app.profile_language import ui_language
            language = ui_language(headers.get('accept-language'), 'en')
            context = {**scope.get('state', {}), 'ui_language':language, 'public_demo_read_only':True}
            return await self.core({**scope, 'root_path':'', 'headers':passed, 'scheme':'https', 'state':context},
                                   receive, localized_send(private, path=path, locale=language))
        await result(scope, receive, send)
