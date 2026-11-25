let employeeSheet=null, sheetFullAction=null;
function dismissEmployeeSheet(restore){
 const sheet=employeeSheet;if(!sheet)return;
 employeeSheet=null;sheet.dialog.close();sheet.dialog.remove();
 if(restore&&sheet.trigger.isConnected&&sheet.owner===identity()){
   sheet.trigger.focus({preventScroll:true});
   history.scrollRestoration=sheet.previousScrollMode;
   window.scrollTo({top:sheet.y,behavior:'instant'});revealMobileEmployee();
   requestAnimationFrame(()=>{
     if(!employeeSheet&&current()&&overview?.person.id===sheet.personId&&document.activeElement===sheet.trigger)revealMobileEmployee();
   });
 }
}
function showEmployeeSheet(kind,trigger,index,full,fromHistory=false){
 if(!ready()||reading||form||view!=='people'||!canSection(kind)||!['documents','expenses'].includes(kind))return;
 const person=overview.person,owner=identity(),dialog=document.createElement('dialog');
 const valid=()=>current()&&owner===identity()&&overview?.person.id===person.id&&canSection(kind);
 const make=(tag,text)=>{const n=document.createElement(tag);if(text)n.textContent=text;return n};
 const control=(label,action)=>{const b=make('button',label);b.type='button';b.className='btn secondary';b.onclick=action;return b};
 const label=kind==='documents'?wtext('Certificados, exames e cursos','Certificates, medicals and courses'):wtext('Despesas','Expenses');
 const header=make('header'),caption=make('h2',label);caption.id='employee-record-caption';
 header.append(make('strong',person.name),caption);
 const close=()=>{if(employeeSheet?.dialog===dialog)history.back()};
 const closeButton=control(wtext('Fechar','Close'),close);header.append(closeButton);
 dialog.className='hr-employee-sheet';dialog.setAttribute('aria-labelledby',caption.id);
 const field=make('label',wtext('Buscar nos registros carregados','Search loaded records')),input=make('input');input.type='search';field.append(input);
 const results=make('div'),empty=make('p',wtext('Nenhum registro encontrado.','No matching records.'));
 for(const row of overview[kind]){
   if(row.user_id!==person.id)continue;
   const item=make('div');item.innerHTML=AJInterface.markup(card(kind,row,false));results.append(item);
 }
 const filter=()=>{const needle=window.WavelinkUX.fold(input.value.trim());let hits=0;
   for(const item of results.children){item.hidden=!window.WavelinkUX.fold(item.textContent).includes(needle);if(!item.hidden)hits++}
   empty.hidden=hits!==0;
 };
 input.oninput=filter;filter();
 const body=make('div');body.className='hr-employee-sheet-body';body.append(field,results,empty);
 if(overview.truncated?.[kind])body.append(make('p',wtext('Abra a seção completa para ver registros anteriores.','Open the full section for older records.')));
 const footer=make('footer');footer.append(control(wtext('Abrir seção completa','Open full section'),()=>{
   if(valid()){sheetFullAction=full;close()}
 }));
 dialog.append(header,body,footer);host.append(dialog);
 const previousScrollMode=history.scrollRestoration;
 if(!fromHistory)history.scrollRestoration='manual';
 if(!fromHistory)history.pushState({...history.state,wlEmployeeSheet:{id:person.id,kind,index}},'',location.href);
 employeeSheet={dialog,trigger,owner,personId:person.id,previousScrollMode,y:window.scrollY};dialog.addEventListener('cancel',e=>{e.preventDefault();close()});
 dialog.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();e.stopPropagation();close()}});
 dialog.showModal();closeButton.focus({preventScroll:true});
}
window.addEventListener('popstate',()=>{
 const state=history.state?.wlEmployeeSheet;
 if(employeeSheet){
   const next=sheetFullAction;sheetFullAction=null;
   dismissEmployeeSheet(true);if(next&&current()&&!form)next();return;
 }
 if(!state||!current()||form||view!=='people'||overview?.person.id!==state.id||!canSection(state.kind))return;
 const source=host.querySelectorAll('.hr-person-layout > section [data-hr-jump]')[state.index];
 if(source?.dataset.hrJump===state.kind)source.openEmployeeSheet?.(true);
});
