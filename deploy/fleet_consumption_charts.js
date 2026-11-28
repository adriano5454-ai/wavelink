function fleetConsumptionOverview(overview, related, fmt, make) {
 const tr=(pt,en)=>fmT(pt,en), utc=86400000, svgNS='http://www.w3.org/2000/svg';
 const dateFmt=new Intl.DateTimeFormat(document.documentElement.lang,{timeZone:'UTC',month:'short',day:'numeric'});
 const numberFmt=new Intl.NumberFormat(document.documentElement.lang,{notation:'compact',maximumFractionDigits:1});
 const svg=(tag,attrs={},value='')=>{
  const el=document.createElementNS(svgNS,tag);for(const [k,v] of Object.entries(attrs))el.setAttribute(k,v);
  el.textContent=value;return el;
 };
 const grid=make('div');grid.className='wl-usage-grid';
 const heading=make('h3',tr('Consumo no período','Consumption in this period'));
 const caveat=make('p',tr('Somente dias com balanço registrado. Espaços em branco não são consumo zero.','Only recorded days are plotted. Gaps do not mean zero consumption.'));
 caveat.className='wl-usage-note';
 overview.replaceChildren(heading,caveat,grid);
 for(const [key,label,unit,color] of [
 ['fresh_water',tr('Água doce','Freshwater'),'m³','#087f83'],
 ['diesel','Diesel','L','#335f9b']]){
  const art=make('article');art.className='wl-usage-tile';art.dataset.usageKind=key;
  const head=make('div');head.className='wl-usage-label';head.append(make('h4',label),make('span',unit));art.append(head);grid.append(art);
  const rows=related(key).filter(r=>Number.isFinite(r.used)&&r.used>=0&&Number.isFinite(Date.parse(r.day))).slice().reverse();
  if(!rows.length){art.append(make('p',tr('Sem balanços neste período.','No daily balances in this period.')));continue;}
  const dates=rows.map(r=>Date.parse(r.day)), first=Math.min(...dates), last=Math.max(...dates), days=Math.round((last-first)/utc)+1;
  const total=rows.reduce((s,r)=>s+Math.round(r.used*1000),0)/1000;
  const stat=make('div');stat.className='wl-usage-stat';stat.append(make('strong',fmt.format(total)+' '+unit),make('span',rows.length+' '+(rows.length===1?tr('dia registrado','recorded day'):tr('dias registrados','recorded days'))));art.append(stat);
  const max=Math.max(...rows.map(r=>r.used)), step=Math.pow(10,Math.floor(Math.log10(max||1)));
  const limit=Math.ceil((max||1)/step)*step, left=49,right=335,baseline=100,height=79;
  const width=(right-left)/days, barW=Math.min(24,Math.max(.8,width*.72));
  const img=svg('svg',{viewBox:'0 0 348 132',role:'img','aria-label':label+' · '+tr('consumo diário registrado','recorded daily consumption')+' · '+unit,class:'wl-usage-chart'});
  for(const t of [1,.5,0]){
   const y=baseline-height*t;
   img.append(svg('line',{x1:left,x2:right,y1:y,y2:y,class:'wl-usage-rule'}),svg('text',{x:left-7,y:y+4,'text-anchor':'end'},numberFmt.format(limit*t)));
  }
  for(let i=0;i<rows.length;i++){
   const r=rows[i], x=left+(Math.round((dates[i]-first)/utc)+.5)*width,q=r.used>0?height*r.used/limit:0;
   const bar=q>0?svg('rect',{x:x-barW/2,y:baseline-q,width:barW,height:q,rx:Math.min(2,barW/2),fill:color,'data-day':r.day}):
    svg('circle',{cx:x,cy:baseline,r:2,fill:color,'data-day':r.day});
   bar.append(svg('title',{},r.day+' · '+fmt.format(r.used)+' '+unit+(r.sample?' · '+tr('Teste','Practice'):'')));img.append(bar);
  }
  for(const [x,d,anchor] of first===last?[[ (left+right)/2,first,'middle']]:[[left,first,'start'],[right,last,'end']]){
   img.append(svg('text',{x,y:121,'text-anchor':anchor},dateFmt.format(d)));
  }
  art.append(img);
 }
}
