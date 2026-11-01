export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');if(req.method!=='POST')return res.status(405).json({message:'Método não permitido'});
 const b=req.body||{};if(typeof b.name!=='string'||!b.name.trim()||typeof b.email!=='string'||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(b.email)||typeof b.phone!=='string'||b.phone.replace(/\D/g,'').length<10)return res.status(400).json({message:'Dados do pedido inválidos'});
 const key=process.env.DLOCAL_API_KEY||process.env.DLOCALGO_API_KEY,secret=process.env.DLOCAL_SECRET_KEY||process.env.DLOCALGO_API_SECRET,smart=process.env.DLOCAL_SMARTFIELDS_KEY;
 if(!key||!secret||!smart)return res.status(503).json({message:'Configure as chaves Sandbox, incluindo DLOCAL_SMARTFIELDS_KEY, na Vercel.'});
 const amount=(4700+(b.bumpExpress===true?1990:0)+(b.bumpPdf===true?990:0))/100;
 const host=process.env.VERCEL_URL?`https://${process.env.VERCEL_URL}`:null;const origin=process.env.PUBLIC_SITE_URL||host;
 if(!origin||!/^https:\/\//.test(origin))return res.status(503).json({message:'Configure PUBLIC_SITE_URL com a URL HTTPS publicada na Vercel.'});
 const payload={amount,currency:'BRL',country:'BR',description:'Canção de Fé - música personalizada (Sandbox)',notification_url:`${origin}/api/dlocal-webhook`,success_url:`${origin}/?payment_return=1`,allow_transparent:true};
 try{const r=await fetch('https://api-sbx.dlocalgo.com/v1/payments',{method:'POST',headers:{'Content-Type':'application/json',Authorization:`Bearer ${key}:${secret}`},body:JSON.stringify(payload),signal:AbortSignal.timeout(18000)});const data=await r.json().catch(()=>({}));if(!r.ok){
   // Exibe somente campos de diagnóstico conhecidos; nunca retorna payload, headers ou credenciais.
   const safeString=(v)=>typeof v==='string'?v.slice(0,240).replace(/Bearer\s+[^\s]+/gi,'[credencial omitida]').replace(/(?:sk|pk)_(?:live|test)_[A-Za-z0-9_-]+/gi,'[credencial omitida]').replace(/https?:\/\/[^\s]+/gi,'[URL omitida]'):undefined;
   const errorCode=safeString(data?.code)||safeString(data?.error_code)||safeString(data?.error);
   const errorMessage=safeString(data?.message)||safeString(data?.description)||safeString(data?.error_description);
   console.error('dLocal Go Sandbox create-payment rejected', {httpStatus:r.status,errorCode,errorMessage});
   return res.status(502).json({message:`dLocal Go recusou a criação do pagamento (HTTP ${r.status}).`,upstreamStatus:r.status,errorCode,errorMessage});
  }if(!data.merchant_checkout_token)return res.status(502).json({message:'A API não retornou merchant_checkout_token. Confira a permissão do Checkout Transparente.'});return res.status(200).json({merchant_checkout_token:data.merchant_checkout_token,smartfieldsKey:smart,amount,currency:'BRL'})}catch(e){return res.status(502).json({message:'Falha de comunicação com a API Sandbox.'})}
}
