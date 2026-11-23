from pathlib import Path
import runpy
import sys


def workspace(source):
    start = source.index('<form id="fr-filters"')
    search = source.index('<label class="field"><span>Find reference', start)
    vessel = source.index("${window.WLPageVessels", search)
    end = source.index('<div class="fr-layout">', vessel)
    selectors = source[start:search].replace('fr-toolbar wl-native-toolbar', 'fr-filter-fields')
    query_field = source[search:vessel].replace('id="fr-query"', 'id="fr-query" form="fr-filters"')
    vessel_field, apply_button = source[vessel:end].removesuffix('</form>').split('<button', 1)
    source = source[:start] + (
        '<div class="fr-filter-shell"><details id="fr-filter-panel"><summary>${panelText("Filtros","Filters")}</summary>'
        + selectors + vessel_field
        + '<button type="button" id="fr-clear" class="btn secondary">${panelText("Limpar filtros","Clear filters")}</button>'
        + '</form></details><div class="fr-results"><div class="fr-search">' + query_field
        + '<button form="fr-filters"' + apply_button + '</div><div id="fr-applied"></div>'
    ) + source[end:]
    source = source.replace('</section></div></section>\x60);', '</section></div></div></div></section>\x60);', 1)
    anchor = " let context=''"
    source = source.replace(anchor, """ const wideFilters = window.matchMedia('(min-width:801px)');
 const filterPreference = {wide:true, narrow:false};
 const filterSize = () => wideFilters.matches ? 'wide' : 'narrow';
 const panelText = (pt,en) => window.WavelinkI18n?.locale === 'pt-BR' ? pt : en;
 wideFilters.addEventListener('change', () => {
  const panel=document.getElementById('fr-filter-panel');
  if(panel) panel.open=filterPreference[filterSize()];
 });
""" + anchor, 1)
    anchor = "  const vesselForm=el('fr-filters');"
    source = source.replace(anchor, anchor + """
  const panel=el('fr-filter-panel');
  panel.open=filterPreference[filterSize()];
  panel.ontoggle=()=>{if(panel.isConnected) filterPreference[filterSize()]=panel.open;};
  const applied=el('fr-applied');
  const vesselSelect=vesselForm.querySelector('[data-page-vessel]');
  function describeFilters(){
   const labels=[el('fr-status').selectedOptions[0]?.textContent];
   if(assignment!=='all') labels.push(el('fr-assignment').selectedOptions[0]?.textContent);
   if(vesselId) labels.push(vesselSelect?.value===vesselId ? vesselSelect.selectedOptions[0]?.textContent : vesselId);
   if(query) labels.push(query);
   applied.textContent=panelText('Filtros ativos','Active filters')+' · '+labels.filter(Boolean).join(' · ');
  }
  vesselForm.addEventListener('submit', describeFilters);
  describeFilters();
  if(vesselId && vesselSelect){
   const observer=new MutationObserver(()=>{describeFilters();if(vesselSelect.value===vesselId)observer.disconnect();});
   observer.observe(vesselSelect,{childList:true,subtree:true});
  }
  el('fr-clear').onclick=()=>{
   el('fr-status').value='active';
   el('fr-assignment').value='all';
   el('fr-query').value='';
   vesselId='';
   if(vesselSelect) vesselSelect.value='';
   vesselForm.requestSubmit();
  };""", 1)
    return source


def transforms():
    return {'app/static/fault_reports.js': workspace,
            'app/static/operations_workspace_ui76.css': lambda src: src + Path(__file__).with_suffix('.css').read_text(encoding='utf-8')}


if __name__ == '__main__':
    apply = runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]), parent='2a0740b6d28856c211f54f308951fececeb0cb9eae6cd5c0c394789b835dcd4a',
          overlays=(Path(__file__).name,), previous_cache='ui162-roster-period', cache='ui162-fault-filters',
          suffix='fault-filters', scope='Responsive filter panel on Fault Reports.')
