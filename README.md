# 🤖 Atendente de WhatsApp com IA — Planos de Saúde + Palestras

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Flask](https://img.shields.io/badge/Flask-3-green) ![WhatsApp](https://img.shields.io/badge/WhatsApp-Evolution_API-25D366) ![License](https://img.shields.io/badge/License-MIT-gray)

> **Case real:** bot conectado ao número comercial de Diego Sales (Coordenador Comercial de Planos de Saúde + Palestrante Premium) — boas-vindas, horário, preço, palestras e agenda no Google Calendar.
> 📖 **[Ler o case](docs/CASE_DIEGO.md)** · 🧠 **[Arquitetura](docs/ARQUITETURA.md)** · 💬 **Demo online:** https://Ricklima991.github.io/atendente-whatsapp-ia/demo.html (após ativar o Pages) — o cérebro do bot clicável no navegador, sem instalar nada.

Projeto REAL e completo. Conecta o **número real do cliente via QR Code** (Evolution API),
responde **horário, preço e agenda**, integra **Google Calendar**, funciona **sem chave de IA**
(modo regras grátis) ou com **Gemini grátis / OpenAI**.

## O que o bot faz
- Saudação, horário, preço de planos (individual/familiar/empresarial/adesão), palestras
- Agenda reunião (pede nome + dia/horário + tipo) e salva no Google Calendar ou arquivo local
- Transfere para humano, trata urgência médica com responsabilidade, respeita LGPD
- Roda no PC do cliente ou nuvem grátis. Celular serve só para escanear o QR.

## Estrutura
```
whatsapp-atendente/
  app/main.py            servidor Flask (webhook + simulador)
  app/bot.py             cérebro (regras + OpenAI/Gemini)
  app/calendar_service.py Google Calendar + fallback agenda.json
  app/evolution.py       WhatsApp real via Evolution API
  config/config.json     EDITE: nome, horários, preços, palestras
  config/prompts/sistema.txt  personalidade da IA
  simulator.html         teste sem WhatsApp
  test_bot.py            teste automático
  install.bat / start.bat / start-evolution.bat
  docker-compose.yml     Evolution API local
```

## Uso rápido (5 min, sem WhatsApp)
```bat
cd whatsapp-atendente
install.bat
start.bat
```
Abra http://localhost:8000 e teste. Teste automático: `python test_bot.py`

## WhatsApp real (número do cliente)
1. Instale Docker Desktop, rode `start-evolution.bat`
2. `python conectar_whatsapp.py` → abre `qrcode.png`, escaneie com o WhatsApp do cliente
3. Na Evolution, configure o webhook: `http://SEU_IP:8000/webhook/evolution` (eventos messages-upsert)
4. Mande "oi" de outro celular → o bot responde. Agendamentos caem na agenda.

Detalhe completo e leigo em **PASSO_A_PASSO_CLIENTE.md**.

## IA — qual chave usar?
| Opção | Custo | Como |
|---|---|---|
| Sem chave (regras) | grátis | funciona de cara, respostas fixas inteligentes |
| Gemini | grátis (limite generoso) | https://aistudio.google.com/app/apikey → cole em `.env` GEMINI_API_KEY |
| OpenAI | pago por uso | https://platform.openai.com/api-keys → `.env` OPENAI_API_KEY |

Recomendação: comece sem chave ou Gemini grátis. Troque depois sem mexer no código.

## Google Calendar
- Sem config: salva em `agenda.json` (funciona).
- Com Google: crie projeto em console.cloud.google.com → ative Calendar API → OAuth Desktop → baixe `credentials.json` para esta pasta → rode `python setup_google.py` uma vez e faça login. Pronto, agendamentos entram no calendário real.
- Nuvem (Render/Railway): suba `token.pickle` gerado + `GOOGLE_CALENDAR_ID` nas env vars.

## No celular do cliente?
Verdade importante: o robô **não roda dentro do WhatsApp**. Opções:
- **A (recomendado):** robô no PC/nuvem, celular só escaneia o QR uma vez. WhatsApp pode ficar fechado depois (usa sessão do aparelho).
- **B (nuvem grátis):** hospede em Render/Railway, configure webhook da Evolution Cloud. Cliente não deixa PC ligado.
- **C (Termux, avançado):** roda o Python no Android via Termux, mas instável — só para teste.

## Personalizar
Edite `config/config.json` (nome, whatsapp, horários, preços, temas de palestra). Sem programar.
