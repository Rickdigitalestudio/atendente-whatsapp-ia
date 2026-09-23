"""Teste rápido sem WhatsApp: python test_bot.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from app.config_loader import load_config
from app.bot import responder, detectar_intencao
from app import calendar_service as agenda

cfg = load_config()
casos = [
    "Olá, tudo bem?",
    "Qual o horário de atendimento?",
    "Quanto custa o plano familiar?",
    "Sou MEI, tem plano empresarial?",
    "Você faz palestra? Qual o valor?",
    "Quero agendar uma reunião",
    "Ana, amanhã 15h, cotação familiar",
    "Quero falar com humano",
    "Tô com dor forte, e agora?",
    "Obrigado, tchau!",
]
ok = 0
for c in casos:
    inten = detectar_intencao(c)
    resp, motor = responder(c, cfg, [], "")
    passou = len(resp) > 10
    ok += passou
    print(f"\n> {c}\n  [{inten}|{motor}] {resp[:220]}")
print(f"\n{ok}/{len(casos)} respostas OK (motor: regras sem chave, openai/gemini com chave)")
r = agenda.agendar("Cliente Teste", "amanhã 15h", "Cotação plano", "5511999999999", "teste automático")
print("Agenda:", r["mensagem"])
