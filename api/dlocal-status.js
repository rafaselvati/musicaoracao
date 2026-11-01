// Vercel Function: testa autenticação Sandbox sem expor chaves ao navegador.
export default async function handler(req,res){
  if(req.method!=='GET') return res.status(405).json({message:'Método não permitido'});
  const key=process.env.DLOCAL_API_KEY, secret=process.env.DLOCAL_SECRET_KEY;
  if(!key||!secret) return res.status(503).json({message:'Configure DLOCAL_API_KEY e DLOCAL_SECRET_KEY nas variáveis de ambiente da Vercel (Sandbox).'});
  try{
    const response=await fetch('https://api-sbx.dlocalgo.com/v1/me',{method:'GET',headers:{authorization:`Bearer ${key}:${secret}`,accept:'application/json'},signal:AbortSignal.timeout(12000)});
    if(!response.ok) return res.status(502).json({message:`A dLocal Go respondeu HTTP ${response.status}. Confira as credenciais de TESTE e as permissões.`});
    return res.status(200).json({message:'Conexão com dLocal Go Sandbox validada. Nenhuma cobrança foi realizada.'});
  }catch(err){return res.status(502).json({message:'Não foi possível acessar a API Sandbox. Verifique a conexão e tente novamente.'})}
}
