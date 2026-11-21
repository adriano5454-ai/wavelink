/* Browse the saved library and files attached to authorised workspace records. */
window.WavelinkFileBrowser = (() => {
  'use strict';
  const pt = () => window.WavelinkI18n?.locale === 'pt-BR';
  const t = (en, br) => pt() ? br : en;
  const groups = {
    checklist:['Checklists','Listas de verificação'], toolbox:['Toolbox talks','Diálogos de segurança'],
    maintenance:['Maintenance','Manutenção'], logbook:['Logbooks','Livros de registro'],
    inventory:['Inventory','Inventário'], certificates:['Equipment certificates','Certificados de equipamentos'],
    fleet:['Shipping manifests','Manifestos de carga'], handovers:['Handovers','Passagens de turno'],
    qshe:['Safety & quality','Segurança e qualidade'], it:['IT requests','Solicitações de TI'],
    hr:['Human resources','Recursos humanos'], 'hr-documents':['Personal documents','Documentos pessoais'],
    'hr-timesheets':['Timesheets','Folhas de ponto'], 'hr-shifts':['Crew schedules','Escalas'],
    'hr-expenses':['Expenses & receipts','Despesas e recibos'], 'hr-travel':['Travel','Viagens']
  };
  const groupName = key => groups[key] ? t(...groups[key]) : key;
  const groupPath = key => (key.startsWith('hr-') ? groupName('hr')+' / ' : '')+groupName(key);
  const node = (tag, cls, value) => {
    const element = document.createElement(tag);
    if (cls) element.className = cls;
    if (value !== undefined) element.textContent = value;
    return element;
  };
  const fold = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase();
  const fileType = (name='') => {
    const ext = name.split('.').pop().toLowerCase();
    if (ext==='pdf') return 'pdf';
    if (['xlsx','xlsm','xls','xlsb','xltx','xltm','csv','tsv'].includes(ext)) return 'sheet';
    if (['png','jpg','jpeg','tif','tiff','webp','gif'].includes(ext)) return 'image';
    if (['docx','doc','txt','md','rtf'].includes(ext)) return 'document';
    return 'other';
  };
  const dateText = text => {
    const value = text ? new Date(text) : null;
    return value && Number.isFinite(+value) ? new Intl.DateTimeFormat(pt()?'pt-BR':'en-GB',{day:'numeric',month:'short',year:'numeric',timeZone:'UTC'}).format(value) : '';
  };
  function select(label, options, value, change) {
    const field=node('label','wf-select'), control=node('select');
    control.setAttribute('aria-label',label);
    field.append(node('span','',label),control);
    for (const [id,text] of options) control.add(new Option(text,id));
    control.value=value; control.onchange=()=>change(control.value);
    return field;
  }
  let pendingGroup='';
  function render(h) {
    if(pendingGroup){h.ui.group=pendingGroup;pendingGroup='';}
    const {shell,data,ui,button,selected}=h;
    const allLabel=t('All files','Todos os arquivos'), rootLabel=t('Unfiled','Sem pasta');
    const byFolder=new Map(data.folders.map(f=>[f.id,f]));
    const physicalName=id=>byFolder.get(id)?.name || rootLabel;
    const workspaceFiles=data.workspace_files||[];
    const nativeById=new Map(data.documents.map(d=>[d.id,{...d,groups:[]}]));
    const docs=[...nativeById.values()];
    for (const file of workspaceFiles) {
      const native=nativeById.get(file.original_id);
      if (native) { if (!native.groups.includes(file.group)) native.groups.push(file.group); continue; }
      docs.push({...file,id:file.url,groups:[file.group],workspace:true});
    }
    const visible=docs.filter(d=>h.archived||!d.archived);
    const counts=new Map(), folderCounts=new Map();
    for(const d of visible){
      for(const group of d.groups) counts.set(group,(counts.get(group)||0)+1);
      if(!d.workspace) folderCounts.set(d.folder_id,(folderCounts.get(d.folder_id)||0)+1);
    }
    const types=[['',t('All types','Todos os tipos')],['pdf','PDF'],['document',t('Documents & text','Documentos e textos')],
      ['sheet',t('Spreadsheets','Planilhas')],['image',t('Images','Imagens')],['other',t('Other files','Outros arquivos')]];
    const sortOptions=[['new',t('Newest first','Mais recentes')],['name',t('Name A–Z','Nome A–Z')],['old',t('Oldest first','Mais antigos')]];
    const layout=node('div','wf-layout'), sidebar=node('details','wf-sidebar'), nav=node('nav','wf-folder-list');
    sidebar.open=ui.folderOpen;
    sidebar.ontoggle=()=>{if(sidebar.isConnected)ui.folderOpen=sidebar.open;};
    const foldersTitle=t('Folders','Pastas');
    sidebar.append(node('summary','wf-folder-heading',foldersTitle),nav);
    nav.setAttribute('aria-label',t('Document folders','Pastas de documentos'));
    const buttons=[];
    const pick=(id,group='')=>{ui.group=group;ui.page=0;ui.selecting=false;h.folder(id);};
    function folderButton(host,label,count,current,click,kind='folder') {
      const b=button('',click,'wf-folder-button');
      b.append(node('span','wf-folder-icon '+kind),node('span','wf-folder-name',label),node('span','wf-folder-count',String(count)));
      b.firstChild.setAttribute('aria-hidden','true');
      b.setAttribute('aria-label',label+' ('+count+')'); host.append(b);buttons.push([b,current]);
      return b;
    }
    folderButton(nav,allLabel,visible.length,h.folderId==='*'&&!ui.group,()=>pick('*'),'all');
    const available = new Set([...workspaceFiles.map(d=>d.group),...(data.workspace_imports||[])]);
    const compare=new Intl.Collator(pt()?'pt-BR':'en',{numeric:true,sensitivity:'base'}).compare;
    const sorted = [...available].sort((a,b)=>compare(groupName(a),groupName(b)));
    const hrKeys=sorted.filter(k=>k.startsWith('hr-'));
    if (available.size) {
      nav.append(node('h3','wf-nav-label',t('By workspace','Por área')));
      const keys=sorted.filter(k=>!k.startsWith('hr-'));
      if(hrKeys.length) keys.push('hr');
      keys.sort((a,b)=>compare(groupName(a),groupName(b)));
      for(const key of keys){
        if(key==='hr'){
          const wrap=node('div','wf-branch'), header=node('div','wf-branch-heading');
          const list=node('div','wf-subfolders');
          const opened=ui.expanded.has('hr')||ui.group.startsWith('hr-');
          list.id='wf-hr-folders';list.hidden=!opened;
          const toggle=disclosure(list,'hr',groupName(key),opened);
          header.append(toggle);
          folderButton(header,groupName(key),hrKeys.reduce((n,k)=>n+(counts.get(k)||0),0),ui.group==='hr',()=>{ui.expanded.add('hr');pick('*','hr');});
          wrap.append(header,list);nav.append(wrap);
          for(const child of hrKeys) folderButton(list,groupName(child),counts.get(child)||0,ui.group===child,()=>pick('*',child));
        }else folderButton(nav,groupName(key),counts.get(key)||0,ui.group===key,()=>pick('*',key));
      }
    }
    function disclosure(target,key,name,opened) {
      const b=button('',()=>{target.hidden=!target.hidden;if(target.hidden)ui.expanded.delete(key);else ui.expanded.add(key);paint();},'wf-disclosure');
      b.setAttribute('aria-controls',target.id); target.hidden=!opened;
      function paint(){b.textContent=target.hidden?'▸':'▾';b.setAttribute('aria-expanded',String(!target.hidden));b.setAttribute('aria-label',(target.hidden?t('Expand ','Expandir '):t('Collapse ','Recolher '))+name);}
      paint();return b;
    }
    nav.append(node('h3','wf-nav-label',t('Library folders','Pastas da biblioteca')));
    folderButton(nav,rootLabel,folderCounts.get(null)||0,h.folderId===null&&!ui.group,()=>pick(null));
    const children=new Map();
    for(const f of data.folders){const pid=byFolder.has(f.parent_id)?f.parent_id:null;if(!children.has(pid))children.set(pid,[]);children.get(pid).push(f);}
    const seen=new Set();
    function branch(parent,host){
      for(const f of (children.get(parent)||[]).sort((a,b)=>compare(a.name,b.name))){
        if(seen.has(f.id)) continue;
        seen.add(f.id);
        const wrap=node('div','wf-branch'),row=node('div','wf-branch-heading'), sub=node('div','wf-subfolders');
        sub.id='wf-folder-'+f.id; const nested=children.has(f.id);
        if(nested)row.append(disclosure(sub,f.id,f.name,ui.expanded.has(f.id)));
        const b=folderButton(row,f.name,folderCounts.get(f.id)||0,!ui.group&&h.folderId===f.id,()=>pick(f.id));b.dataset.folderId=f.id;
        wrap.append(row);host.append(wrap);if(nested){wrap.append(sub);branch(f.id,sub);}
      }
    }
    branch(null,nav);
    for(const f of data.folders)if(!seen.has(f.id))folderButton(nav,f.name,folderCounts.get(f.id)||0,h.folderId===f.id&&!ui.group,()=>pick(f.id));
    if(data.can_organise)nav.append(button(t('New folder','Nova pasta'),()=>h.manage('create_folder'),'btn secondary wf-new-folder'));

    const main=node('section','wf-main'),top=node('div','wf-heading'),titles=node('div'),heading=node('h2');
    heading.id='wf-list-title';main.setAttribute('aria-labelledby',heading.id);titles.append(heading);
    const resultCount=node('p','wf-result-count');resultCount.setAttribute('role','status');titles.append(resultCount);top.append(titles);
    const topActions=node('div','wf-top-actions');topActions.id='of-primary';
    if(data.can_upload&&!ui.group)topActions.append(button(t('Upload original','Enviar original'),h.upload,'btn wf-upload'));
    if((data.workspace_imports||[]).includes(ui.group)){
      const link=node('a','btn wf-upload',t('Import file','Importar arquivo'));link.href='#builders/import/'+ui.group;topActions.append(link);
    }
    top.append(topActions);main.append(top);
    const search=node('input');search.type='search';search.id='of-search';search.placeholder=t('Search files, folders or people','Buscar arquivos, pastas ou pessoas');
    search.setAttribute('aria-label',t('Search all files','Buscar em todos os arquivos'));search.value=h.query;
    const tools=node('div','wf-tools'), searchwrap=node('div','wf-search');searchwrap.append(search);
    const clear=button(t('Clear','Limpar'),()=>{search.value='';search.oninput();search.focus();},'wf-clear');
    clear.id='of-clear-search';searchwrap.append(clear);tools.append(searchwrap);
    const filters=node('details','wf-filter');filters.open=ui.filters;filters.ontoggle=()=>{if(filters.isConnected)ui.filters=filters.open;};
    const filterTitle=node('summary',''), drawer=node('div','wf-filter-body');
    filters.append(filterTitle,drawer);tools.append(filters);main.append(tools);
    const subtype=select(t('File type','Tipo de arquivo'),types,ui.type,v=>{ui.type=v;reset();});
    const toggle=node('label','wf-archive');const archived=node('input');archived.type='checkbox';archived.id='of-archived';archived.checked=h.archived;
    archived.onchange=()=>{ui.page=0;h.archive(archived.checked);};toggle.append(archived,node('span','',t('Include archived files','Incluir arquivos arquivados')));drawer.append(subtype,toggle);
    const context=node('div','wf-list-tools'), path=node('div','wf-path'), listControls=node('div','wf-top-actions');
    if(!ui.group&&h.folderId!==null&&h.folderId!=='*')path.append(h.breadcrumb(h.folderId,id=>pick(id)));
    context.append(path,listControls);main.append(context);
    const order=select(t('Sort','Ordenar'),sortOptions,ui.sort,v=>{ui.sort=v;ui.page=0;paint();});listControls.append(order);
    const selBtn=button('',()=>{ui.selecting=!ui.selecting;selected.clear();paint();},'btn secondary');
    if(data.can_organise&&!ui.group)listControls.append(selBtn);
    const folderTools=node('details','wf-folder-options');folderTools.id='of-current-actions';
    if(data.can_organise&&!ui.group&&h.folderId!==null&&h.folderId!=='*'){
      folderTools.append(node('summary','',t('Folder options','Opções da pasta')));
      const menu=node('div','wf-options-list');for(const action of ['rename_folder','move_folder','remove_folder'])menu.append(button(h.actions[action],()=>h.manage(action),'wf-text-button'));folderTools.append(menu);main.append(folderTools);
    }
    const bulk=node('div','wf-bulk');main.append(bulk);
    const list=node('div','wf-results');list.id='of-results';main.append(list);
    const pager=node('div','wf-pager');main.append(pager);
    layout.append(sidebar,main);shell.append(layout);
    const foot=node('div','wf-footer');
    foot.append(button(t('Refresh files','Atualizar arquivos'),h.refresh,'wf-text-button'));
    if(data.can_organise)foot.append(button(t('Folder history','Histórico de pastas'),h.history,'wf-text-button'));shell.append(foot);

    function reset(){ui.page=0;selected.clear();paint();}
    search.oninput=()=>{h.setQuery(search.value);reset();};
    function paint(){
      const q=fold(search.value.trim());
      clear.hidden=!q;
      for(const [b,on]of buttons)b.setAttribute('aria-current',on&&!q?'location':'false');
      path.hidden=!!q;folderTools.hidden=!!q;
      filterTitle.textContent=t('Filters','Filtros')+((ui.type||h.archived)?' ('+(Number(!!ui.type)+Number(h.archived))+')':'');
      heading.textContent=q?t('Search results','Resultados da busca'):ui.group?groupName(ui.group):h.folderId==='*'?allLabel:physicalName(h.folderId);
      const matches=visible.filter(d=>{
        if(ui.type&&fileType(d.filename)!==ui.type)return false;
        if(q)return fold([d.title,d.filename,d.code,d.revision,d.folder_path,d.employee_name,...d.groups.map(groupPath)].join(' ')).includes(q);
        if(ui.group)return d.groups.some(k=>k===ui.group||ui.group==='hr'&&k.startsWith('hr-'));
        return h.folderId==='*'||(!d.workspace&&d.folder_id===h.folderId);
      });
      matches.sort((a,b)=>{const stamp=d=>d.imported_at||'';const byName=compare(a.title||a.filename,b.title||b.filename)||compare(a.filename,b.filename)||compare(a.id,b.id);
        return (ui.sort==='name'?0:stamp(a)&&stamp(b)?(ui.sort==='new'?stamp(b).localeCompare(stamp(a)):stamp(a).localeCompare(stamp(b))):Number(!!stamp(b))-Number(!!stamp(a)))||byName;});
      const count=matches.length;
      resultCount.textContent=count+' '+(count===1?t('file','arquivo'):t('files','arquivos'));
      const eligible=matches.filter(d=>!d.workspace);
      selBtn.textContent=ui.selecting?t('Done selecting','Concluir seleção'):t('Select files','Selecionar arquivos');selBtn.disabled=!eligible.length&&!ui.selecting;
      bulk.replaceChildren();bulk.hidden=!ui.selecting;
      if(ui.selecting){const total=node('strong','',selected.size+' '+t('selected','selecionados'));bulk.append(total,button(t('Select up to 100','Selecionar até 100'),()=>{selected.clear();eligible.slice(0,100).forEach(d=>selected.add(d.id));paint();},'wf-text-button'),button(t('Clear selection','Limpar seleção'),()=>{selected.clear();paint();},'wf-text-button'));
        const move=button(t('Move selected files','Mover selecionados'),()=>h.manage('move_documents'),'btn secondary');move.id='of-move';move.disabled=!selected.size;bulk.append(move);}
      const focused=document.activeElement?.closest('.wf-row')?.dataset.documentId;
      list.replaceChildren();pager.replaceChildren();ui.page=Math.min(ui.page,Math.max(0,Math.ceil(count/25)-1));
      for(const d of matches.slice(ui.page*25,ui.page*25+25)){
        const row=node('article','wf-row of-file');row.dataset.documentId=d.id;
        if(ui.selecting&&!d.workspace){const check=node('input');check.type='checkbox';check.className='wf-check';check.checked=selected.has(d.id);check.setAttribute('aria-label',t('Select ','Selecionar ')+d.title);
          check.onchange=()=>{if(check.checked&&selected.size>=100){check.checked=false;h.error(t('Select up to 100 files at a time.','Selecione até 100 arquivos por vez.'));return;}if(check.checked)selected.add(d.id);else selected.delete(d.id);paint();};row.append(check);}
        const ext=(d.filename.includes('.')?d.filename.split('.').pop():'').slice(0,5).toUpperCase()||t('FILE','ARQ');
        const emblem=node('span','wf-file-icon wf-'+fileType(d.filename),ext);emblem.setAttribute('aria-hidden','true');row.append(emblem);
        const body=node('div','wf-file-body'),title=button(d.title||d.filename,e=>h.open(d,e,true),'wf-file-title');
        const titleHeading=node('h3');titleHeading.append(title);body.append(titleHeading);
        if(d.title!==d.filename)body.append(node('p','wf-filename',d.filename));
        const meta=node('div','wf-metadata');const location=d.workspace?groupPath(d.group):d.folder_id===null?rootLabel:h.path(d.folder_id);
        meta.append(node('span','wf-location-label',location));if(d.employee_name)meta.append(node('span','wf-employee',d.employee_name));if(d.code)meta.append(node('span','',d.code));if(d.revision)meta.append(node('span','','Rev. '+d.revision));
        if(d.archived)meta.append(node('span','wf-archived',t('Archived','Arquivado')));body.append(meta);row.append(body);
        const facts=node('div','wf-file-facts');facts.append(node('span','',h.size(d.size)),node('span','',dateText(d.imported_at)));row.append(facts);
        const more=node('details','wf-more'),summary=node('summary','',t('Actions','Ações'));summary.setAttribute('aria-label',t('Actions for ','Ações de ')+(d.title||d.filename));more.append(summary);
        const menu=node('div','wf-options-list');
        if(!d.workspace)menu.append(button(t('Revision details','Detalhes da revisão'),()=>h.detail(d.id),'wf-text-button'));
        if(d.workspace&&d.record){const label=d.group.startsWith('hr-')?t('Open employee profile','Abrir perfil do colaborador'):d.group==='logbook'&&!d.url.includes('/imports/')?t('Open logbook','Abrir livro de registro'):t('Open source record','Abrir registro de origem');const link=node('a','wf-text-button',label);link.href=d.record;menu.append(link);}
        menu.append(button(t('Download original','Baixar original'),e=>h.open(d,e,false),'wf-text-button'));
        if(!d.workspace&&data.can_upload&&!d.archived)menu.append(button(t('Add revision','Adicionar revisão'),()=>h.revise(d),'wf-text-button'));
        more.append(menu);row.append(more);list.append(row);
      }
      if(!count){const empty=node('div','wf-empty');empty.append(node('h3','',q?t('No matching files','Nenhum arquivo encontrado'):t('No files here yet','Nenhum arquivo nesta pasta')));
        if(q||ui.type)empty.append(button(t('Clear search and filters','Limpar busca e filtros'),()=>{search.value='';h.setQuery('');ui.type='';subtype.querySelector('select').value='';reset();},'btn secondary'));
        else if(ui.group)empty.append(node('p','',t('Files appear here when saved in this workspace.','Os arquivos aparecem aqui quando são salvos nesta área.')));
        else if(data.can_upload)empty.append(button(t('Upload a file','Enviar um arquivo'),h.upload,'btn secondary'));
        list.append(empty);}
      if(count>25){const prev=button(t('Previous','Anterior'),()=>{ui.page--;paint();heading.scrollIntoView({block:'nearest'});},'btn secondary');
        const next=button(t('Next','Próxima'),()=>{ui.page++;paint();heading.scrollIntoView({block:'nearest'});},'btn secondary');prev.disabled=!ui.page;next.disabled=(ui.page+1)*25>=count;pager.append(prev,node('span','',(ui.page*25+1)+'–'+Math.min(count,(ui.page+1)*25)+' / '+count),next);}
      if(focused&&ui.selecting)Array.from(list.children).find(row=>row.dataset.documentId===focused)?.querySelector('input')?.focus({preventScroll:true});
      h.stale();
    }
    paint();
  }
  return {render,groupName,nextGroup:key=>{pendingGroup=Object.hasOwn(groups,key)?key:'';}};
})();
