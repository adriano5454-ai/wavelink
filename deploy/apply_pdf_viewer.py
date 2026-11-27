"""Wire the same verified, local PDF viewer into the existing read paths."""
from hashlib import sha256
from pathlib import Path
import json, runpy, sys

BASE = Path(__file__).resolve().parent
STATIC = 'app/static/'
PARENT = 'b9044596929351e0080a6915f5ccfcc203ff86f17f15871e83086ba115ce185f'

def once(source, old, new):
    if source.count(old)!=1: raise ValueError('Unexpected PDF viewer anchor: '+repr(old))
    return source.replace(old,new,1)

def original(source):
    source=once(source,
    '''    const inline=preview&&['application/pdf','image/jpeg','image/png','image/webp'].includes(ref.mime);''',
    '''    const pdf=preview&&ref.mime==='application/pdf';
    const inline=preview&&['image/jpeg','image/png','image/webp'].includes(ref.mime);
    const trigger=document.activeElement;''')
    source=once(source,
    '''    if(viewer&&!viewer.closed){const url=URL.createObjectURL(new Blob([file],{type:ref.mime}));''',
    '''    if(pdf){
        const allowed=()=>{if(scope)scope();return hub===state.hub_id&&person===state.auth?.person?.user_id&&!!person&&(!trigger||trigger.isConnected);};
        if(!window.WLPdfViewer?.open(file,{name:ref.filename,trigger,allowed}))throw new Error(__wl118.locale==='pt-BR'?'Visualização indisponível. Use Baixar original.':'Preview unavailable. Use Download original.');
    }else if(viewer&&!viewer.closed){const url=URL.createObjectURL(new Blob([file],{type:ref.mime}));''')
    return once(source,"await downloadOriginal(ref);}catch(e){toast(e.message);}",
                       "await downloadOriginal(ref,()=>{if(!button.isConnected)throw Error('Original reference changed.');},ref.mime==='application/pdf');}catch(e){toast(e.message);}")

def handover(source):
    source=once(source,
    """r.mime.startsWith('image/')?__wl118.t('Open photo'):__wl118.t('Download file')""",
    """r.mime.startsWith('image/')?__wl118.t('Open photo'):r.mime==='application/pdf'?(__wl118.locale==='pt-BR'?'Abrir PDF':'Open PDF'):__wl118.t('Download file')""")
    return once(source,
    """slot.scrollIntoView({block:'nearest'});}else download(blob,r.filename);""",
    """slot.scrollIntoView({block:'nearest'});}else if(r.mime==='application/pdf'){
       const trigger=q(`[data-ha-open="${r.id}"]`);
       if(!window.WLPdfViewer?.open(blob,{name:r.filename,trigger,allowed:()=>owned()&&epoch===stamp&&!!trigger?.isConnected})){
         error.textContent=__wl118.locale==='pt-BR'?'Não foi possível abrir a visualização.':'Could not open the preview.';
       }
     }else download(blob,r.filename);""".replace("\\\u0060","\u0060").replace("\\\u0024","\u0024"))

def hr(source):
    source=once(source,"function previewPrivateFile(host,file,blob,trigger=null){","function previewPrivateFile(host,file,blob,trigger=null,allowed=()=>true){")
    start="  if(file.mime==='application/pdf'){H.download(blob,file.filename);H.toast("
    lo=source.index(start)
    hi=source.index('\n',lo)
    source=source[:lo]+'''  if(file.mime==='application/pdf'){
   if(!window.WLPdfViewer?.open(blob,{name:file.filename,trigger:trigger||document.activeElement,allowed:()=>host.isConnected&&H.dialog.open&&allowed()}))
    H.toast(wtext('Não foi possível abrir a visualização.','Could not open the preview.'));
   return;
  }'''+source[hi:]
    source=once(source,"before();previewPrivateFile(f.node,file,blob);","before();previewPrivateFile(f.node,file,blob,b,()=>{before();return true;});")
    source=once(source,"if(b.hasAttribute('data-hr-review-preview'))previewPrivateFile(f.node,file,blob,b);else H.download(blob,file.filename);",
                       "if(file.mime==='application/pdf'||b.hasAttribute('data-hr-review-preview'))previewPrivateFile(f.node,file,blob,b,()=>{formGuard(f);return true;});else H.download(blob,file.filename);")
    source=once(source,"previewPrivateFile(section,file,blob,b);","previewPrivateFile(section,file,blob,b,valid);")
    source=once(source,"wtext('Baixar PDF','Download PDF')","wtext('Abrir PDF','Open PDF')")
    source=once(source,"wtext('Abrir / baixar PDF','Open / download PDF')","wtext('Baixar PDF','Download PDF')")
    old="""(file.mime==='application/pdf'?'':__hr121.markup('<button type="button" class="btn secondary small" data-hr-preview="')+E(file.id)+__hr121.markup('">Visualizar anexo</button>'))"""
    new="""(__hr121.markup('<button type="button" class="btn secondary small" data-hr-preview="')+E(file.id)+__hr121.markup('">')+E(file.mime==='application/pdf'?wtext('Abrir PDF','Open PDF'):__hr121.t('Visualizar anexo'))+__hr121.markup('</button>'))"""
    source=once(source,old,new)
    prefix="  const pdfNote="
    lo=source.index(prefix)
    hi=source.index("\n",lo)
    return source[:lo]+"  const pdfNote='';"+source[hi:]

def shell(source):
    viewer=sha256((BASE/'wl_pdf_viewer.js').read_bytes()).hexdigest()[:12]
    css=sha256((BASE/'wl_pdf_viewer.css').read_bytes()).hexdigest()[:12]
    anchor='</head>'
    return once(source,anchor,
        f'<link rel="stylesheet" href="/static/wl_pdf_viewer.css?v=1.34.61-{css}">\n'
        f'<script defer src="/static/wl_pdf_viewer.js?v=1.34.61-{viewer}"></script>\n{anchor}')

def additions():
    pack=BASE/'pdfjs-6.5.438'
    data=json.loads((pack/'ASSET_HASHES.json').read_bytes())
    assert data['version']=='6.5.438'
    result={STATIC+name:(BASE/name).read_bytes() for name in ('wl_pdf_viewer.js','wl_pdf_viewer.css')}
    for name,want in data['files'].items():
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or ':' in name or '\\' in name: raise ValueError('Invalid viewer asset')
        payload=(pack/p).read_bytes()
        if sha256(payload).hexdigest()!=want: raise ValueError('PDF.js asset mismatch: '+name)
        result[STATIC+'wl-pdfjs-6.5.438/'+name]=payload
    return result


def original_detail(source):
    return once(source,
    """    const acts=el('div','of-actions');acts.append(button(__wl118.t('Back to list'),()=>backToBrowse()),button(__wl118.t('Open / save original'),e=>download(doc,e)));""",
    """    const acts=el('div','of-actions');acts.append(button(__wl118.t('Back to list'),()=>backToBrowse()));
    if(doc.mime==='application/pdf'){
     const pt=__wl118.locale==='pt-BR';
     acts.append(button(pt?'Abrir PDF':'Open PDF',e=>download(doc,e,true)),button(pt?'Baixar original':'Download original',e=>download(doc,e)));
    }else acts.append(button(__wl118.t('Open / save original'),e=>download(doc,e)));""")


def transforms():
    return {STATIC+'app.js':original,STATIC+'hr_workspace.js':hr,
            STATIC+'handover_attachments.js':handover,STATIC+'index.html':shell,STATIC+'original_library.js':original_detail}

if __name__=='__main__':
    apply=runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply']
    apply(Path(sys.argv[1]),parent=PARENT,overlays=(Path(__file__).name,),previous_cache='ui162-toolbox-retained-row',
          cache='ui162-pdf-viewer',suffix='pdf-viewer',
          scope='Private in-app PDF viewing for Original Files, HR and handovers; preserve download and access checks.')
