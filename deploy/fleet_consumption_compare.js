function renderFleetConsumptionComparison(card,result,make){
 const t=fmT, fmt=new Intl.NumberFormat(document.documentElement.lang,{maximumFractionDigits:3});
 const wrap=make('section');wrap.className='wl-usage-overview';wrap.id='fleet-usage-compare';
 const title=make('h2',t('Comparar consumo da frota','Compare fleet consumption'));title.id='fleet-usage-compare-title';wrap.setAttribute('aria-labelledby',title.id);
 const note=make('p',t('Totais dos dias registrados no período. Compare também a quantidade de dias com registros: sem registros não significa consumo zero.','Totals for recorded days in the selected period. Check how many days each vessel reported: no records does not mean zero consumption.'));
 note.className='wl-usage-note';
 wrap.append(title,note);card.append(wrap);
 if(result.practice){const p=make('p',t('Dados fictícios da demonstração.','Fictional demo data.'));p.className='wl-usage-note';wrap.append(p);}
 const grid=make('div');grid.className='wl-usage-grid';wrap.append(grid);
 for(const [kind,label,unit] of [['fresh_water',t('Água doce','Freshwater'),'m³'],['diesel','Diesel','L']]){
  const tile=make('article');tile.className='wl-usage-tile';tile.dataset.compareKind=kind;
  const h=make('h3',label+' ('+unit+')');tile.append(h);
  const rows=result.sites.map(s=>[s,result.comparison[s.id]?.[kind]]);
  const max=rows.reduce((n,[,v])=>Math.max(n,v?.total||0),0);
  const scale=make('div');scale.className='wl-compare-scale';scale.setAttribute('aria-hidden','true');
  if(max>0){scale.append(make('span','0'),make('span',fmt.format(max)+' '+unit));tile.append(scale);}
  const list=make('ul');list.className='wl-compare-list';tile.append(list);
  for(const [site,value] of rows){
   const row=make('li');row.dataset.compareSite=site.id;
   const header=make('div');header.className='wl-compare-row';row.append(header);
   const link=make('a',site.name);link.href='#waterfuel/'+encodeURIComponent(site.id);link.addEventListener('click',()=>{readingRangeConsumption=true;});
   header.append(link);
   if(value){
    const amount=make('strong',fmt.format(value.total)+' '+unit);amount.dataset.compareTotal=String(value.total);header.append(amount);
    const track=make('div');track.className='wl-compare-track';track.setAttribute('aria-hidden','true');
    const bar=make('span');bar.style.width=(max ? (100*value.total/max) : 0)+'%';if(value.total===0)bar.dataset.zero='true';track.append(bar);row.append(track);
    row.append(make('small',String(value.days)+' '+(value.days===1?t('dia registrado','recorded day'):t('dias registrados','recorded days'))));
   }else row.append(make('small',t('Sem registros no período','No records in this period')));
   list.append(row);
  }
  grid.append(tile);
 }
}
