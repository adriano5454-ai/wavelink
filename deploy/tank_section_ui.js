async function showTankSection(id=''){
 beginPage('waterfuel');root.replaceChildren();
 const pending=document.createElement('p');pending.textContent=fmT('Carregando leituras…','Loading readings…');root.append(pending);
 if(id&&!/^[a-f0-9-]{36}$/i.test(id))id='';
 const result=await api('/api/fleet/tank-readings'+(id?'?site_id='+encodeURIComponent(id):''));
 const make=(tag,txt)=>{const e=document.createElement(tag);if(txt!==undefined)e.textContent=txt;return e};
 const card=make('section');card.className='card fleet77-card';
 root.innerHTML=AJInterface.markup(heading(fmT('Água e combustível','Water & fuel'),fmT('Leituras manuais por embarcação. As quantidades de tanques não são somadas.','Manual readings by vessel. Tank quantities are not added together.')));
 const drop=make('select');drop.id='tank-vessel';const label=make('label',fmT('Embarcação','Vessel'));label.htmlFor=drop.id;
 for(const s of [{id:'',name:fmT('Selecione uma embarcação','Select a vessel')},...result.sites]){const opt=make('option',s.name);opt.value=s.id;drop.append(opt);}
 drop.value=id;drop.onchange=()=>{location.hash='waterfuel'+(drop.value?'/'+drop.value:'')};
 card.append(label,drop);root.append(card);
 if(!id){if(!result.sites.length)card.append(make('p',fmT('Nenhuma embarcação disponível.','No vessels available.')));return;}
 const kinds=[['fresh_water',fmT('Água doce','Fresh water')],['diesel','Diesel / MGO'],['fuel_oil',fmT('Óleo combustível','Fuel oil')],['other_fuel',fmT('Outro combustível','Other fuel')]];
 const methods=[['gauge',fmT('Indicador','Gauge')],['sounding',fmT('Sondagem','Sounding')],['manual',fmT('Outra medição manual','Other manual measurement')]];
 const units=[['L','L'],['m3','m³'],['kg','kg'],['t','t']];
 const site=result.sites.find(s=>s.id===id);
 if(result.can_record&&site){const b=make('button',fmT('Registrar leitura','Record reading'));b.className='btn';card.append(b);
 b.onclick=()=>{const send=operation((p,o)=>action('record_tank_reading',p,o));
 modal(fmT('Registrar leitura','Record reading'),field('tr-tank',fmT('Nome ou código do tanque','Tank name or ID'),'','text',true)+select('tr-kind',fmT('Conteúdo','Contents'),kinds,'fresh_water')+field('tr-qty',fmT('Quantidade restante','Remaining quantity'),'','text',true)+select('tr-unit',fmT('Unidade','Unit'),units,'L')+select('tr-method',fmT('Método','Method'),methods,'gauge')+field('tr-at',fmT('Horário UTC','Time (UTC)'),'','datetime-local',true),
 async()=>{const raw=val('tr-qty').trim().replace(',','.');if(!/^\d+(?:\.\d+)?$/.test(raw))throw Error(fmT('Confira a quantidade.','Check the quantity.'));await send({site_id:id,version:site.version,tank:val('tr-tank'),contents:val('tr-kind'),quantity:Number(raw),method:val('tr-method'),unit:val('tr-unit'),observed:val('tr-at')+'Z'});lockTransition();await route();});};
 }
 const render=(title,rows)=>{card.append(make('h2',title));if(!rows.length){card.append(make('p',fmT('Nenhuma leitura registrada.','No readings recorded.')));return;}
 const ul=make('ul');for(const r of rows){const unit=units.find(x=>x[0]===r.unit)?.[1]||r.unit;const qty=new Intl.NumberFormat(document.documentElement.lang,{maximumFractionDigits:12}).format(r.quantity);const li=make('li',r.tank+' · '+(kinds.find(x=>x[0]===r.contents)?.[1]||r.contents)+' · '+qty+' '+unit+' · '+(methods.find(x=>x[0]===r.method)?.[1]||r.method)+' · '+r.observed);li.style.overflowWrap='anywhere';ul.append(li);}card.append(ul);};
 render(fmT('Última leitura por tanque','Latest reading per tank'),result.latest);
 const groups=new Map();
 for(const r of result.history){const k=JSON.stringify([r.tank.trim().toLowerCase(),r.contents,r.unit]);if(!groups.has(k))groups.set(k,[]);groups.get(k).push(r);}
 if(groups.size){
  const hd=make('h2',fmT('Tendência por tanque e unidade','Trend by tank and unit'));const pick=make('select'),lbl=make('label',fmT('Série','Series')),plot=make('div');pick.id='tank-series';lbl.htmlFor=pick.id;card.append(hd,lbl,pick,plot);
  const sets=[...groups.values()];sets.forEach((g,i)=>{const r=g[0],o=make('option',r.tank+' · '+(kinds.find(x=>x[0]===r.contents)?.[1]||r.contents)+' · '+r.unit);o.value=i;pick.append(o);});
  const draw=()=>{plot.replaceChildren();const data=[...sets[Number(pick.value)]].reverse();const first=Date.parse(data[0].observed),last=Date.parse(data.at(-1).observed),max=Math.max(1,...data.map(r=>r.quantity));
   if(data.length<2||first===last){plot.append(make('p',fmT('São necessárias leituras em pelo menos dois horários diferentes.','Readings at two different times are needed.')));return;}
   const svg=(p,n,a,t)=>{const e=document.createElementNS('http://www.w3.org/2000/svg',n);for(const [k,v] of Object.entries(a))e.setAttribute(k,v);if(t)e.textContent=t;p.append(e);return e;};
   const s=svg(plot,'svg',{width:'100%',viewBox:'0 0 600 180',role:'img','aria-label':fmT('Gráfico cronológico da quantidade medida, valores no histórico','Measured quantity over time; exact values in history')});
   const coords=data.map(r=>[60+(Date.parse(r.observed)-first)/(last-first)*528,146-r.quantity/max*130]);
   svg(s,'path',{d:'M60 16V146H588',fill:'none',stroke:'#8c9da4'});svg(s,'polyline',{points:coords.map(p=>p.join(',')).join(' '),fill:'none',stroke:'#157a8b','stroke-width':3});
   coords.forEach(([cx,cy],i)=>{const dot=svg(s,'circle',{cx,cy,r:4,fill:'#157a8b'});svg(dot,'title',{},data[i].observed+' · '+data[i].quantity+' '+data[i].unit);});
   svg(s,'text',{x:3,y:22,fill:'currentColor','font-size':13},String(max));svg(s,'text',{x:32,y:149,fill:'currentColor','font-size':13},'0');
   svg(s,'text',{x:60,y:171,fill:'currentColor','font-size':13},data[0].observed.slice(0,10));svg(s,'text',{x:588,y:171,'text-anchor':'end',fill:'currentColor','font-size':13},data.at(-1).observed.slice(0,10));
  };pick.onchange=draw;draw();
 }

 render(fmT('Histórico recente','Recent history'),result.history);
 if(result.more)card.append(make('p',fmT('São mostradas as 100 leituras mais recentes.','Shows the 100 most recent readings.')));
}
