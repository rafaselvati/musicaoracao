// Sandbox: não confirma pedidos nem envia mensagens. Configure verificação de autenticidade
// das notificações conforme sua conta antes de ativar pagamentos em produção.
export default function handler(req,res){res.setHeader('Cache-Control','no-store');return res.status(200).json({received:true,sandbox:true});}
