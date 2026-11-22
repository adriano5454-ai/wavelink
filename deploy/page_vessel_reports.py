"""Filter operational report registers by their saved Fleet vessel."""

def replace(source, old, new, count=1):
    if source.count(old) != count:
        raise ValueError('Unexpected report source: ' + old[:100])
    return source.replace(old, new)


def report_api(source):
    source = replace(source, "assignment:str='all',a=Depends(logged)):", "assignment:str='all',vessel_id:str='',a=Depends(logged)):")
    return replace(source, "assignment=assignment)", "assignment=assignment,vessel_id=vessel_id)")


def report_store(source):
    source = replace(source, "assignment='all'):", "assignment='all',vessel_id=''):")
    source = replace(source, 'member(c,a,self.view);items=[]', '''member(c,a,self.view);items=[]
            vessel = sites.report_vessel_filter(c, a, vessel_id) if vessel_id else None''')
    return replace(source, 'if not allowed(c,f,a):continue',
                   'if not allowed(c,f,a):continue\n                if vessel and not vessel(f):continue')


def report_vessel_filter(source):
    return replace(source, 'def pages(fetch, key):', '''def report_vessel_filter(c, actor, vessel_id):
    lookup = SiteLookup(catalog(c, actor))
    vessel = lookup.by_id.get(vessel_id)
    if not vessel or vessel['kind'] != 'vessel':
        return lambda record: False

    def matches(record):
        saved = (record.get('work_site') or {}).get('id')
        if saved:
            return saved == vessel_id
        return any(site['id'] == vessel_id for site in lookup.resolve(record))
    return matches


def pages(fetch, key):''')


def report_ui(source, prefix, category=False):
    source = replace(source, "status='active',query='',offset=0", "status='active',query='',vesselId='',offset=0")
    source = replace(source, "status='active';query='';offset=0", "status='active';query='';vesselId='';offset=0")
    keys = 'status,query,offset,' + ('category,' if category else '') + 'assignment'
    source = replace(source, 'new URLSearchParams({'+keys+'})',
                     'new URLSearchParams({'+keys+',...(vesselId?{vessel_id:vesselId}:{})})', 3)
    end = 'value="${E(query)}"></label>'
    source = replace(source, end, end+'${window.WLPageVessels?.field(vesselId)||\'\'}')
    anchor = "  for(const key of ['status','assignment'"
    return replace(source, anchor, """
  const vesselForm=el('PREFIX-filters');
  window.WLPageVessels?.bind(vesselForm.querySelector('[data-page-vessel]'),{api,value:vesselId,onChange:id=>{
   vesselId=id;
   vesselForm.requestSubmit();
  }});
""".replace('PREFIX',prefix)+anchor)


def toolbox_data(source):
    return replace(source, "talks=rows(c,'toolbox_talks'),directory=directory(c))",
                   "talks=rows(c,'toolbox_talks'),directory=directory(c),sites=sites.catalog(c,actor))")


def toolbox_ui(source):
    source = replace(source, "let toolboxViewKey='',toolboxEpoch=0;", "let toolboxViewKey='',toolboxEpoch=0,toolboxVessel='',toolboxQuery='';")
    source = replace(source, "if(changed){toolboxViewKey=key;lastResponse='';}",
                     "if(changed){toolboxViewKey=key;lastResponse='';toolboxVessel='';toolboxQuery='';}")
    source = replace(source, "  if(text){for(const x of root.querySelectorAll('[data-toolbox-id]",
                     """  const filters=root.querySelector('#tb-filters');if(filters)filters.disabled=!!text;
  if(text){for(const x of root.querySelectorAll('[data-toolbox-id]""")
    start = source.index(' function toolboxHome(data){')
    end = source.index(' function chooseTemplate(data)', start)
    head, cards = source[start:end].split('+__wl118.html`<div class="fw-cards">${[...data.talks]')
    card, buttons = cards.split('}</div>`);click(',1)
    card, empty = card.split("||__wl118.markup(",1)
    head = head.removeprefix(' function toolboxHome(data){')
    return source[:start] + """ function toolboxHome(data){
  const vessels=window.WLPageVessels;
  const words=(en,pt)=>window.WLWorkSites?.words(pt,en)||en;
  function filteredTalks(){
   const q=toolboxQuery.toLocaleLowerCase().trim();
   return data.talks.filter(talk=>(!toolboxVessel || vessels.matches(talk,toolboxVessel,data.sites)) &&
    (!q || [talk.meta?.work_description,talk.meta?.site,talk.meta?.work_site?.name,talk.template?.definition?.name,
      talk.meta?.event_utc,talk.status].some(v=>String(v||'').toLocaleLowerCase().includes(q))));
  }
  const count=rows=>words(`${rows.length} of ${data.talks.length} toolbox talks`,`${rows.length} de ${data.talks.length} diálogos de segurança`);
  function cards(rows){
   return rows""" + card + """ || (data.talks.length
    ? `<div class="card">${words('No matching toolbox talks.','Nenhum diálogo de segurança encontrado.')}</div>`
    : __wl118.markup(""" + empty + """);
  }
  const initial=filteredTalks();
  """ + head + """+__wl118.html`<fieldset id="tb-filters" class="wl-native-toolbar"><label class="field"><span>${words('Search toolbox talks','Buscar diálogos de segurança')}</span><input type="search" id="tb-query" maxlength="200" value="${esc(toolboxQuery)}"></label>${vessels?.field(toolboxVessel)||''}</fieldset><p class="small" id="tb-count" role="status">${count(initial)}</p><div class="fw-cards" id="tb-results">${cards(initial)}</div>`);
  function update(){
   const shown=filteredTalks();
   document.getElementById('tb-count').textContent=count(shown);
   AJViewStability.paint(document.getElementById('tb-results'),cards(shown));
  }
  const query=document.getElementById('tb-query');
  if(query)query.oninput=()=>{toolboxQuery=query.value;update();};
  vessels?.bind(document.getElementById('tb-filters').querySelector('[data-page-vessel]'),{
   api,sites:data.sites,value:toolboxVessel,onChange:id=>{toolboxVessel=id;update();}
  });
  click(""" + buttons + source[end:]


def certificate_ui(source):
    source = replace(source, "prefs={q:'',view:'current',contact:'all'}", "prefs={q:'',view:'current',contact:'all',vessel:''}", 3)
    source = replace(source, "},data=null;", "},data=null,certificateSites;")
    source = replace(source, "owner=account;prefs=", "owner=account;certificateSites=undefined;prefs=")
    fetch = "api('/api/certificates'+(id?'/'+encodeURIComponent(id):''),{beforeSend:c.before})"
    source = replace(source,'const d=await '+fetch+';if(n!==serial||!c.current())return;', '''const [d,directory]=await Promise.all([
    '''+fetch+''',
    (id||!window.WLPageVessels)?Promise.resolve(null):api('/api/fleet/work-locations',{beforeSend:c.before}).catch(()=>null)
   ]);if(n!==serial||!c.current())return;''')
    source = replace(source,"const sig=account+hash+JSON.stringify(d)+JSON.stringify(prefs);",
                     "if(!id)certificateSites=directory?.sites;\n   const sig=account+hash+JSON.stringify(d)+JSON.stringify(prefs)+JSON.stringify(certificateSites);")
    source = replace(source,"shown=all.filter(c=>matches(c,prefs,uid));const summary=all.reduce(",
                     "inVessel=prefs.vessel?all.filter(c=>WLPageVessels.matches(c,prefs.vessel,certificateSites)):all,shown=inVessel.filter(c=>matches(c,prefs,uid));const summary=inVessel.reduce(")
    source = replace(source,'<details id="cert-contact-filter">','${window.WLPageVessels?.field(prefs.vessel)||\'\'}<details id="cert-contact-filter">')
    return replace(source,"  const q=root.querySelector('[name=certsearch]');","""  window.WLPageVessels?.bind(root.querySelector('[data-page-vessel]'),{api,sites:certificateSites,value:prefs.vessel,onChange:id=>{
   prefs.vessel=id;catalogue(all);
  }});
  const q=root.querySelector('[name=certsearch]');""")


def logs_ui(source):
    source = replace(source, "let logSiteFilter = '';", "let logSiteFilter = '', logQuery = '';")
    source = replace(source,"if(context!==c){logSiteFilter='';", "if(context!==c){logSiteFilter='';logQuery='';")
    source = replace(source,' function groupedLogbooks(books) {', ''' function matchingLogbooks(books) {
  const q=logQuery.trim().toLocaleLowerCase();
  return books.filter(book=>(!logSiteFilter || bookSite(book)===logSiteFilter) &&
   (!q || [book.name,book.description,bookSiteName(book)].some(v=>String(v||'').toLocaleLowerCase().includes(q))));
 }

 function groupedLogbooks(books) {''')
    source = replace(source,"   if (logSiteFilter && logSiteFilter!==id) continue;\n","")
    source = replace(source,"No logbooks at this location.','Nenhum diário nesta localização.",
                     "No matching logbooks.','Nenhum diário encontrado.")
    source = replace(source,'return `<label class="field log-location-filter">',
                     '''return `<div class="wl-native-toolbar"><label class="field"><span>${logWords('Search logbooks','Buscar diários')}</span><input type="search" id="logs-page-query" maxlength="200" value="${esc(logQuery)}" aria-controls="logs-by-site"></label><label class="field log-location-filter">''')
    source = replace(source,'id="logs-location-filter" aria-controls=', 'id="logs-location-filter" data-page-vessel aria-controls=')
    source = replace(source,'</select></label><div id="logs-by-site">${groupedLogbooks(books)}</div>',
                     '</select></label></div><div id="logs-by-site">${books.length?groupedLogbooks(matchingLogbooks(books)):\'\'}</div>')
    source = replace(source,'''  filter.onchange = () => {
   logSiteFilter=filter.value;
   const container=document.getElementById('logs-by-site');
   AJViewStability.paint(container,groupedLogbooks(books));
  };''','''  const query=document.getElementById('logs-page-query');
  function update(){
   logSiteFilter=filter.value;
   logQuery=query.value;
   const shown=matchingLogbooks(books);
   document.getElementById('logs-visible-books').textContent=shown.length;
   document.getElementById('logs-visible-entries').textContent=shown.reduce((sum,book)=>sum+(Number(book.entries)||0),0);
   AJViewStability.paint(document.getElementById('logs-by-site'),books.length?groupedLogbooks(shown):'');
  }
  filter.onchange=update;
  query.oninput=update;
  update();''')
    source = replace(source, '<span>Saved logbooks</span><strong>', '<span>Saved logbooks</span><strong id="logs-visible-books">')
    source = replace(source, '<span>Active entries</span><strong>', '<span>Active entries</span><strong id="logs-visible-entries">')
    return replace(source,'${books.length?logSiteBrowser(books,directory):__wl118.html`', "${logSiteBrowser(books,directory)}${books.length?'':__wl118.html`")


def transforms():
    return {'app/work_locations.py':report_vessel_filter,
            'app/fault_reports.py':report_store, 'app/qshe_reports.py':report_store,
            'app/fault_reports_api.py':report_api, 'app/qshe_reports_api.py':report_api,
            'app/static/fault_reports.js':lambda source:report_ui(source, 'fr'),
            'app/static/qshe_reports.js':lambda source:report_ui(source, 'qs', category=True),
            'app/toolbox.py':toolbox_data, 'app/static/fieldwork.js':toolbox_ui,
            'app/static/certificate_workspace.js':certificate_ui, 'app/static/logs.js':logs_ui}
