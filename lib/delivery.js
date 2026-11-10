const crypto = require('crypto');
const Stripe = require('stripe');
const catalog = Object.freeze({
 libro: {file:'Desbloquea_Tu_Septimo_Sentido.pdf',title:'Desbloquea Tu Séptimo Sentido',pages:35},
 diario: {file:'Diario_del_Despertar.pdf',title:'Diario del Despertar',pages:27},
 oraciones: {file:'Bajo_Sus_Alas.pdf',title:'Bajo Sus Alas',pages:17},
 salmos: {file:'7_Noches_con_los_Salmos.pdf',title:'7 Noches con los Salmos',pages:17},
 tarjetas: {file:'Palabras_de_Luz.pdf',title:'Palabras de Luz',pages:9}
});
const planFiles={esencial:['libro','diario'],completa:['libro','diario','oraciones','salmos','tarjetas']};
function secret(){if(!process.env.DELIVERY_SECRET||process.env.DELIVERY_SECRET.length<32)throw Error('Delivery not configured');return process.env.DELIVERY_SECRET}
function sign(sessionId, now=Date.now()){
 if(typeof sessionId!=='string'||!/^cs_[A-Za-z0-9_]+$/.test(sessionId))throw Error('Invalid session');
 const payload=Buffer.from(JSON.stringify({sid:sessionId,exp:Math.floor(now/1000)+90*86400})).toString('base64url');
 const signature=crypto.createHmac('sha256',secret()).update(payload).digest('base64url');
 return payload+'.'+signature;
}
function verify(token,now=Date.now()){
 if(typeof token!=='string'||token.length>1500)throw Error('Invalid token');
 const parts=token.split('.');if(parts.length!==2)throw Error('Invalid token');
 const expected=crypto.createHmac('sha256',secret()).update(parts[0]).digest();
 const supplied=Buffer.from(parts[1],'base64url');
 if(supplied.length!==expected.length||!crypto.timingSafeEqual(expected,supplied))throw Error('Invalid token');
 const data=JSON.parse(Buffer.from(parts[0],'base64url').toString('utf8'));
 if(!Number.isSafeInteger(data.exp)||data.exp<=Math.floor(now/1000)||typeof data.sid!=='string'||!/^cs_[A-Za-z0-9_]+$/.test(data.sid))throw Error('Expired or invalid token');
 return data;
}
async function authorize(token){
 const data=verify(token);
 const stripe=new Stripe(process.env.STRIPE_SECRET_KEY,{apiVersion:'2026-03-25.dahlia'});
 const session=await stripe.checkout.sessions.retrieve(data.sid,{expand:['payment_intent.latest_charge']});
 const plan=session.metadata?.plan;
 const charge=session.payment_intent?.latest_charge;
 if(session.metadata?.product!=='septimo_sentido'||session.payment_status!=='paid'||session.mode!=='payment'||session.currency!=='usd'||!Object.hasOwn(planFiles,plan)||session.amount_total!==(plan==='esencial'?990:1990)||!charge||typeof charge==='string'||charge.refunded||charge.disputed||charge.amount_refunded>0)throw Error('Access unavailable');
 return {plan,files:planFiles[plan],session};
}
function baseURL(){const url=new URL(process.env.PUBLIC_SITE_URL||'');if(url.protocol!=='https:'||url.username||url.password||url.search||url.hash)throw Error('Invalid site URL');return url.origin}
function deliveryURL(sessionId,createdAt){return baseURL()+'/entrega.html?token='+encodeURIComponent(sign(sessionId,Number.isSafeInteger(createdAt)?createdAt*1000:Date.now()))}
module.exports={catalog,planFiles,sign,verify,authorize,deliveryURL,baseURL};
