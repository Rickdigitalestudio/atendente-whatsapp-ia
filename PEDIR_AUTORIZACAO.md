# Como pedir permissão para conectar na conta do Diego

## Opção A — Você conecta PARA ele (acesso temporário)
Mande esta mensagem no WhatsApp dele:

> Oi Diego! Para deixar seu atendente automático funcionando no seu número (21 98384-3924), preciso de uma permissão sua de 2 minutos — você tem controle total e pode desconectar quando quiser. Funciona assim:
>
> 1) Eu te mando um QR Code na tela
> 2) Você abre seu WhatsApp → Config → Aparelhos conectados → Conectar aparelho → escaneia
> 3) Pronto: o robô passa a responder boas-vindas, horário, preço e agenda no seu número. Suas conversas continuam suas.
>
> O que o robô NÃO faz: não apaga nada, não entra em grupos sozinho, não manda mensagem sem ser chamado. E você pode pedir "desconectar" a qualquer hora (também dá para remover em Aparelhos conectados).
>
> Pode me liberar esses 2 min hoje? Te mando o passo com print. Se preferir, faço tudo por chamada de vídeo com você escaneando aí do seu lado.

## Na hora da conexão (com ele ao vivo)
1. Garanta: servidor Evolution rodando + instância `atendente` criada
2. Gere o QR: `python conectar_whatsapp.py` (vale ~30-60s, se expirar gere outro)
3. Ele escaneia com o PRÓPRIO celular (conta comercial 21 98384-3924)
4. Confirme: `status_conexao` = open + mande "oi" de outro número e mostre a resposta
5. Configure o webhook e registre: data, hora e print da tela de "Aparelhos conectados" como comprovante

## Opção B — Ele conecta SOZINHO (controle total, recomendado se ele desconfiar)
Mande o ZIP da pasta + este texto:

> Diego, segue seu robô com tudo pronto e o passo a passo `PASSO_A_PASSO_CLIENTE.md`. Você instala no seu computador (2 cliques), escaneia o QR com SEU WhatsApp e ninguém além de você tem acesso. Nem eu preciso da sua senha. Qualquer dúvida me chama que faço com você por vídeo em 15 min.

## Termo simples de autorização (guarde assinado/print)
```
AUTORIZAÇÃO DE CONEXÃO — ATENDENTE WHATSAPP

Eu, Diego Sales (WhatsApp comercial 55 21 98384-3924,
e-mail diegoconsultordeplano@gmail.com), autorizo
_____________________ (seu nome/CPF) a conectar o programa
"Atendente WhatsApp IA" ao meu WhatsApp comercial via QR Code
(Aparelhos conectados), com a finalidade de responder
automaticamente boas-vindas, horários, preços e agendamentos.

- Posso revogar a qualquer momento em Aparelhos conectados.
- Meus dados e conversas continuam meus (LGPD).
- O programa não apaga mensagens nem entra em grupos sozinho.

Data: ___/___/___   Assinatura: _______________
```

## Regras de segurança (fale isso que gera confiança)
- Nunca peça a senha do WhatsApp/gmail dele nem o código SMS — QR Code não pede senha
- A chave de IA (.env) e o token do Google ficam NA MÁQUINA DELE, não na sua
- Se ele quiser, troque a `EVOLUTION_APIKEY` na entrega para só ele saber
- Entregue o `PASSO_A_PASSO_CLIENTE.md` junto: ele desliga tudo sozinho (`docker compose down` + remover aparelho)
