const Stripe=require('stripe');
const stripe=new Stripe(process.env.STRIPE_SECRET_KEY||'sk_test_missing',{apiVersion:'2026-03-25.dahlia'});
module.exports=async(req,res)=>{
 if(req.method!=='POST')return res.status(405).end();
 if(!process.env.STRIPE_WEBHOOK_SECRET)return res.status(503).end();
 let event;
 try{let raw;if(Buffer.isBuffer(req.body))raw=req.body;else if(typeof req.body==='string')raw=Buffer.from(req.body);else{const chunks=[];for await(const chunk of req)chunks.push(chunk);raw=Buffer.concat(chunks)}event=stripe.webhooks.constructEvent(raw,req.headers['stripe-signature'],process.env.STRIPE_WEBHOOK_SECRET)}catch(e){return res.status(400).send('Assinatura inválida')}
 if(event.type==='checkout.session.completed'||event.type==='checkout.session.async_payment_succeeded'){
  const session=event.data.object;
  if(session.payment_status==='paid'){
   if(!process.env.RESEND_API_KEY||!process.env.PEDIDOS_EMAIL||!process.env.RESEND_FROM_EMAIL){console.error('E-mail não configurado para o pedido',session.id);return res.status(503).send('Envio não configurado')}
   // Meta Conversions API: server-side Purchase, only after confirmed payment.
   // Never send raw order text, names, or phone numbers to Meta.
   if(process.env.META_CAPI_ACCESS_TOKEN){
    try{
     const crypto=require('crypto');
     const email=String(session.customer_details?.email||session.customer_email||session.metadata?.email||'').trim().toLowerCase();
     const user_data={};
     if(email)user_data.em=[crypto.createHash('sha256').update(email).digest('hex')];
     const payload={data:[{event_name:'Purchase',event_time:Math.floor(Date.now()/1000),event_id:'cdf_purchase_'+session.id,action_source:'website',event_source_url:'https://musicaoracao.vercel.app/checkout.html',user_data,custom_data:{currency:(session.currency||'brl').toUpperCase(),value:(session.amount_total||0)/100,order_id:session.id}}]};
     const url='https://graph.facebook.com/v22.0/1497991535722252/events';
     const metaResponse=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+process.env.META_CAPI_ACCESS_TOKEN},body:JSON.stringify(payload)});
     if(!metaResponse.ok)console.error('Meta CAPI rejeitou Purchase',metaResponse.status,(await metaResponse.text()).slice(0,300));
    }catch(err){console.error('Erro Meta CAPI',err.message)}
   }
   const fields=['recipient','name','genre','voice','qualities','memories','message','email','phone'];
   const labels=['Destinatário','Nome','Estilo','Voz','Qualidades','Memórias','Mensagem','E-mail','Telefone'];
   const body=['PEDIDO PAGO — CANÇÃO DE FÉ','Stripe Session: '+session.id,'Pagamento: '+session.payment_status,'Total pago: R$ '+((session.amount_total||0)/100).toFixed(2).replace('.',','),'Segunda versão da música: '+(session.metadata?.secondSong==='true'?'SIM':'NÃO'),'Música + vídeo: '+(session.metadata?.musicVideo==='true'?'SIM':'NÃO'),'Pacote completo: '+(session.metadata?.bundle==='true'?'SIM':'NÃO'),'',...fields.map((f,i)=>labels[i]+': '+(session.metadata?.[f]||'-'))].join('\n');
   if(session.metadata?.musicVideo==='true'){
    if(!process.env.PHOTO_LINK_SECRET){console.error('PHOTO_LINK_SECRET não configurado');return res.status(503).send('Link de fotos não configurado')}
    const {sign}=require('./photo-link');
    const expires=String(Date.now()+7*24*60*60*1000);
    const base=(process.env.PUBLIC_SITE_URL||'https://musicaoracao.vercel.app').replace(/\/$/,'');
    const url=base+'/enviar-fotos.html?'+new URLSearchParams({sessionId:session.id,expires,signature:sign(session.id,expires)});
    const customerEmail=session.customer_details?.email||session.customer_email||session.metadata?.email;
    if(!customerEmail){console.error('Sem e-mail para envio do link',session.id);return res.status(500).send('E-mail do comprador ausente')}
    const customerResponse=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:'Bearer '+process.env.RESEND_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({from:process.env.RESEND_FROM_EMAIL,to:[customerEmail],subject:'Canção de Fé — envie as fotos do seu vídeo',text:'Seu pagamento foi confirmado! Para criar seu vídeo personalizado, envie de 1 a 6 fotos pelo link abaixo (válido por 7 dias):\n\n'+url+'\n\nPedido: '+session.id})});
    if(!customerResponse.ok){console.error('Falha e-mail cliente',customerResponse.status);return res.status(500).send('Falha no envio do link de fotos')}
   }
   try{const response=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:'Bearer '+process.env.RESEND_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({from:process.env.RESEND_FROM_EMAIL,to:[process.env.PEDIDOS_EMAIL],subject:'Canção de Fé — Pedido pago '+session.id,text:body})});if(!response.ok)throw Error('Resend HTTP '+response.status)}catch(e){console.error('Falha ao notificar pedido',session.id,e.message);return res.status(500).send('Falha no envio')}
  }
 }
 return res.status(200).json({received:true});
};
