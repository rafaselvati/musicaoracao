# Envio de fotos após pagamento (vídeo)

Esta versão NÃO exige fotos no checkout. Após a Stripe confirmar um pedido com vídeo, o webhook envia ao cliente um link de 7 dias para `/enviar-fotos.html`. O cliente seleciona de 1 a 6 imagens, até 2 MB cada, e o servidor as envia como anexos para `PEDIDOS_EMAIL` via Resend. Não é necessário configurar Vercel Blob.

## Variáveis na Vercel

- `PHOTO_LINK_SECRET`: segredo aleatório longo (por exemplo, gerado localmente com `openssl rand -hex 32`). Não publique esse valor.
- `PUBLIC_SITE_URL`: endereço HTTPS do site, sem barra final (por exemplo, `https://musicaoracao.vercel.app`). Em testes use o endereço do projeto de teste.
- Mantenha `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `RESEND_API_KEY`, `RESEND_FROM_EMAIL`, `PEDIDOS_EMAIL` e `STRIPE_PRICE_ID` existentes.

Após salvar as variáveis, faça redeploy. Confirme que o domínio de `RESEND_FROM_EMAIL` está autorizado na Resend para envio aos clientes. O webhook precisa receber `checkout.session.completed` e `checkout.session.async_payment_succeeded`.

## Testes

1. Pague uma compra de música sem vídeo: nenhum link de fotos deve ser enviado.
2. Pague uma compra com vídeo: após confirmação, o cliente recebe o link.
3. Abra o link, selecione 1–6 imagens e envie: os anexos devem chegar a `PEDIDOS_EMAIL`.
4. Teste um link adulterado ou expirado: deve ser rejeitado.

## Limitações operacionais

As fotos são encaminhadas por e-mail, **não** armazenadas no Vercel Blob. Links podem ser reutilizados durante 7 dias; cada envio gera um novo e-mail, então o cliente pode reenviar fotos. Não há painel administrativo, bloqueio de reenvios ou exclusão automática de anexos da caixa de e-mail. Não publique este fluxo como armazenamento privado. Antes de escalar, adicione controle de envio único, limite de requisições e política de retenção/exclusão. O provedor de e-mail pode rejeitar anexos grandes.
