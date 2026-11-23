from pathlib import Path
import runpy
import sys

HERE = Path(__file__).parent


def replace(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected filter source: ' + old[:80])
    return source.replace(old, new)


def panel_behavior(source, anchor, prefix):
    behavior = """
 const widePanel=window.matchMedia('(min-width:801px)');
 const panelChoices={wide:true,narrow:false};
 const sizeKey=()=>widePanel.matches?'wide':'narrow';
 function mountFilters(){
  const panel=document.getElementById('PREFIX-filter-panel');
  panel.open=panelChoices[sizeKey()];
  panel.ontoggle=()=>{if(panel.isConnected) panelChoices[sizeKey()]=panel.open;};
 }
 widePanel.addEventListener('change',()=>{
  const panel=document.getElementById('PREFIX-filter-panel');
  if(panel) panel.open=panelChoices[sizeKey()];
 });
"""
    return replace(source, anchor, behavior.replace('PREFIX', prefix) + anchor)


def toolbox(source):
    source = panel_behavior(source," let toolboxViewKey=", 'tb')
    source = replace(source,"toolboxVessel='',toolboxQuery='';const", "toolboxVessel='',toolboxQuery='',toolboxProject='';const")
    source = replace(source,"toolboxVessel='';toolboxQuery='';}", "toolboxVessel='';toolboxQuery='';toolboxProject='';}")
    source = replace(source, '  function filteredTalks(){', """  const projectOf=t=>String(t.meta?.project_number||'').trim();
  const projects=[...new Set(data.talks.map(projectOf).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
  if(!projects.includes(toolboxProject)) toolboxProject='';
  function filteredTalks(){""")
    source = replace(source, "(!q || [talk.meta?.work_description", "(!toolboxProject || projectOf(talk)===toolboxProject) &&\n    (!q || [projectOf(talk),talk.work_site?.name,talk.work_site?.code,talk.meta?.work_description")
    source = replace(source, '<b>Users: ', '${projectOf(r)?\x60<p>${esc(words("Project","Projeto"))}: ${esc(projectOf(r))}</p>\x60:""}<b>Users: ')
    start = source.index('<fieldset id="tb-filters"')
    end = source.index('  function update(){',start)
    old=source[start:end]
    search=old[old.index('<label'):old.index('${vessels')]
    results=old[old.index('<p class="small"'):old.index('`);')]
    source=source[:start]+"""<div class="hse-filter-shell"><details id="tb-filter-panel" class="hse-filter-panel"><summary>${words('Filters','Filtros')}</summary><div id="tb-filters" class="hse-fields">${vessels?.field(toolboxVessel)||''}<label class="field"><span>${words('Project','Projeto')}</span><select id="tb-project"><option value="">${words('All projects','Todos os projetos')}</option>${projects.map(p=>`<option value="${esc(p)}">${esc(p)}</option>`).join('')}</select></label><button id="tb-clear" type="button" class="btn secondary">${words('Clear filters','Limpar filtros')}</button></div></details><div class="hse-results">"""+search+'<p id="tb-active" class="small"></p>'+results+'</div></div>`);\n'+source[end:]
    source=replace(source,'  function update(){\n   const shown=filteredTalks();',"""  mountFilters();
  const project=document.getElementById('tb-project');
  const vessel=document.querySelector('#tb-filters [data-page-vessel]');
  project.value=toolboxProject;
  function summary(){
   const ship=data.sites?.find(s=>s.id===toolboxVessel);
   const labels=[ship?.name,toolboxProject,toolboxQuery.trim()].filter(Boolean);
   document.getElementById('tb-active').textContent=labels.length?words('Active filters','Filtros ativos')+': '+labels.join(' · '):words('All talks','Todos os diálogos');
  }
  summary();
  project.onchange=()=>{toolboxProject=project.value;update();};
  document.getElementById('tb-clear').onclick=()=>{
   toolboxProject=project.value='';toolboxQuery=document.getElementById('tb-query').value='';
   toolboxVessel='';if(vessel) vessel.value='';update();
  };
  function update(){
   summary();
   const shown=filteredTalks();""")
    return source


def qshe(source):
    source=panel_behavior(source, " let context=''", 'qs')
    nav='<nav class="qs-shortcuts" aria-label="Related workspaces">'
    source=replace(source,nav,'<section class="qs-related"><h2>${filterLabel("Related workspaces","Áreas relacionadas")}</h2>'+nav)
    start=source.index('<form id="qs-filters"')
    search=source.index('<label class="field"><span>Find reference',start)
    vessel=source.index('${window.WLPageVessels',search)
    end=source.index('<div class="qs-layout">',vessel)
    fields=source[start:search].replace('qs-toolbar wl-native-toolbar','hse-fields')
    query=source[search:vessel].replace('id="qs-query"', 'id="qs-query" form="qs-filters"')
    ship,apply=source[vessel:end].removesuffix('</form>').split('<button',1)
    source=source[:start]+('</section><div class="hse-filter-shell"><details id="qs-filter-panel" class="hse-filter-panel"><summary>${filterLabel("Filters","Filtros")}</summary>'+fields+ship+'<button type="button" id="qs-clear" class="btn secondary">${filterLabel("Clear filters","Limpar filtros")}</button></form></details><div class="hse-results"><div class="hse-search">'+query+'<button form="qs-filters"'+apply+'</div><p id="qs-active" class="small"></p>')+source[end:]
    source=replace(source,'</section></div></section>`);','</section></div></div></div></section>`);')
    source=replace(source," let context=''", " const filterLabel=(en,pt)=>window.WLWorkSites?.words(pt,en)||en;\n let context=''")
    anchor="  const vesselForm=el('qs-filters');"
    source=replace(source,anchor,anchor+"""
  mountFilters();
  const ship=vesselForm.querySelector('[data-page-vessel]');
  const selectedText=id=>el(id).selectedOptions[0]?.textContent;
  function describe(){
   if(!vesselForm.isConnected) return;
   const filters=[selectedText('qs-status'),category==='all'?'':selectedText('qs-category'),
    assignment==='all'?'':selectedText('qs-assignment'),vesselId && ship?.value===vesselId?ship.selectedOptions[0]?.textContent:'',query].filter(Boolean);
   el('qs-active').textContent=filterLabel('Active filters','Filtros ativos')+': '+filters.join(' · ');
  }
  describe();
  vesselForm.addEventListener('submit',describe);
  if(vesselId && ship){
   const observer=new MutationObserver(()=>{describe();if(ship.value===vesselId||!ship.isConnected)observer.disconnect();});
   observer.observe(ship,{childList:true});
  }
  el('qs-clear').onclick=()=>{
   el('qs-status').value='active';el('qs-category').value='all';el('qs-assignment').value='all';
   el('qs-query').value='';vesselId='';if(ship)ship.value='';
   vesselForm.requestSubmit();
  };""")
    return source


def transforms():
    return {'app/static/fieldwork.js':toolbox,'app/static/qshe_reports.js':qshe,
            'app/static/operations_workspace_ui76.css':lambda s:s+(HERE/'hse_toolbox_filters.css').read_text(encoding='utf-8')}


if __name__=='__main__':
    apply=runpy.run_path(str(HERE/'apply_editor_exit.py'))['apply']
    apply(Path(sys.argv[1]),parent='0ff06c400b787f49da7ec299446d9bc4ecb2a13d6581345dc6382acd0e9751c5',overlays=(Path(__file__).name,),previous_cache='ui162-fault-filters',cache='ui162-hse-toolbox-filters',suffix='hse-toolbox-filters',scope='Responsive HSE and Toolbox Talks filters and toolbox project search.')
