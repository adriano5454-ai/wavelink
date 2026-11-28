/* One bar per visible register; segments are counts, not a compliance score. */
function readinessSourceChart(d,{el,T,joined,categories,levels,scope}){
 const card=el('section',undefined,'card wl-readiness-chart');
 card.append(el('h2',T('Readiness by source','Prontidão por fonte')),
  el('p',T('Records checked for the findings below. This is not a compliance score.','Registros conferidos para as pendências abaixo. Isto não é uma nota de conformidade.')));
 const key=el('div',undefined,'wl-readiness-key');
 const keys={...levels,none:[T('No finding in this check','Sem pendência nesta conferência')]};
 for(const [name,label] of Object.entries(keys)){
  const chip=el('span');chip.dataset.key=name;chip.textContent=joined(label);key.append(chip);
 }
 card.append(key);
 const svg=(tag,attr)=>{const n=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const [k,v] of Object.entries(attr))n.setAttribute(k,v);return n;};
 for(const [kind,v] of Object.entries(d.sources)){
  const row=el('section',undefined,'wl-chart-row'), title=el('div',undefined,'wl-chart-heading');
  const finding=Object.values(v.findings).reduce((a,b)=>a+b,0);
  title.append(el('h3',joined(categories[kind])),el('span',v.records?finding+' / '+v.records+' '+T('with findings','com pendências'):T('No records to check','Sem registros para conferir')));
  row.append(title);
  if(v.records){
   const chart=svg('svg',{viewBox:'0 0 1000 10',preserveAspectRatio:'none','aria-hidden':'true'});
   let x=0;
   for(const name of Object.keys(keys)){
    const amount=name==='none'?v.records-finding:v.findings[name];
    const w=amount/v.records*1000;
    if(w){const bar=svg('rect',{x,y:0,width:w,height:10});bar.dataset.key=name;chart.append(bar);}
    x+=w;
   }
   row.append(chart);
   const n=Object.entries(v.findings).filter(([,n])=>n>0).map(([k,n])=>n+' '+joined(levels[k]));
   row.append(el('small',n.length?n.join(' · '):T('No findings in the checked records','Nenhuma pendência nos registros conferidos')));
  }
  card.append(row);
 }
 return card;
}

