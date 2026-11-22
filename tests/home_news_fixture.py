"""Loopback browser fixture with the public demo and a separate fictional employee project."""
import base64
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import secrets
import ssl
import sys
import tempfile
from uuid import uuid4

from starlette.testclient import TestClient

from app.feed_news_backend import publish
from app.server import create_app
from deploy.gate import Gate
from deploy.native_showcase import NativeShowcase


def seed_staff(folder, photo):
    app = create_app(folder)
    accounts, store = app.state.accounts, app.state.store
    password = 'Fictional-home-news-password'
    accounts.create('homeqa.editor', 'Fictional editor', password, 'admin')
    _, editor = accounts.login('homeqa.editor', password, 'fictional-fixture')
    crew = accounts.create('homeqa.reader', 'Fictional reader', password, 'technician', editor)
    def site(name, kind):
        return store.fleet.run('save_site', dict(name=name, kind=kind), editor, str(uuid4()))['id']
    ship, base = site('Survey North', 'vessel'), site('South Base', 'shore_base')
    store.fleet.run('set_access', dict(user_id=crew['id'], mode='project_logistics', version=0,
                       confirmed=True, grants=[dict(site_id=ship, role='viewer')], reason='Fictional crew'),
                   editor, str(uuid4()))
    for i in range(15):
        publish(store, editor, dict(op_id=str(uuid4()), title=f'Company briefing {i+1}',
                body='Company update for all crew.', site_id=None))
    publish(store, editor, dict(op_id=str(uuid4()), title='Bridge watch on Survey North', site_id=ship,
            body=('The crew reviewed the bridge watch. ' * 45) + 'Full report ends here.', image=photo))
    publish(store, editor, dict(op_id=str(uuid4()), title='South Base private bulletin', site_id=base,
            body='Only members of the south base may see this bulletin.', image=photo))
    return app


def serve(port, certificate, key):
    origin = f'https://127.0.0.1:{port}'
    repo = Path(__file__).resolve().parents[1]
    gate = Gate(origin, 'fictional-demo-password', secrets.token_bytes(32), 'guest.demo',
                'fictional-pass', public_entry=True)
    demo = NativeShowcase(gate, repo / 'vendor/FICTIONAL_DEMO.ajproject')
    gate.showcase = demo
    public = gate.app()
    with tempfile.TemporaryDirectory(prefix='wavelink-home-news-') as folder:
        picture = (repo / 'deploy/feed_news_drill.webp').read_bytes()
        staff = seed_staff(Path(folder), 'data:image/webp;base64,' + base64.b64encode(picture).decode())

        async def dispatch(scope, receive, send):
            path = scope.get('path', '')
            if path.startswith('/__demo/') or dict(scope.get('headers', [])).get(
                    b'authorization', b'').startswith(b'Bearer wlshow.'):
                return await public(scope, receive, send)
            return await staff(scope, receive, send)

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def serve_request(self):
                if self.headers.get('Upgrade', '').lower() == 'websocket':
                    self.send_error(426)
                    return
                headers = {k: v for k, v in self.headers.items() if k.lower() not in
                           ('connection', 'content-length', 'accept-encoding')}
                data = self.rfile.read(int(self.headers.get('content-length', 0)))
                response = client.request(self.command, self.path, headers=headers, content=data,
                                          follow_redirects=False)
                self.send_response(response.status_code)
                for name, value in response.headers.multi_items():
                    if name.lower() not in ('content-length', 'content-encoding', 'transfer-encoding',
                                            'connection', 'date', 'server'):
                        self.send_header(name, value)
                self.send_header('Content-Length', str(len(response.content)))
                self.end_headers()
                if self.command != 'HEAD':
                    try:
                        self.wfile.write(response.content)
                    except OSError:
                        pass

            do_GET = do_POST = do_HEAD = do_PATCH = do_PUT = do_DELETE = serve_request

        ThreadingHTTPServer.request_queue_size = 128
        try:
            with TestClient(dispatch, base_url=origin) as client, ThreadingHTTPServer(('127.0.0.1', port), Handler) as server:
                tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                tls.load_cert_chain(certificate, key)
                server.socket = tls.wrap_socket(server.socket, server_side=True)
                print(origin, flush=True)
                server.serve_forever()
        finally:
            demo.temp.cleanup()


if __name__ == '__main__':
    serve(int(sys.argv[1]), sys.argv[2], sys.argv[3])
