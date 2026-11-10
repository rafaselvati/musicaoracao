const Stripe = require('stripe');
const AMOUNTS = {esencial: 990, completa: 1990};
async function sendEmail(payload, idempotencyKey) {
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST', headers: {Authorization: 'Bearer ' + process.env.RESEND_API_KEY, 'Content-Type': 'application/json', 'Idempotency-Key': idempotencyKey},
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error('Email HTTP ' + response.status);
}
module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).end();
  if (!process.env.STRIPE_SECRET_KEY || !process.env.STRIPE_WEBHOOK_SECRET) return res.status(503).end();
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {apiVersion: '2026-03-25.dahlia'});
  let event;
  try {
    let raw;
    if (Buffer.isBuffer(req.body)) raw = req.body;
    else if (typeof req.body === 'string') raw = Buffer.from(req.body);
    else { const chunks = []; for await (const chunk of req) chunks.push(chunk); raw = Buffer.concat(chunks); }
    event = stripe.webhooks.constructEvent(raw, req.headers['stripe-signature'], process.env.STRIPE_WEBHOOK_SECRET);
  } catch { return res.status(400).send('Firma no válida'); }
  if (!['checkout.session.completed', 'checkout.session.async_payment_succeeded'].includes(event.type)) return res.status(200).json({received: true});
  const session = event.data.object;
  if (session.payment_status !== 'paid' || session.metadata?.product !== 'septimo_sentido') return res.status(200).json({received: true});
  const plan = session.metadata.plan;
  if (!Object.hasOwn(AMOUNTS, plan) || session.currency !== 'usd' || session.amount_total !== AMOUNTS[plan]) {
    console.error('Pedido requiere revisión', session.id);
    return res.status(400).send('Pedido no válido');
  }
  const customer = session.customer_details?.email || session.customer_email;
  const link = plan === 'completa' ? process.env.COMPLETE_DELIVERY_URL : process.env.ESSENTIAL_DELIVERY_URL;
  // Configurar los enlaces privados cuando estén listos los materiales. Stripe reintenta un fallo.
  if (!customer || !link || !/^https:\/\//.test(link) || !process.env.RESEND_API_KEY || !process.env.RESEND_FROM_EMAIL || !process.env.PEDIDOS_EMAIL || !process.env.SUPPORT_EMAIL) {
    console.error('Entrega pendiente de configuración', session.id);
    return res.status(503).send('Entrega pendiente de configuración');
  }
  const edition = plan === 'completa' ? 'Experiencia Completa' : 'Edición Esencial';
  try {
    await sendEmail({from: process.env.RESEND_FROM_EMAIL, to: [customer], reply_to: process.env.SUPPORT_EMAIL,
      subject: 'Tu libro está aquí — Desbloquea Tu Séptimo Sentido',
      text: `¡Gracias por tu compra!\n\nTu pago ha sido confirmado.\nEdición: ${edition}\nTotal: US$ ${(session.amount_total / 100).toFixed(2)}\n\nAccede a tus materiales:\n${link}\n\nPedido: ${session.id}\n\nPara recibir ayuda o solicitar la garantía de 7 días desde la compra, responde a este correo indicando tu número de pedido.\n\nSéptimo Sentido`
    }, 'septimo-delivery-' + session.id);
    await sendEmail({from: process.env.RESEND_FROM_EMAIL, to: [process.env.PEDIDOS_EMAIL],
      subject: 'Pedido pagado — Séptimo Sentido — ' + edition,
      text: `Pedido: ${session.id}\nEdición: ${edition}\nTotal: USD ${(session.amount_total / 100).toFixed(2)}\nCorreo: ${customer}\nInstrucciones de acceso enviadas.`
    }, 'septimo-owner-' + session.id);
  } catch (error) { console.error('Error de entrega', session.id, error.message); return res.status(502).send('Entrega pendiente'); }
  return res.status(200).json({received: true});
};
module.exports.config = {api: {bodyParser: false}};
