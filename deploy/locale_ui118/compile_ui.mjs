/* Development-only source compiler. Production consumes the verified Python overlay.
 * npm install --prefix <tool-dir> acorn acorn-walk; set WAVELINK_ACORN_ROOT to it.
 * Source literals are translated before record interpolation; user values and API
 * keys are never looked up by a DOM observer or a JSON serializer. */
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const moduleRoot=process.env.WAVELINK_ACORN_ROOT;
const acorn=require(path.join(moduleRoot,'node_modules/acorn'));
const walk=require(path.join(moduleRoot,'node_modules/acorn-walk'));
const [sourceRoot,catalogPath]=process.argv.slice(2);
const dict=JSON.parse(fs.readFileSync(catalogPath,'utf8'));
const folded=new Set(Object.keys(dict).map(k=>k.toLowerCase()));
const has=s=>Object.prototype.hasOwnProperty.call(dict,s)||(/[A-Z]/.test(s)&&s===s.toUpperCase()&&folded.has(s.trim().replace(/\s+/g,' ').toLowerCase()));
const excluded=new Set(['i18n_pt_br.js','locale_pt_br.js','sw.js','log_package_worker.js']);
const opaqueKeys=new Set(['id','key','name','value','code','status','state','kind','type','action','operation','method','route','path','href','url','hash','filename','file_name','user_id','hub_id','company_id','token','role','permission','field','event']);
const comparison=new Set(['==','===','!=','!==','in','instanceof']);
const machineMethods=new Set(['includes','indexOf','startsWith','endsWith','match','test','split','replace','replaceAll','get','set','append','delete','has','querySelector','querySelectorAll','getElementById','closest','matches','setAttribute','getAttribute','removeAttribute']);
const stats={files:[],literals:0,templates:0};
function protectedContext(n,anc){
 const p=anc.at(-2);if(!p)return true;
 if(p.type==='Property'&&p.key===n&&!p.computed)return true;
 if(p.type==='MemberExpression'&&p.property===n)return true;
 if(p.type==='ImportDeclaration'||p.type==='ExportNamedDeclaration'||p.type==='SwitchCase')return true;
 if(p.type==='BinaryExpression'&&comparison.has(p.operator))return true;
 if(p.type==='ExpressionStatement'&&p.directive)return true;
 if(p.type==='Property'&&p.value===n&&opaqueKeys.has(p.key.name??p.key.value))return true;
 if(p.type==='AssignmentExpression'&&p.left.type==='MemberExpression'&&opaqueKeys.has(p.left.property.name??p.left.property.value))return true;
 if(p.type==='AssignmentPattern'&&opaqueKeys.has(p.left.name))return true;
 if(p.type==='CallExpression'){
  const c=p.callee,name=c.type==='MemberExpression'?(c.property.name??c.property.value):c.name;
  if(machineMethods.has(name)||/^(api|fetch|post|request|save|write|createRecord|updateRecord)$/.test(name||''))return true;
 }
 return false;
}
for(const file of fs.readdirSync(sourceRoot).filter(n=>n.endsWith('.js')&&!excluded.has(n))){
 const full=path.join(sourceRoot,file),source=fs.readFileSync(full,'utf8');
 const already=source.includes('/* UI118 localized source */');
 let ast;try{ast=acorn.parse(source,{ecmaVersion:'latest',sourceType:'script'})}catch(error){throw new Error(file+': '+error.message)}
 const edits=[];
 walk.ancestor(ast,{
  Literal(n,anc){
   if(typeof n.value!=='string'||protectedContext(n,anc))return;
   // Lower-case atoms are protocol/route/status/permission keys in this app.
   // Visible lower-case HTML fragments still pass through markup(), not here.
   if(/^[a-z0-9_.:/#-]+$/.test(n.value))return;
   if(anc.slice(0,-1).some(a=>a.type==='CallExpression'&&a.callee.type==='MemberExpression'&&a.callee.object?.name==='__wl118'))return;
   const html=/<\/?[a-z][\s\S]*>/i.test(n.value)||/^<[^>]+$/.test(n.value);
   if(!html&&!has(n.value))return;
   edits.push({start:n.start,end:n.end,text:`__wl118.${html?'markup':'t'}(${source.slice(n.start,n.end)})`});stats.literals++;
  },
  TemplateLiteral(n,anc){
   const p=anc.at(-2);if(p?.type==='TaggedTemplateExpression'||protectedContext(n,anc))return;
   const raw=n.quasis.map(q=>q.value.cooked||'').join('');
   const html=/<\/?[a-z][\s\S]*>/i.test(raw);
   const key=n.quasis.map((q,i)=>(q.value.cooked||'')+(i<n.expressions.length?'{'+i+'}':'')).join('');
   if(!html&&!has(key)&&!n.quasis.some(q=>has(q.value.cooked||'')))return;
   edits.push({start:n.start,end:n.start,text:'__wl118.'+(html?'html':'template')});stats.templates++;
  }
 });
 let result=source;
 for(const edit of edits.sort((a,b)=>b.start-a.start||b.end-a.end))result=result.slice(0,edit.start)+edit.text+result.slice(edit.end);
 if(edits.length){
  const fallback='\nvar __wl118=window.WavelinkI18n||{t:s=>s,markup:s=>s,html:(s,...v)=>s.reduce((a,p,i)=>a+p+(i<v.length?String(v[i]):\'\'),\'\'),template:(s,...v)=>s.reduce((a,p,i)=>a+p+(i<v.length?String(v[i]):\'\'),\'\')};\n';
  const directive=acorn.parse(result,{ecmaVersion:'latest'}).body[0];
  const at=directive?.directive?directive.end:0;
  if(!already)result='/* UI118 localized source */\n'+result.slice(0,at)+fallback+result.slice(at);
  acorn.parse(result,{ecmaVersion:'latest'});fs.writeFileSync(full,result);stats.files.push({file,edits:edits.length});
 }
}
console.log(JSON.stringify(stats));
