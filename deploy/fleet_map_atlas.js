function interactiveFleetMap(box, addSvg, make, sites){
 const t=fmT;
 const pts=sites.map((s,i)=>({p:s.position,i,name:s.name})).filter(({p})=>p&&Number.isFinite(p.lat)&&Number.isFinite(p.lon)&&Math.abs(p.lat)<=90&&Math.abs(p.lon)<=180);
 const rio=[['Rio de Janeiro',-43.1729,22.9068],['Cabo Frio',-42.019,22.88],['Macaé',-41.786,22.377]];
 const regional=[['Niterói',-43.1046,22.8832],['Maricá',-42.8183,22.9194],['Arraial do Cabo',-42.0278,22.9663],['Búzios',-41.886,22.753],['Rio das Ostras',-41.945,22.527],['Saquarema',-42.511,22.929]];
 const coast=pts.length>0&&pts.every(({p})=>p.lon>=-45&&p.lon<=-40&&p.lat>=-24&&p.lat<=-21.4);
 const anchors=pts.map(({p})=>[p.lon,-p.lat]).concat(coast?rio.map(([,x,y])=>[x,y]):[]);
 const fit=()=>{
   if(!anchors.length)return [0,0,360];
   const x=anchors.map(p=>p[0]),y=anchors.map(p=>p[1]),l=Math.min(...x),r=Math.max(...x),top=Math.min(...y),bot=Math.max(...y);
   return [(l+r)/2,(top+bot)/2,Math.min(360,Math.max(coast?3.25:4,(r-l)*1.34,(bot-top)*2.75))];
 };
 let [cx,cy,w]=fit(),mode='coast',active=null;
 const group=(label)=>{const e=make('div');e.setAttribute('role','group');e.setAttribute('aria-label',label);e.style.cssText='display:flex;flex-wrap:wrap;gap:6px;align-items:center';return e;};
 const header=make('div');header.style.cssText='display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:12px 0;justify-content:space-between';
 const layers=group(t('Camadas','Layers')), controls=group(t('Controles do mapa','Map controls'));header.append(layers,controls);box.append(header);
 const button=(parent,label,fn,visual=label)=>{const b=make('button',visual);b.type='button';b.className='btn';b.setAttribute('aria-label',label);b.addEventListener('click',fn);parent.append(b);return b;};
 const layerCoast=button(layers,t('Costa','Coastline'),()=>layer('coast')),layerSat=button(layers,t('Satélite','Satellite'),()=>layer('satellite'));
 layerCoast.dataset.mapLayer='coast';layerSat.dataset.mapLayer='satellite';
 const zoomIn=button(controls,t('Aproximar','Zoom in'),()=>zoom(.65),'+'),zoomOut=button(controls,t('Afastar','Zoom out'),()=>zoom(1/.65),'−');
 button(controls,t('Enquadrar embarcações','Fit vessels'),()=>{[cx,cy,w]=fit();draw()});
 button(controls,t('Mapa-múndi','World view'),()=>{[cx,cy,w]=[0,0,360];draw()});
 const viewport=make('div');viewport.style.cssText='border-radius:12px;overflow:hidden;border:1px solid #819eaf;background:#dcecf3';box.append(viewport);
 const map=addSvg(viewport,'svg',{width:'100%',role:'img',tabindex:'0','aria-label':t('Mapa interativo. Use as setas para mover e mais ou menos para ajustar o zoom.','Interactive map. Use arrow keys to move and plus or minus to zoom.')});
 map.dataset.fleetBasemap='natural-earth';map.style.cssText='display:block;aspect-ratio:2/1;max-height:510px;touch-action:none;cursor:grab;background:#dcecf3';
 addSvg(map,'rect',{x:-180,y:-90,width:360,height:180,fill:'#cce4ef'});
 const land={fill:'#e3e7cf',stroke:'#577882','stroke-width':'1','vector-effect':'non-scaling-stroke','fill-rule':'evenodd'};
 const world=addSvg(map,'path',{d:fleetLand.world,...land});
 const detail=addSvg(map,'g',{});addSvg(detail,'rect',{x:-45,y:21.4,width:5,height:2.6,fill:'#cce4ef'});addSvg(detail,'path',{d:fleetLand.rio,...land});
 const photos=addSvg(map,'g',{'aria-hidden':'true'}),cities=addSvg(map,'g',{'aria-hidden':'true'}),markers=addSvg(map,'g',{});
 const legend=make('div');legend.style.cssText='display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 14px;padding:6px 11px;background:#f4f8fa;color:#294858;font-size:.8rem';
 const scale=make('strong'),credit=make('span');legend.append(scale,credit);viewport.append(legend);
 const picker=make('label',t('Centralizar em uma embarcação','Center on a vessel'));picker.style.cssText='display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:12px 0 7px';
 const select=make('select');select.dataset.mapVessel='true';select.style.maxWidth='100%'; const empty=make('option',t('Selecione uma embarcação','Select a vessel'));empty.value='';select.append(empty);
 for(const v of pts){const o=make('option',v.name);o.value=String(v.i);select.append(o);}
 select.disabled=!pts.length;picker.append(select);box.append(picker);
 const summary=make('div',t('Toque em um marcador para ver a última posição informada.','Select a pin to see its last reported position.'));summary.dataset.mapDetails='true';summary.setAttribute('aria-live','polite');summary.style.cssText='padding:8px 0;min-height:2.2rem';box.append(summary);
 const google=button(box,t('Ver esta área no Google Maps','Open this area in Google Maps'),()=>{
   const widthPx=Math.max(300,map.clientWidth);
   const z=Math.max(0,Math.min(18,Math.round(Math.log2(360*widthPx/(256*w)))));
   const url=new URL('https://www.google.com/maps/@');
   url.search=new URLSearchParams({api:'1',map_action:'map',basemap:'satellite',center:(-cy).toFixed(5)+','+cx.toFixed(5),zoom:String(z)});
   window.open(url.href,'_blank','noopener,noreferrer');
 });
 google.title=t('Abre o Google Maps em outra aba, compartilhando o centro e o zoom desta vista.','Opens Google Maps in another tab, sharing this view’s center and zoom.');
 const coords=(x,d)=>Math.abs(x).toFixed(4)+'° '+(x>=0?d[0]:d[1]);
 function choose(v,recenter){
   if(!v){active=null;summary.textContent=t('Toque em um marcador para ver a última posição informada.','Select a pin to see its last reported position.');draw();return}
   active=v.i;select.value=String(v.i);
   const time=new Date(v.p.observed),stale=Date.now()-time.valueOf()>86400000;
   const status=stale?t('Desatualizada','Stale'):t('Informada','Reported');
   const title=make('strong',v.name),notes=make('span',' · '+status+' · '+coords(v.p.lat,'NS')+'  '+coords(v.p.lon,'EW')+(Number.isFinite(time.valueOf())?' · '+time.toISOString().slice(0,16).replace('T',' ')+' UTC':''));
   summary.replaceChildren(title,notes);
   if(recenter){cx=v.p.lon;cy=-v.p.lat;w=Math.min(w,1.9)}
   draw();
 }
 select.addEventListener('change',()=>choose(pts.find(v=>String(v.i)===select.value),true));
 map.addEventListener('click',e=>{const item=e.target.closest('[data-vessel-pin]');if(item)choose(pts.find(v=>v.i+1===Number(item.dataset.vesselPin)),false)});
 function layer(next){
   mode=next;
   for(const [button,type] of [[layerCoast,'coast'],[layerSat,'satellite']]){
     const on=next===type;button.setAttribute('aria-pressed',String(on));
     button.style.background=on?'#145d74':'';button.style.color=on?'#fff':'';
   }
   map.dataset.fleetLayer=mode;
   if(mode==='satellite'&&!photos.firstChild){
     addSvg(photos,'image',{x:-180,y:-90,width:360,height:180,href:'__WORLD_IMAGE__',preserveAspectRatio:'none'});
     addSvg(photos,'image',{x:-45,y:21.4,width:5,height:2.6,href:'__RIO_IMAGE__',preserveAspectRatio:'none'});
   }
   photos.setAttribute('display',mode==='satellite'?'inline':'none');draw();
 }
 const draw=()=>{
   const h=w/2;cx=Math.min(180-w/2,Math.max(-180+w/2,cx));cy=Math.min(90-h/2,Math.max(-90+h/2,cy));
   map.setAttribute('viewBox',[cx-w/2,cy-h/2,w,h].join(' '));
   const detailShown=w<=5&&cx-w/2>=-45&&cx+w/2<=-40&&cy-h/2>=21.4&&cy+h/2<=24;
   detail.setAttribute('display',detailShown?'inline':'none');
   if(photos.lastChild)photos.lastChild.setAttribute('display',detailShown?'inline':'none');
   const k=w/Math.max(290,Math.min(760,map.clientWidth||530));
   const visible=(x,y,pad=0)=>Math.abs(x-cx)<=w/2-pad&&Math.abs(y-cy)<=h/2-pad;
   cities.replaceChildren();markers.replaceChildren();
   const bright=mode==='satellite',occupied=[];
   if(w<=7) for(const [name,x,y] of (w<=1.8?[...rio,...regional]:rio)){
     if(!visible(x,y,k*8)||occupied.some(([ax,ay])=>Math.abs(ax-x)<k*65&&Math.abs(ay-y)<k*16))continue;
     occupied.push([x,y]);addSvg(cities,'circle',{cx:x,cy:y,r:k*2.3,fill:bright?'#ffdb82':'#386276'});
     const left=x>cx+w*.24, color=bright?'#fff8e2':'#163b50';
     addSvg(cities,'text',{x:x+(left?-1:1)*k*5,y:y-k*6,'text-anchor':left?'end':'start','font-size':k*12,'font-weight':700,fill:color,stroke:bright?'#0b2338':'#f4fbf8','stroke-width':k*2.7,'paint-order':'stroke'},name);
   }
   for(const {p,i,name} of [...pts].sort((a,b)=>Number(a.i===active)-Number(b.i===active))){
     const x=p.lon,y=-p.lat;if(!visible(x,y))continue;
     const stale=Date.now()-Date.parse(p.observed)>86400000,on=i===active;
     const pin=addSvg(markers,'g',{'data-vessel-pin':String(i+1),style:'cursor:pointer'});
     addSvg(pin,'title',{},name);
     const f=on?1.2:1;const r=k*f;
     if(on)addSvg(pin,'circle',{cx:x,cy:y,r:r*14,fill:'#228baf','fill-opacity':'.38'});
     addSvg(pin,'circle',{cx:x,cy:y,r:r*10.5,fill:stale?'#9a5b00':'#0c5776',stroke:'#fff','stroke-width':r*1.8});
     addSvg(pin,'path',{d:'M '+(x-r*5.3)+' '+(y+r*1.8)+' L '+(x+r*5.3)+' '+(y+r*1.8)+' L '+(x+r*2.1)+' '+(y+r*5)+' L '+(x-r*2.1)+' '+(y+r*5)+' Z M '+(x-r*2.7)+' '+(y+r*.3)+' V '+(y-r*3.4)+' H '+(x+r*2.5)+' V '+(y+r*.3),fill:'#fff'});
   }
   const nm=w*60*Math.cos(cy*Math.PI/180);

   scale.textContent='↑ N'+(w<=18 ? ' · '+t('Largura da vista:','View width:')+' ≈ '+new Intl.NumberFormat(document.documentElement.lang||'en',{maximumFractionDigits:1}).format(nm)+' NM' : '');
   credit.textContent=bright?t('Imagem histórica: NASA Earth Observatory · não é ao vivo','Historical imagery: NASA Earth Observatory · not live'):'Natural Earth';
   zoomIn.disabled=w<=.25;zoomOut.disabled=w>=360;
 };
 const zoom=(factor,f=[.5,.5])=>{const next=Math.max(.25,Math.min(360,w*factor));cx+=(f[0]-.5)*(w-next);cy+=(f[1]-.5)*(w-next)/2;w=next;draw()};
__POINTER_CONTROLS__
 layer('coast');
 const resize=new ResizeObserver(()=>{if(map.isConnected)draw();else resize.disconnect()});resize.observe(map);
 return map;
}
