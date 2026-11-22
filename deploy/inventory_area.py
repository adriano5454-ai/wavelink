"""Expose the existing item ownership filter alongside Inventory search."""
def fieldwork(source):
    start = source.index("${select('department',__wl118.t('Owning department')")
    end = source.index("${select('source',", start)
    field = source[start:end]
    source = source[:start] + source[end:]
    def change(old, new):
        nonlocal source
        if source.count(old) != 1:
            raise ValueError("Unexpected Inventory UI: " + old)
        source = source.replace(old, new)
    field = field.replace("__wl118.t('Owning department')", "txt('Área responsável (departamento)','Responsible area (department)')")
    field = field.replace("__wl118.t('All departments')", "txt('Todas as áreas','All areas')")
    field = field.replace('__wl118.t(__wl118.t("Unassigned"))', "txt('Sem área responsável','No responsible area')")
    change("${inventoryVesselField(vessels)}${button('inv-category-toggle'", "${inventoryVesselField(vessels)}" + field + "${button('inv-category-toggle'")
    change("inventoryFilter={query:'',location:'',department:'',source:'',archived:!!byid.get(focusId)?.archived}",
           "inventoryFilter={...inventoryFilter,archived:!!byid.get(focusId)?.archived}")
    change("x.department_id===(inventoryFilter.department", "(x.department_id||'')===(inventoryFilter.department")
    change("labels.push(b.directory.departments.find(x=>x.id===inventoryFilter.department)?.name||__wl118.t('Unassigned department'))",
           "labels.push(txt('Área responsável','Responsible area')+' · '+(b.directory.departments.find(x=>x.id===inventoryFilter.department)?.name||txt('Sem área responsável','No responsible area')))")
    change("const categoryRows=b.items.filter(x=>(!vesselId", "const categoryRows=b.items.filter(x=>(!inventoryFilter.department||(x.department_id||'')===(inventoryFilter.department==='__unassigned'?'':inventoryFilter.department))&&(!vesselId")
    return source


def transforms():
    return {'app/static/fieldwork.js': fieldwork}
