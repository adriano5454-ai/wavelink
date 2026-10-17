"""Private Corcovado Portuguese/English UI QA over disposable native C01 APIs."""
import base64,hashlib,json,os,sys,tempfile
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright,expect

REPO=Path(__file__).resolve().parents[1]
SOURCE=Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
OUT=Path(os.environ.get('WAVELINK_UI118_HR_EVIDENCE_DIR',str(REPO.parent/'private-corcovado-pt-hr-evidence')))
os.environ['WAVELINK_TEST_SOURCE']=str(SOURCE)
sys.path[:0]=[str(SOURCE),str(SOURCE/'tests'),str(REPO),str(REPO/'tests')]
import test_company_c01 as c01
from test_hr_ui117 import HRCompany,PW,OWN,ALL,document,expense,op,pdf,png,today

@contextmanager
def company(folder,portuguese):
    env={**c01.ENV,'COMPANY_ID':'corcovado' if portuguese else 'fictional-company','COMPANY_NAME':'Corcovado' if portuguese else 'Fictional Company','PUBLIC_URL':'https://corcovado.example.test' if portuguese else 'https://english.example.test'}
    process={**env,'WAVELINK_DEPLOYMENT_MODE':'COMPANY'}
    with patch.dict(os.environ,process),patch.dict(c01.ENV,env):
        installation=c01.instance.__wrapped__(folder)
        with c01.client(installation) as client:
            c01.activate(client);h=HRCompany(client,installation)
            h.add_user('home','Home');h.grant('home',OWN)
            h.add_user('draft','Draft');h.grant('draft',OWN)
            h.add_user('travel','Travel');h.grant('travel',OWN)
            h.add_user('none','Fictional no HR');h.grant('none',set())
            h.action('save_document',document(h.uid('home'),title='Draft',reference='Travel',notes='Home'),key='home')
            h.action('save_document',document(h.uid('draft'),title='Fictional other employee private record'),key='draft')
            yield h


def main():
    OUT.mkdir(exist_ok=True)
    report={'checks':[],'errors':[],'screenshots':[],'served_hashes':{},'limitations':['All users, documents and actions are fictional disposable temporary C01 data.','Playwright HTTP routes invoke the actual ASGI app with native authentication/permissions.','WebSocket and service-worker registration suppressed; no production, live mail, device or Windows validation.']}
    def save(): (OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    def ok(name):report['checks'].append(name);save()
    with tempfile.TemporaryDirectory(prefix='fictional-corcovado-pt-hr-') as tmp,sync_playwright() as pw:
        tmp=Path(tmp)
        for portuguese in [True,False]:
            language='pt' if portuguese else 'en'
            with company(tmp/language,portuguese) as h:
                browsers=[];exchanges=[]
                def page():
                    args={'headless':True,'args':['--no-sandbox','--no-zygote','--single-process']}
                    if os.environ.get('WAVELINK_CHROMIUM_EXECUTABLE'):args['executable_path']=os.environ['WAVELINK_CHROMIUM_EXECUTABLE']
                    browser=pw.chromium.launch(**args);browsers.append(browser);report['chromium']=browser.version
                    context=browser.new_context(accept_downloads=True)
                    p=context.new_page();p.set_viewport_size({'width':1440,'height':1000});p.set_default_timeout(20000)
                    p.on('pageerror',lambda err:report['errors'].append(str(err)))
                    p.on('dialog',lambda dialog:dialog.accept())
                    p.add_init_script('class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();')
                    origin=h.installation[2].external_origin
                    def route(r):
                        request=r.request;u=urlsplit(request.url)
                        response=h.client.request(request.method,u.path+('?' +u.query if u.query else ''),headers=request.headers,content=request.post_data_buffer)
                        if u.path.startswith('/static/') and response.status_code==200:report['served_hashes'][language+u.path]=hashlib.sha256(response.content).hexdigest()
                        if u.path.startswith('/api/hr/'):
                            value=response.json() if 'application/json' in response.headers.get('content-type','') else None
                            exchanges.append({'path':u.path,'status':response.status_code,'request':json.loads(request.post_data or '{}'),'response':value})
                        r.fulfill(status=response.status_code,body=response.content,headers=dict(response.headers))
                    p.route(origin+'/**',route)
                    return p
                def login(p,key,hash='#hr/me'):
                    p.goto(h.installation[2].external_origin+'/'+hash)
                    p.locator('[name=login_id]').fill(h.users[key]['login_id']);p.locator('[name=password]').fill(PW)
                    p.locator('#login-form button[type=submit]').click()
                def tab(p,key):p.locator('[data-hr-tab="'+key+'"]').click()
                def field(p,name,value):
                    n=p.locator('#hr-form [name="'+name+'"]')
                    n.select_option(value) if n.evaluate('n=>n.tagName')=='SELECT' else n.fill(value)
                def latest(action):return next(x for x in reversed(exchanges) if x['path']=='/api/hr/action' and x['request'].get('action')==action)
                def saved(p,action):
                    p.locator('#hr-save').click();expect(p.locator('#hr-form')).to_be_hidden()
                    result=latest(action);assert result['status']==200,result
                    expect(p.locator('#hr-person')).to_be_visible();return result
                def button(p,action,kind,id):return p.locator('[data-hr-'+action+'][data-hr-kind="'+kind+'"][data-hr-id="'+id+'"]')
                def screenshot(p,label,form=False):
                    for width in [390,320]:
                        p.set_viewport_size({'width':width,'height':1000})
                        assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(label,width)
                        selector='#hr-form input,#hr-form select,#hr-form textarea,#hr-form button' if form else '#hr-workspace button,#hr-person,#hr-search'
                        bounds=p.locator(selector).evaluate_all('nodes=>nodes.filter(n=>n.getClientRects().length).map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right};})')
                        assert bounds and all(b['left']>=-1 and b['right']<=width+1 for b in bounds),(label,width,bounds)
                        target=OUT/f'{language}_{label}_{width}.png';p.screenshot(path=str(target));report['screenshots'].append(str(target))
                    p.set_viewport_size({'width':1440,'height':1000});save()
                employee=page();manager=page();denied=page()
                try:
                    login(employee,'home');expect(employee.locator('#hr-person')).to_be_visible()
                    expected='Meus registros de RH' if portuguese else 'My HR records'
                    expect(employee.locator('#hr-workspace h1')).to_have_text(expected)
                    assert employee.evaluate('window.WavelinkI18n.locale')==('pt-BR' if portuguese else 'en')
                    assert employee.locator('#hr-person option').count()==1
                    assert employee.locator('#hr-person option').inner_text() in ['Home · eu','Home · me']
                    card=employee.locator('#hr-records .hr-record').first
                    expect(card.locator('h3')).to_have_text('Draft');expect(card).to_contain_text('Travel')
                    assert 'Fictional other employee private record' not in employee.locator('body').inner_text()
                    sidebar=employee.locator('[data-workspace="hr"]')
                    expect(sidebar).to_have_text('Recursos Humanos' if portuguese else 'HR & personal records')
                    assert employee.locator('[data-hr-tab="reviews"]').count()==0
                    ok(language+': native login, fixed locale, sidebar HR, own-only directory, literal Home/Draft/Travel preserved')
                    screenshot(employee,'overview')
                    employee.evaluate('()=>{location.hash="#profile";render();}')
                    expect(employee.locator('.wl-profile-hero h1')).to_have_text('Home')
                    link=employee.locator('.wl-profile-hero a[href="#hr/me"]');expect(link).to_have_text(expected);link.click()
                    expect(employee.locator('#hr-person')).to_be_visible()
                    ok(language+': own profile preserves literal employee name and visible HR entry returns to workspace')
                    employee.locator('#hr-new-document').click();expect(employee.locator('#hr-form')).to_be_visible()
                    expect(employee.locator('#hr-form [name=type] option[value=medical]')).to_have_text('Atestado médico' if portuguese else 'Medical')
                    field(employee,'title','Draft');field(employee,'reference','Travel');field(employee,'notes','Home')
                    field(employee,'expires_on','2027-12-31');screenshot(employee,'document_form',True)
                    employee.locator('#hr-close').click()
                    employee.locator('#hr-discard-retained').click()
                    tab(employee,'timesheets');employee.locator('#hr-new-timesheet').click()
                    field(employee,'title','Draft')
                    employee.locator('#hr-form [data-hr-entry=hours]').fill('12,50' if portuguese else '12.50')
                    employee.locator('#hr-form [data-hr-entry=location]').fill('Travel')
                    employee.locator('#hr-form [data-hr-entry=notes]').fill('Home')
                    expect(employee.locator('#hr-total-hours')).to_have_text('Total registrado: 12,50 horas' if portuguese else 'Recorded total: 12.50 hours')
                    screenshot(employee,'timesheet_form',True)
                    result=saved(employee,'save_timesheet');ts=result['response']
                    assert result['request']['payload']['entries'][0]['hours']=='12.50'
                    assert result['request']['payload']['entries'][0]['activity']=='offshore'
                    assert result['request']['payload']['title']=='Draft' and result['request']['payload']['entries'][0]['location']=='Travel'
                    button(employee,'submit','timesheets',ts['id']).click();saved(employee,'submit_timesheet')
                    assert not button(employee,'review','timesheets',ts['id']).count()
                    ok(language+': timesheet comma/dot input saves exact canonical API values and cannot self-review')
                    login(manager,'hr');expect(manager.locator('#hr-person')).to_be_visible();tab(manager,'reviews')
                    button(manager,'review','timesheets',ts['id']).click();expect(manager.locator('#hr-form')).to_be_visible()
                    expect(manager.locator('#hr-form')).to_contain_text('12,50' if portuguese else '12.50')
                    expect(manager.locator('#hr-form')).to_contain_text('Embarcado' if portuguese else 'Offshore')
                    screenshot(manager,'manager_review',True)
                    field(manager,'decision','approve');field(manager,'comment','Fictional independently approved')
                    result=saved(manager,'review_timesheet');assert result['response']['status']=='approved'
                    assert result['response']['user_id']==h.uid('home')
                    employee.locator('#hr-refresh').click();expect(employee.locator('#hr-records')).to_contain_text('Aprovado' if portuguese else 'Approved')
                    ok(language+': independent authorized manager reviews actual submitted days and approves; employee sees result')
                    tab(employee,'expenses');employee.locator('#hr-new-expense').click();field(employee,'title','Draft');field(employee,'amount','19,25' if portuguese else '19.25');field(employee,'merchant','Travel');field(employee,'currency','BRL');screenshot(employee,'expense_form',True)
                    result=saved(employee,'save_expense');assert result['request']['payload']['amount']=='19.25';assert result['request']['payload']['merchant']=='Travel';assert result['request']['payload']['category']=='travel'
                    ok(language+': expense input preserves staff words and canonical amount/category/currency')
                    login(denied,'none');expect(denied.locator('main')).to_contain_text('Acesso ao RH não habilitado' if portuguese else 'HR access not enabled')
                    assert denied.locator('[data-workspace="hr"]:visible').count()==0
                    denied.evaluate('()=>{location.hash="#profile";render();}')
                    expect(denied.locator('.wl-profile-hero')).to_be_visible();assert denied.locator('.wl-profile-hero a[href="#hr/me"]').count()==0
                    response=h.client.get('/api/hr/overview',params={'user_id':h.uid('draft')},headers=h.headers('home'));assert response.status_code in [403,404]
                    before=h.snapshot();r=h.client.post('/api/hr/action',headers=h.headers('home'),json={'op_id':op(),'action':'review_timesheet','payload':{'id':ts['id'],'version':ts['version'],'decision':'approve','comment':'Fictional forbidden self review'}});assert r.status_code in [403,404,409] and h.snapshot()==before
                    ok(language+': denied account has no HR navigation/profile link and native API prevents cross-person/self-review writes')
                finally:
                    for browser in browsers:browser.close()
    assert not report['errors'],report['errors']
    report['summary']={'checks_passed':len(report['checks']),'unexpected_errors':len(report['errors'])};save();print(json.dumps(report['summary']))

if __name__=='__main__':main()
