const usageScratch=new Map();
function renderConsumption(card,result,site,kinds,make){
 const pt=(a,b)=>fmT(a,b), panel=make('section'), fmt=new Intl.NumberFormat(document.documentElement.lang,{maximumFractionDigits:3});
 panel.id='fleet-consumption';card.append(panel);
 panel.append(make('h2',pt('Consumo diário da embarcação','Daily vessel consumption')),
  make('p',pt('Estimativa por balanço de estoque do dia UTC. Some todos os tanques do mesmo produto. As leituras de tanques não geram consumo automaticamente.','Stock-balance estimate for a UTC day. Include all tanks for the same product. Tank readings do not automatically become consumption.')));
 if(result.practice)panel.append(make('p',pt('Dados fictícios. Você pode testar o lançamento: ele aparece apenas aqui e não é salvo.','Fictional data. Try a practice entry: it is only shown here and is not saved.')));
 const pick=make('select'),label=make('label',pt('Produto','Product'));pick.id='consumption-product';label.htmlFor=pick.id;
 const unit=k=>k==='fresh_water'?'m3':'L', symbol=k=>unit(k)==='m3'?'m³':'L';
 const options=kinds.map(([k,n])=>[k,n+' ('+symbol(k)+')']);
 for(const [k,n] of options){const o=make('option',n);o.value=k;pick.append(o);}
 panel.append(label,pick);
 const status=make('p');status.setAttribute('role','status');
 const chart=make('div');chart.id='consumption-chart';
 const related=k=>[...(result.consumption?.[k]||[]),...(result.practice?(usageScratch.get(site?.id)||[]).filter(x=>x.contents===k):[])].sort((a,b)=>b.day.localeCompare(a.day)).slice(0,30);
 const fields=[
  ['opening',pt('Estoque inicial','Opening stock')],['closing',pt('Estoque final','Closing stock')],
  ['received',pt('Recebido (abastecimento)','Received (refill or bunkering)')],['produced',pt('Produzido a bordo','Produced onboard')],
  ['transfer_in',pt('Transferência externa recebida','External transfer in')],['transfer_out',pt('Transferência externa enviada','External transfer out')],
  ['other_out',pt('Outras saídas sem consumo','Other non-consumption removals')]];
 if(site&&(result.can_record_consumption||result.practice)){
  const b=make('button',result.practice?pt('Testar lançamento','Try adding an entry'):pt('Registrar balanço','Record daily balance'));
  b.id='add-consumption';b.className='btn primary';b.style.marginTop='.65rem';panel.append(b);
  b.onclick=()=>{
   const send=operation((p,o)=>action('record_consumption',p,o)), yesterday=new Date(Date.now()-86400000).toISOString().slice(0,10);
   const amountFields=fields.map(([k,n],i)=>field('usage-'+k,n,i<2?'':'0','text',true)).join('');
   const note=pt('Use a unidade indicada em todos os campos. Não conte transferências entre tanques da mesma embarcação nem registre o mesmo movimento duas vezes.','Use the displayed unit for all fields. Do not count transfers between this vessel’s own tanks or enter any movement twice.');
   const read=()=>{
    const contents=val('usage-kind'),day=val('usage-day'),data={site_id:site.id,version:site.version,contents,day,unit:unit(contents)};
    if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||day<'2000-01-01'||day>yesterday)throw Error(pt('Informe um dia UTC já encerrado.','Enter a completed UTC day.'));
    for(const [k] of fields){
     const raw=val('usage-'+k).trim().replace(',','.');
     if(!/^\d+(?:\.\d{1,3})?$/.test(raw)||Number(raw)>1e9)throw Error(pt('Informe quantidades não negativas com até três casas decimais.','Enter nonnegative amounts with up to three decimal places.'));
     data[k]=Number(raw);
    }
    const used=(['opening','received','produced','transfer_in'].reduce((s,k)=>s+Math.round(1000*data[k]),0)-
      ['closing','transfer_out','other_out'].reduce((s,k)=>s+Math.round(1000*data[k]),0))/1000;
    if(used<0)throw Error(pt('O balanço ficou negativo. Confira os estoques e movimentos.','The balance is negative. Check stocks and movements.'));
    return {data,used};
   };
   modal(b.textContent,'<p>'+note+'</p>'+select('usage-kind',pt('Produto','Product'),options,pick.value)+
    field('usage-day',pt('Data UTC','UTC date'),yesterday,'date',true)+amountFields+
    '<p id="usage-preview" aria-live="polite"></p>',async()=>{
     const {data,used}=read();
     if(related(data.contents).some(r=>r.day===data.day))throw Error(pt('Já existe um balanço deste produto nessa data.','A balance for this product and date already exists.'));
     if(result.practice){
      usageScratch.set(site.id,[...(usageScratch.get(site.id)||[]),{...data,used,sample:true}]);pick.value=data.contents;draw();
      status.textContent=pt('Exemplo adicionado. Nenhum dado foi gravado.','Practice entry added. No data was saved.');
     }else{
      const saved=await send(data);const entry={...data,used:saved.used};result.consumption[data.contents].unshift(entry);pick.value=data.contents;draw();
      status.textContent=pt('Balanço registrado.','Balance recorded.');
     }
     lockTransition();
    },result.practice?pt('Adicionar exemplo','Add practice entry'):pt('Salvar balanço','Save balance'));
   const preview=()=>{
    const kind=val('usage-kind'),production=document.getElementById('usage-produced');
    production.disabled=kind!=='fresh_water';if(production.disabled)production.value='0';
    try{const {used}=read();document.getElementById('usage-preview').textContent=pt('Consumo estimado: ','Estimated consumption: ')+fmt.format(used)+' '+symbol(kind);}
    catch(e){document.getElementById('usage-preview').textContent=!val('usage-opening')||!val('usage-closing')?pt('Preencha o estoque inicial e final para calcular.','Enter opening and closing stock to calculate.'):e.message;}
   };
   for(const id of ['kind','day',...fields.map(([k])=>k)])document.getElementById('usage-'+id)?.addEventListener('input',preview);
   preview();
  };
 }
 if(site&&!result.practice&&!result.can_record_consumption)panel.append(make('p',pt('Somente leitura. Solicite ao administrador permissão para registrar consumo nesta embarcação.','Read only. Ask your administrator for permission to post consumption for this vessel.')));
 panel.append(status,chart);
 function draw(){
  chart.replaceChildren();const k=pick.value,u=symbol(k),rows=related(k);
  if(!rows.length){chart.append(make('p',pt('Nenhum balanço registrado para este produto.','No daily balances recorded for this product.')));return;}
  const newest=rows[0], total=rows.reduce((sum,r)=>sum+Math.round(r.used*1000),0)/1000;
  chart.append(make('p',pt('Último dia registrado: ','Latest recorded day: ')+fmt.format(newest.used)+' '+u+' ('+newest.day+')'),
   make('p',pt('Total dos dias registrados exibidos: ','Total across displayed recorded days: ')+fmt.format(total)+' '+u+' · '+rows.length+' '+pt('dias, não necessariamente consecutivos','days, not necessarily consecutive')),
   make('h3',pt('Últimos 30 dias registrados','Last 30 recorded days')));
  const max=Math.max(1,...rows.map(r=>r.used)), list=make('ul');list.style.cssText='list-style:none;margin:0;padding:0';
  for(const r of rows){
   const li=make('li');li.style.cssText='padding:.5rem 0;border-bottom:1px solid #9cb1bc';
   const row=make('div');row.style.cssText='display:flex;flex-wrap:wrap;justify-content:space-between;gap:.25rem';
   row.append(make('time',r.day+(r.sample?' · '+pt('Teste','Practice'):'')),make('strong',fmt.format(r.used)+' '+u));
   row.querySelector('time').dateTime=r.day;
   const track=make('div');track.style.cssText='height:.55rem;margin:.35rem 0;background:#9cb1bc44;border-radius:1rem';
   track.setAttribute('aria-hidden','true');const bar=make('div');bar.style.cssText='height:100%;border-radius:inherit;background:#14778a;width:'+(r.used/max*100)+'%';track.append(bar);
   const detail=make('details');detail.append(make('summary',pt('Ver balanço','View balance')));
   for(const [field,label] of fields)detail.append(make('div',label+': '+fmt.format(r[field])+' '+u));
   li.append(row,track,detail);list.append(li);
  }chart.append(list);
 }
 pick.onchange=draw;draw();return panel;
}
