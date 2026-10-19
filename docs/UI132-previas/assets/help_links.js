/* UI41 Help is a separate tab, including dynamic links and embedded Fleet.
   Do not change working routes, forms, account sessions or draft stores. */
(function(global){
 'use strict';
 function isHelp(href){if(/^\s*#/.test(String(href||'')))return false;try{const u=new URL(href,document.baseURI);return u.origin===new URL(document.baseURI).origin&&(/^\/help(?:\/|$)/.test(u.pathname)||/^\/static\/help(?:[_.]|\/)/.test(u.pathname)||u.pathname==='/install');}catch(_){return false;}}
 function prepare(a){if(!a?.getAttribute||!isHelp(a.getAttribute('href')||''))return false;a.target='_blank';a.rel='noopener noreferrer';if(!a.title)a.title=global.WavelinkI18n?.t?.('Opens in a new tab')||'Opens in a new tab';return true;}
 function scan(root=document){root.querySelectorAll?.('a[href]').forEach(prepare);if(root.matches?.('a[href]'))prepare(root);}
 function open(url){if(!isHelp(url))throw new Error('Unrecognised Help address.');const a=document.createElement('a');a.href=url;prepare(a);document.body.append(a);a.click();a.remove();}
 // Prepare before any working-page navigation handler. The browser opens the
 // link directly in the user's gesture, preserving modifier/middle clicks.
 for(const name of ['click','auxclick'])document.addEventListener(name,e=>{const a=e.target?.closest?.('a[href]');if(prepare(a))e.stopImmediatePropagation();},true);
 new MutationObserver(rs=>{for(const r of rs)for(const n of r.addedNodes)if(n.nodeType===1)scan(n);}).observe(document.documentElement,{childList:true,subtree:true});
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>scan());else scan();
 global.AJHelpLinks={isHelp,prepare,open};
})(window);
