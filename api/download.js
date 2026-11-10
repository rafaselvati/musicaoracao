const fs=require('fs/promises');const path=require('path');
const {authorize,catalog}=require('../lib/delivery');
module.exports=async(req,res)=>{
 res.setHeader('Cache-Control','private, no-store');res.setHeader('X-Content-Type-Options','nosniff');
 if(req.method!=='POST'){res.setHeader('Allow','POST');return res.status(405).json({error:'Método no permitido.'})}
 try{
  const access=await authorize(req.body?.token),id=req.body?.file;
  if(typeof id!=='string'||!access.files.includes(id)||!Object.hasOwn(catalog,id))return res.status(403).json({error:'Este material no está incluido en tu edición.'});
  const file=catalog[id].file;
  const bytes=await fs.readFile(path.join(process.cwd(),'private_files',file));
  res.setHeader('Content-Type','application/pdf');res.setHeader('Content-Disposition','attachment; filename="'+file+'"');
  return res.status(200).send(bytes);
 }catch{return res.status(403).json({error:'No pudimos validar la descarga. Vuelve al enlace de tu correo o solicita ayuda respondiendo al correo del pedido.'})}
};
