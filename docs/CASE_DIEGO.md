# Case: atendente de WhatsApp com IA — Diego Sales

> **Formato de case para o portfólio:** Problema → Solução → Resultado. Recrutadores e clientes leem isso em 1 minuto.

## O problema
Diego Sales, Coordenador Comercial de Planos de Saúde e Palestrante Motivacional Premium
([consultoriadeplano.com.br](https://consultoriadeplano.com.br/)), perdia leads porque:
- respondia WhatsApp manualmente, fora do horário comercial ninguém atendia;
- preço e horário eram perguntados dezenas de vezes por dia;
- agendamentos se perdiam no meio das conversas, sem calendário.

## A solução
Atendente de WhatsApp com IA conectado ao **número comercial real** via QR Code (Evolution API):
- **Boas-vindas automática** com menu (cotação / palestra / agendar);
- responde **horário** (Seg/Ter/Qui 9h–19h30, Qua 9h–18h, Sex 9h–17h), **preço de referência** dos 3 tipos de plano e **palestras**;
- **agenda reuniões** direto no Google Calendar (com fallback em arquivo local);
- transfere para **humano**, orienta **urgências** (192) e respeita **LGPD**;
- funciona **sem chave de IA** (modo regras, grátis) ou com **Gemini/OpenAI** — troca sem mexer no código;
- cliente configura tudo sozinho com `python configurar.py` (sem programar).

## Stack
Python · Flask · Evolution API (WhatsApp) · Google Calendar API · OpenAI / Gemini · Docker

## Resultado
- ✅ 10/10 testes automatizados passando (`python test_bot.py`)
- ✅ Resposta imediata 24h, agendamento sem fricção
- ✅ Entrega com instalador Windows (2 cliques), passo a passo leigo e termo de autorização LGPD

## Demonstração
- **Online (sem instalar nada):** ative o GitHub Pages neste repo (pasta `docs/`) e abra `demo.html` — é o cérebro do bot rodando no navegador.
- **Local:** `install.bat` → `start.bat` → http://localhost:8000
- **Vídeo sugerido (grave 60s):** tela dividida — você mandando "oi / preço / agendar" no celular e o bot respondendo + evento caindo no Google Calendar. Poste no LinkedIn e linke aqui.

## Arquitetura
Ver [`ARQUITETURA.md`](ARQUITETURA.md).
