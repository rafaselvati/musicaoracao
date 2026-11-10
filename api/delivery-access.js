const {authorize,catalog}=require('../lib/delivery');
module.exports=async(req,res)=>{
 res.setHeader('Cache-Control','no-store');
 if(req.method!=='POST'){res.setHeader('Allow','POST');return res.status(405).json({error:'Método no permitido.'})}
 try{
  const access=await authorize(req.body?.token);
  return res.status(200).json({plan:access.plan,files:access.files.map(id=>({id,title:catalog[id].title,pages:catalog[id].pages})),support:process.env.SUPPORT_EMAIL||'',upsell:process.env.UPSELL_CHECKOUT_URL&&process.env.UPSELL_READY==='true'?{url:process.env.UPSELL_CHECKOUT_URL}:null});
 }catch{return res.status(403).json({error:'No pudimos validar tu acceso. Abre el enlace del correo de compra. Si ya venció o necesitas ayuda, responde a ese correo.'})}
};
