# Desbloquea Tu Séptimo Sentido

Página em espanhol latino, branca e dourada, com checkout Stripe Form SDK preservado do projeto enviado. Sem quiz. Projeto estático + funções Node na Vercel; sem etapa de build.

## Publicar no projeto Vercel existente

Substitua os arquivos antigos pelo conteúdo desta pasta (não apenas sobreponha o index). Mantenha as variáveis de ambiente existentes indicadas abaixo. Framework Preset: Other; Build Command vazio; Output Directory vazio/raiz. O ZIP não inclui chaves.

### Pagamento

- `STRIPE_SECRET_KEY` e `STRIPE_PUBLISHABLE_KEY`: mesmo ambiente e conta usados no projeto original.
- `STRIPE_WEBHOOK_SECRET`: mantenha o segredo do endpoint `/api/stripe-webhook`.
- Eventos: `checkout.session.completed` e `checkout.session.async_payment_succeeded`.
- `STRIPE_PRICE_ID` antigo não é usado. O servidor cria os itens em USD: essencial 990 centavos; completa 1990 centavos. Um preço BRL do produto anterior não pode ser reutilizado para USD.
- Mantidos `ui_mode: form`, API `2026-03-25.dahlia`, SDK Dahlia e fluxo integrado de confirmação. Idioma Stripe `es`; textos da página `es-419`.
- Não foi realizada cobrança real ou teste com credenciais: elas não estavam no arquivo enviado. Validar na conta de teste antes de colocar tráfego.

### Entrega — finalizar após criar os livros

O livro e os bônus ainda serão produzidos na próxima etapa. Não iniciar vendas antes de criar os materiais e configurar:

- `RESEND_API_KEY`, `RESEND_FROM_EMAIL` (remetente validado), `PEDIDOS_EMAIL` (notificação interna).
- `SUPPORT_EMAIL`: endereço monitorado para respostas e solicitações da garantia.
- `ESSENTIAL_DELIVERY_URL`: URL HTTPS da entrega da edição essencial.
- `COMPLETE_DELIVERY_URL`: URL HTTPS da entrega completa com os quatro bônus.

Os links ficam no servidor e são enviados por e-mail somente após webhook assinado e pagamento confirmado, com validação de plano, valor e moeda. Utilize uma plataforma de acesso apropriada; um link compartilhável simples pode ser repassado. Se faltar configuração de entrega, o webhook retorna erro para permitir nova tentativa do Stripe. Não há download liberado por simplesmente visitar a página de sucesso. Garantia é solicitada por e-mail e processada manualmente pelo vendedor, não automaticamente.

O novo webhook só processa o produto `septimo_sentido`. Antes de substituir um projeto em produção, conclua os pedidos pendentes de músicas ou mantenha o endpoint legado separadamente. Arquivos de músicas, fotos e formulário antigo foram retirados; rotas antigas redirecionam para a oferta.

## Conteúdo e revisões

- Preços: US$ 9.90 e US$ 19.90, pagamento único.
- Bônus planejados: Diario del Despertar, Bajo Sus Alas, 7 Noches con los Salmos e Palabras de Luz.
- Capa é um mockup HTML/CSS para apresentação; o PDF e a arte final fazem parte da próxima etapa.
- Prévia de leitura na página é texto de apresentação, a incorporar/revisar na produção do livro.
- Depoimentos: seção implementada, oculta enquanto `site-config.js` tiver lista vazia. Adicionar somente relatos reais com autorização. Não foram inventados nomes, avaliações ou números de vendas.
- Textos de termos, privacidade e garantia incluídos. Completar identificação comercial e suporte do vendedor antes de vendas públicas.
- Pixel antigo de músicas não foi transferido para a nova oferta. Não há conversões falsas na página de sucesso. Parâmetros UTM são preservados até o checkout; configurar mensuração da nova oferta posteriormente.
- Visualização estática permite revisar a página; os endpoints Stripe exigem execução na Vercel. Um checkout em visualização estática exibe erro recuperável e não cobra.

## Verificação

`npm test`: testes de preço definido no servidor, planos inválidos, idioma, moeda e webhook (assinatura, pagamento, valores, entrega e repetição). Testes usam mock do Stripe e não realizam pagamentos.
