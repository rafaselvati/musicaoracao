# Integração Stripe — Canção de Fé

## Valores a configurar na Vercel

- `STRIPE_SECRET_KEY`: chave secreta da Stripe, **somente servidor**.
- `STRIPE_PUBLISHABLE_KEY`: chave pública (`pk_test_...` em testes).
- `STRIPE_PRICE_ID`: ID do preço Stripe **BRL 47,00, pagamento único**, criado no Dashboard (ex.: `price_...`). Não use um preço de assinatura.
- `STRIPE_WEBHOOK_SECRET`: segredo do endpoint webhook (`whsec_...`).
- `RESEND_API_KEY`: chave da Resend para notificar pedidos pagos.
- `RESEND_FROM_EMAIL`: remetente autorizado/verificado na Resend.
- `PEDIDOS_EMAIL`: e-mail que receberá os dados dos pedidos.

## Configured Parameters

Arquivo: [api/create-checkout-session.js](api/create-checkout-session.js)

| Parâmetro | Valor |
|---|---|
| ui_mode | form |
| mode | payment (venda única) |
| billing_address_collection | auto |
| phone_number_collection.enabled | false |
| automatic_tax.enabled | false |
| submit_type | auto |
| integration_identifier | custom_embedded_web_0001 |
| line_items | STRIPE_PRICE_ID x 1 |

`payment_method_collection` foi omitido porque `mode=payment`, conforme instrução da Stripe.

## Webhook

No Stripe Dashboard, configure endpoint `https://SEU-DOMINIO.vercel.app/api/stripe-webhook` para eventos `checkout.session.completed` e `checkout.session.async_payment_succeeded`. O código verifica assinatura e pagamento confirmado antes de notificar. Configure todas as variáveis no ambiente de produção e faça novo deploy.

## Atenções antes de vender

1. Teste com chaves e preço de teste. Consulte cartões de teste oficiais: https://docs.stripe.com/testing .
2. Ative Pix no Dashboard se elegível; a Stripe determina métodos de pagamento disponíveis.
3. A integração não cria banco de dados. Respostas são enviadas para Stripe Session metadata (cada campo limitado a 500 caracteres) e, após pagamento, para o e-mail configurado.
4. **Pedidos grandes podem ter texto truncado** em campos longos. Para produção com textos completos e robustez, use armazenamento persistente seguro.
5. **Webhooks podem ser reenviados**; sem persistência/idempotência, podem gerar e-mails duplicados. Não considere esse fluxo pronto para produção de alto volume sem controle de eventos processados.
6. A confirmação do Pix pode ser assíncrona. Não entregue produto apenas por retorno do navegador.
7. Os order bumps antigos não estão conectados à Stripe nesta versão; preço fixo R$ 47,00.
8. Nunca publique `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` ou `RESEND_API_KEY` em HTML ou Git.

## Fluxo

`index.html` → `formulario.html` → `checkout.html` → Stripe embedded form → webhook Stripe → e-mail via Resend.

Documentação: https://docs.stripe.com/checkout e https://support.stripe.com
