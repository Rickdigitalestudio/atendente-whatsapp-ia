"""Servidor do atendente: recebe mensagens da Evolution API e responde.
Roda com: python -m app.main
Endpoints:
  GET  /health
  POST /webhook/evolution   (configure na Evolution: webhook url = http://SEU_PC:8000/webhook/evolution)
  POST /api/simular         (usado pelo simulator.html p/ testar sem WhatsApp)
"""
import re
from flask import Flask, request, jsonify, send_file
from pathlib import Path
from .config_loader import load_config, BASE
from .bot import responder, detectar_intencao
from . import calendar_service as agenda

app = Flask(__name__)
CFG = load_config()
historicos: dict[str, list] = {}  # numero -> lista {role, content}

def extrair_dados_agendamento(texto: str) -> dict | None:
    """Tenta extrair 'Nome, dia/horário, tipo' de mensagens como 'Ana, amanhã 15h, cotação'."""
    # heurística simples: se tem intenção agendar + tem algo parecido com nome e horário
    if detectar_intencao(texto) != "agendar" and not re.search(r"\d{1,2}\s*h", texto.lower()):
        return None
    partes = [p.strip() for p in re.split(r"[,;]|(?=\bamanh[aã]\b)|(?=\bhoje\b)|(?=\bdia\b)", texto) if p.strip()]
    nome = partes[0] if partes else "Cliente"
    nome = re.sub(r"^(agendar|marca|quero|gostaria de)\s+", "", nome, flags=re.I).strip()[:40] or "Cliente"
    tipo = "Cotação plano" if re.search(r"plano|cota|famil|empres|ades", texto.lower()) else \
           "Palestra" if re.search(r"palestra|evento", texto.lower()) else "Reunião"
    m = re.search(r"(hoje|amanh[aã]|dia\s+\d{1,2}[\/-]\d{1,2}|\d{1,2}[\/-]\d{1,2})?\s*(\d{1,2})\s*h?", texto.lower())
    quando = m.group(0).strip() if m else texto[:60]
    return {"nome": nome.title(), "quando": quando, "tipo": tipo}

@app.get("/health")
def health():
    return {"ok": True, "modo_google": agenda.google_disponivel()}

@app.get("/")
def index():
    html = BASE / "simulator.html"
    if html.exists():
        return send_file(html)
    return {"ok": True, "msg": "Atendente rodando. Abra simulator.html ou POST /api/simular"}

@app.post("/api/simular")
def simular():
    data = request.get_json(force=True, silent=True) or {}
    texto = data.get("mensagem", "").strip()
    numero = data.get("numero", "teste") or "teste"
    if not texto:
        return jsonify({"resposta": "Digite uma mensagem para testar."}), 400
    hist = historicos.setdefault(numero, [])
    contexto = agenda.listar_proximos()
    resposta, motor = responder(texto, CFG, hist, contexto)
    # tenta agendar automaticamente se mensagem parece agendamento completo
    dados = extrair_dados_agendamento(texto)
    if dados and re.search(r"\d{1,2}\s*h", texto.lower()) and len(texto) > 12:
        r = agenda.agendar(dados["nome"], dados["quando"], dados["tipo"], numero)
        resposta += f"\n\n{r['mensagem']}"
    hist.append({"role": "user", "content": texto})
    hist.append({"role": "assistant", "content": resposta})
    return jsonify({"resposta": resposta, "motor": motor, "intencao": detectar_intencao(texto)})

@app.post("/webhook/evolution")
def webhook():
    """Recebe eventos da Evolution API (messages-upsert)."""
    data = request.get_json(force=True, silent=True) or {}
    try:
        # formato Evolution v2: data.message..., data.key.remoteJid, etc.
        msg = data.get("data", {}).get("message", {}) or {}
        texto = (msg.get("conversation")
                 or msg.get("extendedTextMessage", {}).get("text") or "").strip()
        jid = data.get("data", {}).get("key", {}).get("remoteJid", "") or ""
        numero = re.sub(r"\D", "", jid.split("@")[0])
        if not texto or not numero or data.get("data", {}).get("key", {}).get("fromMe"):
            return jsonify({"ignored": True})
        from . import evolution as evo
        hist = historicos.setdefault(numero, [])
        resposta, _ = responder(texto, CFG, hist, agenda.listar_proximos())
        dados = extrair_dados_agendamento(texto)
        if dados and re.search(r"\d{1,2}\s*h", texto.lower()) and len(texto) > 12:
            r = agenda.agendar(dados["nome"], dados["quando"], dados["tipo"], numero)
            resposta += f"\n\n{r['mensagem']}"
        hist.append({"role": "user", "content": texto})
        hist.append({"role": "assistant", "content": resposta})
        evo.enviar_texto(numero, resposta)
        return jsonify({"ok": True})
    except Exception as e:
        print(f"[webhook] erro: {e} | payload: {str(data)[:500]}")
        return jsonify({"ok": False, "erro": str(e)}), 500

if __name__ == "__main__":
    print("Atendente rodando em http://localhost:8000  | simulador: http://localhost:8000/")
    print(f"Google Calendar: {'CONECTADO' if agenda.google_disponivel() else 'arquivo local (coloque credentials.json p/ ativar Google)'}")
    app.run(host="0.0.0.0", port=8000, debug=False)
