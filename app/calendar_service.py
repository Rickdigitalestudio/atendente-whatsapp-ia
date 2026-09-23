"""Agenda: Google Calendar (quando configurado) + fallback em arquivo local."""
import json
from datetime import datetime, timedelta
from pathlib import Path
from .config_loader import env, BASE

ARQ_FALLBACK = BASE / "agenda.json"

def _ler_fallback() -> list:
    if ARQ_FALLBACK.exists():
        try:
            return json.loads(ARQ_FALLBACK.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def _salvar_fallback(item: dict):
    dados = _ler_fallback()
    dados.append(item)
    ARQ_FALLBACK.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

def google_disponivel() -> bool:
    return (BASE / "credentials.json").exists()

def listar_proximos(limite: int = 5) -> str:
    """Texto curto com próximos horários — usado como contexto do bot."""
    if google_disponivel():
        try:
            from google.oauth2.credentials import Credentials
            from googleapiclient.discovery import build
            # token.json gerado no 1º login (ver PASSO_A_PASSO)
            from google.auth.transport.requests import Request
            import pickle
            tok = BASE / "token.pickle"
            if not tok.exists():
                return ""
            with open(tok, "rb") as f:
                creds = pickle.load(f)
            if not creds.valid:
                if creds.expired and creds.refresh_token:
                    creds.refresh(Request())
            svc = build("calendar", "v3", credentials=creds)
            agora = datetime.utcnow().isoformat() + "Z"
            evs = svc.events().list(calendarId=env("GOOGLE_CALENDAR_ID", "primary"),
                                    timeMin=agora, maxResults=limite,
                                    singleEvents=True, orderBy="startTime").execute().get("items", [])
            if not evs:
                return "Agenda livre nos próximos dias."
            linhas = []
            for e in evs:
                ini = e.get("start", {}).get("dateTime", e.get("start", {}).get("date", "?"))
                linhas.append(f"• {ini} — {e.get('summary','Ocupado')}")
            return "Compromissos próximos: " + " | ".join(linhas)
        except Exception as e:
            print(f"[agenda] Google falhou: {e}")
    # fallback
    dados = _ler_fallback()
    if not dados:
        return ""
    ult = dados[-3:]
    return "Agendados (arquivo local): " + " | ".join(f"{d.get('quando','?')} — {d.get('nome','?')}" for d in ult)

def agendar(nome: str, quando_txt: str, tipo: str, telefone: str, obs: str = "") -> dict:
    """Tenta Google, senão salva local. Sempre retorna dict com ok + mensagem."""
    item = {"nome": nome, "quando": quando_txt, "tipo": tipo,
            "telefone": telefone, "obs": obs,
            "criado_em": datetime.now().isoformat()}
    if google_disponivel():
        try:
            import pickle
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            tok = BASE / "token.pickle"
            if tok.exists():
                with open(tok, "rb") as f:
                    creds = pickle.load(f)
                if creds.valid or (creds.expired and creds.refresh_token):
                    if creds.expired:
                        creds.refresh(Request())
                    svc = build("calendar", "v3", credentials=creds)
                    # quando_txt esperado: "2026-09-23 15:00" — tenta converter
                    try:
                        ini = datetime.fromisoformat(quando_txt)
                    except Exception:
                        ini = datetime.now() + timedelta(days=1)
                        ini = ini.replace(hour=15, minute=0, second=0, microsecond=0)
                    fim = ini + timedelta(minutes=30)
                    ev = svc.events().insert(calendarId=env("GOOGLE_CALENDAR_ID", "primary"), body={
                        "summary": f"{tipo} — {nome}",
                        "description": f"Tel: {telefone}\nObs: {obs}\nVia WhatsApp IA",
                        "start": {"dateTime": ini.isoformat(), "timeZone": "America/Sao_Paulo"},
                        "end": {"dateTime": fim.isoformat(), "timeZone": "America/Sao_Paulo"},
                    }).execute()
                    item["google_event_id"] = ev.get("id")
                    item["google_link"] = ev.get("htmlLink", "")
                    _salvar_fallback(item)  # espelho local
                    return {"ok": True, "onde": "google",
                            "mensagem": f"Agendado no Google Calendar para {ini.strftime('%d/%m %H:%M')} ✅",
                            "link": item.get("google_link", "")}
        except Exception as e:
            print(f"[agenda] erro Google, usando arquivo: {e}")
    _salvar_fallback(item)
    return {"ok": True, "onde": "local",
            "mensagem": f"Registrado para {quando_txt} ✅ (arquivo local — conecte o Google p/ sincronizar)."}
