/* UI118: only authored UI literals pass through this adapter. No DOM observer,
 * storage rewrite, global fetch interception, or automatic translation of records. */
(function(global){
 'use strict';
 const locale=global.WAVELINK_LOCALE==='pt-BR'?'pt-BR':'en';
 const dictionary=Object.freeze(global.WAVELINK_PT_BR||{});
 const own=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
 const folded=new Map(Object.keys(dictionary).map(key=>[key.toLocaleLowerCase('en'),key]));
 function t(source){
  if(typeof source!=='string'||locale!=='pt-BR')return source;
  if(own(dictionary,source))return dictionary[source];
  const key=source.trim().replace(/\s+/g,' ');
  let match=own(dictionary,key)?key:folded.get(key.toLocaleLowerCase('en'));
  let prefix='',suffix='';
  if(!match){const decorated=key.match(/^([＋+✓→↗›]\s*)(.*)$/);if(decorated){prefix=decorated[1];match=folded.get(decorated[2].toLocaleLowerCase('en'));}}
  if(!match&&key.endsWith(':')){suffix=':';match=folded.get(key.slice(0,-1).toLocaleLowerCase('en'));}
  if(!match)return source;
  let translated=dictionary[match];
  if(/[A-Z]/.test(key)&&key===key.toUpperCase())translated=translated.toLocaleUpperCase('pt-BR');
  return source.slice(0,source.length-source.trimStart().length)+prefix+translated+suffix+source.slice(source.trimEnd().length);
 }
 const decode=s=>s.replace(/&(?:amp|lt|gt|quot|#39|apos|nbsp);/g,x=>({'&amp;':'&','&lt;':'<','&gt;':'>','&quot;':'"','&#39;':"'",'&apos;':"'",'&nbsp;':' '}[x]));
 const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function textFragment(source){
  const decoded=decode(source),translated=t(decoded);
  if(translated!==decoded)return escape(translated);
  if(decoded.includes('\uE000')){
   const markers=[];
   const key=decoded.replace(/\uE000\d+\uE001/g,marker=>'{'+(markers.push(marker)-1)+'}');
   const localized=t(key);
   if(localized!==key)return escape(localized.replace(/\{(\d+)\}/g,(match,i)=>markers[Number(i)]??match));
   return source.split(/(\uE000\d+\uE001)/g).map((part,i)=>i%2?part:textFragment(part)).join('');
  }
  // Separators delimit independent authored labels; interpolated values never
  // enter this function. Retain punctuation and whitespace exactly.
  return source.split(/(\s*[·|]\s*|\s+—\s+)/).map((part,i)=>i%2?part:(t(decode(part))!==decode(part)?escape(t(decode(part))):part)).join('');
 }
 function markup(source){
  if(locale!=='pt-BR'||typeof source!=='string')return source;
  return source.replace(/\b(aria-label|title|placeholder|alt)=(['"])(.*?)\2/gi,(_,name,quote,value)=>name+'='+quote+textFragment(value)+quote)
   .replace(/(^|>)([^<>]+)(?=<|$)/g,(_,start,body)=>start+textFragment(body));
 }
 function html(strings,...values){
  // Translation is applied to the source segments before user values are joined.
  let source='';
  for(let i=0;i<strings.length;i++)source+=strings[i]+(i<values.length?'\uE000'+i+'\uE001':'');
  return markup(source).replace(/\uE000(\d+)\uE001/g,(_,i)=>String(values[Number(i)]));
 }
 function template(strings,...values){
  if(locale!=='pt-BR'){let result='';for(let i=0;i<strings.length;i++)result+=strings[i]+(i<values.length?String(values[i]):'');return result;}
  const source=strings.map((s,i)=>s+(i<values.length?'{'+i+'}':'')).join('');
  const translated=t(source);
  if(translated!==source)return translated.replace(/\{(\d+)\}/g,(_,i)=>String(values[Number(i)]));
  let result='';for(let i=0;i<strings.length;i++)result+=t(strings[i])+(i<values.length?String(values[i]):'');return result;
 }
 Object.defineProperty(global,'WavelinkI18n',{value:Object.freeze({locale,t,markup,html,template}),writable:false,configurable:false});
 if(global.document)global.document.documentElement.lang=locale;
})(window);
