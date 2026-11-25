from pathlib import Path
import runpy
import sys

BASE=Path(__file__).resolve().parent
replace=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']


def ui(s):
    s=replace(s,' const searchRecord=',(BASE/'hr_employee_context.js').read_text('utf8')+'\n const searchRecord=')
    s=replace(s,'||newProfileDocument.test(hash)||searchRecord.test(hash)','||newProfileDocument.test(hash)||employeeRecords.test(hash)||searchRecord.test(hash)')
    s=replace(s,'const match=location.hash.match(newProfileDocument)||','const match=location.hash.match(employeeRecords)||location.hash.match(newProfileDocument)||')
    s=replace(s,"owner=next;account=acct;generation++","employeeReturn=null;returningToEmployee=false;owner=next;account=acct;generation++")
    s=replace(s,"const hash=location.hash;if(host", """const hash=location.hash,recordRoute=hash.match(employeeRecords);
  returningToEmployee=employeeRecords.test(lastHash)&&employeeReturn?.hash===hash;
  if(recordRoute)view=recordRoute[2];
  else if(employeeRecords.test(lastHash)&&(/^#hr\\/staff\\/[0-9a-f-]{36}$/.test(hash)||hash===employeeReturn?.hash))view='people';
  else if(!host?.isConnected&&/^#hr\\/staff\\/[0-9a-f-]{36}$/.test(hash))view='people';
  if(host""")
    a='  const ticket=++generation,session=owner,queryFilters={...workspaceFilters};'
    s=replace(s,a,"""  const layout=!force&&view==='people'&&/^#hr\\/staff\\/[0-9a-f-]{36}$/.test(hash)&&host?.isConnected&&host.querySelector('.hr-person-layout');
  const previousTabs=layout?JSON.stringify(tabs()):null;
  if(layout){
    host.dataset.hrRoute=hash;
    const detail=layout.querySelector(':scope > section');detail.setAttribute('aria-busy','true');
    detail.textContent=wtext('Carregando perfil…','Loading profile…');
  }
"""+a)
    s=replace(s,'   renderOverview();\n   if(createDocument)',"""   if(layout&&view==='people'&&workspace&&previousTabs===JSON.stringify(tabs())&&replaceEmployeePanel(layout))return;
   renderOverview();
   if(createDocument)""")
    s=replace(s,"else if(overview)status(", "else if(overview&&!layout)status(")
    s=replace(s,"   else{node.innerHTML=AJInterface.markup", "   else{overview=null;workspace=null;node.innerHTML=AJInterface.markup")
    s=replace(s,"(workspace?.people?.find(p=>p.id===person.id)?.departments||[]).map(d=>d.name).join(' ')","employeeDepartments(person).join(' ')")
    s=replace(s,"(workspace.people.find(v=>v.id===p.id)?.departments||[]).map(d=>d.name).join(', ')","employeeDepartments(p).join(', ')")
    s=replace(s,"  renderRecords();renderReceipt();H.nav();","  renderRecords();recordContext();restoreEmployee();renderReceipt();H.nav();")
    s=replace(s,"  el('hr-report-kind')?.addEventListener", """  if(view==='people'){const panel=body.querySelector('.hr-person-layout > section');if(panel)bindEmployeePanel(panel)}
  el('hr-report-kind')?.addEventListener""")
    # bindEmployeePanel owns all person detail actions; generic dashboard actions stay intact.
    s=s.replace("body.querySelectorAll('[data-hr-cert-create]')","body.querySelectorAll(':not(.hr-person-layout *)[data-hr-cert-create]')")
    s=replace(s,"  el('hr-person-edit')?.addEventListener('click',()=>{if(ready())beginForm('people',overview.people?.[0]||null,'save');});\n","")
    s=replace(s,'if(!handles()&&!form){generation++','if(!handles()&&!form){employeeReturn=null;returningToEmployee=false;generation++')
    s=replace(s,'function ready(){return current()&&!form&&!contextBusy();}', """function ready(){
  const selecting=reading&&host?.querySelector('.hr-person-layout > [aria-busy="true"]');
  return current()&&!form&&!contextBusy()&&(!selecting||host.querySelector('.hr-person-layout aside')?.contains(document.activeElement));
 }""")
    s=replace(s,'view=b.dataset.hrTab;query=', 'if(employeeSectionRoute(b.dataset.hrTab))return;view=b.dataset.hrTab;query=')
    s=replace(s,'view=e.target.value;query=', 'if(employeeSectionRoute(e.target.value))return;view=e.target.value;query=')
    return s


def transforms():
    return {'app/static/hr_workspace.js':ui,'app/static/hr_workspace.css':lambda s:s+"""
.hr-person-layout{align-items:start}
.hr-person-layout .hr-person-list{overflow:auto;max-height:55vh;overscroll-behavior:contain}
.hr-person-layout>section{overflow:auto;max-height:76vh;min-width:0}
.hr-employee-context{display:flex;align-items:center;justify-content:space-between;gap:.5rem;flex-wrap:wrap;position:sticky;top:4rem;background:var(--surface,#fff);z-index:2;padding:.5rem}
@media(max-width:700px){.hr-person-layout .hr-person-list{max-height:29vh}.hr-person-layout>section{max-height:none;overflow:visible}}
"""}


if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='ef11eae1e4d6e527a24b205ee5d4c799e646868c49335674096da28d69237238',overlays=(Path(__file__).name,),previous_cache='ui162-org-chart-viewport',cache='ui162-employee-context',suffix='employee-context',scope='Preserve employee selection and return context for authorized HR records.')
