"""Recovery browser acceptance through the actual C01 hosted middleware."""
import json,os,re,sys,tempfile
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests'))
from test_company_c01 import instance,client,activate,login
from test_hosted_auth_ui98 import configured,NEW
OUT=Path(os.environ.get('WAVELINK_UI98_EVIDENCE_DIR','/tmp/wavelink-ui98/evidence/browser'))

def layout(p):
    box=p.evaluate("""()=>{const w=innerWidth;return {overflow:document.documentElement.scrollWidth-w,outside:[...document.querySelectorAll('input,button,h1,footer a')].filter(n=>n.offsetParent!==null).map(n=>n.getBoundingClientRect()).filter(r=>r.x<0||r.right>w+1).length}}""")
    assert box['overflow']<=1 and box['outside']==0,box

def main():
    OUT.mkdir(parents=True,exist_ok=True);report={'checks':[],'errors':[],'method':'Real HTTPS-origin Chromium routed to actual HostedBoundary/CompanyAccess/core with fictional prepared projects and captured mail. No live Nginx/Render/SMTP.'}
    def ok(name,width):report['checks'].append({'check':name,'width':width})
    with tempfile.TemporaryDirectory(prefix='fictional-ui98-browser-') as td:
      with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,args=['--no-sandbox'])
        try:
          for width in [1440,390,320]:
            i=instance.__wrapped__(Path(td)/str(width))
            with client(i) as c:
                activate(c);origin=i[2].external_origin;errors=[];p=browser.new_page(viewport={'width':width,'height':900})
                p.on('pageerror',lambda e:errors.append(str(e)))
                def route(r):
                    req=r.request;response=c.request(req.method,urlsplit(req.url).path,headers=req.headers,content=req.post_data_buffer)
                    r.fulfill(status=response.status_code,body=response.content,headers=dict(response.headers))
                p.route(origin+'/**',route)
                try:
                    p.goto(origin+'/reset-password');expect(p.locator('#recovery-content')).to_contain_text('not configured');assert p.locator('#recovery-title').inner_text()=='Reset your password';assert p.locator('#request-code').count()==0;layout(p);ok('Unauthenticated hosted bootstrap shows honest mail-configuration state',width)
                    p.screenshot(path=str(OUT/f'unconfigured_{width}.png'),full_page=True)
                    mail=configured(c.app.state.core,i[2]);p.reload();p.wait_for_selector('#request-code');assert p.locator('#recovery-status').is_hidden();layout(p);ok('Configured hosted service opens usable recovery form before sign-in',width)
                    p.screenshot(path=str(OUT/f'recovery_{width}.png'),full_page=True)
                    p.locator('#recovery-identifier').fill('admin@example.test');p.locator('#send-code').click();p.wait_for_selector('#reset-code');code=re.search(r'code is (\d{8})',mail.messages[-1][2])[1];assert len(mail.messages)==1;layout(p);ok('Hosted request reaches verified-mail code service without normal credentials',width)
                    p.screenshot(path=str(OUT/f'code_{width}.png'),full_page=True)
                    p.locator('#reset-code').fill(code);p.locator('#new-password').fill(NEW);p.locator('#confirm-password').fill(NEW);p.locator('#reset-submit').click();p.wait_for_selector('.success-mark');assert login(c,NEW);layout(p);ok('Hosted reset saves and returns to normal sign-in',width)
                    p.screenshot(path=str(OUT/f'success_{width}.png'),full_page=True)
                    assert c.get('/api/me').status_code==401;assert not errors,errors;ok('Anonymous operational access remains blocked; no JavaScript errors',width)
                finally:report['errors'].extend(errors);p.close()
        finally:browser.close()
    (OUT/'UI98_HOSTED_BROWSER_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');assert not report['errors'];print(json.dumps({'passed':len(report['checks']),'errors':report['errors']}))

if __name__=='__main__':main()
