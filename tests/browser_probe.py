"""Local TLS terminator + genuine gateway + real Chromium application.
No external sites are contacted. Self-signed LOCAL certificate is not a Render test.
"""
import datetime
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from deploy.provision import prepare
from deploy.entrypoint import minimal_environment,wait_ready
from deploy.nginx_config import render
SOURCE=Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
OUT=Path(os.environ.get('WAVELINK_BROWSER_OUTPUT','/tmp/wavelink-browser-probe'));OUT.mkdir(parents=True,exist_ok=True)
checks=[]
def ok(text):checks.append(text);print('PASS',text,flush=True)
def port():
    with socket.socket() as s:s.bind(('127.0.0.1',0));return s.getsockname()[1]

def run():
    with tempfile.TemporaryDirectory(prefix='fictional-wavelink-tls-') as td:
        tmp=Path(td);ap,gp,ep,tp=port(),port(),port(),port()
        authority=f'demo.wavelink.test:{tp}';origin='https://'+authority
        env={'PUBLIC_URL':origin,'DEMO_ACCESS_PASSWORD':'Fictional-browser-gate-password-2026',
             'INITIAL_ADMIN_PASSWORD':'Fictional-browser-admin-password-2026','INITIALISE_FICTIONAL_DEMO':'YES_FIRST_DEPLOY_ONLY'}
        cfg=prepare(tmp/'data',SOURCE,ROOT/'vendor/FICTIONAL_DEMO.ajproject',env,app_port=ap)
        processes=[];streams=[]
        def spawn(cmd,cwd,e,label):
            stream=(tmp/(label+'.log')).open('w');streams.append(stream)
            p=subprocess.Popen(cmd,cwd=cwd,env=e,stdout=stream,stderr=subprocess.STDOUT);processes.append(p);return p
        try:
            app=spawn([sys.executable,'run_hosted.py','serve','--config',str(cfg['config'])],SOURCE,minimal_environment(),'app')
            wait_ready(app,ap,'/readyz')
            g=spawn([sys.executable,'-m','deploy.gate'],ROOT,{**minimal_environment(),'DEMO_GATE_ORIGIN':origin,
                    'DEMO_ACCESS_PASSWORD':env['DEMO_ACCESS_PASSWORD'],'DEMO_GATE_KEY_FILE':str(cfg['gate_key']),'DEMO_GATE_PORT':str(gp),'DEMO_GUEST_LOGIN':'guest.demo','DEMO_GUEST_PASSWORD':'Fictional-browser-guest-2026'},'gate')
            wait_ready(g,gp,'/__demo/check',accepted=(401,))
            key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
            subject=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'demo.wavelink.test')])
            now=datetime.datetime.now(datetime.timezone.utc)
            cert=(x509.CertificateBuilder().subject_name(subject).issuer_name(subject).public_key(key.public_key())
                  .serial_number(x509.random_serial_number()).not_valid_before(now-datetime.timedelta(minutes=2))
                  .not_valid_after(now+datetime.timedelta(hours=2))
                  .add_extension(x509.SubjectAlternativeName([x509.DNSName('demo.wavelink.test')]),critical=False).sign(key,hashes.SHA256()))
            crt=tmp/'test.crt';kf=tmp/'test.key';crt.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
            kf.write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
            generated=render(authority,ep,tmp/'nginx',app_port=ap,gate_port=gp,bind='127.0.0.1')
            front=f'''server {{ listen 127.0.0.1:{tp} ssl; server_name demo.wavelink.test;
              ssl_certificate {crt}; ssl_certificate_key {kf};
              location / {{ proxy_pass http://127.0.0.1:{ep}; proxy_http_version 1.1;
                proxy_set_header Host $http_host; proxy_set_header X-Forwarded-Proto https;
                proxy_set_header Upgrade $http_upgrade; proxy_set_header Connection $connection_upgrade;
                proxy_read_timeout 120s; }} }}\n'''
            generated=generated.rsplit('}',1)[0]+front+'}\n';ng=tmp/'nginx.conf';ng.write_text(generated)
            subprocess.run(['nginx','-t','-c',str(ng)],check=True,capture_output=True)
            proxy=spawn(['nginx','-c',str(ng),'-g','daemon off;'],ROOT,minimal_environment(),'nginx')
            wait_ready(proxy,ep,'/healthz')
            with sync_playwright() as pw:
                browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--no-proxy-server','--host-resolver-rules=MAP demo.wavelink.test 127.0.0.1'])
                ctx=browser.new_context(ignore_https_errors=True,viewport={'width':1440,'height':1000})
                page=ctx.new_page();page.set_default_timeout(15000)
                errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(origin+'/',wait_until='domcontentloaded')
                page.locator('input[name=password]').wait_for()
                assert '/__demo/login' in page.url
                page.locator('input[name=password]').fill(env['DEMO_ACCESS_PASSWORD'])
                page.get_by_role('button',name='Enter demonstration').click()
                page.locator('#login-form').wait_for()
                assert 'PRIVATE ONLINE DEMO' in page.locator('#app').inner_text()
                ok('Actual Chromium follows HTTPS invitation gate into online-labelled account sign-in')
                page.locator('[name=login_id]').fill('adriano.admin')
                page.locator('#login-form [name=password]').fill(env['INITIAL_ADMIN_PASSWORD'])
                page.locator('#login-form button').click()
                page.locator('#home-attention').wait_for()
                ok('Named administrator opens real Home using normal application storage and HTTP, not a mocked API')
                page.locator('#nav-admin').click();page.locator('#ba-create').wait_for()
                page.locator('#ba-create').click()
                page.locator('#ba-login').fill('client.web')
                page.locator('#ba-name').fill('Fictional Client Browser')
                page.locator('#ba-password-value').fill('Fictional-client-browser-account-2026')
                page.locator('#ba-reason').fill('Fictional demonstration account')
                page.locator('#ba-confirm').check();page.locator('#ba-save').click()
                page.locator('#ba-create').wait_for()
                assert page.locator('#ba-list').get_by_text('Fictional Client Browser').count()>0
                ok('Administrator creates a new account through the actual browser form, with no desktop Admin')
                page.screenshot(path=str(OUT/'Browser_Admin_Demo.png'),full_page=True)
                page.locator('a[href="#admin/departments"]').click();page.locator('#ba-create').wait_for()
                page.locator('#ba-create').click();page.locator('#ba-name').fill('Client Demo Department')
                page.locator('#ba-description').fill('Fictional review only');page.locator('#ba-reason').fill('Browser demonstration')
                page.locator('#ba-confirm').check();page.locator('#ba-save').click();page.locator('#ba-create').wait_for()
                assert 'Client Demo Department' in page.locator('#ba-list').inner_text()
                ok('Administrator creates a department through the actual browser form')
                page.reload(wait_until='domcontentloaded');page.locator('#ba-create').wait_for()
                assert 'Client Demo Department' in page.locator('#ba-list').inner_text()
                ok('Same-origin browser reload retains saved administration and authorised workspace')
                page.set_viewport_size({'width':390,'height':844})
                page.screenshot(path=str(OUT/'Mobile_Admin_Demo.png'),full_page=True)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
                ok('Administration layout fits a 390-pixel browser viewport through the HTTPS gateway')
                assert not errors, errors
                ok('No unhandled JavaScript page errors during the exercised flows')
                ctx.close();browser.close()
        finally:
            for p in reversed(processes):
                if p.poll() is None:p.terminate()
            for p in reversed(processes):
                try:p.wait(timeout=35)
                except subprocess.TimeoutExpired:p.kill();p.wait(timeout=5)
            for f in streams:f.close()
    return {'passed':True,'checks':checks,'local_tls':True,'self_signed_test_certificate':True,
            'real_browser_form_writes':True,'render_tested':False,'public_dns_tested':False,
            'docker_image_built':False,'physical_phone_tested':False}

if __name__=='__main__':
    try:result=run()
    except Exception:
        (OUT/'browser_results.json').write_text(json.dumps({'passed':False,'checks':checks},indent=2))
        raise
    (OUT/'browser_results.json').write_text(json.dumps(result,indent=2)+'\n')
