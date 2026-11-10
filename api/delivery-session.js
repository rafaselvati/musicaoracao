const {authorizeSession,sign}=require('../lib/delivery');
module.exports=async(req,res)=>{
 res.setHeader('Cache-Control','no-store');
 if(req.method!=='POST'){res.setHeader('Allow','POST');return res.status(405).json({error:'Método no permitido.'})}
 const id=req.body?.session_id;
 if(typeof id!=='string'||!/^cs_[A-Za-z0-9_]+$/.test(id)||id.length>255)return res.status(400).json({error:'No encontramos el identificador de tu compra.'});
 try{await authorizeSession(id);return res.status(200).json({token:sign(id)})}
 catch{return res.status(202).json({pending:true,message:'Estamos verificando el pago. Los materiales se liberan únicamente cuando Stripe confirma la aprobación.'})}
};
