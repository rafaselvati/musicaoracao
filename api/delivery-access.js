const {authorize,catalog}=require('../lib/delivery');
module.exports=async(req,res)=>{
 res.setHeader('Cache-Control','no-store');
 if(req.method!=='POST'){res.setHeader('Allow','POST');return res.status(405).json({error:'Método no permitido.'})}
 try{const access=await authorize(req.body?.token);return res.status(200).json({plan:access.plan,basePlan:access.basePlan,files:access.files.map(id=>({id,title:catalog[id].title,pages:catalog[id].pages,minutes:catalog[id].minutes,type:catalog[id].type})),support:process.env.SUPPORT_EMAIL||process.env.PEDIDOS_EMAIL||'',upsell:access.plan!=='audios'?{plan:'audios',amount:2990}:null})}
 catch{return res.status(403).json({error:'No pudimos validar tu acceso. Vuelve al enlace de tu compra o solicita ayuda respondiendo al correo del pedido.'})}
};
