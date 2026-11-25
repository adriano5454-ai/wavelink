const {chromium}=require('playwright-core');
const assert=require('node:assert/strict');

async function check(browser, origin, width, baseline) {
 const ctx=await browser.newContext({viewport:{width,height:919},locale:'pt-BR',serviceWorkers:'block'});
 try {
  const p=await ctx.newPage();
  const writes=[];
  p.on('request', req=>{if(req.method()==='POST' && new URL(req.url()).pathname==='/api/me/language')writes.push('profile language')});
  await p.goto(origin+'/__demo/public?area=home');
  const pt=p.locator('#personal-home .ph-footer a[hreflang="pt-BR"]');
  await pt.waitFor();assert.equal(await p.locator('html').getAttribute('lang'),'en');
  const visit=new URL(p.url()).searchParams.get('browser_workspace');assert(visit);
  await pt.click();
  if(baseline){
   await p.waitForURL(u=>u.pathname==='/');
   await pt.waitFor();
   console.log('BASELINE',width,'footer selection returned to English');
   return;
  }
  const en=p.locator('html[lang="pt-BR"] #personal-home .ph-footer a[hreflang=en]');
  await en.waitFor();
  await p.locator('.ph-footer a[href="#workspaces"]').click();await p.locator('html[lang="pt-BR"] #home-find').waitFor();
  await p.reload();await p.locator('html[lang="pt-BR"] #home-find').waitFor();
  await p.goBack();await en.waitFor();assert.equal(new URL(p.url()).searchParams.get('browser_workspace'),visit);
  const fresh=await ctx.newPage();await fresh.goto(origin+'/__demo/public?area=home');await fresh.locator('html[lang=en] #personal-home .ph-footer a[hreflang="pt-BR"]').waitFor();
  assert.notEqual(new URL(fresh.url()).searchParams.get('browser_workspace'),visit);
  await en.click();await p.locator('html[lang=en] #personal-home .ph-footer a[hreflang="pt-BR"]').waitFor();
  await p.reload();await pt.waitFor();assert.equal(await p.locator('html').getAttribute('lang'),'en');
  assert.deepEqual(writes,[]);console.log('PASS',width,'footer PT, Workspaces, reload, Back, independent visit EN, switch back EN, no account language write');
 }finally{await ctx.close()}
}
async function loopbackCertificatePin(url) {
 // Pin only this disposable local fixture's public key. Per-context TLS
 // overrides can exhaust Chromium's retries on parallel HTTP/1.0 connections.
 assert.equal(url.protocol, 'https:');
 assert.equal(url.hostname, '127.0.0.1');
 const tls = require('node:tls');
 const {createHash} = require('node:crypto');
 const socket = tls.connect({host:url.hostname, port:Number(url.port || 443), rejectUnauthorized:false});
 try {
  await require('node:events').once(socket, 'secureConnect');
  const key = socket.getPeerX509Certificate().publicKey.export({type:'spki', format:'der'});
  return createHash('sha256').update(key).digest('base64');
 } finally {socket.destroy();}
}

(async()=>{const url=new URL(process.argv[2]);assert.equal(url.hostname,'127.0.0.1');const browser=await chromium.launch({args:['--ignore-certificate-errors-spki-list='+await loopbackCertificatePin(url)],executablePath:process.env.WAVELINK_TEST_CHROMIUM});try{for(const w of [1360,389])await check(browser,url.origin,w,process.argv.includes('baseline'))}finally{await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
