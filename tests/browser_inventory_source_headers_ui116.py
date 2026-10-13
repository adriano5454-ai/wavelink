"""UI116 source-header advice in a disposable fictional native C01 company.

Literal fictional XLSX, real Chromium/IndexedDB and HostedBoundary/core APIs.
No production or user workbook data. WebSockets/service workers are suppressed.
"""
import copy
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path(os.environ['WAVELINK_TEST_SOURCE']).resolve()
sys.path[:0]=[str(SOURCE),str(ROOT),str(ROOT/'tests')]
from test_company_c01 import PASS,activate,client,instance
from browser_import_row_selection_ui105 import selection_workbook

OUT=Path(os.environ.get('WAVELINK_UI116_HEADERS_EVIDENCE_DIR',str(ROOT.parent/'evidence-ui116/browser-headers')))
TRACKED=('app/document_import.py','app/document_extract.py','app/inventory.py','app/static/document_import.js','app/static/document_import.css','app/static/setup_builders.js','app/static/index.html','app/static/sw.js')
SHEET='Fictional mixed tables'
BASE=['Record reference','Name','Asset','SN','Model','Type','Subtype','Quantity','Unit','Location','Notes','Is box','Parent box reference','PN','Extra detail']
CANDIDATE_INDICES=[0,2,3,4,5,6,9,10,11,12,13,251,4999]


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    chrome=Path(os.environ['WAVELINK_CHROMIUM_EXECUTABLE']).resolve()
    report=dict(checks=[],errors=[],widths=[1440,1024,390,320],screenshots=[],source_hashes={n:sha(SOURCE/n) for n in TRACKED},served_asset_hashes={},harness_sha256=sha(Path(__file__)),chromium_executable_sha256=sha(chrome),limitations=['WebSockets and service-worker registration suppressed.','No production, Render, Windows desktop or user workbook acceptance in this fictional harness.','Missing-coordinate, invalid applied record and ownership cases are controlled sidecar/session fixtures. Exact source indices4999/5000 use a controlled fictional source-sidecar boundary because the unchanged native extractor permits only5000source lines including worksheet headings; native XLSX has4997rows.','Busy/uncertain retry is a genuine temporary-company save whose response is held then lost. Repeated headers retain invalid Is-box source text in mappedTSV; existing item choices explicitly exclude those nonphysical rows before signedCheck/save, never the header advisory.'])

    def ok(name):
        report['checks'].append(name)
        (OUT/'PROGRESS.json').write_text(json.dumps(report,indent=2)+'\n')

    def variants():
        wording=BASE.copy();wording[1]='Equipment name';wording[3]='Serial number';wording[13]='Part No.';wording[10]='Remarks'
        moved=BASE.copy();moved[3],moved[13]=moved[13],moved[3]
        missing=BASE.copy();missing[13]='Unrecognized field'
        duplicate=BASE+['Serial']
        return {0:BASE,2:BASE,3:wording,4:moved,5:missing,6:duplicate,9:BASE,10:wording,11:moved,12:missing,13:duplicate,251:BASE,4999:moved,5000:BASE}

    with tempfile.TemporaryDirectory(prefix='fictional-ui116-source-headers-') as td:
        td=Path(td)
        fixtures=[]
        for suffix in ('READ','RETRY'):
            rows=[['Fictional note '+str(i)] for i in range(4997)]
            for index,row in variants().items():
                if index<4995:rows[index]=row
            rows[4995]=variants()[4999]
            rows[1]=['REF-001','Fictional component '+suffix,'ASSET-001-'+suffix,'0007','MODEL-001','Sensor','Optical',1,'pcs','Fictional bench','Full fictional note\nSecond line remains intact','no','','000-PN-001','Fictional unmapped wording & <unsafe> '+('retained detail '*20)]
            rows[7]=['Record reference','Serial','Part number']
            rows[8]=['Record reference','Name']
            rows[4996]=['REF-002','Fictional later component '+suffix,'ASSET-002-'+suffix,'0008','MODEL-002','Sensor','Optical',2,'pcs','Fictional locker','Another intact note','no','','000-PN-002','Later unmapped wording']
            path=td/('Fictional_UI116_'+suffix+'.xlsx')
            selection_workbook(path,[(SHEET,[(5+4*i,row) for i,row in enumerate(rows)])])
            fixtures.append(path)
        report['fictional_fixture_hashes']={p.name:sha(p) for p in fixtures}
        installation=instance.__wrapped__(td)
        with client(installation) as c,sync_playwright() as pw:
            activate(c)
            origin=installation[2].external_origin
            store=c.app.state.core.state.store
            browser=pw.chromium.launch(headless=True,args=['--no-sandbox','--no-zygote','--single-process'],executable_path=str(chrome))
            p=browser.new_page(viewport={'width':1440,'height':1000})
            p.set_default_timeout(30000)
            p.on('pageerror',lambda e:report['errors'].append(str(e)))
            p.on('dialog',lambda d:d.accept())
            p.add_init_script('class ReviewSocket{constructor(){this.readyState=3;}close(){}send(){}}window.WebSocket=ReviewSocket;WebSocket.OPEN=1;if(navigator.serviceWorker)navigator.serviceWorker.register=()=>Promise.resolve();')
            exchanges,delayed=[],{'path':None,'held':None}

            def route(r):
                req,u=r.request,urlsplit(r.request.url)
                response=c.request(req.method,u.path+('?' +u.query if u.query else ''),headers=req.headers,content=req.post_data_buffer)
                name='app'+u.path
                if name in TRACKED and response.status_code==200:report['served_asset_hashes'][name]=hashlib.sha256(response.content).hexdigest()
                if u.path.startswith(('/api/builders/','/api/inventory/','/api/verification/')):exchanges.append(dict(path=u.path,status=response.status_code,request=json.loads(req.post_data or '{}'),response=response.json()))
                if delayed['path']==u.path:
                    delayed['path'],delayed['held']=None,(r,response);return
                r.fulfill(status=response.status_code,body=response.content,headers=dict(response.headers))

            p.route(origin+'/**',route)

            def latest(suffix):return next(e for e in reversed(exchanges) if e['path'].endswith(suffix))
            def calls():return len(exchanges)
            def active():return p.evaluate('()=>JSON.parse(JSON.stringify(ui116Form.document.inventory_import.sheets[0]))')
            def material():
                return p.evaluate('''()=>JSON.stringify({resource:ui116Form.resource,dirty:ui116Form.dirty,source:ui116Form.document.source,source_token:ui116Form.document.source_token,draft:ui116Form.document.draft,sheets:ui116Form.document.inventory_import.sheets.map(s=>({sheet:s.sheet,selected:s.selected,location:s.location,rows:s.rows,data:s.data,mapping:s.mapping,last_applied_mapping:s.last_applied_mapping,manual:s.manual,source_rows:s.source_rows,source_review:s.source_review,selected_rows:s.selected_rows})),summary:document.querySelector('#di-summary').innerHTML,confirmed:document.querySelector('#di-confirm').checked})''')
            def signed():return p.evaluate('()=>JSON.stringify({review:ui116Form.review,request:ui116Form.request})')
            def snapshot():
                with store.connection() as con:
                    names=[r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
                    return {name:[tuple(r) for r in con.execute('SELECT * FROM "'+name+'" ORDER BY rowid')] for name in names}
            def immutable():return material(),signed(),snapshot(),calls()
            def raw_rows():return list(csv.DictReader(io.StringIO(p.locator('#di-inventory_rows').input_value()),delimiter='\t'))
            def source(index):return p.locator('[data-di-table-header-source="'+str(index)+'"]')
            def items(index):return p.locator('[data-di-table-header-items="'+str(index)+'"]')
            def panel():return p.locator('#di-source-table-headers').inner_text()

            def open_builder(path):
                if p.locator('#sb-close').count():p.locator('#sb-close').click()
                p.evaluate('()=>{location.hash="#builders";render();}')
                p.locator('#sb-document').click()
                p.locator('#sb-file').set_input_files(str(path))
                expect(p.locator('#di-sheet')).to_be_visible(timeout=90000)
                assert latest('/document/scan')['status']==200
                p.locator('#di-source-table-headers').evaluate('n=>n.open=true')

            def include_physical_rows():
                kept={i+1 for i,row in enumerate(raw_rows()) if row['name'].startswith(('Fictional component ','Fictional later component '))}
                assert len(kept)==2
                p.locator('#di-row-picker').evaluate('n=>n.open=true')
                p.locator('#di-row-filter').select_option('all')
                for control in p.locator('[data-di-row-select]').all():
                    if int(control.get_attribute('data-di-row-select')) not in kept:control.uncheck()
                    else:control.check()
                assert active()['selected_rows']==sorted(kept)

            def check():
                p.locator('#sb-review').click()
                expect(p.locator('#di-confirm')).to_be_enabled()
                response=latest('/document/review')
                assert response['status']==200 and response['response']['summary']['inventory_review']['can_save']
                p.locator('#di-confirm').check()
                expect(p.locator('#sb-import-save')).to_be_enabled()
                return copy.deepcopy(response)

            def jump(index,kind='source'):
                before=immutable()
                (source(index) if kind=='source' else items(index)).click()
                target='#di-inspected-source-row' if kind=='source' else '#di-inspected-source-table-item'
                expect(p.locator(target)).to_be_focused()
                assert immutable()==before
                if kind=='source':assert ('Excel row '+str(5+4*index)) in p.locator(target).inner_text()

            def expand_comparison(index):
                node=p.locator('[data-di-table-header-comparison="'+str(index)+'"]')
                node.evaluate('n=>n.open=true')
                expect(node.locator('table')).to_be_visible()
                assert node.locator('tbody tr').count()==13
                return node

            def capture(index=2):source(index).evaluate('n=>{window.ui116CapturedSource=n.onclick;}')
            def invoke():p.evaluate('()=>ui116CapturedSource()')

            def layout(case):
                for width in report['widths']:
                    p.set_viewport_size({'width':width,'height':1000})
                    expand_comparison(2)
                    p.locator('#di-source-table-headers').evaluate('n=>n.scrollIntoView({block:"start"})')
                    assert p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(case,width)
                    bounds=p.locator('#di-source-table-headers button').evaluate_all('ns=>ns.map(n=>{const b=n.getBoundingClientRect();return {left:b.left,right:b.right,top:b.top,bottom:b.bottom};})')
                    assert bounds and all(b['left']>=-1 and b['right']<=width+1 for b in bounds),(case,width,bounds)
                    assert all(not(min(a['right'],b['right'])>max(a['left'],b['left'])+1 and min(a['bottom'],b['bottom'])>max(a['top'],b['top'])+1) for i,a in enumerate(bounds) for b in bounds[i+1:]),(case,width,bounds)
                    jump(2);jump(2,'items')
                    p.locator('#di-source-table-headers').evaluate('n=>n.scrollIntoView({block:"start"})')
                    filename=case+'_'+str(width)+'.png';p.screenshot(path=str(OUT/filename));report['screenshots'].append(filename)
                    ok(case+': 13-field comparisons/actions wrap at '+str(width)+'px; precise source and current-item jumps retain checked material, signed request, API count and every SQLite table')
                p.set_viewport_size({'width':1440,'height':1000})

            try:
                p.goto(origin+'/')
                p.locator('[name=login_id]').fill('admin');p.locator('[name=password]').fill(PASS)
                p.locator('#login-form button[type=submit]').click()
                expect(p.locator('#workspace-nav')).to_be_visible()
                p.evaluate('''()=>{const n=window.AJDocumentImport;window.AJDocumentImport={...n,scan(f,h){window.ui116Form=f;window.ui116Hooks=h;return n.scan(f,h);},lock(f){window.ui116Form=f;return n.lock(f);}};}''')
                open_builder(fixtures[0])
                scanned=latest('/document/scan')['response']['sheets'][0]
                assert len(scanned['rows'])==4997 and scanned['row_numbers'][4995]==19985
                original=copy.deepcopy(active())
                original_tsv=p.locator('#di-inventory_rows').input_value()
                original_rows=raw_rows()
                assert original_rows[0]['serial']=='0007' and original_rows[0]['part_number']=='000-PN-001'
                assert 'Second line remains intact' in original_rows[0]['notes'] and ('retained detail '*20).strip() in original_rows[0]['notes']
                assert source(0).count()==1 and items(0).is_disabled()
                assert source(7).count()==0 and source(8).count()==0
                assert p.locator('[data-di-table-header-source]').count()==10
                assert '5,000' in panel() and '13' in panel()
                comparison=expand_comparison(2)
                assert comparison.locator('tbody tr').nth(2).inner_text().count('SN')>=2
                moved=expand_comparison(4).locator('tbody tr').nth(2).inner_text()
                assert 'SN' in moved and 'PN' in moved
                duplicate=expand_comparison(6).locator('tbody tr').nth(2).inner_text()
                assert 'Column 4' in duplicate and 'Column 16' in duplicate
                assert any(word in duplicate.lower() for word in ('ambiguous','more than one','multiple'))
                before=immutable();p.locator('#di-table-headers-next').click()
                assert p.locator('[data-di-table-header-source]').count()==3
                assert source(251).count()==1 and source(4995).count()==1 and source(5000).count()==0
                assert immutable()==before
                jump(4995)
                p.locator('#di-table-headers-prev').click()
                native_before=immutable()
                p.evaluate('''()=>{const table=ui116Form.document.sheets[0];window.ui116NativeTableRows=table.rows;window.ui116NativeTableCoordinates=table.row_numbers;const rows=table.rows.slice(0,4995);for(let i=4995;i<4999;i++)rows.push(['Fictional boundary note '+i]);const moved=table.rows[4995].slice();rows.push(moved,table.rows[0].slice(),['Fictional boundary note 5001']);table.rows=rows;table.row_numbers=rows.map((_,i)=>5+4*i);}''')
                p.locator('#di-table-headers-next').click()
                assert source(251).count()==1 and source(4999).count()==1 and source(5000).count()==0
                assert '5000 of 5002' in p.locator('#di-source-table-header-count').inner_text()
                jump(4999)
                assert immutable()==native_before
                p.evaluate('()=>{ui116Form.document.sheets[0].rows=ui116NativeTableRows;ui116Form.document.sheets[0].row_numbers=ui116NativeTableCoordinates;}')
                p.locator('#di-table-headers-prev').click()
                assert len(p.evaluate('()=>ui116Form.document.sheets[0].rows'))==4997
                assert active()==original and p.locator('#di-inventory_rows').input_value()==original_tsv and raw_rows()==original_rows
                ok('Native4997-row fictional XLSX finds13eligible candidates, shows10perpage and includesindex251/4995; controlled fictional source-sidecar5002-row case includes4999and excludes5000, restoring native source beforeCheck/save and Name-less/single-field rows; all mapped TSV/fullNotes/leadingzero identities/provenance remain identical')

                # A real explicit shared mapping remains the recorded comparison basis.
                p.locator('[data-di-column="2"]').select_option('2')
                p.locator('#di-map').click()
                assert active()['last_applied_mapping']['columns'][2]==2
                shared=expand_comparison(2).locator('tbody tr').nth(2).locator('td').nth(0).inner_text()
                assert 'Column 3' in shared and 'Asset' in shared
                assert raw_rows()[0]['serial']=='ASSET-001-READ'
                p.locator('[data-di-column="2"]').select_option('3')
                p.locator('#di-map').click()
                assert p.locator('#di-inventory_rows').input_value()==original_tsv
                ok('Explicit shared Asset/SN source-column choice is compared at that exact recorded column across all13 fields; no automatic alias choice replaces it, and explicit remap alone restores original TSV')

                # Pending choices compare the validated applied record, not un-applied columns.
                p.locator('[data-di-column="2"]').select_option('13')
                assert active()['mapping']['dirty'] and 'pending' in panel().lower()
                assert p.locator('#di-inventory_rows').input_value()==original_tsv
                p.locator('#di-restore-mapping').click()
                assert not active()['mapping']['dirty']
                include_physical_rows()
                checked=check();summary=p.locator('#di-inventory-review').inner_text()
                before=immutable()
                p.locator('#di-table-headers-next').click();jump(251);p.locator('#di-table-headers-prev').click()
                assert immutable()==before and p.locator('#di-inventory-review').inner_text()==summary
                layout('checked_header_review')

                # Missing coordinate can still navigate a literal extracted source index.
                saved_source_rows=active()['source_rows']
                saved_coordinates=p.evaluate('()=>ui116Form.document.sheets[0].row_numbers')
                p.evaluate('()=>{delete ui116Form.document.sheets[0].row_numbers;ui116Form.document.inventory_import.sheets[0].mapping.dirty=true;ui116Hooks.lock();}')
                p.locator('#di-restore-mapping').click()
                assert items(2).is_disabled()
                before=immutable();source(2).click();assert immutable()==before
                expect(p.locator('#di-inspected-source-row')).to_be_focused()
                assert 'extracted row 3' in p.locator('#di-inspected-source-row').inner_text()
                p.evaluate('(values)=>{const duplicate=values.slice();duplicate[2]=duplicate[1];ui116Form.document.sheets[0].row_numbers=duplicate;ui116Form.document.inventory_import.sheets[0].mapping.dirty=true;ui116Hooks.lock();}',saved_coordinates)
                p.locator('#di-restore-mapping').click()
                assert items(2).is_disabled()
                before=immutable();source(2).click();assert immutable()==before
                expect(p.locator('#di-inspected-source-row')).to_be_focused()
                p.evaluate('(values)=>{ui116Form.document.sheets[0].row_numbers=values;ui116Form.document.inventory_import.sheets[0].mapping.dirty=true;ui116Hooks.lock();}',saved_coordinates)
                p.locator('#di-restore-mapping').click()
                p.evaluate('()=>{delete ui116Form.document.inventory_import.sheets[0].source_rows;ui116Form.document.inventory_import.sheets[0].mapping.dirty=true;ui116Hooks.lock();}')
                p.locator('#di-restore-mapping').click()
                assert items(2).is_disabled()
                before=immutable();source(2).click();assert immutable()==before
                expect(p.locator('#di-inspected-source-row')).to_be_focused()
                p.evaluate('(values)=>{ui116Form.document.inventory_import.sheets[0].source_rows=values;ui116Form.document.inventory_import.sheets[0].mapping.dirty=true;ui116Hooks.lock();}',saved_source_rows)
                p.locator('#di-restore-mapping').click()
                ok('Header source jumps remain available independently of mapped-item coordinates; absent or ambiguous native Excel coordinates and absent mapped references disable only current-item jump and never fabricate provenance')

                # Manual draft is compared honestly to original headers, without item links.
                p.locator('#di-inventory_rows').evaluate('n=>{let d=n.closest("details");while(d){d.open=true;d=d.parentElement?.closest("details");}}')
                p.locator('#di-inventory_rows').fill(original_tsv+'\n')
                assert active()['manual'] and 'manual' in panel().lower() and items(2).is_disabled()
                before=immutable();source(2).click();assert immutable()==before
                manual_raw=p.locator('#di-inventory_rows').input_value()
                p.locator('#di-map').click()
                assert not active()['manual'] and p.locator('#di-inventory_rows').input_value()==original_tsv
                ok('Manual mapped rows keep original-header comparison and honest warning; original-source jump is view-only while current-item jump stays disabled; explicit Apply alone restores mapped rows/provenance')

                # A missing validated record gets unavailable comparison, even with plausible pending choices.
                saved_record=active()['last_applied_mapping']
                p.evaluate('()=>{delete ui116Form.document.inventory_import.sheets[0].last_applied_mapping;}')
                p.locator('[data-di-column="2"]').select_option('13')
                assert 'unavailable' in panel().lower() and p.locator('#di-inventory_rows').input_value()==original_tsv
                p.evaluate('(record)=>{ui116Form.document.inventory_import.sheets[0].last_applied_mapping=record;ui116Hooks.lock();}',saved_record)
                p.locator('#di-restore-mapping').click()
                include_physical_rows();check();capture();before=immutable()
                p.evaluate('''()=>{const d=document.createElement('dialog');d.id='fictional-ui116-modal';d.innerHTML='<input id="fictional-ui116-modal-focus">';document.body.append(d);d.showModal();document.querySelector('#fictional-ui116-modal-focus').focus();}''')
                invoke();assert immutable()==before and p.evaluate('document.activeElement.id')=='fictional-ui116-modal-focus'
                p.evaluate('()=>{const d=document.querySelector("#fictional-ui116-modal");d.close();d.remove();}')
                before=immutable();p.evaluate('()=>{const token=state.auth.token;state.auth.token="fictional-stale";ui116CapturedSource();state.auth.token=token;}');assert immutable()==before
                ok('Missing applied record produces unavailable comparison without falling back to dirty choices; modal/session ownership keeps accepted review/confirmation and exact material unchanged')

                # Genuine save/lost response/unchanged retry, after view-only source/item browsing.
                open_builder(fixtures[1])
                detached_before=immutable();invoke();assert immutable()==detached_before
                include_physical_rows();reviewed=check();jump(2);jump(2,'items');capture()
                before_items=len(snapshot()['inventory_items'])
                delayed['path'],delayed['held']='/api/builders/document/action',None
                p.locator('#sb-import-save').click()
                for _ in range(300):
                    if delayed['held'] is not None:break
                    p.wait_for_timeout(100)
                assert delayed['held'] is not None
                assert p.locator('[data-di-table-header-source],[data-di-table-header-items]').evaluate_all('ns=>ns.every(n=>n.disabled)')
                request=copy.deepcopy(latest('/document/action')['request'])
                busy_before=immutable();invoke();assert immutable()==busy_before
                saved_items=len(snapshot()['inventory_items']);assert saved_items==before_items+2
                held_route,_=delayed['held'];held_route.abort('failed')
                expect(p.locator('#sb-import-save')).to_have_text('Retry unchanged request')
                assert p.locator('[data-di-table-header-source],[data-di-table-header-items]').evaluate_all('ns=>ns.every(n=>n.disabled)')
                uncertain_before=immutable();invoke();assert immutable()==uncertain_before
                before_reviews=sum(e['path'].endswith('/document/review') for e in exchanges)
                p.locator('#sb-import-save').click();expect(p.locator('#sb-success')).to_be_visible()
                retried=latest('/document/action')
                assert retried['request']==request and request['draft']==reviewed['request']['draft'] and request['review_token']==reviewed['response']['review_token']
                assert len(snapshot()['inventory_items'])==saved_items and sum(e['path'].endswith('/document/review') for e in exchanges)==before_reviews
                report['retry']=dict(exact_request_match=True,imported_items=2,operation_id=request['op_id'],receipt_id=retried['response']['id'])
                ok('Detached controls, busy and uncertain state cannot browse or alter a frozen signed request; genuine retry reuses identical draft/token/op_id, adds fictional items exactly once and requires no new review')

                p.wait_for_load_state('networkidle')
                assert not report['errors'],report['errors']
                assert all(v==report['source_hashes'][n] for n,v in report['served_asset_hashes'].items())
                assert all(sha(SOURCE/n)==v for n,v in report['source_hashes'].items())
                assert sha(Path(__file__))==report['harness_sha256'] and sha(chrome)==report['chromium_executable_sha256']
                assert all(sha(path)==report['fictional_fixture_hashes'][path.name] for path in fixtures)
                report['passed']=True
            except Exception:
                report['passed']=False;p.screenshot(path=str(OUT/'FAILURE.png'))
                print(json.dumps(dict(status=p.locator('#sb-result').inner_text() if p.locator('#sb-result').count() else '',recent_api=[dict(path=e['path'],status=e['status']) for e in exchanges[-4:]])))
                raise
            finally:
                report['summary']=dict(checks_passed=len(report['checks']),unexpected_errors=len(report['errors']))
                (OUT/'UI116_SOURCE_HEADERS_BROWSER_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n');browser.close()
    print(json.dumps(report['summary']))


if __name__=='__main__':main()
