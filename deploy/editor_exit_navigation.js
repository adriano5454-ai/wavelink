// Ask the owner of each editor before a route change reaches shell shortcuts,
// account controls, or workspace-specific hash listeners.
window.AJEditorNavigation = (() => {
 const pt = () => window.WavelinkI18n?.locale === 'pt-BR';
 const label = (portuguese, english) => pt() ? portuguese : english;
 const confirmKeep = () => window.confirm(label('Manter este rascunho nesta aba e sair da edição?',
                                                'Keep this draft in this tab and leave the editor?'));
 const confirmDiscard = uncertain => window.confirm(uncertain
   ? label('O envio pode já ter sido salvo. Descartar apenas as alterações locais e sair?',
           'The earlier submission may already be saved. Discard the local edits and leave?')
   : label('Descartar as alterações não salvas e sair?', 'Discard unsaved changes and leave?'));
 let waiting = false;
 function wait(){
   waiting = true;
   toast(label('Aguarde o término da preparação ou do salvamento antes de sair.',
              'Wait for the current file preparation or save to finish before leaving.'));
   return false;
 }
 function prepare(target){
   waiting = false;
   // Profile tabs, skip links and other in-page fragments belong to their
   // local handlers. Only a workspace transition can end an editing session.
   const route=target||'#home';
   if(!/^#(?:access-requests|admin|asset|asset-alerts|assets|builders|calendar|certificate|certificates|checklists|demo|dive|faults|fleet|handover|handovers|home|hr|inventory|it|logs|maintenance|new|original-files|profile|qshe|tasks|team|toolbox|workspaces)(?:[/?]|$)/.test(route))return true;
   const checks = [window.AJRecognition?.prepareNewsLeave, window.AJRecognition?.prepareProfileLeave,
                   window.AJProfessionalContacts?.prepareLeave, window.AJEmailAlerts?.prepareLeave,
                   window.AJFaults?.prepareLeave, window.AJQshe?.prepareLeave,
                   window.AJHR?.prepareLeave, window.AJIT?.prepareLeave];
   return checks.every(check => !check || check(route) !== false);
 }
 const sameDocument = url => url.origin===location.origin && url.pathname===location.pathname &&
                             url.search===location.search;
 window.addEventListener('click', event => {
   if(event.defaultPrevented || event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)return;
   const a=event.target.closest?.('a[href]');
   if(!a || a.hasAttribute('download') || (a.target && a.target!=='_self'))return;
   const href=a.getAttribute('href');
   const url=new URL(href,location.href);
   let target;
   if(url.origin===location.origin && url.pathname==='/fleet'){
     target=url.hash ? '#fleet/'+url.hash.slice(1) : window.AJWorkspaceShell?.destination();
   }else if(href.startsWith('#') || (url.hash && sameDocument(url))){
     target=url.hash||'#home';
   }
   if(target && target!==(location.hash||'#home') && !prepare(target)){
     event.preventDefault();
     event.stopImmediatePropagation();
     if(document.body.classList.contains('shell-mobile-open'))window.AJNavShell?.close();
   }
 },true);

 // Supporting browsers can refuse a Back/Forward operation before the address
 // changes, keeping the form, pending requests and both history entries intact.
 const nav=window.navigation;
 nav?.addEventListener('navigate', event => {
   if(event.defaultPrevented || !event.cancelable || !event.destination.sameDocument)return;
   const url=new URL(event.destination.url);
   if(sameDocument(url) && (url.hash||'#home')!==(location.hash||'#home') && !prepare(url.hash)){
     event.preventDefault();
   }
 });

 const marker='wlWorkspaceRouteIndex';
 const stamp=()=>history.state?.[marker];
 const index=()=>nav?.currentEntry?.index ?? stamp();
 let last=index() ?? 0;
 function record(position){
   last=position;
   if(!nav && history.state?.[marker]!==position && (!history.state || typeof history.state==='object')){
     history.replaceState({...history.state,[marker]:position},'');
   }
 }
 record(last);
 window.addEventListener('hashchange',event=>{
   if(event.newURL && event.newURL!==location.href){
     event.stopImmediatePropagation();
     return;
   }
   const target=index();
   if(!prepare(location.hash)){
     event.stopImmediatePropagation();
     if(!waiting && Number.isInteger(target) && target!==last)history.go(last-target);
     else if(event.oldURL)history.replaceState(history.state,'',event.oldURL);
     return;
   }
   record(Number.isInteger(target) ? target : last+1);
 },true);
 return Object.freeze({prepare,wait,confirmKeep,confirmDiscard});
})();
