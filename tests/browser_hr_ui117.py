"""Private UI117 HR acceptance: real Chromium and disposable fictional C01.

No production endpoints, user workbooks, live mail or persistent company data.
Screenshots/private records stay in scratch; only counts and hashes are reported.
"""
import copy
import hashlib
import io
import json
import os
import sys
import tempfile
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import expect,sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
sys.path[:0]=[str(SOURCE),str(SOURCE/'tests'),str(ROOT),str(ROOT/'tests')]
from test_hr_ui117 import PW,ALL,OWN,company_context,document,expense,op,png,pdf,today

OUT=Path(os.environ.get('WAVELINK_UI117_HR_EVIDENCE_DIR',str(ROOT.parent/'private-hr-evidence/browser')))
TRACKED=('app/hr.py','app/hr_api.py','app/access.py','app/store.py','app/server.py','app/static/hr_workspace.js','app/static/hr_workspace.css','app/static/app.js','app/static/index.html')
BOB_TITLE='Fictional Bob private medical'
ALICE_TITLE='Fictional Alice personal medical <unsafe>'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    chrome=Path(os.environ['WAVELINK_CHROMIUM_EXECUTABLE']).resolve()
    report=dict(checks=[],errors=[],screenshots=[],widths=[1440,390,320],source_hashes={n:sha(SOURCE/n) for n in TRACKED},served_asset_hashes={},harness_sha256=sha(Path(__file__)),chromium_version='',limitations=['WebSockets and service-worker registration are suppressed.','All HR people, evidence and receipts are fictional; temporary SQLite/company and screenshots are private scratch only.','Current-permission revocation without token change is a controlled fixture: native saved policy and observed browser /api/me permissions are updated together.','No live mail, payroll, tickets, Windows desktop or production acceptance.'])

    def ok(name):
        report['checks'].append(name);(OUT/'PROGRESS.json').write_text(json.dumps(report,indent=2)+'\n')

    with tempfile.TemporaryDirectory(prefix='fictional-ui117-hr-browser-') as td:
        td=Path(td);receipt=td/'Fictional_receipt.png';receipt.write_bytes(png());evidence=td/'Fictional_personal_evidence.pdf';evidence.write_bytes(pdf())
        with company_context(td) as h,sync_playwright() as pw:
            bob=h.action('save_document',document(h.uid('bob'),title=BOB_TITLE),key='bob')
            import base64
            bob=h.action('add_attachment',dict(kind='documents',id=bob['id'],version=bob['version'],filename='Fictional_Bob_evidence.png',data=base64.b64encode(png((1,2,3))).decode()),key='bob')
            h.action('save_document',document(h.uid('alice'),title='Fictional expired recorded medical',expires_on=(today()-timedelta(days=1)).isoformat()),key='alice')
            for index in range(201):h.action('save_expense',expense(h.uid('alice'),title=f'Fictional historical browser claim {index:03d}'),key='alice')
            origin=h.installation[2].external_origin
            browsers=[];contexts=[];exchanges=[];delayed={'path':None,'held':None};downloads=[]

            def page():
                browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--no-zygote','--single-process'],executable_path=str(chrome));browsers.append(browser);report['chromium_version']=browser.version
                context=browser.new_context(accept_downloads=True);contexts.append(context)
                p=context.new_page();p.set_viewport_size({'width':1440,'height':1000});p.set_default_timeout(30000)
                p.on('pageerror',lambda error:report['errors'].append(str(error)))
                p.on('dialog',lambda dialog:dialog.accept())
                p.on('download',lambda download:downloads.append(download.suggested_filename))
                p.add_init_script('class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();')
                def route(r):
                    req,u=r.request,urlsplit(r.request.url)
                    response=h.client.request(req.method,u.path+('?' +u.query if u.query else ''),headers=req.headers,content=req.post_data_buffer)
                    name='app'+u.path
                    if name in TRACKED and response.status_code==200:report['served_asset_hashes'][name]=hashlib.sha256(response.content).hexdigest()
                    if u.path.startswith('/api/hr/'):
                        value=response.json() if 'application/json' in response.headers.get('content-type','') else None
                        exchanges.append(dict(path=u.path,status=response.status_code,request=json.loads(req.post_data or '{}'),response=value))
                    if delayed['path']==u.path:
                        delayed['path'],delayed['held']=None,(r,response);return
                    r.fulfill(status=response.status_code,body=response.content,headers=dict(response.headers))
                p.route(origin+'/**',route);return p

            def latest(action=None):
                return next(e for e in reversed(exchanges) if e['path']=='/api/hr/action' and (not action or e['request'].get('action')==action))
            def snapshot():return h.snapshot()
            def actions():return len([e for e in exchanges if e['path']=='/api/hr/action'])
            def login(p,key):
                p.goto(origin+'/#hr/me');p.locator('[name=login_id]').fill(h.users[key]['login_id']);p.locator('[name=password]').fill(PW)
                p.locator('#login-form button[type=submit]').click();expect(p.locator('#hr-workspace')).to_be_visible();expect(p.locator('#hr-person')).to_be_visible()
                assert p.evaluate('workspaceReady&&!workspaceIssue&&!storageFailed')
            def navigate(p,hash):
                p.evaluate('(value)=>{location.hash=value;render();}',hash);expect(p.locator('#hr-person')).to_be_visible()
            def tab(p,value):p.locator('[data-hr-tab="'+value+'"]').click()
            def field(p,name,value):
                node=p.locator('#hr-form [name="'+name+'"]')
                if node.evaluate('n=>n.tagName')=='SELECT':node.select_option(str(value))
                else:node.fill(str(value))
            def saved(p,action):
                before=actions();p.locator('#hr-save').click();expect(p.locator('#hr-form')).to_be_hidden()
                assert actions()==before+1;result=latest(action);assert result['status']==200,result
                expect(p.locator('#hr-status')).to_be_hidden();expect(p.locator('#hr-person')).to_be_visible();return copy.deepcopy(result['response'])
            def button(p,action,kind,id):return p.locator('#hr-records [data-hr-'+action+'][data-hr-kind="'+kind+'"][data-hr-id="'+id+'"]')
            def open_form(p,action,kind,id):button(p,action,kind,id).click();expect(p.locator('#hr-form')).to_be_visible()
            def wait_held(p):
                for _ in range(300):
                    if delayed['held'] is not None:return
                    p.wait_for_timeout(100)
                raise AssertionError('Native HR response was not held within30seconds')
            def release():
                r,response=delayed['held'];delayed['held']=None;r.fulfill(status=response.status_code,body=response.content,headers=dict(response.headers))
            def form_values(p):
                return p.locator('#hr-form').evaluate('n=>JSON.stringify([...n.querySelectorAll("[name],[data-hr-entry]")].map(i=>[i.name||i.dataset.hrEntry,i.value]))')
            def layout(p,case,form=False):
                for width in report['widths']:
                    p.set_viewport_size({'width':width,'height':1000})
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(case,width)
                    selector='#hr-form input,#hr-form select,#hr-form textarea,#hr-form button' if form else '#hr-workspace button,#hr-person,#hr-search'
                    bounds=p.locator(selector).evaluate_all('ns=>ns.filter(n=>n.getClientRects().length).map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right};})')
                    assert bounds and all(b['left']>=-1 and b['right']<=width+1 for b in bounds),(case,width,bounds)
                    filename=case+'_'+str(width)+'.png';p.screenshot(path=str(OUT/filename));report['screenshots'].append(filename)
                p.set_viewport_size({'width':1440,'height':1000})
                ok(case+': actual fields/actions fit1440/390/320px without page overflow or clipping')

            employee=page();manager=page()
            try:
                login(employee,'alice')
                assert employee.locator('#hr-person option').count()==1 and BOB_TITLE not in employee.locator('body').inner_text()
                assert 'Expired' in employee.locator('#hr-workspace').inner_text()
                assert employee.locator('#hr-workspace img[onerror]').count()==0
                ok('Employee sees only own HR identity and own expiry warnings; another employee private document is absent')

                employee.locator('#hr-new-document').click();expect(employee.locator('#hr-form')).to_be_visible()
                for name,value in [('title',ALICE_TITLE),('type','medical'),('reference','000-PERSONAL-117'),('issuer','Fictional issuer'),('issued_on',(today()-timedelta(days=1)).isoformat()),('expires_on',(today()+timedelta(days=60)).isoformat()),('reminder_days','90'),('notes','Fictional supplied evidence only')]:field(employee,name,value)
                layout(employee,'employee_document_form',True)
                alice_doc=saved(employee,'save_document');assert alice_doc['user_id']==h.uid('alice')
                open_form(employee,'attach','documents',alice_doc['id']);employee.locator('#hr-form [name=file]').set_input_files(str(evidence));alice_doc=saved(employee,'add_attachment')
                button(employee,'open','documents',alice_doc['id']).click();expect(employee.locator('.hr-detail')).to_be_visible()
                before=len(downloads)
                with employee.expect_download():employee.locator('[data-hr-file]').click()
                assert len(downloads)==before+1
                employee.locator('#hr-history').click();expect(employee.locator('#hr-history-records')).to_contain_text('Saved change history')
                employee.locator('#dialog-content [data-close]').click()
                assert employee.locator('#hr-workspace img[onerror]').count()==0
                ok('Actual employee document form saves named ownership, reference/notes and privatePDF; authenticated file download/history work and unsafe title remains escaped')

                # A dirty modal blocks route changes and keeps its values; parking cannot be overwritten.
                tab(employee,'expenses');employee.locator('#hr-new-expense').click()
                field(employee,'title','Fictional retained expense');field(employee,'amount','19.25');field(employee,'merchant','Fictional retained merchant')
                pending_values=form_values(employee);before=snapshot(),actions()
                employee.evaluate('()=>{location.hash="#home";}');employee.wait_for_function('location.hash==="#hr/me"')
                expect(employee.locator('#hr-form')).to_be_visible();assert employee.evaluate('location.hash')=='#hr/me'
                assert form_values(employee)==pending_values and (snapshot(),actions())==before
                employee.locator('#hr-close').click();expect(employee.locator('#hr-resume')).to_be_visible()
                employee.locator('#hr-new-expense').click();assert not employee.locator('#hr-form').is_visible()
                employee.locator('#hr-resume').click();expect(employee.locator('#hr-form')).to_be_visible();assert form_values(employee)==pending_values
                field(employee,'description','Fictional travel expense');field(employee,'project','Fictional vessel');expense_a=saved(employee,'save_expense')
                assert expense_a['amount']=='19.25' and expense_a['user_id']==h.uid('alice')
                open_form(employee,'attach','expenses',expense_a['id']);employee.locator('#hr-form [name=file]').set_input_files(str(receipt));expense_a=saved(employee,'add_attachment')
                open_form(employee,'submit','expenses',expense_a['id']);expense_a=saved(employee,'submit_expense')
                assert expense_a['status']=='submitted' and button(employee,'edit','expenses',expense_a['id']).count()==0 and button(employee,'attach','expenses',expense_a['id']).count()==0
                ok('Dirty expense route guard keeps exact values; parking blocks newwrite until restored; actual receipt attaches and submitted claim exposes no edit/attachment controls')

                tab(employee,'timesheets');employee.locator('#hr-new-timesheet').click()
                field(employee,'title','Fictional exact hours');field(employee,'start_on','2026-10-14');field(employee,'end_on','2026-10-15')
                row=employee.locator('[data-hr-day="0"]');row.locator('[data-hr-entry=date]').fill('2026-10-14');row.locator('[data-hr-entry=hours]').fill('0.10');row.locator('[data-hr-entry=location]').fill('Fictional vessel')
                employee.locator('#hr-add-day').click();row=employee.locator('[data-hr-day="1"]');row.locator('[data-hr-entry=date]').fill('2026-10-15');row.locator('[data-hr-entry=hours]').fill('0.20');row.locator('[data-hr-entry=activity]').select_option('travel')
                assert '0.30 hours' in employee.locator('#hr-total-hours').inner_text()
                layout(employee,'employee_timesheet_form',True)
                sheet=saved(employee,'save_timesheet');assert sheet['total_hours']=='0.30'
                open_form(employee,'submit','timesheets',sheet['id']);sheet=saved(employee,'submit_timesheet')
                assert sheet['status']=='submitted' and button(employee,'edit','timesheets',sheet['id']).count()==0
                ok('Actual dated two-line timesheet computes exact0.10+0.20=0.30 hours, saves source entries and submits without automatic approval')

                login(manager,'hr');manager.locator('#hr-person').select_option(h.uid('alice'));expect(manager.locator('#hr-workspace h1')).to_contain_text('Alice')
                tab(manager,'timesheets');open_form(manager,'review','timesheets',sheet['id']);expect(manager.locator('#hr-form table')).to_contain_text('2026-10-14');expect(manager.locator('#hr-form table')).to_contain_text('0.10');expect(manager.locator('#hr-form table')).to_contain_text('0.20');layout(manager,'hr_timesheet_review_form',True);field(manager,'decision','return');field(manager,'comment','Fictional please add day context');sheet=saved(manager,'review_timesheet');assert sheet['status']=='returned'
                employee.locator('#hr-refresh').click();expect(button(employee,'edit','timesheets',sheet['id'])).to_be_visible()
                open_form(employee,'edit','timesheets',sheet['id']);field(employee,'notes','Fictional requested context added');sheet=saved(employee,'save_timesheet');open_form(employee,'submit','timesheets',sheet['id']);sheet=saved(employee,'submit_timesheet')
                manager.locator('#hr-refresh').click();open_form(manager,'review','timesheets',sheet['id']);field(manager,'decision','approve');field(manager,'comment','Fictional independent approval');sheet=saved(manager,'review_timesheet')
                assert sheet['status']=='approved' and sheet['total_hours']=='0.30'
                tab(manager,'reviews');expect(button(manager,'review','expenses',expense_a['id'])).to_be_visible();open_form(manager,'review','expenses',expense_a['id']);expect(manager.locator('#hr-form')).to_contain_text('Fictional travel expense');expect(manager.locator('[data-hr-review-file]')).to_be_visible()
                with manager.expect_download():manager.locator('[data-hr-review-file]').click()
                expect(manager.locator('#hr-save')).to_be_enabled();layout(manager,'hr_expense_review_form',True);field(manager,'comment','Fictional receipt reviewed');expense_a=saved(manager,'review_expense');assert expense_a['status']=='approved'
                ok('HR staff reviewer returns exact employee timesheet, employeecorrects/resubmits, HR independently approves; reviewqueue approves submitted expense with original receipt intact')

                tab(manager,'assignments');manager.locator('#hr-new-travel').click()
                for name,value in [('title','Fictional crew flight'),('origin','Fictional port'),('destination','Fictional offshore base'),('depart_on','2026-10-14'),('depart_time','09:30'),('time_zone','America/Bahia')]:field(manager,name,value)
                travel_a=saved(manager,'save_travel');assert travel_a['user_id']==h.uid('alice')
                manager.locator('#hr-new-shift').click()
                for name,value in [('title','Fictional crew assignment'),('location','Fictional vessel'),('start_on','2026-10-14'),('end_on','2026-10-28'),('shift_name','Day'),('start_time','06:00'),('end_time','18:00'),('time_zone','America/Bahia')]:field(manager,name,value)
                shift_a=saved(manager,'save_shift');assert shift_a['user_id']==h.uid('alice')
                layout(manager,'hr_staff_assignments')
                ok('HR staff forms create explicit time-zone travel and crew plans for selectedemployee; companyassignment alone creates no timesheet hours')

                # Staff A draft parked while staff B selected retains immutable employee identity.
                tab(manager,'documents');manager.locator('#hr-new-document').click();field(manager,'title','Fictional parked Alice document');field(manager,'expires_on',(today()+timedelta(days=20)).isoformat());manager.locator('#hr-close').click()
                manager.locator('#hr-person').select_option(h.uid('bob'));expect(manager.locator('#hr-workspace h1')).to_contain_text('Bob')
                before=snapshot(),actions();manager.locator('#hr-new-document').click();assert not manager.locator('#hr-form').is_visible()
                manager.locator('#hr-resume').click();expect(manager.locator('#hr-form .hr-form-person')).to_contain_text('Alice');field(manager,'reference','Fictional parked owner evidence');parked=saved(manager,'save_document')
                assert parked['user_id']==h.uid('alice') and (snapshot(),actions())!=before
                ok('Parked staffA document cannot be overwritten by staffB newform; restoration displaysA and save targetsimmutableA, not the current staffselector')

                # Individual right revocation with same token closes existing detail and rejects a late file response.
                manager.locator('#hr-person').select_option(h.uid('bob'));expect(manager.locator('#hr-workspace h1')).to_contain_text('Bob')
                manager.locator('#hr-new-document').click();field(manager,'title','Fictional revoked staff draft');field(manager,'expires_on',(today()+timedelta(days=20)).isoformat());revoked_values=form_values(manager);manager.locator('#hr-close').click();expect(manager.locator('#hr-resume')).to_be_visible()
                button(manager,'open','documents',bob['id']).click();expect(manager.locator('#dialog-content')).to_contain_text(BOB_TITLE)
                file_path='/api/hr/documents/'+bob['id']+'/files/'+bob['attachments'][0]['id']
                delayed['path'],delayed['held']=file_path,None;before_downloads=len(downloads);manager.locator('[data-hr-file]').click();wait_held(manager)
                token_before=manager.evaluate('state.auth.token')
                with h.store.connection(True) as con:
                    values={k:k in ALL-{'hr.documents_manage'} for k in __import__('app.access',fromlist=['KEYS']).KEYS};con.execute('UPDATE account_permissions SET permissions=? WHERE user_id=?',(json.dumps(values),h.uid('hr')))
                manager.evaluate('''async()=>{const person=await api('/api/me');state.auth.person=person;render();}''')
                assert manager.evaluate('state.auth.token')==token_before and manager.evaluate('canUse("hr.view_own")&&!canUse("hr.documents_manage")')
                expect(manager.locator('.hr-detail')).to_be_hidden();release();manager.wait_for_timeout(250)
                assert len(downloads)==before_downloads and BOB_TITLE not in manager.locator('body').inner_text()
                assert manager.locator('[data-hr-tab=documents]').count()==0
                expect(manager.locator('#hr-resume')).to_be_visible();manager.locator('#hr-resume').click();assert not manager.locator('#hr-form').is_visible()
                with h.store.connection(True) as con:con.execute('UPDATE account_permissions SET permissions=? WHERE user_id=?',(json.dumps({k:k in ALL for k in __import__('app.access',fromlist=['KEYS']).KEYS}),h.uid('hr')))
                manager.evaluate('''async()=>{const person=await api('/api/me');state.auth.person=person;render();}''');expect(manager.locator('#hr-resume')).to_be_visible();manager.locator('#hr-resume').click();expect(manager.locator('#hr-form')).to_be_visible();assert form_values(manager)==revoked_values;manager.locator('#hr-close').click()
                ok('Samehub/token document-manager revocation with ownview retained clears cachedstaff/detail immediately; held authorized-old file response cannot download or restore private content; revoked draft remains exact and can resume only after rights restore')

                # A genuine uncertain save retries the exact original body/op_id and adds only one claim.
                tab(employee,'expenses');employee.locator('#hr-refresh').click();employee.locator('#hr-new-expense').click()
                for name,value in [('title','Fictional retry claim'),('amount','0.30'),('currency','USD'),('description','Fictional unchanged retry')]:field(employee,name,value)
                before_count=len(snapshot()['hr_records']);delayed['path'],delayed['held']='/api/hr/action',None
                employee.locator('#hr-save').click();wait_held(employee);request=copy.deepcopy(latest('save_expense')['request']);busy_values=form_values(employee)
                assert employee.locator('#hr-close').is_disabled() and employee.locator('#hr-form [name=title]').is_disabled()
                employee.evaluate('()=>{location.hash="#home";}');employee.wait_for_function('location.hash==="#hr/me"');assert employee.evaluate('location.hash')=='#hr/me' and form_values(employee)==busy_values
                held_route,_=delayed['held'];delayed['held']=None;held_route.abort('failed');expect(employee.locator('#hr-save')).to_have_text('Retry unchanged request')
                assert employee.locator('#hr-form [name=title]').is_disabled();assert len(snapshot()['hr_records'])==before_count+1
                before_retry=snapshot();employee.locator('#hr-save').click();expect(employee.locator('#hr-form')).to_be_hidden()
                retried=latest('save_expense');assert retried['request']==request and snapshot()==before_retry
                report['retry']=dict(exact_request_match=True,record_added_once=True,operation_id=request['op_id'])
                ok('Native lostsave response keeps frozen fields/op_id and route guard; unchangedretry sends identical action/payload and originalreceipt without adding or editing another HRrecord')

                # Source pages make historic records outside the first100 genuinely reachable.
                expect(employee.locator('#hr-status')).to_be_hidden()
                old=h.get('records?kind=expenses&offset=200&limit=100',key='alice')['items'][0]
                before=snapshot(),actions()
                older='[data-hr-source-kind=expenses][data-hr-source-direction=older]'
                newer='[data-hr-source-kind=expenses][data-hr-source-direction=newer]'
                employee.locator(older).click();expect(employee.locator(older+'[data-hr-source-offset="200"]')).to_be_visible();assert employee.locator('.hr-record').count()==20
                employee.locator(older).click();expect(employee.locator(older)).to_be_disabled();expect(button(employee,'open','expenses',old['id'])).to_be_visible()
                assert employee.locator('.hr-record').count()<=20 and 'of 203' in employee.locator('.hr-source-pages').inner_text()
                layout(employee,'employee_historic_source_page')
                button(employee,'open','expenses',old['id']).click();expect(employee.locator('#dialog-content')).to_contain_text(old['title']);employee.locator('#dialog-content [data-close]').click()
                employee.locator(newer).click();expect(employee.locator(newer+'[data-hr-source-offset="0"]')).to_be_visible();employee.locator(newer).click();expect(employee.locator(newer)).to_be_disabled()
                assert (snapshot(),actions())==before
                delayed['path'],delayed['held']='/api/hr/records',None;employee.locator(older).click();wait_held(employee);tab(employee,'timesheets');release();employee.wait_for_timeout(250)
                expect(employee.locator('[data-hr-tab=timesheets]')).to_have_attribute('aria-pressed','true');assert old['title'] not in employee.locator('#hr-records').inner_text() and (snapshot(),actions())==before
                ok('Actual employee Older/Newer sourcepages reach203 historic claims, boundcards20, openolderrecord and preserveHRstate; delayed sourcepage aftertab change remains inert')

                employee.wait_for_load_state('networkidle');manager.wait_for_load_state('networkidle')
                assert not report['errors'],report['errors']
                assert all(sha(SOURCE/n)==value for n,value in report['source_hashes'].items())
                assert all(value==report['source_hashes'][n] for n,value in report['served_asset_hashes'].items())
                assert sha(Path(__file__))==report['harness_sha256']
                report['passed']=True
            except Exception:
                report['passed']=False;employee.screenshot(path=str(OUT/'employee_FAILURE.png'));manager.screenshot(path=str(OUT/'manager_FAILURE.png'))
                print(json.dumps(dict(recent_api=[{'path':e['path'],'status':e['status'],'action':e['request'].get('action')} for e in exchanges[-6:]],errors=report['errors'])))
                raise
            finally:
                report['summary']=dict(checks_passed=len(report['checks']),unexpected_errors=len(report['errors']));(OUT/'UI117_HR_BROWSER_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
                for context in contexts:context.close()
                for browser in browsers:browser.close()
    print(json.dumps(report['summary']))


if __name__=='__main__':main()
