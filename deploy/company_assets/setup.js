'use strict';
(() => {
  const $ = id => document.getElementById(id);
  let key = new URLSearchParams(location.hash.slice(1)).get('setup') || '';
  history.replaceState(null, '', location.pathname); // admission secret never in the request URL/referrer
  let pending = null, busy = false, disposed = false;
  const fields = ['login', 'temporary', 'fresh', 'confirm'];
  const tell = text => { if (!disposed) $('status').textContent = text; };
  const lock = value => { busy = value; fields.forEach(x => $(x).readOnly = value || !!pending); $('save').disabled=value; $('check').disabled=value; };
  function complete() {
    pending=null;key='';fields.forEach(x=>$(x).value='');$('setup').hidden=true;$('check').hidden=true;$('normal').hidden=false;
    tell('First sign-in is complete. Use your new passphrase at the normal Wavelink login.');
  }
  async function post(path, body) {
    const ctrl = new AbortController(), timer=setTimeout(()=>ctrl.abort(),20000);
    try {
      const response=await fetch(path,{method:'POST',cache:'no-store',credentials:'omit',redirect:'error',headers:{'Content-Type':'application/json',Authorization:'Bearer '+key},body:JSON.stringify(body),signal:ctrl.signal});
      const result=await response.json();
      if(!response.ok) { const err=new Error(result.error||'First sign-in was refused.');err.status=response.status;throw err; }
      return result;
    } finally {clearTimeout(timer);}
  }
  $('setup').addEventListener('submit',async event=>{
    event.preventDefault(); if(busy||disposed)return;
    if(!key){tell('Open the private first sign-in link supplied to the operator.');return;}
    if(!pending){
      if($('fresh').value!==$('confirm').value){tell('The new passphrases do not match.');return;}
      pending={request_id:crypto.randomUUID(),login_id:$('login').value,temporary_password:$('temporary').value,new_password:$('fresh').value,confirm_password:$('confirm').value};
    }
    lock(true);tell('Saving the new administrator passphrase…');
    try{const result=await post('/company-setup/activate',pending);if(result.completed)complete();else throw new Error('Outcome not confirmed.');}
    catch(error){
      if(disposed)return;
      // Validation refuses before writing. Server/transport failures may follow a
      // committed change, so retain the EXACT request and offer outcome checking.
      if([403,410,413,415,422,429].includes(error.status)){pending=null;$('check').hidden=true;$('save').textContent='Set passphrase & finish setup';tell(error.message);}
      else{$('save').textContent='Retry unchanged setup';$('check').hidden=false;tell('The outcome is not confirmed. Retry the same request or check its saved outcome. Do not reset the project.');}
    }finally{lock(false);}
  });
  $('check').addEventListener('click',async()=>{
    if(busy||!pending||disposed)return;lock(true);
    try{const result=await post('/company-setup/outcome',{request_id:pending.request_id});if(result.completed)complete();else tell('No completed setup was found for this request. Retry the unchanged setup.');}
    catch(error){tell(error.message||'Outcome unavailable. Keep this page open and retry.');}finally{lock(false);}
  });
  fetch('/company-setup/status',{cache:'no-store',credentials:'omit',redirect:'error'}).then(async r=>{
    if(!r.ok)throw new Error('Setup status unavailable.');return r.json();
  }).then(data=>{
    if(disposed)return;$('company').textContent=data.company+' · first sign-in';document.title=data.company+' | Wavelink';
    if(data.active)complete();else{$('login').value=data.login_id||'admin';if(!key){$('setup').hidden=true;tell('Use the private first sign-in link supplied to the installation operator.');}}
  }).catch(()=>tell('Setup status unavailable. Retry when connected; do not reset the company project.'));
  addEventListener('beforeunload',event=>{if(pending){event.preventDefault();event.returnValue='';}});
  addEventListener('pagehide',()=>{disposed=true;key='';pending=null;fields.forEach(x=>$(x).value='');});
})();
