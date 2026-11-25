"""Keep the handover journal's chosen subject and date range across vessel changes."""
from pathlib import Path
import runpy

one = runpy.run_path(str(Path(__file__).with_name('apply_org_chart_filters.py')))['replace_once']


def handovers(source):
    return one(source,
               "preview.close();vesselId=id;journalSelection={vessel_id:id};setJournalTab(journalTab);",
               """preview.close();
   vesselId=id;
   const {subject_key,date_from,date_to,include_archived,rangeOpen}=journalSelection;
   journalSelection={vessel_id:id,subject_key,date_from,date_to,include_archived,
    rangeOpen:el('hwd-range')?.open??rangeOpen};
   setJournalTab(journalTab);""")


def overview(source):
    source = one(source, "  const changeScope=()=>{",
                 """  $('#hwd-range').open=!!selection.rangeOpen;
  const unavailableLabel=window.WavelinkI18n?.locale==='pt-BR'
   ? 'Assunto indisponível para os filtros atuais' : 'Subject unavailable with these filters';
  function showUnavailable(){
   clear();
   status(window.WavelinkI18n?.locale==='pt-BR'
    ? 'O assunto selecionado está indisponível. Escolha outro assunto ou ajuste os filtros.'
    : 'The selected subject is unavailable. Choose another subject or change the filters.');
  }
  const changeScope=()=>{""")
    source = one(source, "if(!subjects.some(x=>x.key===selection.subject_key)){clear();",
                 "if(!selection.subject_key){clear();")
    source = one(source, "    const options=subjects.length?", """    const unavailable=!!selection.subject_key&&!subjects.some(x=>x.key===selection.subject_key);
    let options=subjects.length?""")
    source = one(source, "    if($('#hwd-subject').innerHTML!==options)",
                 """    if(unavailable)options='<option value="" disabled>'+E(unavailableLabel)+'</option>'+options;
    if($('#hwd-subject').innerHTML!==options)""")
    source = one(source, "$('#hwd-subject').value=selection.subject_key;",
                 "$('#hwd-subject').value=unavailable?'':selection.subject_key;")
    source = one(source, "    if(!subjects.length){clear();",
                 """    if(unavailable){showUnavailable();return;}
    if(!subjects.length){clear();""")
    source = one(source, "if(!live()||!selection.subject_key)return;const run=++epoch,s=selected();",
                 """if(!live()||!selection.subject_key)return;
   if(!subjects.some(x=>x.key===selection.subject_key)){showUnavailable();return;}
   const run=++epoch,s=selected();""")
    return source


def transforms():
    return {'app/static/handovers.js': handovers, 'app/static/handover_workspace.js': overview}
