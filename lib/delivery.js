const crypto=require('crypto');const Stripe=require('stripe');
const catalog=Object.freeze({
 libro:{file:'Desbloquea_Tu_Septimo_Sentido.pdf',title:'Desbloquea Tu Séptimo Sentido',pages:35,type:'pdf'},
 diario:{file:'Diario_del_Despertar.pdf',title:'Diario del Despertar',pages:27,type:'pdf'},
 oraciones:{file:'Bajo_Sus_Alas.pdf',title:'Bajo Sus Alas',pages:17,type:'pdf'},
 salmos:{file:'7_Noches_con_los_Salmos.pdf',title:'7 Noches con los Salmos',pages:17,type:'pdf'},
 tarjetas:{file:'Palabras_de_Luz.pdf',title:'Palabras de Luz',pages:9,type:'pdf'},
 audio1:{file:'audio/01_Pausa_396Hz.mp3',title:'Pausa · 396 Hz',minutes:5,type:'audio'},
 audio2:{file:'audio/02_Presencia_417Hz.mp3',title:'Presencia · 417 Hz',minutes:5,type:'audio'},
 audio3:{file:'audio/03_Espacio_432Hz.mp3',title:'Espacio · 432 Hz',minutes:5,type:'audio'},
 audio4:{file:'audio/04_Quietud_528Hz.mp3',title:'Quietud · 528 Hz',minutes:5,type:'audio'},
 audio5:{file:'audio/05_Encuentro_639Hz.mp3',title:'Encuentro · 639 Hz',minutes:5,type:'audio'},
 audio6:{file:'audio/06_Horizonte_741Hz.mp3',title:'Horizonte · 741 Hz',minutes:5,type:'audio'},
 audio7:{file:'audio/07_Continuidad_852Hz.mp3',title:'Continuidad · 852 Hz',minutes:5,type:'audio'}
});
const planFiles={esencial:['libro','diario'],completa:['libro','diario','oraciones','salmos','tarjetas'],audios:['audio1','audio2','audio3','audio4','audio5','audio6','audio7']};
const amounts={esencial:990,completa:1990,audios:2990};
function secret(){
 if(process.env.DELIVERY_SECRET){if(process.env.DELIVERY_SECRET.length<32)throw Error('Delivery secret too short');return process.env.DELIVERY_SECRET}
 // Separate signing key derived from the existing server key; no new variable is required.
 if(!process.env.STRIPE_SECRET_KEY)throw Error('Stripe not configured');
 return crypto.createHmac('sha256',process.env.STRIPE_SECRET_KEY).update('septimo-sentido:delivery-signing:v1').digest();
}
function sign(sessionId,now=Date.now()){
 if(typeof sessionId!=='string'||!/^cs_[A-Za-z0-9_]+$/.test(sessionId))throw Error('Invalid session');
 const payload=Buffer.from(JSON.stringify({sid:sessionId,exp:Math.floor(now/1000)+90*86400})).toString('base64url');
 return payload+'.'+crypto.createHmac('sha256',secret()).update(payload).digest('base64url');
}
function verify(token,now=Date.now()){
 if(typeof token!=='string'||token.length>1500)throw Error('Invalid token');
 const parts=token.split('.');if(parts.length!==2)throw Error('Invalid token');
 const expected=crypto.createHmac('sha256',secret()).update(parts[0]).digest(),supplied=Buffer.from(parts[1],'base64url');
 if(supplied.length!==expected.length||!crypto.timingSafeEqual(expected,supplied))throw Error('Invalid token');
 const data=JSON.parse(Buffer.from(parts[0],'base64url').toString('utf8'));
 if(!Number.isSafeInteger(data.exp)||data.exp<=Math.floor(now/1000)||typeof data.sid!=='string'||!/^cs_[A-Za-z0-9_]+$/.test(data.sid))throw Error('Expired or invalid token');return data;
}
function validate(session){
 const plan=session.metadata?.plan,charge=session.payment_intent?.latest_charge;
 if(session.metadata?.product!=='septimo_sentido'||session.payment_status!=='paid'||session.mode!=='payment'||session.currency!=='usd'||!Object.hasOwn(planFiles,plan)||session.amount_total!==amounts[plan]||!charge||typeof charge==='string'||charge.refunded||charge.disputed||charge.amount_refunded>0)throw Error('Access unavailable');
 return plan;
}
async function authorizeSession(sessionId){
 if(typeof sessionId!=='string'||!/^cs_[A-Za-z0-9_]+$/.test(sessionId)||sessionId.length>255)throw Error('Invalid session');
 const stripe=new Stripe(process.env.STRIPE_SECRET_KEY,{apiVersion:'2026-03-25.dahlia'});
 const retrieve=id=>stripe.checkout.sessions.retrieve(id,{expand:['payment_intent.latest_charge']});
 const session=await retrieve(sessionId),plan=validate(session);let files=[...planFiles[plan]],basePlan=plan;
 // Only a server-created parent association can unlock the original purchase after the upsell.
 if(plan==='audios'&&/^cs_[A-Za-z0-9_]+$/.test(session.metadata?.parent_session||'')){
  try{const parent=await retrieve(session.metadata.parent_session),parentPlan=validate(parent);if(parentPlan!=='audios'){files=[...planFiles[parentPlan],...files];basePlan=parentPlan}}catch{/* A refunded original purchase does not cancel a separately paid audio purchase. */}
 }
 return {plan,basePlan,files,session};
}
async function authorize(token){return authorizeSession(verify(token).sid)}
function baseURL(){const raw=process.env.PUBLIC_SITE_URL||(process.env.VERCEL_PROJECT_PRODUCTION_URL?'https://'+process.env.VERCEL_PROJECT_PRODUCTION_URL:'');const url=new URL(raw);if(url.protocol!=='https:'||url.username||url.password||url.search||url.hash)throw Error('Invalid site URL');return url.origin}
function deliveryURL(sessionId,createdAt){return baseURL()+'/entrega.html?token='+encodeURIComponent(sign(sessionId,Number.isSafeInteger(createdAt)?createdAt*1000:Date.now()))}
module.exports={catalog,planFiles,amounts,sign,verify,authorize,authorizeSession,deliveryURL,baseURL};
