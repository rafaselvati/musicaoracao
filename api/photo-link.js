const crypto=require('crypto');
function sign(id,expires){const secret=process.env.PHOTO_LINK_SECRET;if(!secret)throw Error('PHOTO_LINK_SECRET não configurado');return crypto.createHmac('sha256',secret).update(id+'.'+expires).digest('hex')}
function verify(id,expires,signature){if(!/^cs_[a-zA-Z0-9_]+$/.test(id||'')||!/^\d{10,13}$/.test(String(expires||''))||Number(expires)<Date.now()||!(/^[a-f0-9]{64}$/i.test(signature||'')))return false;const a=Buffer.from(sign(id,expires),'hex'),b=Buffer.from(signature,'hex');return crypto.timingSafeEqual(a,b)}
module.exports={sign,verify};
