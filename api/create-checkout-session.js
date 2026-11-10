const Stripe = require('stripe');
const PLANS = Object.freeze({
  esencial: {amount: 990, name: 'Desbloquea Tu Séptimo Sentido — Edición Esencial + Diario del Despertar'},
  completa: {amount: 1990, name: 'Desbloquea Tu Séptimo Sentido — Experiencia Completa + 4 bonos'}
});
module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({error: 'Método no permitido.'}); }
  const key = req.body?.plan;
  if (typeof key !== 'string' || !Object.hasOwn(PLANS, key)) return res.status(400).json({error: 'Selecciona una edición válida.'});
  if (!process.env.STRIPE_SECRET_KEY || !process.env.STRIPE_PUBLISHABLE_KEY) return res.status(503).json({error: 'El pago no está disponible en este momento. Intenta nuevamente más tarde.'});
  if (!process.env.DELIVERY_SECRET || process.env.DELIVERY_SECRET.length < 32 || !process.env.PUBLIC_SITE_URL?.startsWith('https://') || !process.env.RESEND_API_KEY || !process.env.RESEND_FROM_EMAIL || !process.env.PEDIDOS_EMAIL || !process.env.SUPPORT_EMAIL || !process.env.STRIPE_WEBHOOK_SECRET) return res.status(503).json({error: 'Estamos preparando el acceso a los materiales. Intenta nuevamente más tarde.'});
  const plan = PLANS[key];
  try {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {apiVersion: '2026-03-25.dahlia'});
    // Mismo Checkout Form SDK del proyecto original. El servidor fija precio y moneda.
    const session = await stripe.checkout.sessions.create({
      ui_mode: 'form', mode: 'payment',
      line_items: [{price_data: {currency: 'usd', unit_amount: plan.amount, product_data: {name: plan.name}}, quantity: 1}],
      billing_address_collection: 'auto', phone_number_collection: {enabled: false},
      automatic_tax: {enabled: false}, submit_type: 'auto',
      integration_identifier: 'custom_embedded_web_0001',
      locale: 'es', metadata: {product: 'septimo_sentido', plan: key, expected_total_cents: String(plan.amount)}
    });
    return res.status(200).json({client_secret: session.client_secret, publishable_key: process.env.STRIPE_PUBLISHABLE_KEY});
  } catch (error) {
    console.error('Stripe session error', error.type, error.code);
    return res.status(502).json({error: 'No se pudo iniciar el pago. Intenta nuevamente en unos minutos.'});
  }
};
