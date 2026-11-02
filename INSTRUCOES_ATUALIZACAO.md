# Canção de Fé — versão brasileira integrada

Esta versão mantém o site funcional em português brasileiro, com preço de **R$ 47,00**, vídeo atual `video-inicio.mp4` com botão **OUÇA UM EXEMPLO**, formulário com estilos brasileiros e seleção de voz, e **somente Stripe** como checkout.

## Formulário

Estilos: Gospel/Louvor, Sertanejo, Pagode, Samba, MPB, Forró, Pop, Romântico, Rock, Rap/Hip-Hop, Funk, Piseiro, Arrocha, Reggae e Outro estilo (campo livre). Preferência vocal: masculina, feminina ou sem preferência.

## Stripe

As funções existentes `api/create-checkout-session.js` e `api/stripe-webhook.js` foram preservadas. O preço real depende do `STRIPE_PRICE_ID` na Vercel: confirme que o Price ID ativo corresponde a **R$ 47,00 BRL**, cobrança única. Não inclua chaves de API no repositório.

## Pixel e e-mail

Integração Meta e Resend existente preservada. Confirme o webhook e os eventos assíncronos do Pix antes de vender.

## Escopo desta entrega

O ZIP de referência PrayerSong inclui dezenas de páginas de marketing e páginas de músicas de outra empresa. Esta entrega conserva a estrutura própria do Canção de Fé já localizada em PT-BR e seus fluxos funcionais, **não é uma tradução integral página a página do site externo**. Não foram importados depoimentos, garantias, preços ou políticas de terceiros.
