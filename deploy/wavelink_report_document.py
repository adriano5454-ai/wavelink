"""Shared print-ready table reports using only scoped export data."""
import io
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import LongTable, Paragraph, SimpleDocTemplate, Spacer, TableStyle

NAVY = colors.HexColor('#102F43')
TEAL = colors.HexColor('#087F83')
SLATE = colors.HexColor('#405A70')
LIGHT = colors.HexColor('#EFF5F8')
EDGE = colors.HexColor('#B9CED8')


def date_text(s, pt):
    return '/'.join(s.split('-')[::-1]) if pt else s


def number(v, pt, min_places=0, max_places=3):
    try:
        d = Decimal(str(v))
        if not d.is_finite():
            return str(v)
        raw = f'{d:,.{max_places}f}'
    except (InvalidOperation, ValueError):
        return str(v)
    whole, _, fractional = raw.partition('.')
    frac = fractional.rstrip('0').ljust(min_places, '0')
    return (whole.replace(',','.') if pt else whole) + ((',' if pt else '.')+frac if frac else '')


def report_pdf(title, sheets, pt, *, demo=False, summary=()):
    label = lambda en, br: br if pt else en
    buf = io.BytesIO()
    w, h = landscape(A4)
    margin = 42
    doc = SimpleDocTemplate(buf, pagesize=(w,h),leftMargin=margin,rightMargin=margin,
                            topMargin=57,bottomMargin=46,title=title,author='WaveLink')
    def p(value,style='cell'):
        s = ('' if value is None else str(value)).replace('\r\n','\n').replace('\r','\n')
        return Paragraph(escape(s).replace('\n','<br/>') or '&#160;', styles[style])

    styles = {
        'title': ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=27,leading=32,textColor=NAVY,spaceAfter=9),
        'heading': ParagraphStyle('heading',fontName='Helvetica-Bold',fontSize=13,leading=17,textColor=NAVY,spaceBefore=12,spaceAfter=6,keepWithNext=True),
        'text': ParagraphStyle('text',fontSize=9,leading=13,textColor=SLATE,spaceAfter=4),
        'summary': ParagraphStyle('summary',fontName='Helvetica-Bold',fontSize=11,leading=15,textColor=TEAL,spaceAfter=4),
        'cell': ParagraphStyle('cell',fontSize=8.4,leading=11.5,textColor=NAVY,splitLongWords=True),
        'header': ParagraphStyle('header',fontName='Helvetica-Bold',fontSize=8.3,leading=11,textColor=colors.white),
    }
    now = datetime.now(timezone.utc)
    generated = (now.strftime('%d/%m/%Y %H:%M') if pt else now.strftime('%Y-%m-%d %H:%M'))+' UTC'
    def decorate(c,d):
        c.saveState()
        c.setFillColor(NAVY);c.rect(0,h-38,w,38,fill=1,stroke=0)
        c.setFillColor(colors.white);c.setFont('Helvetica-Bold',11);c.drawString(margin,h-24,'WAVELINK  /  '+label('REPORTS','RELATÓRIOS'))
        if demo:
            c.setFont('Helvetica-Bold',8);c.drawRightString(w-margin,h-24,label('DEMO DATA','DADOS FICTÍCIOS'))
        c.setStrokeColor(EDGE);c.line(margin,34,w-margin,34)
        c.setFillColor(SLATE);c.setFont('Helvetica',8)
        c.drawString(margin,20,label('Generated','Gerado em')+' '+generated)
        c.drawRightString(w-margin,20,label('Page','Página')+' '+str(d.page));c.restoreState()

    def cell(v,kind):
        if kind == 'date' and isinstance(v,str) and len(v)==10 and v[4:5]=='-' and v[7:8]=='-':
            return date_text(v,pt)
        if kind in ('integer','amount','number') and v not in ('',None):
            return number(v,pt,2 if kind=='amount' else 0)
        return v

    story = [p(title,'title')]
    story.extend(p(x,'summary') for x in summary)
    headers = ('headers', 'types', 'rows')
    for i,sheet in enumerate(sheets):
        if len(sheets)>1:
            story.append(p(sheet['title'],'heading'))
        story.extend(p(x,'text') for x in sheet.get('metadata',()))
        cols,kinds,rows=(sheet[k] for k in headers)
        if not rows:
            story.append(p(label('No records match these filters.','Nenhum registro corresponde aos filtros.'),'summary'))
            continue
        story.append(Spacer(1,6))
        weights=sheet.get('widths',[1.42 if kind=='text' else .9 for kind in kinds])
        usable=w-2*margin-12
        t=LongTable([[p(x,'header') for x in cols]]+[
            [p(cell(v,k)) for v,k in zip(row,kinds)] for row in rows
        ], colWidths=[usable*x/sum(weights) for x in weights], repeatRows=1, splitInRow=1, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),(colors.white,LIGHT)),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LINEBELOW',(0,0),(-1,0),1,TEAL),('LINEBELOW',(0,-1),(-1,-1),.6,EDGE),
        ]))
        story.append(t)
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
    return buf.getvalue()


def expense_summary(sheet, pt):
    totals = {}
    for row in sheet['rows']:
        try:
            n = Decimal(str(row[4]))
            if n.is_finite() and row[5]:
                totals[row[5]] = totals.get(row[5], Decimal(0))+n
        except InvalidOperation:
            continue
    if not totals:
        return []
    return [('Valores listados (todas as situações; não confirma pagamento): ' if pt else
             'Listed claims (all statuses; not a payment total): ')+
            '  |  '.join(code+' '+number(total,pt,2,2) for code,total in sorted(totals.items()))]
