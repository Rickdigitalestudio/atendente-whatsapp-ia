"""Cliente HTTP da Evolution API (WhatsApp real via QR Code)."""
import requests
from .config_loader import env

def base_url() -> str:
    return env("EVOLUTION_URL", "http://localhost:8080").rstrip("/")

def api_key() -> str:
    return env("EVOLUTION_APIKEY", "minha-senha-forte")

def instance() -> str:
    return env("EVOLUTION_INSTANCE", "atendente")

def headers() -> dict:
    return {"apikey": api_key(), "Content-Type": "application/json"}

def criar_instancia_qr() -> dict:
    """Cria instância e retorna QR Code (base64) para escanear no celular."""
    url = f"{base_url()}/instance/create"
    r = requests.post(url, headers=headers(),
                      json={"instanceName": instance(), "qrcode": True}, timeout=20)
    r.raise_for_status()
    return r.json()

def status_conexao() -> dict:
    url = f"{base_url()}/instance/connectionState/{instance()}"
    r = requests.get(url, headers=headers(), timeout=15)
    r.raise_for_status()
    return r.json()

def enviar_texto(numero: str, texto: str) -> dict:
    """numero formato: 5511999999999 (só dígitos, com DDI)."""
    url = f"{base_url()}/message/sendText/{instance()}"
    r = requests.post(url, headers=headers(),
                      json={"number": numero, "text": texto}, timeout=20)
    r.raise_for_status()
    return r.json()
