/* Forward a record card's empty space to its normal navigation control. */
(() => {
 'use strict';
 const routes = [
  ['.maintenance-step[data-mw-step-key]', ['[data-maint-step]','[data-maint-detail]']],
  ['article[data-cw-card]', ['[data-cw-open]']],
  ['article[data-home-workspace]', ['a.home-open[href]']],
  ['.home-work-row[data-home-record]', ['a.home-work-action[href]']],
  ['.ph-row[data-home-record],.ph-shift-card[data-home-record]', ['a.btn[href]']],
  ['article.hr-record,article.ux-roster-card',['[data-hr-open]']],
  ['article.ho-card',['[data-ho-open]']],
  ['article.hwd-record', ['[data-hwd-open]']],
  ['article.ho-day-entry', ['[data-ho-day-open]']],
  ['article.sh-resume,article.sh-record', ['[data-sh-resume]','[data-sh-record]']],
  ['article[data-ha-card]', ['[data-ha-open]']],
  ['article.log-mobile-entry,tr.log-entry', ['[data-log-view]']],
  ['article[data-shipment-card]', ['a[href^="#manifest/"]']],
  ['tr[data-fleet-record^="asset-"]', ['a[href^="#asset/"]']],
  ['tr:has(a.it-request-link)', ['a.it-request-link']],
  ['tr[data-stock-row]', ['[data-check]']],
  ['article.tw47-stock-item', ['[data-task-check]']]
 ];
 const controls='a,button,input,select,textarea,label,summary,details,[role="button"],[role="link"],[contenteditable="true"],[tabindex="0"]';
 const selector=routes.map(([box])=>box).join(',');
 document.addEventListener('click', event=>{
  if(event.defaultPrevented||event.button!==0||event.ctrlKey||event.metaKey||event.altKey||event.shiftKey)return;
  if(!(event.target instanceof Element)||event.target.closest(controls))return;
  const box=event.target.closest(selector);
  if(!box||box.closest('[inert],[hidden],[aria-disabled="true"]'))return;
  const selected=getSelection();
  if(selected&&!selected.isCollapsed&&box.contains(selected.anchorNode))return;
  for(const [match,targets] of routes){
   if(!box.matches(match))continue;
   for(const target of targets){
    const action=box.querySelector(target);
    if(!action||action.matches(':disabled,[aria-disabled="true"]')||action.closest('[hidden],[inert]')||!action.getClientRects().length)continue;
    event.preventDefault();action.click();return;
   }
   return;
  }
 });
})();
