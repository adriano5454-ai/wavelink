const chartImageCache=new WeakMap();
function chartAvatar(name,profile){
 const badge=document.createElement('span');
 badge.className='org-avatar';badge.setAttribute('aria-hidden','true');
 const words=(name||'').trim().split(/\s+/).filter(Boolean);
 badge.textContent=[words[0],words.length>1?words.at(-1):''].map(w=>Array.from(w||'')[0]||'').join('').toLocaleUpperCase()||'?';
 if(!profile?.has_avatar||!profile.profile_id||window.WavelinkNativeDemo?.active())return badge;
 const session=H.session(),uid=profile.profile_id;
 let cache=chartImageCache.get(directory);
 if(!cache){cache=new Map();chartImageCache.set(directory,cache)}
 // Delay until the synchronous tree builder has attached the cards.
 queueMicrotask(async()=>{
   if(!badge.isConnected||session!==H.session())return;
   try{
     if(!cache.has(uid))cache.set(uid,H.api('/api/recognition/avatar/'+encodeURIComponent(uid),{blob:true}));
     const blob=await cache.get(uid);
     if(!blob||session!==H.session()||!badge.isConnected)return;
     const image=new Image(),url=URL.createObjectURL(blob);
     try{
       image.alt='';image.src=url;await image.decode();
       if(session===H.session()&&badge.isConnected)badge.replaceChildren(image);
     }finally{URL.revokeObjectURL(url)}
   }catch{/* Keep initials for inaccessible, missing or invalid images. */}
 });
 return badge;
}
