from pathlib import Path
import runpy
import sys

BASE=Path(__file__).resolve().parent
one=runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']


def ui(s):
    s=one(s,'function bindEmployeePanel(panel){',(BASE/'hr_employee_record_panel.js').read_text('utf8')+'\nfunction bindEmployeePanel(panel){')
    s=one(s,"forEach((button,index)=>button.onclick=()=>{","forEach((button,index)=>{const full=()=>{")
    a="location.hash='#hr/staff/'+overview.person.id+'/'+button.dataset.hrJump;\n });"
    s=one(s,a,"""location.hash='#hr/staff/'+overview.person.id+'/'+button.dataset.hrJump;
   };
   if(['documents','expenses'].includes(button.dataset.hrJump)){
     button.openEmployeeSheet=fromHistory=>showEmployeeSheet(button.dataset.hrJump,button,index,full,fromHistory);
     button.onclick=()=>button.openEmployeeSheet(false);
   }else button.onclick=full;
 });""")
    s=one(s,"detail.textContent=wtext('Carregando perfil…','Loading profile…');","detail.inert=true;")
    s=one(s,"status(__wl118.t('Refreshing saved HR records…'));lockReportButtons();","if(!layout)status(__wl118.t('Refreshing saved HR records…'));lockReportButtons();")
    s=one(s,'function card(kind,row){','function card(kind,row,actions=true){')
    s=one(s,'+compactRecordButtons(kind,row)+','+(actions?compactRecordButtons(kind,row):\'\')+')
    s=one(s,'if(next!==owner){if(dialogView','if(next!==owner){dismissEmployeeSheet(false);sheetFullAction=null;if(dialogView')
    return one(s,'if(!handles()&&!form){employeeReturn=null;', 'if(!handles()&&!form){dismissEmployeeSheet(false);sheetFullAction=null;employeeReturn=null;')


def transforms():
    return {'app/static/hr_workspace.js':ui,'app/static/hr_workspace.css':lambda s:s+"""
.hr-employee-sheet{position:fixed;inset:0 0 0 auto;box-sizing:border-box;margin:0;width:min(34rem,100vw);height:100dvh;max-height:100dvh;max-width:100%;padding:0;border:1px solid var(--line);background:var(--surface,#fff);color:inherit}
.hr-employee-sheet[open]{display:flex;flex-direction:column}
.hr-employee-sheet::backdrop{background:rgb(10 26 36/.38)}
.hr-employee-sheet header,.hr-employee-sheet footer,.hr-employee-sheet-body{padding:1rem}
.hr-employee-sheet>header{display:grid;grid-template-columns:1fr auto;gap:.25rem;align-items:center;border-bottom:1px solid var(--line)}
.hr-employee-sheet>header h2{grid-column:1;margin:0;font-size:1.2rem}
.hr-employee-sheet>header button{grid-row:1/3;grid-column:2}
.hr-employee-sheet-body{overflow:auto;flex:1;min-height:0}
.hr-employee-sheet-body label{display:grid;gap:.3rem;margin-bottom:.75rem}
.hr-employee-sheet footer{border-top:1px solid var(--line)}
@media(max-width:700px){.hr-employee-sheet{inset:auto 0 0;width:100%;height:min(80dvh,48rem);border-radius:1rem 1rem 0 0;padding-bottom:env(safe-area-inset-bottom)}}
"""}


if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='d1beee2152eff9de825080f96530a8863baac15d11b171b7631835eaaf95450d',
        overlays=(Path(__file__).name,),previous_cache='ui162-handover-files-return',cache='ui162-employee-sheet',
        suffix='employee-sheet',scope='Read an employee’s certificates and expenses in context without leaving their profile.')
