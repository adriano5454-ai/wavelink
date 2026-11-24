from pathlib import Path
import runpy
import sys


def saved_drafts(source):
    old = "__wl118.markup('<p class=\"small\">No active saved notes for your account. Create handover starts a new private draft.</p>')"
    anchor = "  const c=readViewContext(host);host.querySelectorAll('[data-ho-resume]')"
    if source.count(old) != 1 or source.count(anchor) != 1:
        raise ValueError('Unexpected saved draft renderer')
    empty = """(vesselId
    ? `<p>${hoLabel('No saved drafts for the selected vessel.','Nenhum rascunho salvo para a embarcação selecionada.')}</p><button type="button" class="btn secondary" id="ho-drafts-all">${hoLabel('Show all vessels','Mostrar todas as embarcações')}</button>`
    : `<p>${hoLabel('You have no saved drafts.','Você não tem rascunhos salvos.')}</p>${directory?.can_create ? button('ho-drafts-start',hoLabel('Start a draft','Iniciar rascunho'),'') : ''}`)"""
    source = source.replace(old, empty)
    return source.replace(anchor, """  const c=readViewContext(host);
  const all=host.querySelector('#ho-drafts-all'),start=host.querySelector('#ho-drafts-start');
  if(all)all.onclick=()=>{
   if(!readViewLive(c)||journalTab!=='drafts')return;
   const select=el('ho-vessel-filter')?.querySelector('[data-page-vessel]');
   if(!select||select.disabled)return;
   select.value='';select.dispatchEvent(new Event('change',{bubbles:true}));select.focus();
  };
  if(start)start.onclick=()=>{if(readViewLive(c)&&journalTab==='drafts')chooseHandover();};
  host.querySelectorAll('[data-ho-resume]')""")


def transforms():
    return {'app/static/handovers.js': saved_drafts}


if __name__=='__main__':
    apply=runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]),parent='380f627c8d64badd48898acabb0b006d8f3e03dce5773486500d6f2a234dc999',overlays=(Path(__file__).name,),previous_cache='ui162-handover-navigation',cache='ui162-handover-draft-empty',suffix='handover-draft-empty',scope='Recover from an empty vessel filter or start a private draft from saved drafts.')
