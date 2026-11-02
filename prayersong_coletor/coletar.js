const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const ORIGIN = 'https://prayersong.com';
const OUT = path.join(__dirname, 'captura');
const pages = ['/', '/create'];
const delay = ms => new Promise(r => setTimeout(r, ms));
const safe = s => s.replace(/[^a-z0-9_-]/gi, '_').slice(0, 120);
const save = (p, data) => { fs.mkdirSync(path.dirname(p), {recursive:true}); fs.writeFileSync(p, data); };
const download = (url, dest, redirects=0) => new Promise((resolve) => {
  if (redirects>4) return resolve(false);
  const client = url.startsWith('https:') ? https : http;
  const req=client.get(url, {headers:{'User-Agent':'Mozilla/5.0 (compatible; PublicPageArchive/1.0)'}}, res => {
    if ([301,302,303,307,308].includes(res.statusCode) && res.headers.location) return resolve(download(new URL(res.headers.location,url).href,dest,redirects+1));
    if(res.statusCode!==200) {res.resume(); return resolve(false)}
    const parts=[]; let size=0;
    res.on('data', c=> {size+=c.length; if(size>15*1024*1024) req.destroy(); else parts.push(c)});
    res.on('end', ()=> {if(size<=15*1024*1024){save(dest,Buffer.concat(parts)); resolve(true)}else resolve(false)});
  });
  req.on('error',()=>resolve(false)); req.setTimeout(15000,()=>req.destroy());
});
(async()=>{
  fs.mkdirSync(OUT,{recursive:true});
  const browser=await chromium.launch({headless:false});
  const context=await browser.newContext({viewport:{width:1440,height:900},locale:'en-US'});
  const assets=new Set();
  for(const route of pages){
    const page=await context.newPage();
    page.on('response', response=>{
      const u=response.url(); const type=response.request().resourceType();
      if(['stylesheet','script','image','font'].includes(type) && /^https?:/.test(u)) assets.add(u);
    });
    console.log('Abrindo', ORIGIN+route);
    try {await page.goto(ORIGIN+route,{waitUntil:'domcontentloaded',timeout:45000}); await delay(4500)}
    catch(e){console.warn('Aviso:',e.message)}
    const id=route==='/'?'inicio':'criar';
    save(path.join(OUT,id+'.html'),await page.content());
    await page.screenshot({path:path.join(OUT,id+'.png'),fullPage:true}).catch(()=>{});
    const text=await page.locator('body').innerText().catch(()=> '');
    save(path.join(OUT,id+'.txt'),text);
    const domAssets=await page.evaluate(()=>[...document.querySelectorAll('img[src],script[src],link[href]')].map(e=>e.src||e.href).filter(Boolean)).catch(()=>[]);
    domAssets.forEach(u=>assets.add(u));
    await page.close();
  }
  console.log('Recursos encontrados:',assets.size);
  const manifest=[]; let count=0;
  for(const u of assets){
    if(!/^https?:/.test(u) || count>=200) continue;
    let parsed;try{parsed=new URL(u)}catch{continue}
    const ext=path.extname(parsed.pathname).slice(0,10)||'.bin';
    const dest=path.join(OUT,'recursos',safe(parsed.hostname),safe(parsed.pathname)+ext);
    const ok=await download(u,dest);
    manifest.push({url:u,arquivo:ok?path.relative(OUT,dest):null}); count++;
    if(count%20===0)console.log('Recursos processados:',count);
    await delay(150);
  }
  save(path.join(OUT,'manifesto.json'),JSON.stringify(manifest,null,2));
  await browser.close();
  console.log('Concluído. Pasta:',OUT);
  console.log('Observação: captura para estudo, não é cópia funcional do checkout ou backend.');
})().catch(e=>{console.error(e);process.exit(1)});
