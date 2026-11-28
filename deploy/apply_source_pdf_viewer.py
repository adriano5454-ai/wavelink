"""Extend the installed PDF viewer to authenticated source-file entry points."""
from pathlib import Path
import runpy, sys
BASE=Path(__file__).resolve().parent
STATIC='app/static/'
PARENT='5c539e9b3cd8dd651707d6a999e0fcb2c8cdd79edcdea894c0a0fbbd1eca068d'
def once(s,a,b):
    if s.count(a)!=1: raise ValueError(a)
    return s.replace(a,b,1)
def it(s):
    s=once(s,"E(t('Baixar','Download'))+'</button>'+(can?", "E(f.mime==='application/pdf'?t('Abrir PDF','Open PDF'):t('Baixar','Download'))+'</button>'+(can?")
    return once(s,"if(c.same())H.download(blob,file.filename);","""const allowed=()=>c.same()&&b.isConnected;
      if(!allowed())return;
      if(file.mime==='application/pdf'){
        if(!window.WLPdfViewer?.open(blob,{name:file.filename,trigger:b,allowed}))throw local('Não foi possível abrir a visualização.','Could not open the preview.');
      }else H.download(blob,file.filename);""")
def cert(s):
    s=once(s,'''>Open / save</button><p class="cw136-file-state small"''','''>${f.mime==='application/pdf'?window.WavelinkUX.text('Abrir PDF','Open PDF'):__wl118.t('Open / save')}</button><p class="cw136-file-state small"''')
    return once(s,"if(!active())return;downloadBlob(blob,f.filename);status.textContent=","""if(!active())return;
   if(f.mime==='application/pdf'){
    if(!window.WLPdfViewer?.open(blob,{name:f.filename,trigger:b,allowed:active}))throw err(window.WavelinkUX.text('Não foi possível abrir a visualização.','Could not open the preview.'));
    status.textContent='';return;
   }
   downloadBlob(blob,f.filename);status.textContent=""")
def related(s):
    s=once(s,"const label=record.kind==='checklist_guidance'?","const pdf=file.mime==='application/pdf';const label=pdf?'Open PDF':record.kind==='checklist_guidance'?")
    return once(s,"cardScope();await download(blob,file.filename);if(current())","""cardScope();
      if(pdf){
       if(!window.WLPdfViewer?.open(blob,{name:file.filename,trigger:b,allowed:()=>current()&&b.isConnected}))throw Error(tr().locale==='pt-BR'?'Não foi possível abrir a visualização.':'Could not open the preview.');
       feedback.hidden=true;
      }else await download(blob,file.filename);
      if(!pdf&&current())""").replace("const b=button(t(label)+'","const b=button((pdf&&tr().locale==='pt-BR'?'Abrir PDF':t(label))+'",1)
def fleet(s):
    return once(s," root.querySelectorAll('[data-file]').forEach(b=>b.onclick=()=>download('/api/fleet/manifests/'+id+'/files/'+b.dataset.file,m.files.find(f=>f.id===b.dataset.file).filename).catch(showError));",""" root.querySelectorAll('[data-file]').forEach(b=>b.onclick=async()=>{
  if(b.disabled||!active())return;
  const file=m.files.find(f=>f.id===b.dataset.file);if(!file)return;
  const path='/api/fleet/manifests/'+id+'/files/'+file.id;
  const owner=context(),allowed=()=>active()&&owns(owner)&&b.isConnected;
  b.disabled=true;
  try{
   if(file.mime!=='application/pdf'){await download(path,file.filename);return;}
   const response=await api(path,{binary:true}),blob=await response.blob();
   if(!allowed())return;
   // In the embedded workspace keep the preview in the browser viewport,
   // not halfway down the document-height iframe.
   const target=embedded?window.parent:window;
   const source=embedded?new target.Blob([blob],{type:blob.type}):blob;
   if(!target.WLPdfViewer?.open(source,{name:file.filename,trigger:b,allowed}))
    throw Error(__wl118.locale==='pt-BR'?'Não foi possível abrir a visualização.':'Could not open the preview.');
  }catch(error){if(allowed()&&!error?.obsolete&&!error?.fleetHandled)showError(error);}
  finally{if(b.isConnected)b.disabled=false;}
 });""")
def fleet_shell(s):
    render=runpy.run_path(str(BASE/'apply_pdf_viewer.py'))['shell']
    return render(s)
def transforms():
    return {STATIC+'it_workspace.js':it,STATIC+'certificate_workspace.js':cert,
            STATIC+'documentos_context.js':related,STATIC+'fleet.js':fleet,STATIC+'fleet.html':fleet_shell}
if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent=PARENT,overlays=(Path(__file__).name,),
        previous_cache='ui162-original-mobile-layout',cache='ui162-source-pdf-viewer',suffix='source-pdf-viewer',
        scope='Open authenticated source PDFs in the existing viewer from IT, equipment certificates, Fleet manifests and related documents.')
