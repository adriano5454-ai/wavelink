// Local Natural Earth basemap. Maps display reported positions, never live vessel tracks.
const fleetLand=__FLEET_LAND__;
function interactiveFleetMap(box,addSvg,make,sites){
 const t=fmT, pts=sites.map((s,i)=>({p:s.position,i,name:s.name})).filter(({p})=>p&&Number.isFinite(p.lat)&&Number.isFinite(p.lon)&&Math.abs(p.lat)<=90&&Math.abs(p.lon)<=180);
 const rio=[['Rio de Janeiro',-43.1729,22.9068],['Cabo Frio',-42.019,22.88],['Macaé',-41.786,22.377]];
 const coast=pts.length>0&&pts.every(({p})=>p.lon>=-45&&p.lon<=-40&&p.lat>=-24&&p.lat<=-21.4);
 const bounds=pts.map(({p})=>[p.lon,-p.lat]).concat(coast?rio.map(([,x,y])=>[x,y]):[]);
 const fit=()=>{
   if(!bounds.length)return [0,0,360];
   const x=bounds.map(p=>p[0]),y=bounds.map(p=>p[1]),l=Math.min(...x),r=Math.max(...x),top=Math.min(...y),bot=Math.max(...y);
   return [(l+r)/2,(top+bot)/2,Math.min(360,Math.max(coast?3.25:4,(r-l)*1.34,(bot-top)*2.75))];
 };
 let [cx,cy,w]=fit();
 const controls=make('div');controls.style.cssText='display:flex;flex-wrap:wrap;gap:.45rem;margin:.7rem 0';
 controls.setAttribute('role','group');controls.setAttribute('aria-label',t('Controles do mapa','Map controls'));box.append(controls);
 const button=(text,label,fn)=>{const b=make('button',text);b.type='button';b.className='btn';b.setAttribute('aria-label',label);b.addEventListener('click',fn);controls.append(b);return b;};
 const zoomIn=button('+',t('Aproximar','Zoom in'),()=>zoom(.65)),zoomOut=button('−',t('Afastar','Zoom out'),()=>zoom(1/.65));
 button(t('Enquadrar embarcações','Fit vessels'),t('Enquadrar embarcações','Fit vessels'),()=>{[cx,cy,w]=fit();draw()});
 button(t('Mapa-múndi','World view'),t('Mapa-múndi','World view'),()=>{[cx,cy,w]=[0,0,360];draw()});
 const map=addSvg(box,'svg',{width:'100%',role:'img',tabindex:'0','aria-label':t('Mapa interativo das posições informadas. Use as setas para mover e mais ou menos para ajustar o zoom.','Interactive map of reported positions. Use arrow keys to move and plus or minus to zoom.')});
 map.dataset.fleetBasemap='natural-earth';
 map.style.cssText='display:block;aspect-ratio:2/1;max-height:450px;touch-action:none;cursor:grab;border:1px solid #a0b5be;border-radius:8px;background:#e6f4f7';
 addSvg(map,'rect',{x:-180,y:-90,width:360,height:180,fill:'#dbedf4'});
 const land={fill:'#e8ead7',stroke:'#59757a','stroke-width':'1','vector-effect':'non-scaling-stroke','fill-rule':'evenodd'};
 addSvg(map,'path',{d:fleetLand.world,...land});
 const detail=addSvg(map,'g',{});
 addSvg(detail,'rect',{x:-45,y:21.4,width:5,height:2.6,fill:'#dbedf4'});
 addSvg(detail,'path',{d:fleetLand.rio,...land});
 const cities=addSvg(map,'g',{'aria-hidden':'true'}),markers=addSvg(map,'g',{});
 const caption=make('p',t('Arraste para mover. Use + e − para ajustar o zoom. Base cartográfica: Natural Earth.','Drag to pan. Use + and − to zoom. Basemap: Natural Earth.'));box.append(caption);
 const draw=()=>{
   const h=w/2;
   cx=Math.min(180-w/2,Math.max(-180+w/2,cx));cy=Math.min(90-h/2,Math.max(-90+h/2,cy));
   map.setAttribute('viewBox',[cx-w/2,cy-h/2,w,h].join(' '));
   const k=w/Math.max(290,Math.min(690,map.clientWidth||530)), visible=(x,y)=>x>=cx-w/2&&x<=cx+w/2&&y>=cy-h/2&&y<=cy+h/2;
   const detailed=w<=5&&cx-w/2>=-45&&cx+w/2<=-40&&cy-h/2>=21.4&&cy+h/2<=24;
   detail.setAttribute('display',detailed?'inline':'none');
   cities.replaceChildren(); markers.replaceChildren();
   if(w<=7) for(const [name,x,y] of rio){
     if(!visible(x,y))continue;
     addSvg(cities,'circle',{cx:x,cy:y,r:k*2,fill:'#405751'});
     const left=x>cx+w*.30;
     addSvg(cities,'text',{x:x+(left?-1:1)*k*5,y:y-k*6,'text-anchor':left?'end':'start','font-size':k*12,'font-weight':650,fill:'#243f44',stroke:'#f8faf5','stroke-width':k*2.4,'paint-order':'stroke'},name);
   }
   for(const {p,i,name} of pts){
     const x=p.lon,y=-p.lat;if(!visible(x,y))continue;
     const stale=Date.now()-Date.parse(p.observed)>86400000, group=addSvg(markers,'g',{'data-vessel-pin':String(i+1)});
     addSvg(group,'title',{},name);
     addSvg(group,'circle',{cx:x,cy:y,r:k*9,fill:stale?'#975600':'#086862',stroke:'#fff','stroke-width':k*2});
     addSvg(group,'text',{x,y:y+k*3.6,'text-anchor':'middle','font-size':k*11,'font-weight':700,fill:'#fff'},String(i+1));
   }
   zoomIn.disabled=w<=.25;zoomOut.disabled=w>=360;
 };
 const zoom=(factor,f=[.5,.5])=>{const next=Math.max(.25,Math.min(360,w*factor));cx+=(f[0]-.5)*(w-next);cy+=(f[1]-.5)*(w-next)/2;w=next;draw()};
 const pointers=new Map();
 const fractions=(x,y)=>{
   const r=map.getBoundingClientRect(), width=Math.min(r.width,r.height*2),height=width/2;
   return [(x-r.left-(r.width-width)/2)/width,(y-r.top-(r.height-height)/2)/height];
 };
 const gesture=()=>{const [a,b]=[...pointers.values()];return b?[(a.x+b.x)/2,(a.y+b.y)/2,Math.hypot(a.x-b.x,a.y-b.y)]:[a.x,a.y,0]};
 map.addEventListener('pointerdown',e=>{if(e.button!==0||pointers.size===2)return;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});map.setPointerCapture(e.pointerId);map.style.cursor='grabbing'});
 const stop=e=>{pointers.delete(e.pointerId);if(!pointers.size)map.style.cursor='grab'};
 ['pointerup','pointercancel','lostpointercapture'].forEach(e=>map.addEventListener(e,stop));
 map.addEventListener('pointermove',e=>{
   if(!pointers.has(e.pointerId))return;
   const from=gesture();pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});const to=gesture();
   const [ax,ay]=fractions(from[0],from[1]),[bx,by]=fractions(to[0],to[1]);
   cx+=(ax-bx)*w;cy+=(ay-by)*w/2;
   if(from[2]>5&&to[2]>5)zoom(from[2]/to[2],[bx,by]);else draw();
 });
 map.addEventListener('wheel',e=>{if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();zoom(e.deltaY<0?.8:1.25,fractions(e.clientX,e.clientY))},{passive:false});
 map.addEventListener('keydown',e=>{
   const delta=w/8;
   if(e.key==='ArrowLeft')cx-=delta;else if(e.key==='ArrowRight')cx+=delta;else if(e.key==='ArrowUp')cy-=delta/2;else if(e.key==='ArrowDown')cy+=delta/2;
   else if(['=','+','-'].includes(e.key)){e.preventDefault();zoom(e.key==='-'?1/.65:.65);return}else return;
   e.preventDefault();draw();
 });
 draw();
 const resize=new ResizeObserver(()=>{if(map.isConnected)draw();else resize.disconnect()});resize.observe(map);
 return map;
}
