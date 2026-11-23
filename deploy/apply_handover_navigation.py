from pathlib import Path
import re
import runpy
import sys


def navigation(source):
    start=source.index('<nav class="ho-view-tabs"')
    end=source.index('</nav>',start)+6
    nav=source[start:end]
    buttons=dict(re.findall(r'<button type="button" id="ho-tab-([^"]+)"[^>]*>(.*?)</button>',nav))
    if set(buttons)!={'days','incoming','my-shift','drafts','shifts'}:
        raise ValueError('Unexpected handover views')
    def group(title,pt,items):
        rows=[]
        for key,en,translation in items:
            selected='true' if key=='days' else 'false'
            rows.append(f'<button type="button" id="ho-tab-{key}" aria-selected="{selected}">${{hoLabel("{en}","{translation}")}}</button>')
        return f'<div class="ho-nav-group"><strong>${{hoLabel("{title}","{pt}")}}</strong><div>' + ''.join(rows)+'</div></div>'
    read=group('Find handovers','Encontrar passagens',[('days','By day and subject','Por dia e assunto'),('incoming','Received by me','Recebidas por mim')])
    author=group('My work','Meu trabalho',[('my-shift','My shift','Meu turno'),('drafts','My saved drafts','Meus rascunhos salvos')])
    shifts=group('Team','Equipe',[('shifts','Shifts and people','Turnos e pessoas')])
    source=source[:start]+nav[:nav.index('>')+1]+read+author+shifts+'</nav>'+source[end:]
    anchor=' function shell(){'
    source=source.replace(anchor," const hoLabel=(en,pt)=>window.WLWorkSites?.words(pt,en)||en;\n"+anchor,1)
    source=source.replace("button('ho-new',__wl118.t('Create handover')","button('ho-new',hoLabel('Start a draft','Iniciar rascunho')",1)
    source=source.replace("label('Back to handovers','Voltar às passagens')","label('Back to list','Voltar à lista')",1)
    anchor='for(const [key,caption] of sections()){'
    if source.count(anchor)!=1:raise ValueError('Unexpected preview sections')
    return source.replace(anchor,"""const ordered=sections();
    const pending=ordered.filter(([key])=>key==='next_actions');
    for(const [key,caption] of [...pending,...ordered.filter(([key])=>key!=='next_actions')]){""").replace("element('section','','hop-note')","element('section','',key==='next_actions'?'hop-note hop-next-action':'hop-note')",1)


def transforms():
    return {'app/static/handovers.js':navigation,
            'app/static/ui132_visual.css':lambda s:s+"""
#ho-library .ho-view-tabs{display:flex;flex-wrap:wrap;gap:.65rem 1.2rem;align-items:start}
#ho-library .ho-nav-group>strong{display:block;font-size:.88rem;margin-bottom:.35rem}
#ho-library .ho-nav-group>div{display:flex;flex-wrap:wrap;gap:.35rem}
#ho-library .hop-next-action{border-inline-start:3px solid var(--accent,#146877);padding-inline-start:.8rem}
@media(max-width:600px){#ho-library .ho-view-tabs{gap:.65rem}#ho-library .ho-nav-group{flex:1 1 10rem}}
"""}


if __name__=='__main__':
    apply=runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]),parent='09f26c27efa2cea278ac784314f1cc4523370004ff99672b14e50db461364263',overlays=(Path(__file__).name,),previous_cache='ui162-hse-toolbox-filters',cache='ui162-handover-navigation',suffix='handover-navigation',scope='Separate reading and author navigation and highlight the next action in handover previews.')
