"""Filter originals by saved job/project reference without widening file access."""
from pathlib import Path
import runpy, sys

BASE=Path(__file__).resolve().parent
PARENT='93f8de0ac6a4967b29d323fccde302e34791d0899a21902e2e23d99c9606af25'

def once(s,a,b):
    if s.count(a)!=1: raise ValueError('Unexpected Original Files job-filter anchor: '+repr(a))
    return s.replace(a,b,1)

def backend(s):
    marker='\ndef catalogue(store, actor, token, originals):'
    source='''
def file_job_references(owner, group):
    """Only explicit work references already held by the authorized source record."""
    meta = owner.get('meta') or {}
    values = [level.get(key) for level in (owner, meta) if isinstance(level, dict)
              for key in ('job_number', 'project_number')]
    if group == 'checklist' and isinstance(meta, dict):
        values.append(meta.get('project'))
    if group in ('hr-shifts', 'hr-expenses'):
        values.append(owner.get('project'))
    found = {}
    for value in values:
        if type(value) not in (str, int):
            continue
        label = str(value).strip()
        if 0 < len(label) <= 160:
            found.setdefault(label.casefold(), label)
    return list(found.values())

'''
    s=once(s,marker,'\n'+source+marker)
    s=once(s,"            owner = owner or {}\n            saved =", "            owner = owner or {}\n            file['job_references'] = file_job_references(owner, file['group'])\n            saved =")
    s=once(s,"            key = (row['group'], row['url'])","            row['job_contexts'] = [dict(references=row.pop('job_references'), vessel_ids=list(row['vessel_ids']))]\n            key = (row['group'], row['url'])")
    s=once(s,"                row['vessel_ids'] = sorted(set(row['vessel_ids']) | set(items[key]['vessel_ids']))",
           "                row['vessel_ids'] = sorted(set(row['vessel_ids']) | set(items[key]['vessel_ids']))\n                row['job_contexts'] = items[key]['job_contexts'] + row['job_contexts']")
    return s

def frontend(s):
    s=once(s,"    const nativeById=new Map(data.documents.map(d=>[d.id,{...d,groups:[],vessel_ids:[]}]))","    const nativeById=new Map(data.documents.map(d=>[d.id,{...d,groups:[],vessel_ids:[],jobSources:[]}]))")
    s=once(s,"        if (!native.groups.includes(file.group)) native.groups.push(file.group);","        if (!native.groups.includes(file.group)) native.groups.push(file.group);\n        native.jobSources.push(file);")
    s=once(s,"      docs.push({...file,id:file.url,groups:[file.group],workspace:true});","      docs.push({...file,id:file.url,groups:[file.group],jobSources:[file],workspace:true});")
    s=once(s,"    const counts=new Map(), folderCounts=new Map();",'''    const counts=new Map(), folderCounts=new Map();
    const groupMatches=k=>k===ui.group||ui.group==='hr'&&k.startsWith('hr-');
    const jobsFor=d=>[...new Set((d.jobSources||[]).filter(f=>!ui.group||groupMatches(f.group)).flatMap(f=>(f.job_contexts||[]).filter(ctx=>!ui.vessel||ctx.vessel_ids.includes(ui.vessel)).flatMap(ctx=>ctx.references)))];
    let scopeJobs=new Map();''')
    s=once(s,"      nav.append(node('h3','wf-nav-label',t('By workspace','Por área')));","      nav.append(node('h3','wf-nav-label',t('Automatic workspace groups','Grupos automáticos por área')));")
    s=once(s,"    search.setAttribute('aria-label',t('Search all files','Buscar em todos os arquivos'));search.value=h.query;","    search.setAttribute('aria-label',t('Search files','Buscar arquivos'));search.value=h.query;")
    s=once(s,"search.placeholder=t('Search files, folders or people','Buscar arquivos, pastas ou pessoas');","search.placeholder=t('Search files, people or job numbers','Buscar arquivos, pessoas ou nº do job');")
    s=once(s,"    const toggle=node('label','wf-archive');",'''    const job=select(t('Job / project number','Nº do job / projeto'),[],ui.job,v=>{ui.job=v;reset();});
    const jobControl=job.querySelector('select');jobControl.id='of-job';
    const toggle=node('label','wf-archive');''')
    s=once(s,"drawer.append(subtype,toggle);","drawer.append(job,subtype,toggle);")
    s=once(s,"      const menu=node('div','wf-options-list');for(const action of","      const menu=node('div','wf-options-list');menu.append(button(t('New subfolder','Nova subpasta'),()=>h.manage('create_folder'),'wf-text-button'));for(const action of")
    s=once(s,"      for(const [b,on]of buttons)b.setAttribute('aria-current',on&&!q?'location':'false');","      for(const [b,on]of buttons)b.setAttribute('aria-current',on?'location':'false');")
    a=s.index("      path.hidden=!!q;folderTools.hidden=!!q;")
    z=s.index("      matches.sort(",a)
    s=s[:a]+'''      const inLocation=d=>ui.group?d.groups.some(groupMatches):h.folderId==='*'||(!d.workspace&&d.folder_id===h.folderId);
      const scoped=visible.filter(inLocation);
      const options=new Map();
      for(const d of scoped)for(const j of jobsFor(d))if(!options.has(fold(j)))options.set(fold(j),j);
      if(ui.job&&!options.has(ui.job))options.set(ui.job,scopeJobs.get(ui.job)||ui.jobLabel||ui.job);
      if(JSON.stringify([...scopeJobs])!==JSON.stringify([...options])||!jobControl.options.length){
        scopeJobs=options;
        jobControl.replaceChildren(new Option(t('All jobs / projects','Todos os jobs / projetos'),''));
        for(const [k,label]of [...options].sort((a,b)=>compare(a[1],b[1])))jobControl.add(new Option(label,k));
      }
      jobControl.value=ui.job||'';ui.jobLabel=scopeJobs.get(ui.job)||'';
      const filterCount=Number(!!ui.job)+Number(!!ui.type)+Number(h.archived);
      filterTitle.textContent=t('Filters','Filtros')+(filterCount?' ('+filterCount+')':'');
      heading.textContent=ui.group?groupName(ui.group):h.folderId==='*'?q?t('Search results','Resultados da busca'):allLabel:physicalName(h.folderId);
      const matches=scoped.filter(d=>{
        if(ui.type&&fileType(d.filename)!==ui.type)return false;
        const refs=jobsFor(d);
        if(ui.job&&!refs.some(j=>fold(j)===ui.job))return false;
        return !q||fold([d.title,d.filename,d.code,d.revision,d.folder_path,d.employee_name,...refs,...(d.vessel_ids||[]).filter(id=>!ui.vessel||id===ui.vessel).map(id=>vesselNames.get(id)),...d.groups.map(groupPath)].join(' ')).includes(q);
      });
'''+s[z:]
    s=once(s,"if(d.archived)meta.append(node('span','wf-archived'","for(const ref of jobsFor(d))meta.append(node('span','wf-location-label',t('Job / project: ','Job / projeto: ')+ref));\n        if(d.archived)meta.append(node('span','wf-archived'")
    s=s.replace('q||ui.type||ui.vessel','q||ui.type||ui.vessel||ui.job')
    s=once(s,"ui.type='';ui.vessel='';ui.page=0;","ui.type='';ui.vessel='';ui.job='';ui.jobLabel='';ui.page=0;")
    s=once(s,"const browseUi={group:'',type:'',sort:","const browseUi={group:'',type:'',job:'',jobLabel:'',sort:")
    mark="ui:{group:browseUi.group,type:browseUi.type,sort:"
    if s.count(mark)!=2: raise ValueError("Unexpected browse retention anchors")
    s=s.replace(mark,"ui:{group:browseUi.group,type:browseUi.type,job:browseUi.job,jobLabel:browseUi.jobLabel,sort:")
    s=once(s,"leaveInner();clearSelection();folder=id;query='';revealFolder(id);draw();","leaveInner();clearSelection();folder=id;revealFolder(id);draw();")
    s=once(s,"    busy=false;proposal=null;operation=null;uncertain=false;mode='browse';c.toast(", """    if(proposal.action==='create_folder'&&proposal.parent_id)expandedFolders.add(proposal.parent_id);
    busy=false;proposal=null;operation=null;uncertain=false;mode='browse';c.toast(""")
    return s

def transforms():
    return {'app/static/original_library.js':frontend,'app/library_workspace_files.py':backend}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent=PARENT,overlays=(Path(__file__).name,),
        previous_cache='ui162-pdf-viewer',cache='ui162-original-job-filter',suffix='original-job-filter',
        scope='Original Files can find authorised attachments by saved job/project reference and create a subfolder from a library folder.')
