"""Gera o QR Code para conectar o WhatsApp real do cliente. Rode: python conectar_whatsapp.py"""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from app.config_loader import env
from app import evolution as evo

print(f"Evolution: {evo.base_url()} | instancia: {evo.instance()}")
try:
    dados = evo.criar_instancia_qr()
    print("Resposta:", json.dumps(dados, indent=2)[:2000])
    # tenta salvar QR se vier base64
    qr = (dados.get("qrcode") or {}).get("base64") or dados.get("qrcode", "")
    if isinstance(qr, str) and len(qr) > 200:
        import base64
        b64 = qr.split(",", 1)[-1]
        Path("qrcode.png").write_bytes(base64.b64decode(b64))
        print("QR salvo em qrcode.png — abra a imagem e escaneie com o WhatsApp do cliente.")
    else:
        print("Abra o Evolution Manager em http://localhost:8080 e escaneie o QR da instancia 'atendente'.")
    print("Status:", evo.status_conexao())
except Exception as e:
    print(f"ERRO: {e}\n1) Rode start-evolution.bat (Docker) 2) Confira o .env (EVOLUTION_URL e APIKEY)")
