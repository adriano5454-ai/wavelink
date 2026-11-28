"""Use the same authorised readings snapshot as Fleet, with no export-only access."""
from .fleet_tank_readings import read
from .localization import company_locale
from .store import Problem
from .wavelink_report_document import report_pdf, date_text, number
from .workbook_export import workbook_bytes, XLSX_MIME


def export_report(fleet, actor, sid, start, end, readonly, fmt):
    result = read(fleet, actor, sid, readonly, 'custom', start, end, not sid)
    pt = company_locale() == 'pt-BR'
    t = lambda en, br: br if pt else en
    heading = t('Water & fuel consumption','Consumo de água e combustível')
    names = {'fresh_water':t('Freshwater','Água doce'), 'diesel':'Diesel',
             'fuel_oil':t('Fuel oil','Óleo combustível'), 'other_fuel':t('Other fuel','Outro combustível')}
    base = [t('UTC period: ','Período UTC: ')+date_text(start,pt)+' - '+date_text(end,pt)]
    if readonly:
        base.append(t('Fictional demo records only. Unsaved practice entries are excluded.',
                      'Somente registros fictícios da demonstração. Testes não salvos não são incluídos.'))
    missing = t('No records','Sem registros')
    summary = []
    if not sid:
        metadata = [*base,t('Scope: all authorised vessels','Escopo: todas as embarcações autorizadas'),
                    t('Totals include recorded days only. Missing records do not mean zero consumption.',
                      'Os totais incluem apenas os dias registrados. Ausência de registro não significa consumo zero.')]
        rows = []
        for vessel in result['sites']:
            values = result['comparison'][vessel['id']]
            w,d=values.get('fresh_water'),values.get('diesel')
            rows.append([vessel['name'],w['total'] if w else missing,w['days'] if w else 0,
                         d['total'] if d else missing,d['days'] if d else 0])
        sheets = [dict(title=t('Fleet comparison','Comparação da frota'),metadata=metadata,
                       headers=[t('Vessel','Embarcação'),t('Freshwater (m³)','Água doce (m³)'),t('Recorded days','Dias registrados'),
                                'Diesel (L)',t('Recorded days','Dias registrados')],
                       types=['text','number','integer','number','integer'],rows=rows,widths=[1.75,1,1,1,1])]
    else:
        vessel = next((s for s in result['sites'] if s['id']==sid),None)
        if not vessel:
            raise Problem(404, 'Vessel not available.')
        base.append(t('Vessel: ','Embarcação: ')+vessel['name'])
        base.append(t('Recorded stock balances only. This does not include current tank levels.',
                      'Somente balanços de estoque registrados. Não inclui os níveis atuais dos tanques.'))
        totals,rows = [],[]
        for kind, data in result['consumption'].items():
            unit='m³' if kind=='fresh_water' else 'L'
            count=len(data)
            totals.append([names[kind],unit,sum(round(r['used']*1000) for r in data)/1000 if count else missing,count])
            rows.extend([r['day'],names[kind],unit,r['used'],r['opening'],r['closing'],r['received'],
                         r['produced'],r['transfer_in'],r['transfer_out'],r['other_out']] for r in data)
        sheets=[dict(title=t('Period totals','Totais do período'),metadata=base,
                     headers=[t('Product','Produto'),t('Unit','Unidade'),t('Consumption','Consumo'),t('Recorded days','Dias registrados')],
                     types=['text','text','number','integer'],rows=totals),
                dict(title=t('Daily balances','Balanços diários'),
                     headers=[t('UTC day','Dia UTC'),t('Product','Produto'),t('Unit','Unidade'),t('Used','Consumo'),
                              t('Opening','Inicial'),t('Closing','Final'),t('Received','Recebido'),t('Produced','Produzido'),
                              t('Transfer in','Transf. entrada'),t('Transfer out','Transf. saída'),t('Other out','Outras saídas')],
                     types=['date','text','text']+['number']*8,rows=sorted(rows,reverse=True))]
    if fmt == 'pdf':
        return report_pdf(heading,sheets,pt,demo=readonly,summary=summary),'application/pdf'
    if fmt == 'xlsx':
        return workbook_bytes(sheets), XLSX_MIME
    raise Problem(404, 'Report format not available.')
