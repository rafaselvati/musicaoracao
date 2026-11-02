const Stripe=require('stripe');
const stripe=new Stripe(process.env.STRIPE_SECRET_KEY||'sk_test_missing',{apiVersion:'2026-03-25.dahlia'});
module.exports=async(req,res)=>{
 if(req.method!=='POST')return res.status(405).json({error:'Método não permitido'});
 if(!process.env.STRIPE_SECRET_KEY||!process.env.STRIPE_PRICE_ID)return res.status(503).json({error:'Configure STRIPE_SECRET_KEY e STRIPE_PRICE_ID na Vercel.'});
 const order=req.body?.order||{};
 // O servidor decide os preços; valores enviados pelo navegador são ignorados.
 const offers=req.body?.offers||{};
 const secondSong=offers.secondSong===true;
 const musicVideo=offers.musicVideo===true;
 const bundle=secondSong&&musicVideo;
 const totalCents=bundle?3490:990+(secondSong?790:0)+(musicVideo?1990:0);

 const fields=['recipient','name','genre','voice','qualities','memories','message','email','phone'];
 if(!order.recipient||!order.name||!order.genre||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(order.email||'')||String(order.phone||'').replace(/\D/g,'').length<10)return res.status(400).json({error:'Dados do formulário incompletos.'});
 const metadata={};for(const f of fields)metadata[f]=String(f==='genre'&&order.genre==='Outro estilo'?(order.genreOther||'Outro estilo'):(f==='voice'?(order.voice||'Sem preferência'):order[f]||'')).slice(0,500);
 try{
  const line_items=bundle
   ?[{price_data:{currency:'brl',unit_amount:3490,product_data:{name:'Pacote completo Canção de Fé — música + segunda versão + vídeo'}},quantity:1}]
   :[{price:process.env.STRIPE_PRICE_ID,quantity:1},...(secondSong?[{price_data:{currency:'brl',unit_amount:790,product_data:{name:'Segunda versão da música — outro estilo opcional'}},quantity:1}]:[]),...(musicVideo?[{price_data:{currency:'brl',unit_amount:1990,product_data:{name:'Música + vídeo personalizado — adicional'}},quantity:1}]:[])];
  const session=await stripe.checkout.sessions.create({ui_mode:'form',mode:'payment',line_items,billing_address_collection:'auto',phone_number_collection:{enabled:false},automatic_tax:{enabled:false},submit_type:'auto',integration_identifier:'custom_embedded_web_0001',customer_email:String(order.email).slice(0,254),metadata:{...metadata,secondSong:String(secondSong),musicVideo:String(musicVideo),bundle:String(bundle),expected_total_cents:String(totalCents)},locale:'pt-BR'});
  return res.status(200).json({client_secret:session.client_secret,publishable_key:process.env.STRIPE_PUBLISHABLE_KEY});
 }catch(e){console.error('Stripe session error',e.type,e.code,e.message);return res.status(400).json({error:e.message||'Erro ao iniciar pagamento'});}
};
