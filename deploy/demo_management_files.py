"""Downloadable examples for the public preview. All content belongs to the fictional catalogue."""
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from .demo_management_data import BY_RECORD, EVIDENCE


_DOCUMENTS = {
    'training': ('TREINAMENTO-EXEMPLO.pdf', 'personnel', 'survival'),
    'itinerary': ('BILHETE-EXEMPLO.pdf', 'travel', 'lia-flight'),
    'expense': ('RECIBO-EXEMPLO.pdf', 'expenses', 'taxi'),
    'it-report': ('PORTA-REDE-EXEMPLO.pdf', 'it', 'ticket-018'),
    'calibration': ('CAL-204-EXEMPLO.pdf', 'certificates', 'cal204'),
    'observation': ('CONVES-EXEMPLO.pdf', 'safety', 'route'),
    'report': ('OCN-001-EXEMPLO.pdf', 'branding', 'cover'),
    'manifest': ('MF-014-EXEMPLO.xlsx', 'documents', 'manifest'),
}
SAMPLE_FILES = {filename: key for key, (filename, _, _) in _DOCUMENTS.items()}
_XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


@lru_cache(maxsize=16)
def sample_file(key, language):
    """Accept only the eight fixed examples and the two presentation languages."""
    if key not in _DOCUMENTS or language not in ('en', 'pt'):
        return None
    filename, section, record = _DOCUMENTS[key]
    if key == 'manifest':
        return filename, _XLSX, Path(__file__).with_name('demo_manifest.xlsx').read_bytes()

    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    pt = language == 'pt'
    example = BY_RECORD[section, record]
    title = example.title[pt]
    out = BytesIO()
    doc = SimpleDocTemplate(out, pagesize=A4, title=title, author='Maré Alta Surveys',
                            leftMargin=22*mm, rightMargin=22*mm, topMargin=26*mm, bottomMargin=22*mm)
    ink = colors.HexColor('#173846')
    teal = colors.HexColor('#006e73')
    heading = ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=23, leading=28, textColor=ink)
    body = ParagraphStyle('body', fontName='Helvetica', fontSize=11, leading=15, textColor=ink)
    field = ParagraphStyle('field', parent=body, fontName='Helvetica-Bold', fontSize=10, textColor=teal)
    mark = 'Documento fictício de demonstração' if pt else 'Fictional demonstration document'
    items = [Paragraph('Maré Alta Surveys', field), Spacer(0, 8), Paragraph(escape(title), heading),
             Spacer(0, 6), Paragraph(mark, body), Spacer(0, 20)]
    rows = [[Paragraph(escape(label[pt]), field), Paragraph(escape(value[pt]), body)]
            for label, value in example.fields if label != EVIDENCE]
    table = Table(rows, colWidths=[50*mm, 112*mm], hAlign='LEFT')
    table.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('LINEABOVE', (0, 0), (-1, -1), .5, colors.HexColor('#ccdbe0')),
                               ('TOPPADDING', (0, 0), (-1, -1), 10),
                               ('BOTTOMPADDING', (0, 0), (-1, -1), 10)]))
    doc.build([*items, table])
    return filename, 'application/pdf', out.getvalue()
