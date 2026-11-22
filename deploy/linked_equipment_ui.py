"""Wire the existing work-site controls to the reviewed equipment links."""
from pathlib import Path

HERE = Path(__file__).parent


def replace(*edits):
    def apply(source):
        for old, new in edits:
            if source.count(old) != 1:
                raise ValueError('Unexpected linked-equipment UI source at ' + old[:96])
            source = source.replace(old, new)
        return source
    return apply


def transforms():
    common = (HERE / 'equipment_site_hint.js').read_text(encoding='utf-8')
    return {'app/static/' + path: transform for path, transform in {
        'action_center_ui82.js': replace(
            (' function picker(host, api,', common + '\n function picker(host, api,'),
            ('    if(initial)onPick?.(initial);',
             '    if(initial)onPick?.(initial);\n    refreshEquipmentSite(select);'),
            ("  if(siteInput){\n   const sync=", """  if(['General task','Verification task','Asset maintenance order','Certificate draft'].includes(kind)){
   const selected=restore?.values?.work_site_id || original.work_site?.id || '';
   prepareEquipmentSite(control.select,{selected,hint:restore?.values?.equipment_site_hint||''});
  }
  if(siteInput){
   const sync="""),
            ('Object.freeze({body,words,label,choose,describe,options,active,picker,nameField,fw})',
             'Object.freeze({body,words,label,choose,describe,options,active,picker,nameField,fw,prepareEquipmentSite,equipmentSites,equipmentHint,equipmentBody})')),
        'fieldwork.js': replace(
            ('draft.values=values;draft.updated=', """const hint=locationField&&WLWorkSites.equipmentHint(locationField.select);
   if(hint)values.equipment_site_hint=hint;
   draft.values=values;draft.updated="""),
            ('if(locationField)(payload.task||payload).work_site_id=siteId;', """if(locationField){
    const record=payload.task||payload;
    const site=WLWorkSites.equipmentBody(locationField.select,siteId);
    if(site.equipment_site_hint)delete record.work_site_id;
    else delete record.equipment_site_hint;
    Object.assign(record,site);
   }""")),
        'report_forms.js': replace(
            ("const rows=[...items],v=p[key]||'';", "const rows=[...items],v=p[key]||(key==='work_site_id'?p.equipment_site_hint:'')||'';"),
            ("  if($('evidence-files'))o.bindEvidence", """  if(a==='create'){
   const site=$('work_site_id');
   WLWorkSites.prepareEquipmentSite(site,{selected:p.work_site_id,hint:p.equipment_site_hint,onUpdate:()=>{
    const choice=WLWorkSites.equipmentBody(site,site.value);
    if(choice.equipment_site_hint)delete p.work_site_id;
    else delete p.equipment_site_hint;
    Object.assign(p,choice);
   }});
  }
  if($('evidence-files'))o.bindEvidence"""),
            ("f.sourceReviewed=true;p[(a==='create'?'asset':'task')+'_link']={id:x.id,", """if(a==='create')WLWorkSites.equipmentSites($('work_site_id'),[x.work_site]);
    f.sourceReviewed=true;p[(a==='create'?'asset':'task')+'_link']={id:x.id,"""),
            ("f.sourceError=false;f.sourceReviewed=true;p[(a==='create'?'asset':'task')+'_link']=null;",
             "f.sourceError=false;f.sourceReviewed=true;if(a==='create')WLWorkSites.equipmentSites($('work_site_id'),[]);p[(a==='create'?'asset':'task')+'_link']=null;")),
        'task_create.js': replace(
            ("f.querySelector('#tf-link-update').hidden=!current||current.current_version===r.version;", """f.querySelector('#tf-link-update').hidden=!current||current.current_version===r.version;
   if(!r || current?.current_version===r.version)WLWorkSites.equipmentSites(f.elements.work_site_id,r?[current.work_site]:[]);
  """)),
        'general_tasks.js': replace(
            ("function show(){f.querySelectorAll('[data-gt-step]')", """function show(){const r=linkRef(),row=r&&options.find(item=>item.id===r.id&&item.kind===r.kind);
   if(!r || row?.current_version===r.version)WLWorkSites.equipmentSites(f.elements.work_site_id,r?[row.work_site]:[]);
   f.querySelectorAll('[data-gt-step]')""")),
        'assets.js': replace(
            ("'Certificate draft',{id:r.id||'',version:r.version||0}", """'Certificate draft',{id:r.id||'',version:r.version||0,...(r.id?{certificate:{work_site:r.work_site}}:{})}"""),
            ('  AJMaintenanceForms.attachCreate(f,data,restore,x);', """  AJMaintenanceForms.attachCreate(f,data,restore,x);
  WLWorkSites.equipmentSites(f.elements.work_site_id,[x.equipment_work_site]);""")),
        'asset_workspace.js': replace(
            ("${fact(pos.location_label,pos.location)}",
             "${x.equipment_work_site?.name?fact(WLWorkSites.label(),x.equipment_work_site.name):''}${fact(pos.location_label,pos.location)}")),
        'maintenance_forms.js': replace(
            ("[__wl118.t('Item'),asset.name],[__wl118.t('Serial number'),asset.serial]",
             "[__wl118.t('Item'),asset.name],...(asset.equipment_work_site?.name?[[WLWorkSites.label(),asset.equipment_work_site.name]]:[]),[__wl118.t('Serial number'),asset.serial]")),
        'certificate_form.js': replace(
            ('  let ownError=null;', '  let ownError=null;\n  const equipmentById=new Map(d.items.map(item=>[item.id,item]));'),
            ("   const checked=f.querySelectorAll('input[name^=\"asset_\"]:checked').length;", """   const checked=v.asset_ids.length;
   WLWorkSites.equipmentSites(f.elements.work_site_id,v.asset_ids.map(id=>equipmentById.get(id)?.work_site));""")),
        'operations.js': replace(
            ("   f.querySelector('#task-scope-summary').textContent=", """   const scopeById=new Map(all.map(item=>[item.id,item]));
   WLWorkSites.equipmentSites(f.elements.work_site_id,expanded().map(id=>scopeById.get(id)?.work_site));
   f.querySelector('#task-scope-summary').textContent=""")),
        'inventory_workspace.js': replace(
            ("f.elements.department_id.value);f.querySelector('#stock-filter-fields')", """f.elements.department_id.value);
   WLWorkSites.equipmentSites(workLocation.select,proposal.items.map(item=>item.equipment_work_site));
   f.querySelector('#stock-filter-fields')"""),
            ("catch(e){proposal=null;f.querySelector('#stock-scope-preview')", """catch(e){proposal=null;WLWorkSites.equipmentSites(workLocation.select,[]);f.querySelector('#stock-scope-preview')"""),
            ('request={work_site_id:site,list_id:b.id,name:', 'request={...WLWorkSites.equipmentBody(workLocation.select,site),list_id:b.id,name:')),
    }.items()}
