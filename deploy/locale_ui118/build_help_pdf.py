"""Build the complete Portuguese manual from the 77 reviewed HTML help articles.

Usage: python build_help_pdf.py /path/to/reconstructed/runtime [--output manual.pdf]
The English manual and HTML files are read-only inputs. Dependencies: ReportLab,
BeautifulSoup4, and system DejaVu fonts. Never reads company operational data.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, LongTable,
    NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer, XPreformatted)
from reportlab.platypus.tableofcontents import TableOfContents

NAVY = colors.HexColor('#103342')
TEAL = colors.HexColor('#087e86')
INK = colors.HexColor('#173c4b')
MUTED = colors.HexColor('#536f7d')
PALE = colors.HexColor('#edf5f7')
LINE = colors.HexColor('#cbdce3')
ORIGIN = 'https://corcovado.mywavelink.com'
GROUP_ORDER = ['setup', 'inventory', 'logistics', 'checklists', 'work', 'daily', 'safety', 'admin']


def readable(text: str) -> str:
    """Typography only, preserving original technical code separately."""
    return text.translate(str.maketrans({'\u2010': '-', '\u2011': '-', '\u2012': '-',
        '\u2013': '-', '\u2014': ' - ', '\u2212': '-', '\u00a0': ' '}))


def register_fonts(font_dir: Path) -> None:
    for name, filename in [('Guide', 'DejaVuSans.ttf'), ('Guide-Bold', 'DejaVuSans-Bold.ttf'),
            ('Guide-Oblique', 'DejaVuSans-Oblique.ttf'),
            ('Guide-BoldOblique', 'DejaVuSans-BoldOblique.ttf'),
            ('GuideMono', 'DejaVuSansMono.ttf')]:
        path = font_dir / filename
        # Minimal Linux images may omit proportional oblique faces; retain the
        # same readable family instead of silently substituting unsupported glyphs.
        if not path.is_file() and filename.endswith('-Oblique.ttf'):
            path = font_dir / 'DejaVuSans.ttf'
        elif not path.is_file() and filename.endswith('-BoldOblique.ttf'):
            path = font_dir / 'DejaVuSans-Bold.ttf'
        if not path.is_file():
            raise FileNotFoundError(f'Required font missing: {path}')
        pdfmetrics.registerFont(TTFont(name, str(path)))
    pdfmetrics.registerFontFamily('Guide', normal='Guide', bold='Guide-Bold',
        italic='Guide-Oblique', boldItalic='Guide-BoldOblique')


def styles():
    out = StyleSheet1()
    definitions = {
        'Body': dict(fontName='Guide', fontSize=9.2, leading=14.0, textColor=INK,
            spaceAfter=7, allowWidows=0, allowOrphans=0, splitLongWords=True),
        'Small': dict(fontName='Guide', fontSize=8.1, leading=12, textColor=MUTED, spaceAfter=6),
        'Chapter': dict(fontName='Guide-Bold', fontSize=20.5, leading=26, textColor=NAVY,
            spaceBefore=4, spaceAfter=15, keepWithNext=True),
        'Section': dict(fontName='Guide-Bold', fontSize=13.0, leading=18, textColor=TEAL,
            spaceBefore=13, spaceAfter=7, keepWithNext=True),
        'Subsection': dict(fontName='Guide-Bold', fontSize=10.3, leading=15.2, textColor=NAVY,
            spaceBefore=10, spaceAfter=5, keepWithNext=True),
        'Eyebrow': dict(fontName='Guide-Bold', fontSize=7.4, leading=11, textColor=TEAL,
            spaceBefore=2, spaceAfter=7, keepWithNext=True),
        'Notice': dict(fontName='Guide', fontSize=8.8, leading=13.3, textColor=INK,
            backColor=PALE, borderColor=LINE, borderWidth=.45, borderPadding=7,
            leftIndent=7, rightIndent=7, spaceBefore=5, spaceAfter=10),
        'List': dict(fontName='Guide', fontSize=9.2, leading=14, textColor=INK,
            leftIndent=15, firstLineIndent=-11, spaceAfter=6, allowWidows=0, allowOrphans=0),
        'Cell': dict(fontName='Guide', fontSize=8.4, leading=12.3, textColor=INK),
        'CellHead': dict(fontName='Guide-Bold', fontSize=8.4, leading=12.3, textColor=colors.white),
        'Code': dict(fontName='GuideMono', fontSize=8.3, leading=12.4, textColor=INK,
            backColor=PALE, borderColor=LINE, borderWidth=.45, borderPadding=8,
            leftIndent=8, rightIndent=8, spaceBefore=5, spaceAfter=11),
        'CoverLabel': dict(fontName='Guide-Bold', fontSize=11, leading=15, textColor=TEAL,
            spaceAfter=14),
        'CoverTitle': dict(fontName='Guide-Bold', fontSize=34, leading=41,
            textColor=NAVY, spaceAfter=20),
        'CoverSubtitle': dict(fontName='Guide', fontSize=16, leading=23,
            textColor=MUTED, spaceAfter=30),
        'ContentsTitle': dict(fontName='Guide-Bold', fontSize=25, leading=31,
            textColor=NAVY, spaceAfter=15),
        'ContentsEntry': dict(fontName='Guide', fontSize=9.1, leading=14.3,
            textColor=INK, leftIndent=0, firstLineIndent=0, spaceBefore=3),
    }
    for name, kw in definitions.items():
        out.add(ParagraphStyle(name, **kw))
    return out


class ManualDoc(BaseDocTemplate):
    def __init__(self, filename: Path, **kw):
        super().__init__(str(filename), pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
            topMargin=20*mm, bottomMargin=19*mm, title='Wavelink - Guia do usuário - Corcovado',
            author='AJ Offshore Solutions', subject='77 tópicos completos da ajuda em português',
            pageCompression=1, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
            id='body', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='cover', frames=frame, onPage=self.cover_page),
            PageTemplate(id='normal', frames=frame, onPage=self.normal_page)])
        self.current_topic = ''

    def cover_page(self, canvas, doc):
        width, height = A4
        canvas.saveState()
        canvas.setFillColor(NAVY);canvas.rect(0, height-19*mm, width, 19*mm, fill=1, stroke=0)
        canvas.setFillColor(TEAL);canvas.rect(0, 0, width, 8*mm, fill=1, stroke=0)
        canvas.restoreState()

    def normal_page(self, canvas, doc):
        width, height = A4
        canvas.saveState()
        canvas.setFont('Guide-Bold', 8);canvas.setFillColor(TEAL)
        canvas.drawString(doc.leftMargin, height-12*mm, 'WAVELINK')
        canvas.setFont('Guide', 7.5);canvas.setFillColor(MUTED)
        canvas.drawRightString(width-doc.rightMargin, height-12*mm, 'GUIA DO USUÁRIO | CORCOVADO')
        canvas.setStrokeColor(LINE);canvas.setLineWidth(.45)
        canvas.line(doc.leftMargin, height-14.5*mm, width-doc.rightMargin, height-14.5*mm)
        canvas.line(doc.leftMargin, 14*mm, width-doc.rightMargin, 14*mm)
        canvas.setFont('Guide', 7.2)
        canvas.drawString(doc.leftMargin, 9.5*mm, 'AJ Offshore Solutions | Documentação do programa')
        canvas.drawRightString(width-doc.rightMargin, 9.5*mm, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if hasattr(flowable, 'topic_entry'):
            title, anchor = flowable.topic_entry
            self.canv.bookmarkPage(anchor)
            self.canv.addOutlineEntry(title, anchor, level=0, closed=False)
            self.notify('TOCEntry', (0, title, self.page, anchor))


def sources(directory: Path):
    paths = {p.stem: p for p in directory.glob('*.html')}
    if len(paths) != 77:
        raise ValueError(f'Expected exactly 77 reviewed Portuguese topics, found {len(paths)}')
    first = BeautifulSoup(next(iter(paths.values())).read_text(), 'html.parser')
    nav = first.select_one('#help-topic-nav')
    ordered = []
    seen = set()
    if nav:
        groups = sorted(nav.select('details[data-group]'),
            key=lambda n: GROUP_ORDER.index(n['data-group']) if n['data-group'] in GROUP_ORDER else 999)
        for group in groups:
            summary = group.find('summary')
            group_title = ' '.join(summary.get_text(' ', strip=True).split()) if summary else ''
            group_title = re.sub(r'\s+\d+$', '', group_title)
            for row in group.select('[data-topic-row]'):
                slug = row.get('data-topic-row')
                if slug in paths and slug not in seen:
                    ordered.append((slug, paths[slug], group_title));seen.add(slug)
    for slug in sorted(paths.keys()-seen):
        ordered.append((slug, paths[slug], 'Ajuda do programa'))
    result = []
    for slug, path, group in ordered:
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        article = soup.find('article')
        if not article:
            raise ValueError(f'No actual help article in {path}')
        h1 = article.find('h1')
        if not h1:
            raise ValueError(f'No article heading in {path}')
        title = ' '.join(h1.get_text(' ', strip=True).split())
        result.append(dict(slug=slug, path=path, group=group, article=article,
            title=title, h1=h1, sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    return result


class HtmlGuide:
    def __init__(self, source, styleset, width):
        self.sources = source;self.styles = styleset;self.width = width
        self.current_slug = '';self.stats = Counter()
        self.anchors = {}
        for item in source:
            slug = item['slug']
            self.anchors[(slug, '')] = 'topic_'+slug
            for node in item['article'].find_all(id=True):
                self.anchors[(slug, node['id'])] = 'topic_'+slug+'__'+node['id']

    def anchor(self, node):
        if isinstance(node, Tag) and node.get('id'):
            key = self.anchors[(self.current_slug, node['id'])]
            return [Paragraph('<a name="'+escape(key, quote=True)+'"/>', self.styles['Small'])]
        return []

    def link(self, href):
        if not href:
            return ''
        if href.startswith('#'):
            return '#'+self.anchors[(self.current_slug, href[1:])] if (self.current_slug, href[1:]) in self.anchors else ORIGIN+'/help/topics/'+self.current_slug+href
        match = re.fullmatch(r'/help/topics/([a-z0-9_-]+)(?:#(.*))?', href)
        if match:
            key = (match[1], match[2] or '')
            if key in self.anchors:return '#'+self.anchors[key]
        if href.startswith('/'):return ORIGIN+href
        if urlsplit(href).scheme in ('https','http','mailto'):return href
        return ''

    def inline(self, node, *, verbatim=False):
        if isinstance(node, Comment):return ''
        if isinstance(node, NavigableString):
            return escape(str(node) if verbatim else readable(str(node)))
        if node.name in ('script','style'):return ''
        inside = ''.join(self.inline(n, verbatim=verbatim or node.name=='code') for n in node.children)
        if node.name in ('b','strong'):return '<b>'+inside+'</b>'
        if node.name in ('i','em'):return '<i>'+inside+'</i>'
        if node.name=='code':return '<font name="GuideMono">'+inside+'</font>'
        if node.name=='br':return '<br/>'
        if node.name=='a':
            href = self.link(node.get('href',''))
            return '<link href="'+escape(href, quote=True)+'" color="#087e86">'+inside+'</link>' if href else inside
        return inside

    def table(self, node):
        self.stats['tables'] += 1
        rows=[]
        header_rows=0
        for tr in node.find_all('tr'):
            cells=tr.find_all(['th','td'], recursive=False)
            if not cells:continue
            if all(c.name=='th' for c in cells) and not rows:header_rows+=1
            rows.append([Paragraph(self.inline(cell),self.styles['CellHead' if cell.name=='th' else 'Cell']) for cell in cells])
        if not rows:return []
        columns=max(map(len,rows))
        for row in rows:row.extend([Paragraph('',self.styles['Cell'])]*(columns-len(row)))
        widths=[self.width*.32,self.width*.68] if columns==2 else [self.width/columns]*columns
        table=LongTable(rows,colWidths=widths,repeatRows=header_rows,hAlign='LEFT')
        commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),
            ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),
            ('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.45,LINE)]
        if header_rows:commands.append(('BACKGROUND',(0,0),(-1,header_rows-1),NAVY))
        for index in range(header_rows,len(rows)):
            if index%2==0:commands.append(('BACKGROUND',(0,index),(-1,index),colors.HexColor('#f5f9fa')))
        table.setStyle(commands)
        return [Spacer(1,4),table,Spacer(1,10)]

    def render(self, node, *, notice=False, skip_h1=None, list_depth=0):
        if isinstance(node, Comment):return []
        if isinstance(node,NavigableString):
            return [Paragraph(escape(readable(str(node))),self.styles['Notice' if notice else 'Body'])] if node.strip() else []
        if node.name in ('script','style'):return []
        out=self.anchor(node)
        if node is skip_h1:return out
        if node.name=='table':return out+self.table(node)
        if node.name=='pre':
            self.stats['pre']+=1
            return out+[XPreformatted(escape(node.get_text()),self.styles['Code'])]
        if node.name in ('h1','h2','h3','h4','h5','h6'):
            self.stats[node.name]+=1
            style='Section' if node.name in ('h1','h2') else 'Subsection'
            return out+[Paragraph(self.inline(node),self.styles[style])]
        if node.name in ('ul','ol'):
            self.stats['lists']+=1
            for index,li in enumerate(node.find_all('li',recursive=False),1):
                prefix=f'{index}.' if node.name=='ol' else '•'
                inline_children=[c for c in li.children if not isinstance(c,Tag) or c.name not in ('ul','ol')]
                text=''.join(self.inline(c) for c in inline_children)
                style=ParagraphStyle('nested',parent=self.styles['List'],leftIndent=15+list_depth*13)
                out.extend(self.anchor(li));out.append(Paragraph(escape(prefix)+' '+text,style))
                for child in li.find_all(['ul','ol'],recursive=False):out+=self.render(child,notice=notice,skip_h1=skip_h1,list_depth=list_depth+1)
            return out
        if node.name=='p':
            self.stats['paragraphs']+=1
            name='Notice' if notice else 'Eyebrow' if set(node.get('class',[]))&{'kicker','eyebrow'} else 'Body'
            return out+[Paragraph(self.inline(node),self.styles[name])]
        if node.name in ('strong','b','em','i','code','a','span','small'):
            return out+[Paragraph(self.inline(node),self.styles['Notice' if notice else 'Body'])]
        for child in node.children:
            out+=self.render(child,notice=notice or node.name=='aside',skip_h1=skip_h1,list_depth=list_depth)
        return out


def build(source: Path, output: Path, font_dir: Path):
    directory=source/'app/static/pt-BR/help_topics'
    inputs=sources(directory)
    register_fonts(font_dir);st=styles()
    output.parent.mkdir(parents=True,exist_ok=True)
    doc=ManualDoc(output)
    renderer=HtmlGuide(inputs,st,doc.width)
    story=[Spacer(1,35*mm),Paragraph('WAVELINK',st['CoverLabel']),
        Paragraph('Guia do usuário',st['CoverTitle']),Paragraph('Corcovado<br/>Português do Brasil',st['CoverSubtitle']),
        HRFlowable(width='100%',thickness=2,color=TEAL,spaceAfter=18),
        Paragraph('77 tópicos completos da ajuda do programa',st['Section']),
        Paragraph('AJ Offshore Solutions | Core 1.34.19 | UI118',st['Body']),
        Spacer(1,8*mm),Paragraph('Este manual reúne o conteúdo integral dos artigos de ajuda em português incluídos nesta versão. Os números de interface e as indicações de versão dos artigos são preservados; alguns procedimentos descrevem o aplicativo local do Windows ou interfaces anteriores.',st['Body']),
        Paragraph('A documentação não modifica registros operacionais, não aprova procedimentos, não libera equipamentos e não comprova a execução de trabalho. Use os procedimentos aprovados pela sua empresa.',st['Notice']),
        Paragraph('Exemplos técnicos, comandos e identificadores de arquivos são mantidos como na fonte. O sumário e os links entre capítulos funcionam neste arquivo.',st['Small']),
        Paragraph('Atalhos externos da empresa usam o endereço previsto https://corcovado.mywavelink.com. Eles exigem o endereço de implantação correto, com domínio e serviço disponíveis; este guia não confirma a disponibilidade desse endereço. As demais referências externas preservam os destinos dos artigos.',st['Small']),
        NextPageTemplate('normal'),PageBreak(),Paragraph('Sumário',st['ContentsTitle']),
        Paragraph('Os 77 capítulos abaixo reproduzem os artigos completos, organizados por área da ajuda.',st['Body'])]
    toc=TableOfContents();toc.levelStyles=[st['ContentsEntry']];toc.dotsMinLevel=0
    story.extend([toc,PageBreak()])
    for index,item in enumerate(inputs,1):
        renderer.current_slug=item['slug']
        chapter_title=f'{index:02d}. '+readable(item['title'])
        story.append(Paragraph(escape(item['group'].upper()),st['Eyebrow']))
        heading=Paragraph(escape(chapter_title),st['Chapter'])
        heading.topic_entry=(chapter_title,'topic_'+item['slug'])
        story.append(heading)
        story.extend(renderer.render(item['article'],skip_h1=item['h1']))
        if index<len(inputs):story.append(PageBreak())
    doc.multiBuild(story)
    return dict(topics=len(inputs),output=str(output),sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
        stats=dict(renderer.stats),sources=[{k:v for k,v in item.items() if k in ('slug','title','group','sha256')} for item in inputs])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source',type=Path)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--font-dir',type=Path,default=Path('/usr/share/fonts/truetype/dejavu'))
    args=parser.parse_args()
    result=build(args.source.resolve(),args.output or args.source/'app/static/pt-BR/Wavelink_Guia_Usuario.pdf',args.font_dir)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
