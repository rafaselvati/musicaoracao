# Desbloquea Tu Séptimo Sentido — página e entrega

## Ofertas finais

- US$ 9.90: livro principal (35 páginas) + Diario del Despertar (27 páginas).
- US$ 19.90: os dois materiais acima + Bajo Sus Alas (17 páginas), 7 Noches con los Salmos (17 páginas), Palabras de Luz (9 páginas).
- Valores riscados: referências atribuídas aos materiais, identificadas como tais, não preços anteriores de venda. Livro US$ 19.90; bônus US$ 9.90, US$ 12.90, US$ 9.90 e US$ 7.90. Soma US$ 60.50; preço do pacote US$ 19.90.
- Sem depoimentos falsos: exemplos de aplicação identificados. A seção para relatos reais continua disponível em `site-config.js`, oculta enquanto vazia.

## Estrutura

`public/`: arquivos públicos para Vercel. `api/`: pagamento, webhook, validação e download. `lib/`: catálogo e assinatura dos links. `private_files/`: os cinco PDFs; não publicar esta pasta como conteúdo estático. `dist/`: prévia privada sem pagamentos e sem PDFs. Os arquivos HTML na raiz são a fonte editorial. Ao editar o conteúdo, atualizar public/ e dist/ com `python3 content-tools/sync_public.py`.

`vercel.json` define Output Directory como `public` e inclui os PDFs somente na função de download. NÃO configurar a raiz ou private_files como saída pública. Substituir o pacote antigo integralmente para retirar formulários e páginas antigas.

## Configuração na Vercel

Framework Preset: Other. Sem comando de build. Output Directory: public (também definido no arquivo). Node.js compatível com Stripe 20. Instalação padrão de dependências do package.json.

Manter/configurar estas variáveis no servidor, sem colocá-las no HTML:

- STRIPE_SECRET_KEY e STRIPE_PUBLISHABLE_KEY: mesma conta e ambiente.
- STRIPE_WEBHOOK_SECRET: segredo do endpoint `/api/stripe-webhook`.
- RESEND_API_KEY e RESEND_FROM_EMAIL: envio de e-mail com remetente validado.
- PEDIDOS_EMAIL: recebe aviso interno da venda.
- SUPPORT_EMAIL: caixa monitorada para suporte e garantia.
- PUBLIC_SITE_URL: origem HTTPS real da Vercel/domínio, sem caminho ou parâmetros.
- DELIVERY_SECRET: segredo aleatório de pelo menos 32 caracteres. Gerar localmente com `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"` e salvar apenas na configuração de ambiente. Alterá-lo invalida links antigos.

O checkout não cria cobranças enquanto faltar uma das configurações essenciais de pagamento/entrega. Os antigos STRIPE_PRICE_ID, ESSENTIAL_DELIVERY_URL e COMPLETE_DELIVERY_URL não são usados nesta versão.

## Fluxo de entrega

1. A pessoa escolhe a edição e paga no mesmo Stripe Checkout Form SDK do projeto original, agora em USD e espanhol.
2. O webhook verifica a assinatura e só processa um pagamento confirmado do produto septimo_sentido, com valor e moeda corretos.
3. Um e-mail envia `https://SEU-DOMINIO/entrega.html?token=TOKEN_ASSINADO`. O link é gerado pelo servidor; não montar tokens manualmente.
4. A área verifica o pagamento na Stripe e mostra os materiais da edição. Cada download repete a verificação, incluindo reembolso/disputa.
5. O comprador baixa os PDFs e pode guardá-los. O link é pessoal e vale 90 dias; suporte pode emitir outro link após validar o pedido. O arquivo em si não expira. Links são credenciais de acesso, podem ser compartilhados pelo destinatário e devem ser tratados como privados.

A página de sucesso informa que o pagamento está sendo verificado, sem liberar arquivos por simples visita. A função download recebe somente IDs do catálogo, não caminhos de arquivos. PDFs não ficam em public/ nem dist/.

O envio usa chaves de idempotência por sessão, respeitando a janela de idempotência do provedor de e-mail; reenvios manuais posteriores à janela podem gerar novo e-mail. Garantias são atendidas manualmente pelo vendedor. Configure no Stripe os eventos checkout.session.completed e checkout.session.async_payment_succeeded e teste a entrega.

## Upsell opcional

A área de entrega contém uma seção oculta de acompanhamento guiado que reforça que o livro é completo. Áudios, formato e preço ainda não foram aprovados/produzidos. Nenhum upsell é cobrado nesta versão.

Quando o produto adicional estiver pronto, configurar UPSELL_READY=true e UPSELL_CHECKOUT_URL com a URL HTTPS da oferta. O link leva à apresentação/checkout que informa o preço; não é cobrança automática nem one-click.

## Antes do tráfego real

- Fazer uma compra em modo de teste para cada edição e confirmar e-mails/downloads.
- Confirmar que a edição essencial não libera os três bônus adicionais.
- Conferir que /private_files/Desbloquea_Tu_Septimo_Sentido.pdf não serve o PDF publicamente.
- Validar suporte, identificação comercial do vendedor, termos e garantia na operação real.
- Se o projeto anterior ainda tiver pedidos de músicas pendentes, preservar seu webhook legado separadamente até concluir esses pedidos. O novo webhook só atende o novo produto.

Não houve cobrança real nem validação na sua conta Stripe/Vercel, pois essas credenciais e o acesso à implantação não foram fornecidos. A prévia hospedada é privada e não processa pagamentos. O pixel antigo de músicas não foi reaproveitado; UTMs são preservadas até o checkout.

## Conteúdo e validação

Os cinco PDFs são originais, em espanhol. As orações não são atribuídas a textos bíblicos; os materiais indicam referências para leitura, sem reproduzir traduções protegidas. O diário foi diagramado para leitura/impressão, sem campos interativos. Gerador em content-tools/create_books.py; requer ReportLab e fontes DejaVu.

`npm test` verifica preços, planos, assinatura, confirmação, entrega, tokens, expiração e bloqueio de acesso indevido. Testes simulam o Stripe e não substituem uma compra de teste na conta real.
