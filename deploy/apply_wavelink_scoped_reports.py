"""Add scoped, reusable PDF reports and Fleet spreadsheets."""
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent


def once(s, a, b):
    if s.count(a) != 1:
        raise ValueError(a)
    return s.replace(a, b, 1)


def hr_export(s):
    s = once(s, 'def export_workbook(hr, actor, scope, kind, token):',
                'def report_sheet(hr, actor, scope, kind, token):')
    a = s.index('    return workbook_bytes([{"title": title')
    return s[:a]+'''    return {"title": title, "metadata": metadata, "headers": [col[lang] for col in schema],
            "types": [col[2] for col in schema], "rows": rows}


def export_workbook(hr, actor, scope, kind, token):
    return workbook_bytes([report_sheet(hr, actor, scope, kind, token)])


def export_pdf(hr, actor, scope, kind, token, demo=False):
    from .wavelink_report_document import expense_summary, report_pdf
    sheet = report_sheet(hr, actor, scope, kind, token)
    pt = company_locale() == "pt-BR"
    sheet['metadata'] = [*sheet['metadata']]
    if kind == "expenses":
        sheet['metadata'].append("Aprovação de reembolso não confirma pagamento." if pt else
                                 "Approval of a claim does not confirm payment.")
    if kind == "timesheets":
        sheet['metadata'].append("Apontamentos não constituem folha de pagamento." if pt else
                                 "Timesheets are not payroll records.")
    return report_pdf(sheet['title'], [sheet], pt, demo=demo,
                      summary=expense_summary(sheet, pt) if kind == "expenses" else ())
'''


def hr_api(s):
    return once(s, "    from . import org_positions", """    @app.get('/api/hr/reports/{kind}.pdf')
    def report_pdf(request:Request,kind:str,start_on:str,end_on:str,token:str,user_id:str='',location:str='',project:str='',department_id:str='',vessel_id:str='',person=Depends(logged)):
        from .hr_report_export import export_pdf
        scope = dict(start_on=start_on, end_on=end_on, user_id=user_id, location=location, project=project, department_id=department_id)
        if vessel_id: scope['vessel_id']=vessel_id
        content = export_pdf(store.hr, person, scope, kind, token, getattr(request.state,'public_demo_read_only',False))
        headers = dict(PRIVATE_HEADERS)
        headers['Content-Disposition'] = f'attachment; filename="hr-{kind}-{start_on}.pdf"'
        return Response(content, media_type='application/pdf', headers=headers)

    from . import org_positions""")


def hr_js(s):
    s = once(s, """el('hr-export-xlsx')?.addEventListener('click',exportExcelReport);lockReportButtons();""",
                """el('hr-export-xlsx')?.addEventListener('click',()=>exportFileReport('xlsx'));
  el('hr-export-pdf')?.addEventListener('click',()=>exportFileReport('pdf'));lockReportButtons();""")
    s = once(s, "button('hr-export-xlsx',wtext(", """button('hr-export-pdf',wtext('Baixar PDF','Download PDF'))+button('hr-export-xlsx',wtext(""")
    s = once(s, """const csv=el('hr-export-csv'),xlsx=el('hr-export-xlsx');
  if(csv)csv.disabled=reading;
  if(xlsx)xlsx.disabled=reading||!workspace?.report_tokens?.[reportKind]||xlsx.dataset.preparing==='true';""",
                """const csv=el('hr-export-csv');
  if(csv)csv.disabled=reading;
  for(const b of [el('hr-export-pdf'),el('hr-export-xlsx')])if(b)b.disabled=reading||!workspace?.report_tokens?.[reportKind]||b.dataset.preparing==='true';""")
    s = once(s, """async function exportExcelReport(){
  const button=el('hr-export-xlsx'),kind=reportKind,snapshot=workspace,scope=workspaceScope;""",
                """async function exportFileReport(format){
  const id='hr-export-'+format,button=el(id),kind=reportKind,snapshot=workspace,scope=workspaceScope;""")
    s = once(s, """&&el('hr-export-xlsx')===button&&canSection(kind)""", """&&el(id)===button&&canSection(kind)""")
    s = once(s, """'/api/hr/reports/'+kind+'.xlsx?'+query""", """'/api/hr/reports/'+kind+'.'+format+'?'+query""")
    s = once(s, """'rh-'+kind+'-'+scope.start_on+'.xlsx'""", """'rh-'+kind+'-'+scope.start_on+'.'+format""")
    return once(s, """if(el('hr-export-xlsx')===button)lockReportButtons();""", """if(el(id)===button)lockReportButtons();""")


def fleet_api(s):
    return once(s, """    @app.get('/api/fleet/receiving')""", """    @app.get('/api/fleet/consumption-report/{fmt}')
    def consumption_report(request: Request, fmt: str, start: str, end: str, site_id: str='', a=Depends(logged)):
        from .wavelink_fleet_report_model import export_report
        data, mime = export_report(store.fleet,a,site_id,start,end,getattr(request.state,'public_demo_read_only',False),fmt)
        return Response(data,media_type=mime,headers={'Cache-Control':'no-store',
            'Referrer-Policy':'no-referrer','X-Content-Type-Options':'nosniff',
            'Content-Disposition':f'attachment; filename="wavelink-water-fuel-{start}.{fmt}"'})

    @app.get('/api/fleet/receiving')""")


def fleet_ui(s):
    start = 'function renderFleetConsumptionComparison(card,result,make){'
    s = once(s,start,"""function fleetReportActions(id,range,make){
 const block=make('div');block.className='actions';block.id='fleet-consumption-downloads';
 block.setAttribute('role','group');block.setAttribute('aria-label',fmT('Relatórios de consumo','Consumption reports'));
 const status=make('p');status.setAttribute('role','status');
 for(const [format,label] of [['pdf',fmT('Relatório PDF','PDF report')],['xlsx',fmT('Baixar Excel','Download Excel')]]){
  const b=make('button',label);b.type='button';b.className='btn';b.dataset.format=format;block.append(b);
  b.onclick=async()=>{
   const query=new URLSearchParams({start:range.from,end:range.to,...(id?{site_id:id}:{})});
   b.disabled=true;status.textContent=fmT('Preparando relatório…','Preparing report…');
   try{await download('/api/fleet/consumption-report/'+format+'?'+query,'wavelink-water-fuel-'+range.from+'.'+format);
       status.textContent='';}
   catch(e){if(block.isConnected&&!e?.obsolete&&!e?.fleetHandled)status.textContent=e.userMessage||e.message;}
   finally{if(block.isConnected)b.disabled=false;}
  };
 }
 block.append(status);
 return block;
}

"""+start)
    s = once(s,"card.append(readingRangeControls(make,result.range));renderFleetConsumptionComparison(card,result,make);return;",
               "card.append(readingRangeControls(make,result.range),fleetReportActions('',result.range,make));renderFleetConsumptionComparison(card,result,make);return;")
    # Keep reports on the consumption tab, not the tank-level view.
    return once(s," const balance=renderConsumption(card,result,site,kinds,make);",
                  " const balance=renderConsumption(card,result,site,kinds,make);\n balance.prepend(fleetReportActions(id,result.range,make));")


def additions():
    names = ('wavelink_fleet_report_model.py','wavelink_report_document.py')
    return {'app/'+n:(BASE/n).read_bytes() for n in names}


def transforms():
    return {'app/hr_api.py':hr_api,'app/hr_report_export.py':hr_export,'app/static/hr_workspace.js':hr_js,
            'app/fleet_api.py':fleet_api,'app/static/fleet.js':fleet_ui}


if __name__ == '__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='3c2bfe2689e5fed57d1f3c2e0686ca05b33a5a687aa2d53221912c7c94342d7c',
        overlays=(Path(__file__).name,), previous_cache='ui162-fleet-graphs-first', cache='ui162-scoped-app-reports',
        suffix='scoped-app-reports',scope='Reusable PDF summaries for HR and scoped PDF/XLSX consumption reports.')
