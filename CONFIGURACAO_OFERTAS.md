# Canção de Fé — preços e ofertas

- Música principal: R$ 9,90 (usa `STRIPE_PRICE_ID`, que deve apontar para um preço de **R$ 9,90** na Stripe).
- Segunda versão, com outro estilo opcional: + R$ 7,90.
- Música + vídeo: + R$ 19,90.
- Selecionando ambos os adicionais: **total R$ 34,90**, desconto de R$ 2,80 sobre R$ 37,70.
- Apenas segunda versão: total R$ 17,80.
- Apenas vídeo: total R$ 29,80.
- Nenhum adicional: total R$ 9,90.

Os adicionais são criados no servidor com `price_data` em BRL. O pacote completo é um único item Stripe por R$ 34,90. O webhook informa quais adicionais foram comprados no e-mail do pedido.

**Antes de publicar:** conferir se `STRIPE_PRICE_ID` é um preço único de R$ 9,90, validar todos os quatro cenários no modo de teste Stripe, incluindo Pix/cartão e e-mails do webhook. Faça deploy em projeto de teste primeiro.

O vídeo é um serviço produzido manualmente, não um arquivo entregue automaticamente.
