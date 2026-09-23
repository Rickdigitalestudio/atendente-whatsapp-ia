"""Carrega config.json + .env de forma simples."""
import json, os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

def load_config(path: str | None = None) -> dict:
    p = Path(path) if path else BASE / "config" / "config.json"
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def load_system_prompt() -> str:
    p = BASE / "config" / "prompts" / "sistema.txt"
    if p.exists():
        return p.read_text(encoding="utf-8")
    return "Você é um atendente de WhatsApp prestativo."

def env(key: str, default: str = "") -> str:
    # tenta .env manual sem depender de lib externa
    if key in os.environ:
        return os.environ[key]
    dotenv = BASE / ".env"
    if dotenv.exists():
        for line in dotenv.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == key:
                return v.strip().strip('"').strip("'")
    return default
