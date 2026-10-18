/* UI122: exercise the real permission editor; no server or credentials used. */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path'),cp=require('node:child_process');
const root=process.env.WAVELINK_TEST_SOURCE;
assert(root,'Set WAVELINK_TEST_SOURCE');
const groups=JSON.parse(cp.execFileSync(process.env.WAVELINK_TEST_PYTHON||'python',['-c',"import ast,json,sys; m=ast.parse(open(sys.argv[1],encoding='utf8').read()); print(json.dumps(next(ast.literal_eval(n.value) for n in m.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GROUPS' for t in n.targets))))",path.join(root,'app/access.py')],{encoding:'utf8'}));
const source=fs.readFileSync(path.join(root,'app/static/browser_admin.js'),'utf8');
const allKeys=groups.flatMap(([,rows])=>rows.map(([key])=>key));
function setup(locale,script=source) {
 const nodes=new Map(),calls=[];
 const node=id=>{
  if(nodes.has(id))return nodes.get(id);
  const n={id,value:'',checked:false,disabled:false,dataset:{},textContent:'',_html:'',
   addEventListener(type,fn){this['on'+type]=fn;},focus(){},remove(){},setAttribute(){},removeAttribute(){},
   querySelector(){return node('ba-reason');},querySelectorAll(){return [];},
   get innerHTML(){return this._html;},
   set innerHTML(html){this._html=html;for(const m of html.matchAll(/<input\b([^>]*)>/g)){const id=m[1].match(/\bid="([^"]*)"/)?.[1];if(id){const e=node(id);e.checked=/\bchecked\b/.test(m[1]);e.disabled=/\bdisabled\b/.test(m[1]);}}}
  };nodes.set(id,n);return n;
 };
 const directory={users:[],departments:[],groups,defaults:{technician:Object.fromEntries(allKeys.map(k=>[k,false]))},actor_id:'admin'};
 const context={window:{WAVELINK_LOCALE:locale,addEventListener(){}},document:{documentElement:{},getElementById:node,addEventListener(){}},
 state:{hub_id:'fictional',auth:{token:'synthetic-test-token',person:{user_id:'admin',role:'admin'}}},
 location:{hash:'#admin/users'},history:{replaceState(){}},root:node('root'),AJInterface:{markup:s=>s},toast(){},message:e=>e.message,uid:()=> 'synthetic-operation',
 api:async(url,request)=>{calls.push({url,request});if(request)return {saved:true,action:request.body.action};return directory;}
 };
 vm.createContext(context);
 for(const name of ['locale_pt_br.js','i18n_pt_br.js'])vm.runInContext(fs.readFileSync(path.join(root,'app/static',name),'utf8'),context);
 const anchor='window.AJBrowserAdmin=Object.freeze(';
 assert(script.includes(anchor));
 const instrumented=script.replace(anchor,'window.__permissionTest={setDirectory:v=>directory=v,permissionForm,userDetails,getForm:()=>form};'+anchor);
 vm.runInContext(instrumented,context);context.window.__permissionTest.setDirectory(directory);
 const user={id:'synthetic-user',name:'Home <script> & Draft',login_id:'synthetic-login',role:'technician',mode:'project_user',revision:7,department_ids:[],enabled:true,policy:{managed_member:false,permissions:Object.fromEntries(allKeys.map(k=>[k,['hr.view_own','hr.documents_manage','hr.timesheets_review','hr.expenses_review'].includes(k)]))}};
 context.window.__permissionTest.permissionForm(user);
 return {context,node,nodes,calls,user,html:node('ba-details').innerHTML,form:()=>context.window.__permissionTest.getForm(),i18n:context.window.WavelinkI18n};
}
const checks=[];function pass(name,fn){fn();checks.push(name);}
(async()=>{
 const pt=setup('pt-BR'),en=setup('en');
 pass('Portuguese headings and all permission labels',()=>{
  for(const [group,rows] of groups){assert.notEqual(pt.i18n.t(group),group,group);assert(pt.html.includes(pt.i18n.t(group).replace(/&/g,'&amp;')),group);
   for(const [key,label] of rows){assert.notEqual(pt.i18n.t(label),label,key);assert(pt.html.includes(pt.i18n.t(label).replace(/&/g,'&amp;')),key);}
  }
 });
 pass('Company title translated without changing employee text',()=>{
  assert(pt.html.includes('Permissões da empresa — Home &lt;script&gt; &amp; Draft'));
  assert(!pt.html.includes('Início &lt;script&gt;'));assert(!pt.html.includes('<script>'));
 });
 pass('Scope and safety explanations in Portuguese',()=>{
  for(const text of ['Estas permissões são concedidas diretamente','Cada colaborador consulta e envia','Editar escalas e alocar pessoas','Biblioteca compartilhada da empresa','As permissões salvas são mantidas','Revisei separadamente a permissão'])assert(pt.html.includes(text),text);
  assert(!pt.html.includes('These are the independent'));assert(!pt.html.includes('Own records and submission'));
 });
 pass('Expense review remains distinct from reimbursement payment',()=>{
  assert(pt.html.includes('Analisar despesas apresentadas pelos colaboradores'));
  assert(!pt.html.includes('Analisar reembolso de outros colaboradores'));
 });
 pass('Original permission identifiers and selected values preserved',()=>{
  assert.deepEqual(JSON.parse(JSON.stringify(pt.form().payload().permissions)),pt.user.policy.permissions);
  assert.equal(pt.form().payload().id,'synthetic-user');assert.equal(pt.form().payload().revision,7);
  assert.deepEqual([...pt.nodes.keys()].filter(k=>k.startsWith('ba-perm-')).sort(),allKeys.map(k=>'ba-perm-'+k).sort());
 });
 pass('English deployment retains English content',()=>{
  assert(en.html.includes('Company permissions — Home &lt;script&gt; &amp; Draft'));
  assert(en.html.includes('Manage staff personal documents'));
  assert(en.html.includes('These are the independent administrator-owned permission flags.'));
  assert(!en.html.includes('Permissões da empresa'));
 });
 pass('Non-Brazilian locale retains English',()=>{
  assert(setup('pt-PT').html.includes('Company permissions —'));
 });
 pass('Opening the editor never saves or changes authorization',()=>{assert.equal(pt.calls.length,0);assert.equal(en.calls.length,0);});
 pass('Full-database backup still requires separate confirmation',()=>{
  pt.node('ba-perm-backups.export').checked=true;pt.node('ba-form').onchange();assert.equal(pt.node('ba-save').disabled,true);
  pt.node('ba-backup-review').checked=true;pt.node('ba-form').onchange();assert.equal(pt.node('ba-save').disabled,false);
  pt.node('ba-perm-backups.export').checked=false;pt.node('ba-backup-review').checked=false;pt.node('ba-form').onchange();
 });
 await pt.node('ba-form').onsubmit({preventDefault(){}});
 pass('Save without reason and review confirmation remains blocked',()=>{
  assert.equal(pt.calls.length,0);assert.equal(pt.node('ba-result').textContent,'Informe um motivo e confirme a alteração revisada.');
 });
 pt.node('ba-confirm').checked=true;pt.node('ba-reason').value='TESTE SINTETICO';
 await pt.node('ba-form').onsubmit({preventDefault(){}});
 pass('Confirmed save sends identical capability keys and values',()=>{
  const action=pt.calls.find(c=>c.url==='/api/admin/action');assert(action);assert.equal(action.request.body.action,'permissions');
  assert.deepEqual(JSON.parse(JSON.stringify(action.request.body.payload.permissions)),pt.user.policy.permissions);
  assert.equal(action.request.body.confirmed,true);assert.equal(action.request.body.reason,'TESTE SINTETICO');
 });
 pass('Translation dictionary never localizes user-provided data in templates',()=>{
  assert.equal(pt.i18n.html`<p>${'Company permissions'}</p>`,'<p>Company permissions</p>');
 });
 console.log(JSON.stringify({passed:checks.length,permission_labels:allKeys.length,groups:groups.length,checks},null,2));
})().catch(e=>{console.error(e.stack);process.exitCode=1;});
