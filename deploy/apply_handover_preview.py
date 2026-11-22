"""Read-only handover previews in each saved-record register."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

BASE = Path(__file__).resolve().parent
PARENT = '04514baa7b278c4cc1c51654412dfc7219ad418751996d881fcdfe1e5161a23b'
STATIC = 'app/static/'


def change(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected handover source near '+old[:100])
    return source.replace(old, new)


def api(source):
    before = "    @app.get('/api/handovers/{ident}')"
    return change(source, before, '''    @app.get('/api/handovers/{ident}/preview')
    def preview(ident: str, revision: int | None = None, auth=Depends(credentials)):
        from .handovers import SECTIONS
        record = service.detail(ident, *auth, revision=revision)
        if revision is None:
            if not record['mine'] or record.get('draft') is None:
                raise Problem(404, 'This saved draft is unavailable.')
            edit = record['draft']
            files = record.get('draft_attachments', [])
            author = record['author']
        else:
            publication = record['publication']
            edit = publication['edit']
            files = publication.get('attachments', [])
            author = publication['author']
        fields = ('title', 'location', 'period_start', 'period_end', 'time_basis', *(key for key, _ in SECTIONS))
        return dict(id=ident, revision=revision, archived=record['archived'], author=author,
                    can_edit=revision is None and record['can_edit'] and not record['archived'],
                    edit={key: edit.get(key, '') for key in fields}, files=files)

'''+before)


def workspace(source):
    source=change(source,'onSetup,onCreate,onDownload,selection,preferredDepartment','onSetup,onCreate,onDownload,onPreview,selection,preferredDepartment')
    source=change(source,"E(x.can_edit?__wl118.t('Edit my notes'):x.published_revision?__wl118.t('Read handover'):__wl118.t('Open saved draft'))","E(WLHandoverPreview.label())")
    source=change(source,'>Read published r${x.published_revision}</button>','>${E(WLHandoverPreview.label())} · r${x.published_revision}</button>')
    source=change(source,'if(x){remember();onRead(x.id,x.published_revision);}', 'if(x){remember();onPreview(b,x.id,x.published_revision);}')
    return change(source,'if(x.can_edit)onOpen({id:x.id});else onRead(x.id,x.published_revision||null);',
                  "onPreview(b,x.id,x.state==='published'?x.published_revision:null);")


def handovers(source):
    source=change(source,' let fileViews=[];', ''' const preview=WLHandoverPreview.mount({
  api:(...args)=>api(...args),active:()=>allowed()&&!!directory&&mountedScope===scope()&&mountedHash===location.hash&&
   !editor&&!!el('ho-library')&&!el('ho-library').hidden&&!document.querySelector('dialog[open]'),
  sections:()=>directory.sections,onRead:(id,revision)=>showDetail(id,revision),onEdit:target=>openSimple(target)
 });
 let fileViews=[];''')
    source=change(source,'function reset(){shiftRoster', 'function reset(){preview.close();shiftRoster')
    source=change(source,'if(editor)return;const problem=', 'if(editor)return;preview.close();const problem=')
    source=change(source,'return;rememberJournal();journalTab=tab;', 'return;preview.close();rememberJournal();journalTab=tab;')
    source=change(source,'rememberJournal();clearFileViews();generation++;dayGeneration++;currentId=ident;',
                  'preview.close();rememberJournal();clearFileViews();generation++;dayGeneration++;currentId=ident;')
    source=change(source,'onOpen:openSimple,onRead:showDetail,onShifts:', 'onOpen:openSimple,onRead:showDetail,onPreview:preview.open,onShifts:')
    source=change(source,'onOpen:openSimple,onRead:showDetail,onSetup:', 'onOpen:openSimple,onRead:showDetail,onPreview:preview.open,onSetup:')
    source=change(source,'onOpen:(id,revision)=>showDetail(id,revision),onRefresh:()=>load(true)', 'onOpen:(id,revision,b)=>preview.open(b,id,revision),onRefresh:()=>load(true)')
    source=change(source,'data-ho-open="${E(r.id)}">Open handover', 'data-ho-open="${E(r.id)}">${E(WLHandoverPreview.label())}')
    source=change(source,"b.onclick=()=>showDetail(b.dataset.hoOpen)", """b.onclick=()=>{
   const row=list.find(item=>item.id===b.dataset.hoOpen);if(!row)return;
   if(row.archived&&!row.has_private_draft&&!row.published_revision){showDetail(row.id);return;}
   preview.open(b,row.id,row.has_private_draft||row.state==='private_draft'?null:row.published_revision);
  }""")
    # An archived author's list can represent a draft, retained publication, or discarded identity.
    source=change(source,'${E(WLHandoverPreview.label())}</button></article>',"""${E(r.archived&&!r.has_private_draft&&!r.published_revision?__wl118.t('Open handover'):WLHandoverPreview.label())}</button></article>""")
    source=change(source,"directory.can_create?__wl118.t('Continue my notes'):__wl118.t('Read saved draft')","WLHandoverPreview.label()")
    source=change(source,'if(directory.can_create)openSimple({id:b.dataset.hoResume});else showDetail(b.dataset.hoResume);',
                  'preview.open(b,b.dataset.hoResume,null);')
    source=change(source,'type="button">Continue my draft</button>', 'type="button">${E(WLHandoverPreview.label())}</button>')
    source=change(source,'type="button">Read published revision ${revision}</button>','type="button">${E(WLHandoverPreview.label())} · r${revision}</button>')
    source=change(source,'b.onclick=()=>openDailySaved(b.dataset.hoDayOpen,true)','b.onclick=()=>{if(dayReadLive(c))preview.open(b,b.dataset.hoDayOpen,null);}')
    source=change(source,'b.onclick=()=>openDailySaved(b.dataset.hoDayPublished,false,false,Number(b.dataset.hoRevision),true)',
                  'b.onclick=()=>{if(dayReadLive(c))preview.open(b,b.dataset.hoDayPublished,Number(b.dataset.hoRevision));}')
    return (BASE/'handover_preview.js').read_text(encoding='utf-8')+'\n'+source


def inbox(source):
    source=change(source,'>Read published revision ${r.revision}</button>', '>${E(WLHandoverPreview.label())}</button>')
    return change(source,'if (r) onOpen(r.id,r.revision);','if (r) onOpen(r.id,r.revision,b);')


def personal(source):
    source=change(source,"rec?(editable?'Edit my notes':readable?'Read my finished handover':'Editing unavailable')",
                  "rec?(editable||readable?WLHandoverPreview.label():'Editing unavailable')")
    source=change(source,'<section class="shw-personal"><div class="shw-personal-title">',"""<section class="shw-personal" ${rec?'data-hop-personal':''}><div class="shw-personal-title">""")
    return change(source,"if(v.record.can_edit)o.onOpen({id:v.record.id});else if(v.record.published_revision)o.onRead(v.record.id,v.record.published_revision);",
                  """const b=host.querySelector('[data-shw-save-open]');o.onPreview(b,v.record.id,v.record.state==='finished'?v.record.published_revision:null);""")


def board(source):
    source=change(source,'onOpen,onRead,onSetup,selection','onOpen,onRead,onSetup,onPreview,selection')
    source=change(source,"label=r.can_edit?(resume?__wl118.t('Continue my notes'):__wl118.t('Edit my notes')):r.published_revision?__wl118.t('Read handover'):__wl118.t('Editing unavailable')",
                  "label=r.can_edit||r.published_revision?WLHandoverPreview.label():__wl118.t('Editing unavailable')")
    return change(source,'if(row.can_edit)onOpen({id:row.id});else if(row.published_revision)onRead(row.id,row.published_revision);',
                  "if(onPreview)onPreview(b,row.id,row.state==='finished'?row.published_revision:null);else if(row.can_edit)onOpen({id:row.id});else if(row.published_revision)onRead(row.id,row.published_revision);")


def cards(source):
    source=change(source,"['article.ho-card',['[data-ho-open]']]", """['article.ho-card',['[data-ho-open]','[data-ho-incoming]']],
  ['article.ho-resume-entry',['[data-ho-resume]']],
  ['.shw-personal[data-hop-personal]',['[data-shw-save-open]']]""")
    return change(source,"['article.ho-day-entry', ['[data-ho-day-open]']]", "['article.ho-day-entry', ['[data-ho-day-open]','[data-ho-day-published]']]")


def styles(source):
    source=change(source,'.hwd-record, .ho-card, .sh-resume, .sh-record, .ho-day-entry,', '.hwd-record, .ho-card, .ho-resume-entry, .sh-resume, .sh-record, .ho-day-entry,')
    return source+"""
.hop-layout { display:grid; grid-template-columns:minmax(0,var(--wl-register-width)) minmax(0,1fr); align-items:start; gap:1rem; }
.hop-layout > * { min-width:0; }
#ho-record-preview { position:sticky; top:4.5rem; box-sizing:border-box; padding:1rem; margin:0; max-height:calc(100dvh - 6rem); overflow:auto; overscroll-behavior:contain; scroll-margin-block:5rem 1rem; background:var(--surface,#fff); border:1px solid var(--border,#c5d4da); border-radius:.75rem; overflow-wrap:anywhere; }
.hop-head,.hop-actions { display:flex; align-items:center; flex-wrap:wrap; gap:.5rem; }
.hop-head { justify-content:space-between; border-bottom:1px solid var(--border,#d6e1e5); padding-bottom:.65rem; margin-bottom:.8rem; }
.hop-head .btn,.hop-actions .btn { min-height:44px; }
.hop-body h2 { margin:.45rem 0; }
.hop-context,.hop-note p { margin:.3rem 0; }
.hop-actions { margin-block:1rem; }
.hop-note { margin-block:.8rem; }
.hop-note h3 { font-size:1rem; margin:0 0 .3rem; }
.hop-note p { white-space:pre-wrap; }
.hop-evidence { border-top:1px solid var(--border,#d6e1e5); margin-top:.75rem; padding-top:.35rem; }
.hop-evidence > summary { cursor:pointer; padding-block:.6rem; font-weight:600; }
#ho-library .hop-selected { box-shadow:inset 3px 0 #087b81; outline:1px solid #23888e; outline-offset:-1px; }
#ho-library :is(.ho-resume-entry,[data-hop-personal],.ho-card,.ho-day-entry):has(button:enabled) { cursor:pointer; }
@media (max-width:850px) {
 .hop-layout { display:block; }
 .hop-layout > :first-child { display:none !important; }
 #ho-record-preview { position:static; max-height:none; overflow:visible; }
}
"""


def apply(root):
    receipt=root/'RELEASE_FILES.json'
    if sha256(receipt.read_bytes()).hexdigest()!=PARENT:
        raise ValueError('Unexpected runtime before handover preview')
    manifest=json.loads(receipt.read_bytes())
    changed={}
    def edit(path,transform):
        raw=(root/path).read_bytes()
        if sha256(raw).hexdigest()!=manifest['files'][path]:
            raise ValueError('Unexpected resource: '+path)
        out=transform(raw.decode('utf-8')).encode('utf-8')
        if out!=raw: changed[path]=out
    edit('app/handovers_api.py',api)
    edit('app/handovers.py',lambda s:change(s,"row = dict(id=rec['id'], title=edit['title']", "row = dict(id=rec['id'], has_private_draft=own and rec['draft'] is not None, title=edit['title']"))
    for filename,transform in [('handovers.js',handovers),('handover_workspace.js',workspace),
                               ('handover_incoming.js',inbox),('shift_workspace.js',personal),
                               ('simple_handovers.js',board),('action_center_ui82.js',cards),('ui132_visual.css',styles)]:
        edit(STATIC+filename,transform)
    hashes={k[len(STATIC):]:sha256(v).hexdigest()[:12] for k,v in changed.items() if k.startswith(STATIC)}
    pattern=re.compile(r'(/static/('+'|'.join(re.escape(k) for k in hashes)+r')\?v=[\d.]+-)[0-9a-f]{12}')
    def refs(s):
        return pattern.sub(lambda m:m[1]+hashes[m[2]],s)
    for path in manifest['files']:
        if path.startswith(STATIC) and path.endswith('.html'):
            edit(path,refs)
    edit(STATIC+'sw.js',lambda s:change(refs(s),'ui162-20261122-log-locations','ui162-20261122-handover-preview'))
    variant=manifest['variant']+'-handover-preview'
    info=json.loads((root/'UI_PATCH.json').read_bytes())
    info.update(patch_id=variant,parent_patch_id=manifest['variant'],parent_manifest_sha256=PARENT,
                scope='Read-only saved handover and published revision previews, with evidence.')
    changed['UI_PATCH.json']=(json.dumps(info,indent=2)+'\n').encode()
    for name,raw in changed.items():
        (root/name).write_bytes(raw)
        manifest['files'][name]=sha256(raw).hexdigest()
    manifest['variant']=variant
    receipt.write_bytes((json.dumps(manifest,indent=2)+'\n').encode())
    print(variant,sha256(receipt.read_bytes()).hexdigest())


if __name__=='__main__':
    apply(Path(sys.argv[1]))
