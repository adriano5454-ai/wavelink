/* Delegate record surfaces to the same control users can reach with the keyboard. */
(() => {
 'use strict';
 const installed=Symbol.for('wavelink.recordCardNavigation');
 if(document[installed])return;
 const routes=[
  ['.maintenance-step[data-mw-step-key]', ['[data-maint-step]','[data-maint-detail]']],
  ['article[data-cw-card]', ['[data-cw-select]']],
  ['article[data-home-workspace]', ['a.home-open[href]']],
  ['.home-work-row[data-home-record]', ['a.home-work-action[href]']],
  ['.ph-row[data-home-record],.ph-shift-card[data-home-record]', ['a.btn[href]']],
  ['article.hr-record,article.ux-roster-card', ['[data-hr-open]']],
  ['article.ho-card', ['[data-ho-open]','[data-ho-incoming]']],
  ['article.ho-resume-entry', ['[data-ho-resume]']],
  ['.shw-personal[data-hop-personal]', ['[data-shw-save-open]']],
  ['article.hwd-record', ['[data-hwd-open]']],
  ['article.ho-day-entry', ['[data-ho-day-open]','[data-ho-day-published]']],
  ['article.sh-resume,article.sh-record', ['[data-sh-resume]','[data-sh-record]']],
  ['article.shw-department', ['[data-shw-team]']],
  ['article[data-ha-card]', ['[data-ha-open]']],
  ['article.log-book-card', ['a[href^="#logs/"]']],
  ['article.log-mobile-entry,tr.log-entry', ['[data-log-view]']],
  ['article.calendar-agenda-row', ['a[data-calendar-source]']],
  ['article.of-file:has(.wf-check)', ['input.wf-check']],
  ['article.of-file:not(:has(.wf-check))', ['button.wf-file-title']],
  ['article.sb-card', ['button.sb-library']],
  ['.fleet77-site-grid > article.fleet77-card', ['button[data-site]']],
  ['article[data-shipment-card]:has([data-shipment-select])', ['[data-shipment-select]']],
  ['article[data-shipment-card]:not(:has([data-shipment-select]))', ['a[href^="#manifest/"]']],
  ['article[data-receiving-row]', ['[data-receiving-open]']],
  ['tr[data-fleet-record^="asset-"]', ['a[href^="#asset/"]']],
  ['tr:has(a.it-request-link)', ['a.it-request-link']],
  ['tr[data-stock-row]', ['[data-check]']],
  ['article.tw47-stock-item', ['[data-task-check]']]
 ];
 const selector=routes.map(([box])=>box).join(',');
 const interactive='a,button,input,select,textarea,label,summary,details,[role="button"],[role="link"],[contenteditable]:not([contenteditable="false"]),[tabindex="0"]';
 const unavailable='[inert],[hidden],[aria-disabled="true"]';
 document.addEventListener('click',event=>{
  if(event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
  if(!(event.target instanceof Element))return;
  const box=event.target.closest(selector);
  if(!box||box.closest(unavailable))return;
  const control=event.target.closest(interactive);
  if(control&&box.contains(control))return;
  const selection=window.getSelection();
  if(selection&&!selection.isCollapsed&&box.contains(selection.anchorNode))return;
  const route=routes.find(([match])=>box.matches(match));
  for(const target of route[1]){
   const action=box.querySelector(target);
   if(!action||action.matches(':disabled')||action.closest(unavailable)||!action.getClientRects().length)continue;
   if(getComputedStyle(action).visibility!=='visible')continue;
   event.preventDefault();
   action.click();
   return;
  }
 });
 document[installed]=true;
})();
