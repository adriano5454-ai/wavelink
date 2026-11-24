from pathlib import Path
import runpy
import sys


def reader(source):
    anchor = '    const n = p.edit;'
    if source.count(anchor) != 1:
        raise ValueError('Unexpected publication reader')
    source = source.replace(anchor, anchor + """
    const filled = sections.filter(([key])=>n[key].trim());
    const ordered = [...filled.filter(([key])=>key==='next_actions'),...filled.filter(([key])=>key!=='next_actions')];
    const emptyText = window.WLWorkSites?.words('Nenhuma nota registrada nesta revisão.','No notes recorded in this revision.') || 'No notes recorded in this revision.';
""")
    start = source.index('      <div class="ho-reader-layout">')
    end = source.index('      <section class="ho-read-section"><h3>Selected published audience', start)
    source = source[:start] + """      <div class="ho-reader-text ho-published-notes">
      ${ordered.map(([k,label])=>__wl118.html`<section class="ho-read-section" data-ho-read-section="${E(k)}"><h3 id="ho-read-${E(k)}" tabindex="-1">${E(__wl118.t(label))}</h3><p class="ho-pre">${E(n[k])}</p></section>`).join('') || `<p class="small muted">${E(emptyText)}</p>`}
""" + source[end:]
    source = source.replace('id="ho-reader-notes-start">Read the notes</button>', """id="ho-reader-notes-start" ${ordered.length?\'\':\'hidden\'}>Read the notes</button><button type="button" class="btn secondary" id="ho-reader-ack-jump">Acknowledgement &amp; next steps</button>""")
    source = source.replace('</button></div></div></article>`;', '</button></div></article>`;')
    start = source.index("    host.querySelectorAll('[data-ho-read-jump]')")
    end = source.index("    host.querySelector('#ho-reader-top')",start)
    return source[:start] + """    if(ordered.length) host.querySelector('#ho-reader-notes-start').onclick = () => focus(host.querySelector('#ho-read-'+ordered[0][0]));
""" + source[end:]


def journey_inbox(source):
    source = reader(source)
    source = source.replace('observedAt,isActive,onOpen,onRefresh})', "observedAt,isActive,onOpen,onRefresh,selection={status:'pending',kind:'',search:''}})")
    source = source.replace("    const selection = {status:'pending',kind:'',search:''};", '')
    return source.replace('      query(selector).oninput =', '      query(selector).value = selection[key];\n      query(selector).oninput =')


def journey_detail(source):
    source = source.replace(" let vesselId='';"," let vesselId='',incomingFilters={status:'pending',kind:'',search:''};")
    source = source.replace("function reset(){vesselId='';","function reset(){incomingFilters={status:'pending',kind:'',search:''};vesselId='';")
    source = source.replace('mountInbox({host,rows:vesselRows()', 'mountInbox({host,selection:incomingFilters,rows:vesselRows()')
    action = "d.can_acknowledge&&!showDraft?button('ho-ack',__wl118.t('Read & personally acknowledge this revision'),''):''"
    gated = """d.can_acknowledge&&!showDraft?(state.info?.deployment_mode==='public_showcase'||state.publicDemoUserId===state.auth?.person?.user_id
      ? E(hoLabel('Public demo: read only.','Demo pública: somente leitura.'))
      :button('ho-ack',__wl118.t('Read & personally acknowledge this revision'),'')):''"""
    if source.count(action)!=1:
        raise ValueError('Unexpected acknowledgement controls')
    return source.replace(action,gated)


def transforms():
    return {'app/static/handover_incoming.js':journey_inbox, 'app/static/handovers.js':journey_detail,
            'app/static/ui132_visual.css':lambda s:s+"""
.ho-publication-reader .ho-published-notes{min-width:0;overflow-wrap:anywhere}
.ho-publication-reader [data-ho-read-section="next_actions"]{border-inline-start:3px solid var(--accent,#146877);padding-inline-start:.8rem}
"""}


if __name__=='__main__':
    apply=runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]),parent='e4188964fbd58230525470e093e8ac322213e7c261ea559afcec1d1d0462eb4d',overlays=(Path(__file__).name,),previous_cache='ui162-handover-draft-empty',cache='ui162-handover-reader',suffix='handover-reader',scope='Show filled published notes once, with incoming priorities first.')
