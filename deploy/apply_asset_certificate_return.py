"""Restore the authorized equipment/certificate navigation entry and its visible origin."""
import runpy
from pathlib import Path

BASE = Path(__file__).resolve().parent
one = runpy.run_path(str(BASE / 'apply_org_chart_filters.py'))['replace_once']


def assets(s):
    s = one(s, ' function captureAssetView(node){', """ const certificateOrigins=new Map();
 let originScope='',pendingCertificate=null;
 function rememberCertificate(pageNode,link){
  const scope=authScope();
  if(scope!==originScope){certificateOrigins.clear();originScope=scope;}
  const id=crypto.randomUUID();
  certificateOrigins.set(id,{asset:location.hash,certificate:link.hash,view:captureAssetView(pageNode),top:link.getBoundingClientRect().top});
  if(certificateOrigins.size>32)certificateOrigins.delete(certificateOrigins.keys().next().value);
  history.replaceState({...history.state,wlAssetOrigin:id},'');
  pendingCertificate=id;
 }
 function entryOrigin(key){
  return originScope===authScope()?certificateOrigins.get(history.state?.[key]):null;
 }
 function enterCertificate(){
  const saved=originScope===authScope()&&certificateOrigins.get(pendingCertificate);
  if(saved?.certificate===location.hash)history.replaceState({...history.state,wlCertificateFromAsset:pendingCertificate},'');
  pendingCertificate=null;
 }
 function certificateReturn(){
  const saved=entryOrigin('wlCertificateFromAsset');
  return saved?.certificate===location.hash?()=>history.back():null;
 }
 function captureAssetView(node){""")
    s = one(s,'return AJCertificateUI.open({background});', '{enterCertificate();return AJCertificateUI.open({background});}')
    s = one(s,'if(sig===last){',"""if(sig===last&&(kind!=='asset'||root.querySelector('.asset-workspace')?.dataset.assetId===data.item.id)){""")
    s = one(s,'const prefs=restored||(sameAsset?captureAssetView(previous):null);',"""const saved=entryOrigin('wlAssetOrigin');
  const origin=!sameAsset&&saved?.asset===location.hash&&saved.view.id===x.id?saved:null;
  const prefs=restored||(sameAsset?captureAssetView(previous):origin?.view);""")
    s = one(s, '  window.AJContextDocuments?.mount(', '  const documentsReady=window.AJContextDocuments?.mount(')
    s = one(s,'  const openRelatedAsset=href=>{',"""  const certificateLinks=[...pageNode.querySelectorAll('#asset-documents [data-asset-linked][href^="#certificates/"]')];
  for(const link of certificateLinks)link.addEventListener('click',e=>{
   if(current()&&!e.defaultPrevented&&!e.button&&!e.metaKey&&!e.ctrlKey&&!e.shiftKey&&!e.altKey)rememberCertificate(pageNode,link);
  });
  if(origin){
   const link=certificateLinks.find(el=>el.hash===origin.certificate&&el.getClientRects().length);
   if(link){
    const guard=new AbortController();
    const interrupt=()=>guard.abort();
    for(const event of ['pointerdown','keydown','wheel','touchstart'])window.addEventListener(event,interrupt,{capture:true,passive:true,signal:guard.signal});
    link.focus({preventScroll:true});
    const align=()=>{
     if(!current()||guard.signal.aborted||document.activeElement!==link)return;
     const top=Math.min(Math.max(72,origin.top),Math.max(72,innerHeight-link.offsetHeight-8));
     window.scrollBy({top:link.getBoundingClientRect().top-top,behavior:'instant'});
    };
    requestAnimationFrame(align);
    // Document summaries arrive separately and may increase the available scroll range.
    Promise.resolve(documentsReady).then(()=>requestAnimationFrame(()=>{align();guard.abort();}),interrupt);
   }
  }else if(!sameAsset&&!prefs){
   const heading=root.querySelector('h1');
   if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});heading.style.scrollMarginTop='72px';heading.scrollIntoView({block:'start',behavior:'instant'});}
  }
  const openRelatedAsset=href=>{""")
    return one(s,'return {handles,open,certificateWizard,','return {handles,open,certificateReturn,certificateWizard,')


def certificates(s):
    s = one(s, 'function shell(title,buttons,body){','function shell(title,buttons,body,identity=\'\'){')
    s = one(s, '<h1>${E(title)}</h1></div>', '<h1>${E(title)}</h1>${identity?\'<p class="small" data-certificate-identity>\'+E(identity)+\'</p>\':\'\'}</div>')
    s = one(s,' async function history(c){',""" function identityText(c){
  const linked=c.assets.map(a=>[a.name,a.serial||a.asset].filter(Boolean).join(' · ')).join(', ');
  const revision=(window.WavelinkI18n?.locale==='pt-BR'?'Revisão':'Revision')+' '+(c.source_revision||__wl118.t('Not recorded'));
  return [c.number,revision,linked].filter(Boolean).join(' · ');
 }
 async function history(c){""")
    s = one(s, '<p>Saved register changes, not a newly issued certificate.</p>', '<p><strong>${E(c.title)}</strong><br>${E(identityText(c))}</p><p>Saved register changes, not a newly issued certificate.</p>')
    s = one(s,'<p>No saved changes.</p>\')}`);}',"""<p>No saved changes.</p>')}`);dlg.addEventListener('close',()=>{if(ctx.current())document.getElementById('cert-history')?.focus({preventScroll:true});},{once:true});}""")
    s = one(s,"  const sourceBack=window.AJOriginalLibrary?.sourceReturn?.();","""  const sourceBack=window.AJOriginalLibrary?.sourceReturn?.();
  const assetBack=window.AJAssets?.certificateReturn?.();
  const entering=document.getElementById('certificate-workspace')?.dataset.certificateId!==c.id;""")
    s = one(s,'  const header=(sourceBack?',"""  const header=(assetBack?B('cert-back-asset',window.WavelinkUX.text('Voltar ao equipamento','Back to equipment')):'')+(sourceBack?""")
    s = one(s, 'page(shell(c.title,header,body));if(sourceBack)',"""page(shell(c.title,header,body,identityText(c)));
  const workspace=document.getElementById('certificate-workspace'),heading=workspace.querySelector('h1');
  workspace.dataset.certificateId=c.id;
  if(entering){heading.tabIndex=-1;heading.style.scrollMarginTop='72px';heading.focus({preventScroll:true});heading.scrollIntoView({block:'start',behavior:'instant'});}
  if(assetBack)F().click('cert-back-asset',assetBack);
  if(sourceBack)""")
    return s


def transforms():
    return {'app/static/assets.js': assets, 'app/static/certificate_workspace.js': certificates}
