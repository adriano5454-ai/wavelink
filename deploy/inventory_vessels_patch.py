"""Add the Fleet vessel filter to both levels of the native Inventory browser."""


def fieldwork(source):
    def replace(old, new):
        nonlocal source
        if source.count(old) != 1:
            raise ValueError('Unexpected Inventory browser source: ' + old[:80])
        source = source.replace(old, new)

    replace("url='/api/inventory/lists';kind='catalogue'", "url='/api/inventory/lists?include_vessels=true';kind='catalogue'")
    replace("kind==='catalogue'&&!Array.isArray(data)", "kind==='catalogue'&&(!Array.isArray(data?.lists)||!Array.isArray(data?.vessels))")
    replace("const lists=await api('/api/inventory/lists');return paint(lists,inventoryHome);",
            "const catalogue=await api('/api/inventory/lists?include_vessels=true');return paint(catalogue,inventoryHome);")
    replace(" function inventoryHome(lists){", """ function inventoryVesselOptions(vessels){
  const text=window.WavelinkUX.text;
  return [['',text('Todas as embarcações','All vessels')],...vessels.map(site=>[site.id,
   [site.name,site.code,site.active?'':text('Inativa','Inactive')].filter(Boolean).join(' · ')])];
 }
 function inventoryVesselField(vessels){
  const label=window.WavelinkUX.text('Embarcação','Vessel');
  return `<label class="inventory-vessel-filter"><span>${esc(label)}</span><select name="inventory_vessel">${options(inventoryVesselOptions(vessels),inventoryCatalogFilter.vessel||'')}</select></label>`;
 }
 function inventoryHome({lists,vessels}){
  if(!vessels.some(site=>site.id===inventoryCatalogFilter.vessel))inventoryCatalogFilter.vessel='';""")
    replace('    <button type="button" class="btn secondary" id="inventory-catalog-clear"', '''    ${inventoryVesselField(vessels)}
    <button type="button" class="btn secondary" id="inventory-catalog-clear"''')
    replace("const clear=host.querySelector('#inventory-catalog-clear'),archive=", "const vessel=host.querySelector('[name=inventory_vessel]');\n  const clear=host.querySelector('#inventory-catalog-clear'),archive=")
    replace("const records=Number(book.item_count)||0,", "const records=Number(inventoryCatalogFilter.vessel?book.vessel_counts?.[inventoryCatalogFilter.vessel]:book.item_count)||0,")
    replace("<span>${esc(countLabel)}</span><span>${esc(categoryLabel)}</span>${checks?", "<span>${esc(countLabel)}</span>${inventoryCatalogFilter.vessel?'':`<span>${esc(categoryLabel)}</span>`}${checks&&!inventoryCatalogFilter.vessel?")
    replace("const matches=book=>!query||searchKey(book.name+' '+(book.description||'')).includes(query);",
            """const vesselId=inventoryCatalogFilter.vessel;
   const matches=book=>(!vesselId||book.vessel_counts?.[vesselId]>0)&&(!query||searchKey(book.name+' '+(book.description||'')).includes(query));""")
    replace("clear.hidden=!inventoryCatalogFilter.query;", """clear.hidden=!query&&!vesselId;
   clear.textContent=vesselId?text('Limpar filtros','Clear filters'):text('Limpar busca','Clear search');""")
    replace("const count=query?text(", "const count=(query||vesselId)?text(")
    replace("}else if(query){\n    title=text('Nenhum inventário encontrado'", """}else if(vesselId){
    title=text('Nenhum inventário encontrado','No matching inventories');
    description=hasArchivedMatch?text('Há resultados entre os inventários arquivados.','Archived inventories match these filters.'):
     query?text('Experimente outro nome ou outra embarcação.','Try another name or select another vessel.'):
     text('Nenhum inventário nesta lista tem registros ativos nessa embarcação.','No inventory in this list has active records on this vessel.');
   }else if(query){
    title=text('Nenhum inventário encontrado'""")
    replace("clear.onclick=()=>{inventoryCatalogFilter.query='';searchInput.value='';draw();searchInput.focus();};",
            """vessel.onchange=()=>{inventoryCatalogFilter.vessel=vessel.value;draw();};
  clear.onclick=()=>{inventoryCatalogFilter.query='';inventoryCatalogFilter.vessel='';vessel.value='';searchInput.value='';draw();searchInput.focus();};""")
    replace("lists=data;draw();AJInventoryWorkspace.restoreAnchor(a);", """lists=data.lists;
   if(JSON.stringify(vessels)!==JSON.stringify(data.vessels)){
    vessels=data.vessels;
    if(!vessels.some(site=>site.id===inventoryCatalogFilter.vessel))inventoryCatalogFilter.vessel='';
    vessel.innerHTML=options(inventoryVesselOptions(vessels),inventoryCatalogFilter.vessel);
   }
   draw();AJInventoryWorkspace.restoreAnchor(a);""")
    replace("  const txt=window.WavelinkUX.text;\n  if(boxesContext", """  const txt=window.WavelinkUX.text;
  const vessels=b.vessels||[],vesselNames=new Map(vessels.map(site=>[site.id,site.name]));
  if(!vesselNames.has(inventoryCatalogFilter.vessel))inventoryCatalogFilter.vessel='';
  if(boxesContext""")
    replace("${button('inv-category-toggle',__wl118.t('Category'))}", "${inventoryVesselField(vessels)}${button('inv-category-toggle',__wl118.t('Category'))}")
    replace("const searching=!!(q||inventoryFilter.location", "const searching=!!(q||inventoryCatalogFilter.vessel||inventoryFilter.location")
    replace("if(q)rows=rows.filter(x=>AJVerification.matches(x,q));", """const vesselId=inventoryCatalogFilter.vessel;
   if(vesselId)rows=rows.filter(x=>x.vessel_id===vesselId);
   if(q)rows=rows.filter(x=>AJVerification.matches(x,q));""")
    replace("const categoryRows=b.items.filter(x=>x.id!==viewBox", "const categoryRows=b.items.filter(x=>(!vesselId||x.vessel_id===vesselId)&&x.id!==viewBox")
    replace("const scopeLabel=searching?", "const scopeLabel=vesselId&&!activeBox?vesselNames.get(vesselId):searching?")
    replace("  for(const k of ['search','location','department','source'])", """  $('[name=inventory_vessel]',root).onchange=e=>{inventoryCatalogFilter.vessel=e.target.value;draw();};
  for(const k of ['search','location','department','source'])""")
    replace("function clearFilters(){inventoryCategory=", "function clearFilters(){inventoryCatalogFilter.vessel='';inventoryCategory=")
    replace("x.archived,x.locations,x.extra_fields", "x.archived,x.locations,x.vessels,x.extra_fields")
    replace("const loc=inventoryLocationLabel(x.location)||'';", """const local=inventoryLocationLabel(x.location)||'',ship=vesselNames.get(x.vessel_id)||'';
   const loc=ship&&(!local||x.location==='Unassigned'||ship===local)?ship:[ship,local].filter(Boolean).join(' · ');""")
    return source


def styles(source):
    return source + """
.iw162-catalogue-search>.inventory-vessel-filter,
#app .inv-browser .iw-search-row>.inventory-vessel-filter {
  display:grid; gap:.3rem; flex:1 1 12rem; min-width:0; margin:0;
}
.inventory-vessel-filter>span {font-size:.875rem; font-weight:650;}
.inventory-vessel-filter>select {width:100%; min-width:0; min-height:44px;}
@media (max-width:600px){
  .iw162-catalogue-search>.inventory-vessel-filter,
  #app .inv-browser .iw-search-row>.inventory-vessel-filter {flex-basis:100%;}
}
"""


def transforms():
    return {'app/static/fieldwork.js': fieldwork, 'app/static/inventory_navigation.css': styles}
