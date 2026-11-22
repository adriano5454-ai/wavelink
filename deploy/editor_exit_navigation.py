"""Connect workspace navigation to the current editor's own form state."""
from pathlib import Path


def change(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected editor exit source near ' + old[:100])
    return source.replace(old, new)


def host(source):
    js = Path(__file__).with_suffix('.js').read_text(encoding='utf-8')
    source = change(source, 'async function route(){', js + '\nasync function route(){')
    anchor = "async function openFleetWorkspace(destination='/fleet'){"
    source = change(source, anchor, anchor + """
    const requestedFleet=new URL(destination||'/fleet',location.href);
    const fleetHash=requestedFleet.pathname==='/fleet'&&requestedFleet.hash
        ? '#fleet/'+requestedFleet.hash.slice(1) : requestedFleet.hash.startsWith('#fleet/')
        ? requestedFleet.hash : AJWorkspaceShell.destination();
    if(!AJEditorNavigation.prepare(fleetHash))return false;""")
    return source


def reports(source):
    code = """function prepareLeave(target){
  if(!form || target===form.hash)return true;
  syncSession();const f=form;if(!f)return true;
  if(f.busy)return AJEditorNavigation.wait();
  if(AJReportForms.dirty(f)&&!AJEditorNavigation.confirmDiscard(!!f.uncertain))return false;
  selected=f.row?.id||selected;form=null;return true;
 }
 """
    source = change(source, 'function guardRoute(){', code + 'function guardRoute(){')
    return change(source, 'syncSession,guardRoute,hasForm:', 'syncSession,prepareLeave,guardRoute,hasForm:')


def retained(source, finish):
    code = """function prepareLeave(target){
  if(!form || target===form.hash)return true;
  syncSession();const f=form;if(!f)return true;
  if(f.busy)return AJEditorNavigation.wait();
  snapshot(f);
  if(f.dirty||f.request||f.uncertain||f.baseResult||f.created){
   if(!AJEditorNavigation.confirmKeep())return false;
   retained.set(f.account,f);
  }
  if(f.node?.isConnected && H.dialog.contains(f.node))FINISH(f);else form=null;
  return true;
 }
 """.replace('FINISH', finish)
    source = change(source, 'function guardRoute(){', code + 'function guardRoute(){')
    return change(source, 'exitBusy,guardRoute', 'exitBusy,prepareLeave,guardRoute')


def profile(source):
    code = """  s.prepareLeave=target=>{
   if(target===editorHash)return true;
   if(s.busy||preparingPhoto)return AJEditorNavigation.wait();
   const changed=s.pending||profileFormChanged(form,profile)||s.draft.avatar;
   if(changed&&!AJEditorNavigation.confirmDiscard(!!s.pending))return false;
   restore();return true;
  };
"""
    anchor = "  form.querySelector('[data-cancel]').onclick="
    source = change(source, anchor, code + anchor)
    return change(source, 'return {init,handles,open,mountHome,',
                  'return {prepareProfileLeave:target=>profileEditor?.prepareLeave(target)??true,init,handles,open,mountHome,')


def contacts(source):
    code = """function prepareLeave(target){
  if(!form || target===form.hash)return true;
  syncSession();const f=form;if(!f)return true;
  if(f.busy)return AJEditorNavigation.wait();
  readForm(f);
  if(f.uncertain||f.request||JSON.stringify(f.values)!==JSON.stringify(details?.contacts)){
   if(!AJEditorNavigation.confirmKeep())return false;
   drafts.set(f.key,f);
  }
  form=null;render();return true;
 }
 """
    source = change(source, 'function guardRoute(){', code + 'function guardRoute(){')
    return change(source, 'hasForm,exitBusy,guardRoute,syncSession', 'hasForm,exitBusy,prepareLeave,guardRoute,syncSession')


def email(source):
    code = """function prepareLeave(target){
  if(!active || target===active.hash)return true;
  syncSession();const s=active;if(!s)return true;
  if(exitBusy())return AJEditorNavigation.wait();
  snapshot(s);
  if(s.dirty||s.pending){
   if(!AJEditorNavigation.confirmKeep())return false;
   preserve(s);
  }
  const open=[...dialogs].filter(d=>d.open);
  if(open.some(d=>[...d.querySelectorAll('input')].some(i=>i.value!==i.defaultValue))
     &&!AJEditorNavigation.confirmDiscard(false))return false;
  for(const d of open)d.close();
  active=null;epoch++;return true;
 }
 """
    source = change(source, 'function guardRoute(){', code + 'function guardRoute(){')
    return change(source, 'hasForm,exitBusy,guardRoute}', 'hasForm,exitBusy,prepareLeave,guardRoute}')


def transforms():
    assets = {'app.js': host, 'recognition_workspace.js': profile, 'professional_contacts.js': contacts,
              'email_alerts_ui93.js': email, 'fault_reports.js': reports, 'qshe_reports.js': reports,
              'it_workspace.js': lambda s: retained(s, 'finish'), 'hr_workspace.js': lambda s: retained(s, 'finishFormClose'),
              'experience_shell.js': lambda s: change(s, 'if (!currentPerson() || H.hasOpenEditor?.()) {',
                  "if (!currentPerson() || (H.hasOpenEditor?.() && !(window.AJRecognition?.hasNewsEditor?.() && !document.querySelector('dialog[open]')))) {")}
    return {'app/static/' + name: transform for name, transform in assets.items()}
