'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const sourceRoot=process.env.WAVELINK_TEST_SOURCE||path.resolve(__dirname,'..');
const escape=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
function load(locale,rights=new Set(['hr.view_own','hr.documents_submit','hr.expenses_submit','hr.timesheets_submit'])){
 const uid='00000000-0000-0000-0000-000000000001';
 const window={addEventListener(){},WAVELINK_LOCALE:locale||'en'};
 const context=vm.createContext({window,document:{},location:{hash:'#hr/me'},AJInterface:{markup:x=>x},console,Map,Set,URLSearchParams});
 vm.runInContext(fs.readFileSync(sourceRoot+'/app/static/locale_pt_br.js','utf8'),context);
 vm.runInContext(fs.readFileSync(sourceRoot+'/app/static/i18n_pt_br.js','utf8'),context);
 let source=fs.readFileSync(sourceRoot+'/app/static/hr_workspace.js','utf8');
 source=source.replace('return Object.freeze({init,handles,open,syncSession,hasForm,exitBusy,guardRoute,profileLink});',`return Object.freeze({init,handles,open,syncSession,hasForm,exitBusy,guardRoute,profileLink,__test:{formFields,departmentField,defaults,card,payload,cents,decimal,date,formPermission,setDirectory(value){directory=value},setOverview(value){overview=value}}});`);
 vm.runInContext(source,context);
 const module=window.AJHR;module.init({session:()=>uid,account:()=>uid,person:()=>({user_id:uid}),can:key=>rights.has(key),escape});
 module.__test.setDirectory({me:{id:uid},capabilities:Object.fromEntries([...rights].map(key=>[key,true])),departments:[{id:'travel-dept',name:'Travel'}]});
 module.__test.setOverview({person:{id:uid,name:'Draft'}});
 return {window,context,module,uid,test:module.__test};
}
(async()=>{
 const pt=load('pt-BR'),en=load();
 assert(pt.module.profileLink({is_me:true}).includes('Meus registros de RH'));
 assert(en.module.profileLink({is_me:true}).includes('My HR records'));
 assert.equal(pt.module.profileLink({is_me:false}),'');
 assert.equal(load('pt-BR',new Set()).module.profileLink({is_me:true}),'');
 const d=pt.test.defaults('documents');d.type='medical';d.title='Draft';d.notes='<script>alert(1)</script>';
 const rendered=pt.test.formFields({kind:'documents',mode:'save',values:d});
 assert(rendered.includes('Tipo de documento')&&rendered.includes('Atestado médico'));
 assert(rendered.includes('value="medical"')&&rendered.includes('value="Draft"'));
 assert(rendered.includes('&lt;script&gt;')&&!rendered.includes('<script>'));
 const departments=pt.test.departmentField({values:{department_id:'travel-dept'}});
 assert(departments.includes('>Travel</option>')&&!departments.includes('>Viagens</option>'));
 const expense=pt.test.defaults('expenses');Object.assign(expense,{amount:'19,25',currency:'brl',title:'Draft'});
 const before=JSON.stringify(expense),payload=await pt.test.payload({kind:'expenses',mode:'save',values:expense});
 assert.equal(payload.amount,'19.25');assert.equal(payload.currency,'BRL');assert.equal(payload.title,'Draft');assert.equal(JSON.stringify(expense),before);
 const timesheet=pt.test.defaults('timesheets');timesheet.entries[0].hours='12,50';
 assert.equal((await pt.test.payload({kind:'timesheets',mode:'save',values:timesheet})).entries[0].hours,'12.50');
 assert.equal(pt.test.date('2026-10-17'),'17/10/2026');assert.equal(en.test.date('2026-10-17'),'2026-10-17');
 assert.equal(pt.test.cents('19,25'),1925n);assert.equal(en.test.cents('19,25'),null);
 assert.equal(pt.test.formPermission({kind:'travel',mode:'save',values:{user_id:pt.uid}}),false);
 assert.equal(pt.test.formPermission({kind:'expenses',mode:'save',values:{user_id:'someone-else'}}),false);
 assert.equal(pt.test.formPermission({kind:'expenses',mode:'review',values:{user_id:pt.uid}}),false);
 const card=pt.test.card('documents',{id:'record',version:1,user_id:pt.uid,title:'Draft',type:'medical',reference:'Training',expiry_mode:'dated',expires_on:'2026-12-31',reminder_days:90,attachment_count:0,expiry_status:'current'});
 assert(card.includes('<h3>Draft</h3>')&&card.includes('Training')&&card.includes('Atestado médico')&&card.includes('90 dias')&&card.includes('31/12/2026'));
 for(const loaded of [pt,en]){
  vm.runInContext(fs.readFileSync(sourceRoot+'/app/static/workspace_catalogue.js','utf8'),loaded.context);
  const cat=loaded.window.AJWorkspaceCatalogue;
  assert.equal(cat.available(()=>false,{user_id:loaded.uid}).some(row=>row.key==='hr'),false);
  assert.equal(cat.available(key=>key==='hr.view_own',{user_id:loaded.uid}).some(row=>row.key==='hr'),true);
 }
 assert.equal(pt.window.AJWorkspaceCatalogue.rows.find(row=>row.key==='hr').title,'Recursos Humanos');
 assert.equal(en.window.AJWorkspaceCatalogue.rows.find(row=>row.key==='hr').title,'HR & personal records');
 assert(pt.window.AJWorkspaceCatalogue.matches('hr','recursos humanos'));
 assert(pt.window.AJWorkspaceCatalogue.matches('hr','passaporte'));
 console.log('Portuguese HR UI: labels, own-profile discovery, literal employee data/HTML safety, API enums, exact comma decimals, dates, catalogue search, English fallback and permission boundaries passed.');
})().catch(error=>{console.error(error);process.exitCode=1});
