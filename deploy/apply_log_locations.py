"""Present logbooks by the current fleet site and keep the checklist stage label intact."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
PARENT = 'f8acd8d79a14dddfff3e878405b5aba7529c69dba3e04385bf34d59335efb2d3'
STATIC = 'app/static/'


def change(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected logbook release source near '+old[:90])
    return source.replace(old, new)


def register(source):
    start = source.index('<div class="log-book-grid">${books.length?books.map(b=>')
    card_start = source.index('__wl118.html`<article', start)
    card_end = source.index("`).join(''):", card_start) + 1
    single_card = source[card_start:card_end].replace('<h2>${esc(b.name)}</h2>', '<h3>${esc(b.name)}</h3>')
    empty = source.index('__wl118.html`<section class="card"><h2>No saved logbooks', card_end)
    end = source.index('}</div></section>${footer()}', empty)
    source = source[:start] + '${books.length?logSiteBrowser(books,directory):' + source[empty:end] + '}</section>${footer()}' + source[end+len('}</div></section>${footer()}'):]
    before = ' function validBook(b){'
    extra = (BASE/'logbook_locations.js').read_text('utf-8') + '\n function bookCard(b) {return '+single_card+';}\n'
    source = change(source, before, extra+before)
    source = change(source, 'if(context!==c){activeBook=null;', "if(context!==c){logSiteFilter='';activeBook=null;")
    source = change(source, 'const books=await api(base+\'/books\',{beforeSend:()=>requireRead(own)});', """const [books, directory] = await Promise.all([
    api(base+'/books',{beforeSend:()=>requireRead(own)}),
    api('/api/fleet/work-locations',{beforeSend:()=>requireRead(own)}).then(data=>data.sites||[]).catch(()=>[])
   ]);""")
    source = change(source, "   document.getElementById('logs-refresh').onclick", "   bindLogSiteFilter(books);\n   document.getElementById('logs-refresh').onclick")
    source = change(source, 'JSON.stringify([b.name,b.description,b.archived,b.definitions', 'JSON.stringify([b.name,b.description,b.vessel_scope,b.archived,b.definitions')
    source = change(source, "<p>${esc(b.description||__wl118.t('Saved operational logbook'))}</p>",
                    "${bookLocationLine(b,true)}<p>${esc(b.description||__wl118.t('Saved operational logbook'))}</p>")
    source = change(source, "  $('#log-expand').onclick=toggleExpanded;",
                    "  const assign=$('#log-assign-location');if(assign)assign.onclick=()=>assignLogbookLocation(b);\n  $('#log-expand').onclick=toggleExpanded;")
    return change(source, '<div class="log-editor-body"><p class="small"><b>${esc(b.name)}</b></p>',
                  '<div class="log-editor-body"><p class="small"><b>${esc(b.name)}</b></p>${bookLocationLine(b)}')


def design_service(source):
    source = change(source, "set(value) != {'name', 'description', 'definitions'}",
                    "(set(value)-{'work_site_id'}) != {'name', 'description', 'definitions'}")
    source = change(source, "    return dict(name=clean_text(value['name']", """    site = {}
    if 'work_site_id' in value:
        if not isinstance(value['work_site_id'], str) or len(value['work_site_id']) > 40:
            raise Problem(422, 'Choose a ship or base.')
        site['work_site_id'] = value['work_site_id']
    return dict(**site, name=clean_text(value['name']""")
    source = change(source, "            definition = design(value)\n", """            definition = design(value)
            from .work_locations import selection
            selection(con,actor,definition)
""")
    return change(source, "dict(actor, _logbook_builder=True))",
                  "dict(actor, _logbook_builder=True), work_site_id=definition.get('work_site_id'))")


def native_logs(source):
    source = change(source, 'def create(self,name,description,definitions,actor,*,book_id=None):',
                    'def create(self,name,description,definitions,actor,*,book_id=None,work_site_id=None):')
    return change(source, "            audit(con,bid,'',actor,'create_book'", """            if work_site_id is not None:
                from .vessel_logs import assign_new_location
                assign_new_location(con, actor, bid, work_site_id)
            audit(con,bid,'',actor,'create_book'""")


def new_scope(source):
    anchor = 'def _exists(c, name):'
    return change(source, anchor, '''def import_location_choice(request):
    """Preserve the original retry fingerprint for older callers that omit the site."""
    if 'work_site_id' not in request:
        return []
    site = request['work_site_id']
    if not isinstance(site,str) or len(site)>40:
        raise Problem(422,'Choose a ship or base.')
    return [site]


def assign_new_location(c, actor, book_id, site_id):
    """File the new book without enabling vessel-only access to its entries."""
    from .work_locations import selection
    site = selection(c,actor,{'work_site_id':site_id})
    if not site:
        return
    ensure(c)
    c.execute('INSERT INTO fleet_log_scope(book_id,site_id,enabled,version,updated_at,updated_by) VALUES(?,?,0,1,?,?)',
              (book_id,site['id'],utcnow(),actor['user_id']))
    _audit(c,dict(id=book_id,site_id=site['id'],site_name=site['name'],enabled=False,version=1),
           actor,'log_location_assigned','Location selected for the new logbook.',{})


'''+anchor)


def design_form(source):
    source = change(source, "el('ld-name').oninput=()=>{f.design.name=", """const location=document.createElement('div');el('ld-name').closest('label').after(location);
    f.locationPicker=WLWorkSites.picker(location,api,{value:f.design.work_site_id||'',onPick:site=>{f.design.work_site_id=site?.id||'';f.siteName=site?.name||'';}});
    el('ld-name').oninput=()=>{f.design.name=""")
    source = change(source, "el('ld-name').focus();return;}f.step=2;", """el('ld-name').focus();return;}
   try{f.design.work_site_id=f.locationPicker.read();}catch(error){el('ld-result').textContent=error.message;return;}
   f.step=2;""")
    return change(source, "+preview(f.review.design)+",
                  "+(f.siteName?'<p class=\"log-site-line\">'+E(WLWorkSites.label())+' · <strong>'+E(f.siteName)+'</strong></p>':'')+preview(f.review.design)+")


def import_service(source):
    source = change(source, "if not isinstance(request,dict) or set(request)!={'op_id','kind','file','review_token'}:",
                    "if not isinstance(request,dict) or (set(request)-({'work_site_id'} if request.get('kind')=='logbook' else set()))!={'op_id','kind','file','review_token'}:")
    source = change(source, "fingerprint=self.security.digest(['builders-import-request-v1',actor['user_id'],kind,sha,summary,op])", """from .vessel_logs import import_location_choice
        fingerprint=self.security.digest(['builders-import-request-v1',actor['user_id'],kind,sha,summary,op]+import_location_choice(request))""")
    source = change(source, "result=self._import(con,kind,parsed['data'],actor,sha,summary)",
                    "result=self._import(con,kind,parsed['data'],actor,sha,summary,work_site_id=request.get('work_site_id'))")
    source = change(source, 'def _import(self,con,kind,data,actor,sha,summary):',
                    'def _import(self,con,kind,data,actor,sha,summary,*,work_site_id=None):')
    return change(source, "d['definitions'],dict(actor,_logbook_builder=True))",
                  "d['definitions'],dict(actor,_logbook_builder=True),work_site_id=work_site_id)")


def document_service(source):
    source=change(source,"if save and isinstance(request,dict) and 'file' in request:expected.add('file')",
                  """if save and isinstance(request,dict):
            if 'file' in request:expected.add('file')
            if request.get('kind')=='logbook' and 'work_site_id' in request:expected.add('work_site_id')""")
    source=change(source,"fingerprint=self.security.digest(['document-create-v1',self.identity(actor),digest,op])",
                  """from .vessel_logs import import_location_choice
        fingerprint=self.security.digest(['document-create-v1',self.identity(actor),digest,op]+import_location_choice(request))""")
    return change(source,"else:result=self.hub._import(con,kind,data,actor,source['sha256'],summary)",
                  "else:result=self.hub._import(con,kind,data,actor,source['sha256'],summary,work_site_id=request.get('work_site_id'))")


def import_form(source):
    before=' async function submitImport(f){'
    source=change(source,before,""" function showImportLocation(f,frozen){
  let host=el('sb-log-location');
  if(f.resource!=='logbook'||!f.review){host?.remove();f.logPicker=null;return;}
  if(!host){
   host=document.createElement('fieldset');host.id='sb-log-location';host.className='log-import-site';
   el('sb-preview').after(host);
   f.logPicker=WLWorkSites.picker(host,api,{value:f.logSiteId||'',onPick:site=>{f.logSiteId=site?.id||'';}});
  }
  host.disabled=frozen;
 }
"""+before)
    source=change(source,before+"if(!ready(f)||f.busy||!f.review)return;if(f.document){",
                  before+"""if(!ready(f)||f.busy||!f.review)return;
  let location={};
  if(!f.request&&f.resource==='logbook'){try{location.work_site_id=f.logPicker.read();}catch(error){el('sb-result').textContent=error.message;return;}}
  if(f.document){""")
    source=change(source,'if(!f.request)f.request=AJDocumentImport.request(f);',
                  'if(!f.request)f.request={...AJDocumentImport.request(f),...location};')
    source=change(source,'if(!f.request)f.request={op_id:uid(),kind:f.resource,file:{name:f.preparedFile',
                  'if(!f.request)f.request={...location,op_id:uid(),kind:f.resource,file:{name:f.preparedFile')
    return change(source,"const frozen=f.busy||f.uncertain;el('sb-work')",
                  "const frozen=f.busy||f.uncertain;if(f.kind==='import')showImportLocation(f,frozen);el('sb-work')")


def styles(source):
    source=change(source,".cw-preview-phase { display: flex; align-items: center; gap: .4rem; font-size: .875rem; }", """#cw-preview-items .cw-preview-phase {
  display: inline-grid;
  grid-template-columns: max-content minmax(0,1fr);
  align-items: center;
  gap: .5rem;
  flex: 0 0 auto;
  inline-size: max-content;
  max-inline-size: 100%;
  white-space: nowrap;
  font-size: .875rem;
}""")
    source=change(source,'.cw-preview-phase select { min-height: 44px; max-width: 100%; }',
                  '#cw-preview-items .cw-preview-phase select { inline-size: auto; min-inline-size: 0; max-inline-size: 100%; min-height: 44px; margin: 0; }')
    source=change(source,'  .cw-preview-phase { flex-wrap: wrap; }\n','')
    return source+'''
.log-location-filter { display: grid; gap: .35rem; max-inline-size: 22rem; margin: 1rem 0; }
.log-site-group { margin-block: 1.25rem; }
.log-site-group > h2 { font-size: 1.125rem; }
.log-site-group > h2 small { font-weight: 400; }
.log-site-group .log-book-card > h3 { margin: 0; font-size: 1.125rem; }
.log-import-site { border: 0; padding: 0; margin-block: .5rem; }
.log-site-line { margin-block: .3rem; }
'''


def apply(root):
    receipt=root/'RELEASE_FILES.json'
    if sha256(receipt.read_bytes()).hexdigest()!=PARENT:
        raise ValueError('Unexpected runtime before logbook locations')
    manifest=json.loads(receipt.read_bytes())
    changed={}
    def edit(path,transform):
        raw=(root/path).read_bytes()
        if sha256(raw).hexdigest()!=manifest['files'][path]:
            raise ValueError('Unexpected resource: '+path)
        out=transform(raw.decode('utf-8')).encode('utf-8')
        if out!=raw: changed[path]=out
    edit('app/logs.py',native_logs)
    edit('app/vessel_logs.py',new_scope)
    edit('app/browser_logs.py',design_service)
    edit('app/builder_hub.py',import_service)
    edit('app/document_import.py',document_service)
    edit('app/log_api.py',lambda s:change(change(s,'class NewBook(Strict):','class NewBook(Strict):\n    work_site_id:str|None=Field(default=None,max_length=40)'),
        'store.logs.create(p.name,p.description,p.definitions,a)','store.logs.create(p.name,p.description,p.definitions,a,work_site_id=p.work_site_id)'))
    edit(STATIC+'logs.js',register)
    edit(STATIC+'browser_logs.js',design_form)
    edit(STATIC+'setup_builders.js',import_form)
    edit(STATIC+'ui132_visual.css',styles)
    hashes={k[len(STATIC):]:sha256(v).hexdigest()[:12] for k,v in changed.items() if k.startswith(STATIC)}
    pattern=re.compile(r'(/static/('+'|'.join(re.escape(k) for k in hashes)+r')\?v=[\d.]+-)[0-9a-f]{12}')
    def refs(s):
        return pattern.sub(lambda m:m[1]+hashes[m[2]],s)
    for path in manifest['files']:
        if path.startswith(STATIC) and path.endswith('.html'):
            edit(path,refs)
    edit(STATIC+'sw.js',lambda s:change(refs(s),'ui162-20261122-checklist-panel','ui162-20261122-log-locations'))
    variant=manifest['variant']+'-log-locations'
    info=json.loads((root/'UI_PATCH.json').read_bytes())
    info.update(patch_id=variant,parent_patch_id=manifest['variant'],parent_manifest_sha256=PARENT,
                scope='Logbook locations, grouped register and readable checklist stage selection.')
    changed['UI_PATCH.json']=(json.dumps(info,indent=2)+'\n').encode()
    for name,raw in changed.items():
        (root/name).write_bytes(raw)
        manifest['files'][name]=sha256(raw).hexdigest()
    manifest['variant']=variant
    receipt.write_bytes((json.dumps(manifest,indent=2)+'\n').encode())
    print(variant,sha256(receipt.read_bytes()).hexdigest())


if __name__=='__main__':
    apply(Path(sys.argv[1]))
