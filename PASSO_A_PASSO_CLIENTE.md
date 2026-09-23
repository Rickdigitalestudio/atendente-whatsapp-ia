# Passo a passo para o CLIENTE (linguagem simples)

## 1. O que você vai precisar (5 min)
- Um computador com internet (Windows) OU conta grátis no Render/Railway (nuvem)
- O celular com o WhatsApp que vai atender (pode ser o seu número comercial)
- Opcional: chave grátis do Gemini (para respostas mais inteligentes) e Google Calendar

## 2. Instalação no computador (recomendado)
1. Instale **Python 3.11+** (python.org, marque "Add to PATH") e **Docker Desktop**
2. Copie a pasta `whatsapp-atendente` para o computador
3. Dê 2 cliques em **`install.bat`** e aguarde instalar
4. Abra o arquivo **`.env`** (bloco de notas) e preencha:
   - `EVOLUTION_APIKEY=uma-senha-forte-sua`
   - `GEMINI_API_KEY=` → pegue grátis em https://aistudio.google.com/app/apikey (ou deixe vazio: funciona em modo simples)
5. Abra **`config/config.json`** e troque nome, WhatsApp, horários e preços pelos seus
6. Dê 2 cliques em **`start-evolution.bat`** (sobe o servidor do WhatsApp, aguarde ~30s)
7. Rode **`python conectar_whatsapp.py`**, abra o `qrcode.png` gerado e escaneie com seu WhatsApp: abrir WhatsApp → Config → Aparelhos conectados → Conectar aparelho
8. Dê 2 cliques em **`start.bat`** (liga o robô). Deixe essa janela aberta.
9. No painel da Evolution (http://localhost:8080), na sua instância, configure Webhook URL = `http://SEU_IP:8000/webhook/evolution` marcando evento messages-upsert. (Se só testar local, use o simulador http://localhost:8000)
10. Teste: peça para alguém mandar "oi" no seu WhatsApp comercial. O robô responde!

## 3. Google Calendar (agenda de verdade)
1. Acesse console.cloud.google.com → crie projeto → ative **Google Calendar API**
2. Credenciais → Criar **ID do cliente OAuth (Desktop)** → baixe o JSON e salve como `credentials.json` dentro da pasta
3. Rode `python setup_google.py` uma vez, faça login com sua conta Google
4. Pronto: todo agendamento do WhatsApp entra no seu calendário. Sem isso, salva num arquivo `agenda.json` (funciona igual para demonstração).

## 4. Colocar na nuvem (para não deixar o PC ligado)
- Suba esta pasta no GitHub, crie serviço no **Render** (grátis): Build `pip install -r requirements.txt`, Start `python -m app.main`
- Use uma Evolution Cloud (evolution-api.com ou hospede a Evolution no Railway) e aponte o webhook para `https://seu-app.onrender.com/webhook/evolution`
- Variáveis de ambiente: as mesmas do `.env` + conteúdo do `token.pickle` (Google)

## 5. No celular, como fica?
O robô NÃO mora dentro do WhatsApp. O celular só **escaneia o QR uma vez**. Depois pode fechar o WhatsApp que o robô continua respondendo pelo computador/nuvem. Se trocar de celular, escaneie o QR de novo.

## 6. Problemas comuns
- "QR não aparece": Docker rodando? `docker compose ps`. Porta 8080 livre?
- "Bot não responde": janela do `start.bat` aberta? Webhook configurado? Teste antes no simulador http://localhost:8000
- "Google não salva": rode `setup_google.py` de novo; confira data/hora do PC
- "Quero parar": feche as janelas ou `docker compose down`
- Trocar preços/horários: edite `config/config.json` e reinicie `start.bat`. Sem programador.
