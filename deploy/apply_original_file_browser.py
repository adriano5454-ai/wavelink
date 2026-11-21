"""Install the workspace file catalogue after the personal language release."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

PARENT = '2c18ad8990c03a8f212ee29950b34f5af4f983442bc6f526211002451d051b59'
HERE = Path(__file__).resolve().parent
STATIC = 'app/static/'


def once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected source for file browser: '+old[:95])
    return source.replace(old, new)


def between(source, start, end, replacement):
    if source.count(start) != 1 or source.count(end) != 1:
        raise ValueError('Unexpected file browser block: '+start)
    return source[:source.index(start)] + replacement + source[source.index(end,source.index(start)):]


def frontend(source):
    source = once(source, "const expandedFolders=new Set();", """const expandedFolders=new Set();
   const browseUi={group:'',type:'',sort:'new',page:0,selecting:false,filters:false,expanded:expandedFolders,folderOpen:window.innerWidth>800};""")
    source = once(source, "request('/api/original-documents/library')", "request('/api/original-documents/library?workspaces=true')")
    source = once(source, "copy.append(el('p','eyebrow',__wl118.t('COMPANY LIBRARY')),", "copy.append(")
    source = once(source, "__wl118.t('Controlled source revisions, folders and provenance for this company workspace.')",
                  "(__wl118.locale==='pt-BR'?'Encontre originais e anexos nas pastas das áreas onde foram salvos.':'Find originals and attachments in the workspace where they were saved.')")
    source = between(source, "const bar=el('div','of-heading');", "    const err=el('p','notice error');", "\n")
    source = between(source, '   function shown(){', '   function setHistoryView(', '')
    source = once(source,"folder=id;query='';if(detailInfo?", "browseUi.group='';browseUi.page=0;folder=id;query='';if(detailInfo?")
    source = once(source,"let detailInfo=null,viewStale=false,folderOpen=window.innerWidth>700,browseState=null;", "let detailInfo=null,viewStale=false,browseState=null;")
    source = between(source, "    const primary=el('div','of-actions');", "   async function download(doc,event)", """    window.WavelinkFileBrowser.render({shell,data,ui:browseUi,button,selected,query,archived,folderId:folder,
     setQuery:value=>{query=value;},archive:value=>{scope();archived=value;clearSelection();draw();},
     folder:changeFolder,path:parentPath,breadcrumb:folderBreadcrumb,refresh:load,manage:begin,actions:labels,
     upload:()=>startUpload(null),revise:startUpload,detail:openDetail,history:readHistory,size,
     open:download,stale:disableStale,error:showError});
    if(viewStale)showError(__wl118.t('Last saved library. Refresh before opening or changing records.'));
   }
""")
    source = once(source,'async function download(doc,event)', 'async function download(doc,event,preview=false)')
    source = once(source,'await c.download(doc,scope)', 'await c.download(doc,scope,preview)')
    source = once(source,"shell.append(hist,notice(__wl118.t('Link an exact source revision from the checklist or maintenance routine builder. Save its draft, then publish deliberately. Original files, certificate attachments and handover files remain separate.')));","shell.append(hist);")
    return (HERE/'original_file_browser.js').read_text('utf-8')+'\n'+source


def client(source):
    source = once(source,'async function downloadOriginal(ref,scope=null){','async function downloadOriginal(ref,scope=null,preview=false){')
    source = once(source,'    const file=await api(\x60/api/original-documents/\x24{encodeURIComponent(ref.id)}/file\x60',
                  """    const inline=preview&&['application/pdf','image/jpeg','image/png','image/webp'].includes(ref.mime);
    const viewer=inline?window.open('about:blank','_blank'):null;
    if(viewer){viewer.opener=null;viewer.document.title=ref.filename;viewer.document.body.textContent=__wl118.locale==='pt-BR'?'Abrindo arquivo…':'Opening file…';}
    try{
    const file=await api(ref.workspace?ref.url:'/api/original-documents/'+encodeURIComponent(ref.id)+'/file'""")
    source = once(source, "    downloadBlob(file,ref.filename);toast(__wl118.t('Original saved/opened using your device’s download options.'));",
                  """    if(viewer&&!viewer.closed){const url=URL.createObjectURL(new Blob([file],{type:ref.mime}));viewer.location.replace(url);setTimeout(()=>URL.revokeObjectURL(url),120000);}
    else {downloadBlob(file,ref.filename);toast(__wl118.t('Original saved/opened using your device’s download options.'));}
    }catch(error){if(viewer&&!viewer.closed)viewer.close();throw error;}""")
    return once(source,'download:(ref,guard)=>downloadOriginal(ref,guard)','download:downloadOriginal')


def document_import(source):
    source = once(source,'class DocumentImport:', 'from .library_import_sources import PendingScans, retain\n\nclass DocumentImport:')
    source = once(source,'self.security=self.hub.security','self.security=self.hub.security;self.scanned_sources=PendingScans()')
    source = once(source,'        return dict(kind=kind,suggested_kind=guessed,source=source,',
                  "        self.scanned_sources.remember((actor['user_id'],source['sha256']),raw)\n        return dict(kind=kind,suggested_kind=guessed,source=source,")
    source = once(source,"        if not isinstance(request,dict) or set(request)!=expected:raise Problem(422,'Review the current document draft.')",
                  """        if save and isinstance(request,dict) and 'file' in request:expected.add('file')
        if not isinstance(request,dict) or set(request)!=expected:raise Problem(422,'Review the current document draft.')""")
    return once(source, "            if kind=='inventory':response.update(destination=target['mode'],imported_items=len(data['items']))", """            if 'file' in request:
                name,_,raw=source_file(request['file'])
                if name!=source['filename'] or len(raw)!=source['bytes']:raise Problem(409,'The file no longer matches the reviewed source. Choose the original again.')
            else:
                raw=self.scanned_sources.read((actor['user_id'],source['sha256']))
            retain(con,op,kind,result,source['filename'],raw,source['sha256'])
            response['source_folder']=kind
            if kind=='inventory':response.update(destination=target['mode'],imported_items=len(data['items']))""")


def builders(source):
    return once(source,"            response=dict(saved=True,kind=kind,id=result['id'],title=result['title'],action='import',sha256=sha)",
                """            from .library_import_sources import retain
            # A locally stripped log package contains only the reviewed design.
            stored_name = name if not summary.get('original_filename') else Path(name).stem+'-definitions.ajlogs'
            retain(con,op,kind,result,stored_name,raw,sha)
            response=dict(saved=True,kind=kind,id=result['id'],title=result['title'],action='import',sha256=sha,source_folder=kind)""")


def library_api(source):
    return once(source,"    @app.get('/api/original-documents/library')\n    def catalog(person=Depends(credentials)):\n        return service.catalog(person)", """    from . import library_workspace_files
    from fastapi.responses import JSONResponse
    library_workspace_files.attach(app,store,credentials)

    @app.get('/api/original-documents/library')
    def catalog(req: Request, workspaces: bool=False, person=Depends(credentials)):
        result=service.catalog(person)
        if workspaces:
            result.update(library_workspace_files.catalogue(store,person,
                req.headers['authorization'].removeprefix('Bearer '),{d['id']:d for d in result['documents']}))
        return JSONResponse(result,headers={'Cache-Control':'no-store'})""")


def workspace_export(source):
    source=once(source,"MIXED_TABLES = {'document_invites'", "MIXED_TABLES = {'workspace_file_imports','document_invites'")
    return once(source,"        if 'ops_photo_evidence' in names:", """        if 'workspace_file_imports' in names:
            from .library_import_sources import prune
            prune(c, chosen)
        if 'ops_photo_evidence' in names:""")


def import_ui(source):
    source=once(source,'f.document=result;f.resource=result.kind;paint(f,h);','f.data=data;f.document=result;f.resource=result.kind;paint(f,h);')
    return once(source,'return {op_id:uid(),kind:f.resource,source:f.document.source,',
                'return {op_id:uid(),kind:f.resource,file:{name:f.document.source.filename,data:f.data},source:f.document.source,')


def saved_ui(source):
    return once(source,"el('sb-success').focus", """if(r.source_folder&&canUse('originals.view')){const a=document.createElement('a');a.href='#original-files';a.textContent=(__wl118.locale==='pt-BR'?'Ver original em ':'View original in ')+WavelinkFileBrowser.groupName(r.source_folder);a.onclick=()=>{WavelinkFileBrowser.nextGroup(r.source_folder);};el('sb-work').append(a);}el('sb-success').focus""")


def apply(root):
    receipt=root/'RELEASE_FILES.json'
    if sha256(receipt.read_bytes()).hexdigest()!=PARENT:raise ValueError('Unexpected file library parent release')
    manifest=json.loads(receipt.read_bytes())
    changed={}
    def edit(name, transform):
        raw=changed.get(name,(root/name).read_bytes())
        if name not in changed and sha256(raw).hexdigest()!=manifest['files'][name]:raise ValueError('Changed parent resource '+name)
        source=raw.decode().replace('\r\n','\n')
        updated=transform(source)
        if updated!=source:changed[name]=(updated.replace('\n','\r\n') if b'\r\n' in raw else updated).encode()
    for filename in ('library_workspace_files.py','library_import_sources.py'):
        changed['app/'+filename]=(HERE/filename).read_bytes().replace(b'\r\n',b'\n')
    for name,fn in [('app/original_folders_api.py',library_api),('app/project_modules.py',workspace_export),
                    ('app/document_import.py',document_import),('app/builder_hub.py',builders), (STATIC+'app.js',client),
                    (STATIC+'original_library.js',frontend),(STATIC+'document_import.js',import_ui),(STATIC+'setup_builders.js',saved_ui),
                    (STATIC+'original_library.css',lambda s:s+'\n'+(HERE/'original_file_browser.css').read_text('utf-8'))]:
        edit(name,fn)
    edit('app/server.py',lambda s:once(s,"else 17_000_000 if req.url.path in ('/api/builders/import/review'", "else 18_200_000 if req.url.path=='/api/builders/document/action' else 17_000_000 if req.url.path in ('/api/builders/import/review'"))
    for folder, paragraph in [
        ('help_topics', 'Open <strong>Documents → Original files</strong>. Choose a workspace folder or search by filename, title, code or folder. Confirmed checklist and toolbox talk imports appear in their own folders. Personnel attachments appear under Human resources. Select a file to open it or use Actions to open its source record. Use Library folders for originals you file yourself.'),
        ('pt-BR/help_topics', 'Abra <strong>Documentos → Arquivos originais</strong>. Escolha uma pasta por área ou busque pelo nome do arquivo, título, código ou pasta. As importações confirmadas de listas de verificação e diálogos de segurança aparecem nas respectivas pastas. Os anexos de pessoal ficam em Recursos humanos. Selecione um arquivo para abri-lo ou use Ações para abrir o registro de origem. Use as pastas da biblioteca para organizar os originais enviados diretamente.'),
    ]:
        edit(STATIC+folder+'/originals.html',lambda s:re.sub(r'(<h2 id="open-library">[^<]+</h2>)<p>.*?</p>',lambda m:m[1]+'<p>'+paragraph+'</p>',s,count=1))
    keys={name[len(STATIC):]:sha256(raw).hexdigest()[:12] for name,raw in changed.items() if name.startswith(STATIC)}
    pattern=re.compile(r'(/static/('+'|'.join(re.escape(k) for k in keys)+r')\?v=[\d.]+-)[a-f0-9]{12}')
    for name in manifest['files']:
        if name.startswith(STATIC) and (name.endswith('.html') or name==STATIC+'sw.js'):
            edit(name,lambda s:pattern.sub(lambda m:m[1]+keys[m[2]],s))
    edit(STATIC+'sw.js',lambda s:once(s,"ui162-20261119-native-corcovado-mood-language';","ui162-20261121-workspace-file-library';"))
    variant=manifest['variant']+'-workspace-files'
    info=json.loads((root/'UI_PATCH.json').read_bytes())
    info.update(patch_id=variant,parent_patch_id=manifest['variant'],parent_manifest_sha256=PARENT,
                scope='Searchable original files, automatic workspace folders and permission-aware source attachments.')
    info['boundaries']['data_schema_changed']=True
    changed['UI_PATCH.json']=(json.dumps(info,indent=2)+'\n').encode()
    for name,raw in changed.items():
        (root/name).write_bytes(raw)
        manifest['files'][name]=sha256(raw).hexdigest()
    manifest['variant']=variant
    receipt.write_bytes((json.dumps(manifest,indent=2)+'\n').encode())
    print(variant,sha256(receipt.read_bytes()).hexdigest())


if __name__=='__main__':
    apply(Path(sys.argv[1]))
