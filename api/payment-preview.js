// Sandbox-only: valida o pedido e calcula o valor no servidor.
// Não cria cobrança; requer endpoint dLocal Go confirmado para habilitar Pix real.
export default async function handler(req,res){
  res.setHeader('Cache-Control','no-store');
  if(req.method!=='POST')return res.status(405).json({message:'Método não permitido'});
  const b=req.body||{};
  if(typeof b.email!=='string'||!/^\S+@\S+\.\S+$/.test(b.email)||typeof b.name!=='string'||!b.name.trim()||typeof b.phone!=='string'||b.phone.replace(/\D/g,'').length<10)return res.status(400).json({message:'Informe nome, e-mail e telefone válidos.'});
  if(!['pix','card'].includes(b.method))return res.status(400).json({message:'Forma de pagamento inválida.'});
  const cents=4700+(b.bumpExpress===true?1990:0)+(b.bumpPdf===true?990:0);
  return res.status(200).json({sandbox:true,readyForPayment:false,amount:(cents/100).toFixed(2),currency:'BRL',method:b.method,message:'Pedido validado. A geração de cobrança está bloqueada até confirmar o endpoint de pagamento específico da dLocal Go. Nenhuma cobrança foi realizada.'});
}
