"""Actual local Nginx -> gate -> hosted app HTTP/WS probe, fictional data only.

Does NOT contact Render, public DNS, GitHub or external TLS services.
"""
from contextlib import closing
import asyncio
import base64
from http.cookies import SimpleCookie
import json
import os
from pathlib import Path
import re
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import uuid
import httpx
from websockets.asyncio.client import connect

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from deploy.provision import prepare
from deploy.nginx_config import render
from deploy.entrypoint import minimal_environment,wait_ready
SOURCE=Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
OUT=Path(os.environ.get('WAVELINK_TEST_OUTPUT','/tmp/wavelink-demo-probe.json'))
checks=[]
def ok(text):checks.append(text);print('PASS',text,flush=True)
def free_port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]
def cookie_value(response,name):
    values=SimpleCookie()
    for raw in response.headers.get_list('set-cookie'):values.load(raw)
    return values[name].value

def run():
    with tempfile.TemporaryDirectory(prefix='fictional-client-demo-http-') as td:
        tmp=Path(td);app_port,gate_port,edge_port=8765,free_port(),free_port()
        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1',app_port))  # Refuse to touch an occupied app port.
        origin='https://demo.example.test';authority='demo.example.test'
        env={'PUBLIC_URL':origin,'DEMO_ACCESS_PASSWORD':'Fictional-probe-gate-password-2026',
             'INITIAL_ADMIN_PASSWORD':'Fictional-probe-administrator-2026','INITIALISE_FICTIONAL_DEMO':'YES_FIRST_DEPLOY_ONLY'}
        cfg=prepare(tmp/'data',SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',env,app_port=app_port)
        processes=[];logs=[]
        def spawn(cmd,cwd,environ,name):
            out=(tmp/(name+'.log')).open('w');logs.append(out)
            p=subprocess.Popen(cmd,cwd=cwd,env=environ,stdout=out,stderr=subprocess.STDOUT);processes.append(p);return p
        application=spawn([sys.executable,'run_hosted.py','serve','--config',str(cfg['config'])],SOURCE,minimal_environment(),'app')
        try:
            wait_ready(application,app_port,'/readyz')
            gate_env={**minimal_environment(),'DEMO_GATE_ORIGIN':origin,'DEMO_ACCESS_PASSWORD':env['DEMO_ACCESS_PASSWORD'],
                      'DEMO_GATE_KEY_FILE':str(cfg['gate_key']),'DEMO_GATE_PORT':str(gate_port),
                      'DEMO_GUEST_LOGIN':'client.demo','DEMO_GUEST_PASSWORD':'Fictional-client-user-password-2026'}
            gate=spawn([sys.executable,'-m','deploy.gate'],ROOT,gate_env,'gate')
            wait_ready(gate,gate_port,'/__demo/check',accepted=(401,))
            ngx=tmp/'nginx.conf';ngx.write_text(render(authority,edge_port,tmp/'nginx',app_port=app_port,gate_port=gate_port,bind='127.0.0.1'))
            subprocess.run(['nginx','-t','-c',str(ngx)],check=True,capture_output=True)
            edge=spawn(['nginx','-c',str(ngx),'-g','daemon off;'],ROOT,minimal_environment(),'nginx')
            wait_ready(edge,edge_port,'/healthz')
            with httpx.Client(base_url=f'http://127.0.0.1:{edge_port}',timeout=20,follow_redirects=False) as c:
                headers={'Host':authority,'X-Forwarded-Proto':'https'}
                assert c.get('/healthz').status_code==200
                assert c.get('/',headers={'Host':'other.example.test','X-Forwarded-Proto':'https'}).status_code==421
                assert c.get('/',headers={'Host':authority}).status_code==400
                ok('Minimal health probe, wrong-host rejection and TLS-forwarding requirement')
                assert c.get('/api/info',headers=headers).status_code==401
                assert c.get('/static/app.js',headers=headers).status_code==401
                r=c.get('/',headers={**headers,'Accept':'text/html'})
                assert r.status_code==303 and r.headers['location']=='/__demo/login'
                ok('Unauthenticated app, static assets and API blocked; document navigation opens gate')
                r=c.get('/__demo/login',headers=headers)
                assert r.status_code==200
                csrf=re.search('name="csrf" value="([^"]+)"',r.text).group(1)
                csrf_cookie=cookie_value(r,'__Host-wavelink-demo-csrf')
                r=c.post('/__demo/login',headers={**headers,'Origin':origin,'Cookie':'__Host-wavelink-demo-csrf='+csrf_cookie},data={'csrf':csrf,'password':env['DEMO_ACCESS_PASSWORD']})
                assert r.status_code==303
                access=cookie_value(r,'__Host-wavelink-demo');cookie='__Host-wavelink-demo='+access
                h={**headers,'Cookie':cookie,'Origin':origin}
                assert c.get('/',headers=h).status_code==200
                assert c.get('/static/app.js',headers=h).status_code==200
                info=c.get('/api/info',headers=h).json()
                assert info['defaults']=={} and info['hub_id']==cfg['hub_id']
                ok('Secure gate cookie admits genuine app shell; public bootstrap stays minimal')
                login=c.post('/api/login',headers=h,json={'login_id':'adriano.admin','password':env['INITIAL_ADMIN_PASSWORD'],'device_id':'fictional-client-browser'})
                assert login.status_code==200,login.text
                token=login.json()['token']
                auth={**h,'Authorization':'Bearer '+token,'X-AJ-Hub-ID':cfg['hub_id']}
                assert c.get('/api/me',headers=auth).json()['role']=='admin'
                assert c.get('/api/me',headers={**auth,'X-Forwarded-Host':'evil.example','X-Forwarded-Unknown':'injected','X-Real-IP':'1.2.3.4'}).status_code==200
                assert c.get('/api/me',headers=h).status_code in (401,403)
                assert c.get('/api/me',headers={**auth,'Origin':'https://evil.example'}).status_code==403
                assert c.get('/api/me',headers={k:v for k,v in auth.items() if k!='Cookie'}).status_code==401
                ok('Named Wavelink login survives gate; bearer auth, gate and same-origin checks remain separate')
                directory=c.get('/api/admin/directory',headers=auth)
                assert directory.status_code==200,directory.text
                user_payload={'op_id':str(uuid.uuid4()),'action':'create_user','payload':{'login_id':'client.demo','name':'Fictional Client Tester','password':'Fictional-client-user-password-2026','role':'technician'},'reason':'Fictional demonstration only','confirmed':True}
                created=c.post('/api/admin/action',headers=auth,json=user_payload)
                assert created.status_code==200,created.text
                repeated=c.post('/api/admin/action',headers=auth,json=user_payload)
                assert repeated.json()==created.json()
                department=c.post('/api/admin/action',headers=auth,json={'op_id':str(uuid.uuid4()),'action':'create_department','payload':{'name':'Fictional Client Review','description':'Training-only department'},'reason':'Browser demonstration','confirmed':True})
                assert department.status_code==200,department.text
                ok('Browser administration API creates one user idempotently and a department through actual gateway')
                limited=c.post('/api/login',headers=h,json={'login_id':'client.demo','password':'Fictional-client-user-password-2026','device_id':'fictional-client-limited'}).json()['token']
                assert c.get('/api/admin/directory',headers={**h,'Authorization':'Bearer '+limited,'X-AJ-Hub-ID':cfg['hub_id']}).status_code==403
                assert c.get('/api/admin/directory',headers={**auth,'X-AJ-Hub-ID':str(uuid.uuid4())}).status_code==409
                ok('Limited account and incorrect hub identity denied administration')
                # Use a fresh cookie-free visitor to exercise the complete quick route.
                quick=c.get('/__demo/quick',params={'key':env['DEMO_ACCESS_PASSWORD']},headers=headers)
                assert quick.status_code==200,quick.text[:200]
                assert 'Opening Wavelink' in quick.text and env['DEMO_ACCESS_PASSWORD'] not in quick.text
                assert 'Fictional-client-user-password-2026' not in quick.text
                guest_auth=json.loads(re.search(r'const auth = (.+);',quick.text).group(1))
                assert guest_auth['person']['role']!='admin'
                guest_cookie='__Host-wavelink-demo='+cookie_value(quick,'__Host-wavelink-demo')
                gh={**headers,'Cookie':guest_cookie,'Origin':origin,'Authorization':'Bearer '+guest_auth['token'],'X-AJ-Hub-ID':cfg['hub_id']}
                assert c.get('/api/me',headers=gh).status_code==200
                assert c.get('/api/admin/directory',headers=gh).status_code==403
                assert c.get('/static/fieldwork.js',headers=gh).status_code==200
                ok('Guest quick link authenticates configured non-admin and returns browser bootstrap; guest admin access denied')

                async def ws_probe():
                    async with connect('ws://'+authority+'/ws',host='127.0.0.1',port=edge_port,origin=origin,
                                       additional_headers={'Cookie':cookie,'X-Forwarded-Proto':'https'},proxy=None) as ws:
                        await ws.send(json.dumps({'token':token}))
                        assert json.loads(await ws.recv())['type']=='connected'
                        await ws.send(json.dumps({'type':'ping'}))
                        assert json.loads(await ws.recv())['type']=='pong'
                asyncio.run(ws_probe())
                ok('Real WebSocket upgrade, named session and ping/pong pass through gateway')
                for path in ['/api/original-documents','/api/templates','/api/records']:
                    assert c.get(path,headers=auth).status_code==200,path
                original=c.get('/api/original-documents',headers=auth).json()
                rows=original if isinstance(original,list) else original.get('items',original.get('documents',[]))
                if rows:
                    row=rows[0]
                    file=c.get('/api/original-documents/'+row['id']+'/file',headers=auth)
                    assert file.status_code==200 and file.content
                    assert c.get('/api/original-documents/'+row['id']+'/file',headers={k:v for k,v in auth.items() if k!='Cookie'}).status_code==401
                ok('Fictional record/template reads and original-file route retain access gate')
                db=tmp/'data/project/dives.sqlite3'
                with closing(sqlite3.connect(db)) as con:
                    before={t:con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in ('users','inventory_items','original_documents','fleet_manifests')}
                # Clean application restart (the same initialized volume), no desktop Admin.
                application.terminate();application.wait(timeout=35)
                prepare(tmp/'data',SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',{**env,'INITIALISE_FICTIONAL_DEMO':'NO'},app_port=app_port)
                application=spawn([sys.executable,'run_hosted.py','serve','--config',str(cfg['config'])],SOURCE,minimal_environment(),'app_restart')
                wait_ready(application,app_port,'/readyz')
                with closing(sqlite3.connect(db)) as con:
                    after={t:con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0] for t in before}
                assert before==after
                assert c.get('/api/me',headers=auth).status_code==200
                ok('Application restart retains hub identity, users, inventory, manifests, original files and saved session')
                assert c.post('/api/logout',headers=auth).status_code==200
                assert c.get('/api/me',headers=auth).status_code in (401,403)
                ok('Wavelink logout revokes the app session behind the independent gate')
        finally:
            for p in reversed(processes):
                if p.poll() is None:p.terminate()
            for p in reversed(processes):
                try:p.wait(timeout=35)
                except subprocess.TimeoutExpired:p.kill();p.wait(timeout=5)
            for f in logs:f.close()
            # Log only diagnostics on failure; application has access logging disabled.
            if sys.exc_info()[0]:
                for file in tmp.glob('*.log'):
                    print('PROCESS DIAGNOSTIC',file.name,file.read_text()[-4000:])
    return {'checks':checks,'passed':True,'real_local_http':True,'real_local_websocket':True,
            'render_tested':False,'tls_tested':False,'docker_image_built':False,
            'public_dns_tested':False,'browser_ui_tested':False,'off_host_restore_tested':False}

if __name__=='__main__':
    try:
        result=run()
        OUT.write_text(json.dumps(result,indent=2)+'\n')
    except Exception:
        OUT.write_text(json.dumps({'checks':checks,'passed':False},indent=2)+'\n')
        raise
