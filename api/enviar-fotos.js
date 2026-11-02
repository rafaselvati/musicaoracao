const Stripe=require('stripe');
const {verify}=require('./photo-link');
const stripe=new Stripe(process.env.STRIPE_SECRET_KEY||'sk_test_missing');
module.exports=async(req,res)=>{
 if(req.method!=='POST')return res.status(405).json({error:'Método não permitido'});
 try{
  const {sessionId,expires,signature,photos}=req.body||{};
  if(!process.env.PHOTO_LINK_SECRET||!verify(sessionId,expires,signature))return res.status(403).json({error:'Link inválido ou expirado.'});
  const session=await stripe.checkout.sessions.retrieve(sessionId);
  if(session.payment_status!=='paid'||session.metadata?.musicVideo!=='true')return res.status(403).json({error:'Este pedido não tem vídeo pago.'});
  if(!Array.isArray(photos)||photos.length<1||photos.length>6)return res.status(400).json({error:'Selecione entre 1 e 6 fotos.'});
  const attachments=[];
  for(let i=0;i<photos.length;i++){
   const p=photos[i];if(!p||!['image/jpeg','image/png','image/webp'].includes(p.type)||typeof p.data!=='string'||p.data.length>3_000_000||!/^[A-Za-z0-9+/]+={0,2}$/.test(p.data))return res.status(400).json({error:'Fotos devem ser JPG, PNG ou WEBP de até 2 MB cada.'});
   const buffer=Buffer.from(p.data,'base64');if(buffer.length>2_000_000)return res.status(400).json({error:'Cada foto deve ter até 2 MB.'});
   const valid=p.type==='image/jpeg'&&buffer[0]===0xff&&buffer[1]===0xd8||p.type==='image/png'&&buffer.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))||p.type==='image/webp'&&buffer.toString('ascii',0,4)==='RIFF'&&buffer.toString('ascii',8,12)==='WEBP';
   if(!valid)return res.status(400).json({error:'Uma das imagens não é válida.'});
   attachments.push({filename:`foto-${i+1}.${p.type==='image/jpeg'?'jpg':p.type==='image/png'?'png':'webp'}`,content:p.data});
  }
  if(!process.env.RESEND_API_KEY||!process.env.PEDIDOS_EMAIL||!process.env.RESEND_FROM_EMAIL)return res.status(503).json({error:'Envio de fotos ainda não configurado.'});
  const response=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:'Bearer '+process.env.RESEND_API_KEY,'Content-Type':'application/json'},body:JSON.stringify({from:process.env.RESEND_FROM_EMAIL,to:[process.env.PEDIDOS_EMAIL],subject:`Fotos do vídeo — Canção de Fé — ${sessionId}`,text:`Fotos enviadas pelo cliente após pagamento confirmado.\nPedido Stripe: ${sessionId}\nE-mail: ${session.customer_email||session.customer_details?.email||'-'}\nQuantidade: ${attachments.length}`,attachments})});
  if(!response.ok){console.error('Resend fotos',response.status,(await response.text()).slice(0,200));return res.status(502).json({error:'Não foi possível enviar as fotos. Tente novamente.'})}
  return res.status(200).json({ok:true});
 }catch(e){console.error('Upload fotos',e.message);return res.status(500).json({error:'Falha ao enviar as fotos. Tente novamente.'})}
};
