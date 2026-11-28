let readingRange={period:'1'},readingRangeConsumption=false,readingRangeProduct='fresh_water',readingRangeEditing=false,readingRangeDraft={};
function readingRangeQuery(id){
 return new URLSearchParams({site_id:id,...readingRange}).toString();
}
function readingRangeControls(make,range){
 const block=make('div');block.style.cssText='display:flex;flex-wrap:wrap;align-items:end;gap:.5rem;margin:1rem 0';
 const selectRange=make('select');selectRange.id='vessel-reading-period';
 for(const [v,t] of [['1',fmT('1 mês','1 month')],['3',fmT('3 meses','3 months')],['6',fmT('6 meses','6 months')],['12',fmT('12 meses','12 months')],['custom',fmT('Personalizado','Custom')]]){
  const o=make('option',t);o.value=v;selectRange.append(o);
 }
 selectRange.value=readingRangeEditing?'custom':readingRange.period;
 function wrap(t,input){const l=make('label',t);l.style.cssText='display:grid;gap:.25rem;max-width:100%';l.append(input);return l;}
 const start=make('input'),end=make('input');start.type=end.type='date';start.value=readingRangeDraft.from??range.from;end.value=readingRangeDraft.to??range.to;
 start.max=end.max=new Date().toISOString().slice(0,10);
 const form=make('div');form.style.cssText='display:flex;flex-wrap:wrap;align-items:end;gap:.5rem';
 const apply=make('button',fmT('Mostrar período','Show date range'));apply.id='vessel-reading-range-apply';apply.type='button';apply.className='btn';
 const status=make('p',range.from+' → '+range.to+' (UTC)');status.style.margin='0';status.setAttribute('aria-live','polite');
 form.append(wrap(fmT('De (UTC)','From (UTC)'),start),wrap(fmT('Até (UTC)','To (UTC)'),end),apply);
 const custom=()=>{form.style.display=selectRange.value==='custom'?'flex':'none';};
 const load=next=>{readingRangeEditing=false;readingRangeDraft={};readingRange=next;route();};
 selectRange.onchange=()=>{readingRangeEditing=selectRange.value==='custom';custom();if(!readingRangeEditing)load({period:selectRange.value});}; start.oninput=()=>{readingRangeDraft.from=start.value;};end.oninput=()=>{readingRangeDraft.to=end.value;};
 apply.onclick=()=>{
  if(!start.value||!end.value||start.value<'1900-01-01'||start.value>end.value||end.value>end.max||Date.parse(end.value)-Date.parse(start.value)>366*86400000){
   status.textContent=fmT('Informe datas UTC válidas de até 12 meses, sem datas futuras.','Enter valid UTC dates up to 12 months, with no future dates.');return;
  }
  load({period:'custom',start:start.value,end:end.value});
 };
 custom();block.append(wrap(fmT('Período','Period'),selectRange),form,status);return block;
}
