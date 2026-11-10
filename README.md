# Desbloquea Tu Séptimo Sentido — página e entrega

## Ofertas finais

- US$ 9.90: livro principal (35 páginas) + Diario del Despertar (27 páginas).
- US$ 19.90: os dois materiais acima + Bajo Sus Alas (17 páginas), 7 Noches con los Salmos (17 páginas), Palabras de Luz (9 páginas).
- Valores riscados: referências atribuídas aos materiais, identificadas como tais, não preços anteriores de venda. Livro US$ 19.90; bônus US$ 9.90, US$ 12.90, US$ 9.90 e US$ 7.90. Soma US$ 60.50; preço do pacote US$ 19.90.
- Sem depoimentos falsos: exemplos de aplicação identificados. A seção para relatos reais continua disponível em `site-config.js`, oculta enquanto vazia.

## Estrutura

`public/`: arquivos públicos para Vercel. `api/`: pagamento, webhook, validação e download. `lib/`: catálogo e assinatura dos links. `private_files/`: os cinco PDFs e sete áudios MP3; não publicar esta pasta como conteúdo estático. `dist/`: prévia privada sem pagamentos e sem PDFs. Os arquivos HTML na raiz são a fonte editorial. Ao editar o conteúdo, atualizar public/ e dist/ com `python3 content-tools/sync_public.py`.

`vercel.json` define Output Directory como `public` e inclui os PDFs e MP3 completos somente na função de download. Apenas uma amostra de 25 segundos é pública. NÃO configurar a raiz ou private_files como saída pública. Substituir o pacote antigo integralmente para retirar formulários e páginas antigas.

## Configuração na Vercel

Framework Preset: Other. Sem comando de build. Output Directory: public (também definido no arquivo). Node.js compatível com Stripe 20. Instalação padrão de dependências do package.json.

Pagamento: preservar as duas chaves Stripe já configuradas. O acesso imediato após o pagamento também funciona com essas duas chaves. As demais variáveis abaixo pertencem ao e-mail complementar ou a opções de configuração e não são exigidas para abrir o checkout. Manter/configurar no servidor, sem colocá-las no HTML:

- STRIPE_SECRET_KEY e STRIPE_PUBLISHABLE_KEY: mesma conta e ambiente.
- STRIPE_WEBHOOK_SECRET: segredo do endpoint `/api/stripe-webhook`.
- RESEND_API_KEY e RESEND_FROM_EMAIL: envio de e-mail com remetente validado.
- PEDIDOS_EMAIL: recebe aviso interno da venda.
- SUPPORT_EMAIL: caixa monitorada para suporte e garantia.
- PUBLIC_SITE_URL: origem HTTPS real da Vercel/domínio para os links de e-mail. Opcional se VERCEL_PROJECT_PRODUCTION_URL já estiver disponível automaticamente na Vercel.
- DELIVERY_SECRET: opcional. Sem ele, uma chave exclusiva de assinatura é derivada com HMAC da STRIPE_SECRET_KEY existente. Se quiser definir um segredo independente, use ao menos 32 caracteres aleatórios. Trocar a chave utilizada invalida links antigos.

O checkout usa somente STRIPE_SECRET_KEY e STRIPE_PUBLISHABLE_KEY, já existentes no projeto original. A ausência de configuração de entrega, webhook ou e-mail NÃO bloqueia a criação da sessão de pagamento. A entrega imediata usa as mesmas chaves Stripe e não depende de configuração adicional de e-mail. Os antigos STRIPE_PRICE_ID, ESSENTIAL_DELIVERY_URL e COMPLETE_DELIVERY_URL não são usados nesta versão.

## Fluxo de entrega após o pagamento

1. Compra principal: pessoa escolhe a edição e paga no mesmo Stripe Checkout Form SDK do projeto original, em USD e espanhol.
2. Após a confirmação do formulário, o navegador abre `/entrega.html?session_id=...`. A página consulta o servidor; o servidor consulta o Stripe e verifica status pago, moeda, valor, produto e ausência de reembolso/disputa antes de liberar qualquer arquivo.
3. Se o pagamento ainda estiver processando, a página aguarda e verifica novamente. Não trata a chegada à página como prova de compra e não exige novo pagamento.
4. Pagamento aprovado: a biblioteca mostra os 2 ou 5 PDFs comprados, com download imediato. O e-mail é um meio adicional de recuperar o acesso e não é requisito para essa liberação.
5. Abaixo dos livros aparece o upsell opcional **Frecuencias de Contemplación — US$ 29.90**, com uma amostra pública de 25 segundos. Recusar ou ignorar não bloqueia os livros.
6. Ao aceitar, o cliente confirma uma NOVA compra no Stripe. Não existe débito automático ou cobrança sem nova confirmação. O servidor exige o acesso válido à compra principal para criar essa sessão e associa o pedido original ao pedido dos áudios.
7. Após aprovar os US$ 29.90, a biblioteca passa a liberar os 7 MP3 e também os PDFs vigentes da compra original. Os áudios não liberam bônus de uma edição não comprada.

Os tokens de acesso são assinados e duram 90 dias. Os arquivos baixados não expiram. Cada download consulta o pagamento no Stripe. Links e identificadores de retorno são credenciais privadas de acesso; não compartilhá-los publicamente. O recebimento de um e-mail, por si só, não libera um pedido não pago.

## Áudios do upsell

Sete paisagens sonoras originais, sem voz/narração, com cinco minutos cada (35 minutos no total):

1. Pausa — 396 Hz
2. Presencia — 417 Hz
3. Espacio — 432 Hz
4. Quietud — 528 Hz
5. Encuentro — 639 Hz
6. Horizonte — 741 Hz
7. Continuidad — 852 Hz

As frequências são componentes centrais do arranjo sonoro, acompanhadas de outros tons harmônicos. Não são batidas binaurais e não são apresentadas como tratamento ou garantia de evolução espiritual. A vantagem proposta é acompanhar uma rotina de contemplação, sem substituir ou desvalorizar o livro.

MP3 estéreo, 44,1 kHz, 96 kbps; cada faixa tem aproximadamente 3,6 MB, abaixo do limite de resposta de 4,5 MB da função. A amostra de 25 segundos fica em assets/muestra-432hz.mp3. Os MP3 integrais ficam fora de public/ e dist/. Gerador original: content-tools/create_audio.py (NumPy + FFmpeg); métricas: audio_manifest.json.

O webhook de e-mail usa chaves de idempotência por sessão. A garantia é atendida manualmente pelo vendedor. Para o e-mail, preservar/configurar os eventos checkout.session.completed e checkout.session.async_payment_succeeded. O suporte usa SUPPORT_EMAIL ou, na ausência, PEDIDOS_EMAIL. As antigas variáveis UPSELL_READY e UPSELL_CHECKOUT_URL não são usadas: a oferta aprovada está integrada ao Stripe.

## Antes do tráfego real

- Fazer uma compra em modo de teste para cada edição, confirmar o redirecionamento, os downloads e o e-mail complementar.
- Comprar o upsell em modo de teste e verificar que os sete áudios são liberados sem perder os livros.
- Verificar que um pagamento pendente ou recusado não libera os arquivos.
- Confirmar que a edição essencial não libera os três bônus adicionais.
- Conferir que /private_files/Desbloquea_Tu_Septimo_Sentido.pdf não serve o PDF publicamente.
- Validar suporte, identificação comercial do vendedor, termos e garantia na operação real.
- Se o projeto anterior ainda tiver pedidos de músicas pendentes, preservar seu webhook legado separadamente até concluir esses pedidos. O novo webhook só atende o novo produto.

Não houve cobrança real nem validação na sua conta Stripe/Vercel, pois essas credenciais e o acesso à implantação não foram fornecidos. A prévia hospedada é privada e não processa pagamentos nem libera downloads. A amostra de áudio pode ser ouvida na prévia. O pixel antigo de músicas não foi reaproveitado; UTMs são preservadas até o checkout.

## Conteúdo e validação

Os cinco PDFs são originais, em espanhol. As orações não são atribuídas a textos bíblicos; os materiais indicam referências para leitura, sem reproduzir traduções protegidas. O diário foi diagramado para leitura/impressão, sem campos interativos. Gerador em content-tools/create_books.py; requer ReportLab e fontes DejaVu.

`npm test` verifica preços, planos, assinatura, confirmação, entrega, tokens, expiração e bloqueio de acesso indevido. Testes simulam o Stripe e não substituem uma compra de teste na conta real.

## Google Analytics

ID: G-8D1Y6BW9VN. Eventos: page_view (página), select_item (clique na oferta), checkout_view (checkout aberto), begin_checkout (formulário Stripe carregado) e purchase (compra real validada pelo servidor no retorno do checkout). offer_plan distingue esencial/completa/audios. As compras usam identificador estatístico, sem expor IDs Stripe ou tokens de entrega. Reabrir um link de e-mail não registra nova compra. Deduplicação por pedido no navegador e transaction_id no GA4.

No Analytics, acompanhe Relatórios → Tempo real para validar a instalação e os eventos. Compare usuários por evento, não apenas contagem total (uma pessoa pode clicar mais de uma vez). Dados começam após o deploy na Vercel; não são retroativos. Prévia, localhost e pagamentos Stripe de teste não registram compras. Bloqueadores, cookies e fechamento da página podem impedir medições; o Stripe permanece a fonte do total financeiro. Não há envio de compra pelo webhook para o GA4 nesta versão.
