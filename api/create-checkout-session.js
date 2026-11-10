const Stripe = require('stripe');
const {authorize}=require('../lib/delivery');
const PLANS = Object.freeze({
  esencial: {amount: 990, name: 'Desbloquea Tu Séptimo Sentido — Edición Esencial + Diario del Despertar'},
  completa: {amount: 1990, name: 'Desbloquea Tu Séptimo Sentido — Experiencia Completa + 4 bonos'},
  audios: {amount: 2990, name: 'Frecuencias de Contemplación — 7 audios meditativos'}
});
module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({error: 'Método no permitido.'}); }
  const key = req.body?.plan;
  if (typeof key !== 'string' || !Object.hasOwn(PLANS, key)) return res.status(400).json({error: 'Selecciona una edición válida.'});
  if (!process.env.STRIPE_SECRET_KEY || !process.env.STRIPE_PUBLISHABLE_KEY) return res.status(503).json({error: 'El pago no está disponible en este momento. Intenta nuevamente más tarde.'});
  const plan = PLANS[key];
  let parent;
  if(key === 'audios') {
    try { parent = await authorize(req.body?.parent_token); if(parent.plan === 'audios') return res.status(409).json({error:'Los audios ya están incluidos en este acceso.'}); }
    catch { return res.status(403).json({error:'Abre primero tu biblioteca de la compra original para acceder a esta oferta.'}); }
  }
  try {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {apiVersion: '2026-03-25.dahlia'});
    // Mismo Checkout Form SDK del proyecto original. El servidor fija precio y moneda.
    const session = await stripe.checkout.sessions.create({
      ui_mode: 'form', mode: 'payment',
      line_items: [{price_data: {currency: 'usd', unit_amount: plan.amount, product_data: {name: plan.name}}, quantity: 1}],
      billing_address_collection: 'auto', phone_number_collection: {enabled: false},
      automatic_tax: {enabled: false}, submit_type: 'auto',
      integration_identifier: 'custom_embedded_web_0001',
      locale: 'es', metadata: {product: 'septimo_sentido', plan: key, expected_total_cents: String(plan.amount), ...(parent ? {parent_session: parent.session.id} : {})}
    });
    return res.status(200).json({session_id: session.id, client_secret: session.client_secret, publishable_key: process.env.STRIPE_PUBLISHABLE_KEY});
  } catch (error) {
    console.error('Stripe session error', error.type, error.code);
    return res.status(502).json({error: 'No se pudo iniciar el pago. Intenta nuevamente en unos minutos.'});
  }
};
