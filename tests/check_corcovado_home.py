"""Run the Portuguese Home/Team browser regression in a temporary, named-account company."""
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import sys
import tempfile
from threading import Thread
from unittest.mock import patch


repo = Path(__file__).resolve().parents[1]
source = Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
sys.path[:0] = [str(source), str(source / 'tests'), str(repo), str(repo / 'tests')]
import test_company_c01 as c01
from test_hr_ui117 import HRCompany


def run(browser_script='browser_corcovado_home_mood.cjs'):
    settings = {**c01.ENV, 'COMPANY_ID':'corcovado', 'COMPANY_NAME':'Corcovado',
                'PUBLIC_URL':'https://corcovado.example.test',
                'COMPANY_INITIAL_PASSWORD':'Fictional initial company passphrase 63.'}
    with tempfile.TemporaryDirectory() as folder, patch.dict(c01.ENV, settings), \
            patch.dict(os.environ, {**settings, 'WAVELINK_DEPLOYMENT_MODE':'COMPANY'}):
        installation = c01.instance.__wrapped__(Path(folder).resolve())
        with c01.client(installation) as client:
            c01.activate(client)
            HRCompany(client, installation)

            class Bridge(BaseHTTPRequestHandler):
                def log_message(self, *args):
                    pass

                def request_company(self):
                    if self.headers.get('Upgrade', '').lower() == 'websocket':
                        return self.send_error(426)
                    names = ('Accept', 'Content-Type', 'Authorization', 'X-AJ-Hub-ID',
                             'X-Wavelink-Mood-Day', 'Range')
                    headers = {k:self.headers[k] for k in names if k in self.headers}
                    body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                    response = client.request(self.command, self.path, headers=headers, content=body)
                    self.send_response(response.status_code)
                    for k, v in response.headers.multi_items():
                        if k.lower() not in ('content-length', 'content-encoding', 'transfer-encoding', 'connection'):
                            self.send_header(k, v)
                    self.send_header('Content-Length', str(len(response.content)))
                    self.end_headers()
                    if self.command != 'HEAD':
                        try:
                            self.wfile.write(response.content)
                        except ConnectionError:
                            pass

                do_GET = do_HEAD = do_POST = request_company

            class Server(ThreadingHTTPServer):
                request_queue_size = 128

            with Server(('127.0.0.1', 0), Bridge) as server:
                thread = Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    subprocess.run(['node', str(repo/'tests'/browser_script),
                                    f'http://127.0.0.1:{server.server_port}'], check=True, timeout=180)
                finally:
                    server.shutdown()
                    thread.join()


if __name__ == '__main__':
    run()
