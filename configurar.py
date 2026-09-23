"""Configuração FÁCIL para o Diego (sem programar).
Rode: python configurar.py — responde as perguntas e pronto.
"""
import json
from pathlib import Path

BASE = Path(__file__).parent
CFG = BASE / "config" / "config.json"

def perguntar(txt, atual):
    r = input(f"{txt}\n  [atual: {atual}] (Enter mantém, ou digite novo): ").strip()
    return r if r else atual

def main():
    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    print("=== Configuração fácil — Diego Sales ===")
    print("Dica: aperte Enter para manter o valor atual.\n")
    n = cfg["negocio"]
    n["nome"] = perguntar("1) Seu nome comercial", n["nome"])
    n["whatsapp_comercial"] = perguntar("2) WhatsApp comercial (só números, ex 55219XXXXXXX)", n["whatsapp_comercial"])
    n["email"] = perguntar("3) E-mail", n.get("email", ""))
    n["site"] = perguntar("4) Site", n.get("site", ""))
    n["instagram"] = perguntar("5) Instagram (@...)", n.get("instagram", ""))

    h = cfg["horarios"]
    print("\n--- Horários ---")
    for k in ["segunda", "terca", "quarta", "quinta", "sexta", "sabado", "domingo"]:
        h[k] = perguntar(f"Horário de {k} (ex '09:00 às 19:30' ou 'fechado')", h.get(k, "fechado"))
    h["texto_resumo"] = perguntar("Resumo falado pelo robô", h["texto_resumo"])

    print("\n--- Boas-vindas automática ---")
    cfg["boas_vindas"] = perguntar("Mensagem de boas-vindas", cfg.get("boas_vindas", ""))

    print("\n--- Preços de referência (o robô sempre diz 'a partir de' + pede cotação) ---")
    for p in cfg["planos"]:
        p["preco_referencia"] = perguntar(f"Preço: {p['nome']}", p["preco_referencia"])

    print("\n--- Palestras ---")
    pal = cfg["palestras"]
    temas = perguntar("Temas separados por vírgula", ", ".join(pal["temas"]))
    pal["temas"] = [t.strip() for t in temas.split(",") if t.strip()]
    pal["preco_referencia"] = perguntar("Valor da palestra (ex 'sob consulta...')", pal["preco_referencia"])

    CFG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nOK! Salvo em config/config.json. Reinicie com start.bat para valer.")
    print("Teste no simulador: http://localhost:8000")

if __name__ == "__main__":
    main()
