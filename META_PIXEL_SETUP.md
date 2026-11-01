# Meta Pixel — Canção de Fé

**ID do Pixel:** `1497991535722252`

## Eventos
- `PageView`: index.html, formulario.html, checkout.html e sucesso.html.
- `Lead`: conclusão válida do formulário (uma vez por sessão do navegador).
- `InitiateCheckout`: criação bem-sucedida da sessão de checkout (uma vez por sessão do navegador).
- `Purchase`: somente no webhook da Stripe, quando `payment_status === paid`, via Meta Conversions API (CAPI). Nenhum evento Purchase é disparado pela página de sucesso.

## Para habilitar o Purchase (CAPI)
1. No Gerenciador de Eventos da Meta, gere um token da API de Conversões para o Pixel acima.
2. Na Vercel, adicione a variável secreta **`META_CAPI_ACCESS_TOKEN`** com o token, apenas no ambiente de servidor. Não envie o token em conversas nem coloque-o em HTML.
3. Faça novo deploy.
4. Teste no Gerenciador de Eventos da Meta, usando os eventos de teste. O evento Purchase exige pagamento confirmado (inclusive Pix).

## Observações importantes
- O webhook usa um `event_id` estável por Stripe Checkout Session (`cdf_purchase_<session.id>`) para facilitar deduplicação.
- A API da Meta pode registrar eventos repetidos em reenvios do webhook; deduplicação persistente de ponta a ponta requer armazenamento de IDs processados.
- O webhook atual também pode reenviar e-mails em reentregas do Stripe. Não foi alterada essa lógica já existente.
- O código não envia informações pessoais do formulário à Meta. Para CAPI, apenas o e-mail normalizado e transformado em SHA-256 é incluído, quando disponível.
- Certifique-se de que sua política de privacidade e o gerenciamento de consentimento de cookies estejam adequados antes de ativar publicidade e rastreamento para visitantes reais. O código de Pixel é carregado nas páginas; não foi implementado um banner de consentimento.
- Os eventos devem ser conferidos na Meta antes de iniciar campanhas.
