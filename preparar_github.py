"""Prepara cópia SEGURA para o GitHub (sem dados sensíveis do cliente).
Rode: python preparar_github.py
Cria: ../atendente-whatsapp-ia/ pronta para `git init + push`.
Pede permissão do Diego antes de publicar o nome dele (ver PEDIR_AUTORIZACAO).
"""
import json, shutil
from pathlib import Path

SRC = Path(__file__).parent
DST = SRC.parent / "atendente-whatsapp-ia"

FONE_REAL = "55219XXXXXXX"
FONE_MASK = "55219XXXXXXX"  # mascarado no portfólio público

EXCLUIR = {"__pycache__", ".venv", "agenda.json", ".env", "token.pickle",
           "credentials.json", "qrcode.png", "ENTREGA_DIEGO.md"}

def copiar_limpo():
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns(
        "__pycache__", ".venv", "*.pyc", ".env", "token.pickle",
        "credentials.json", "qrcode.png", "agenda.json", "logs"))
    for nome in EXCLUIR:
        p = DST / nome
        if p.exists():
            p.unlink() if p.is_file() else shutil.rmtree(p, ignore_errors=True)
    # mascara telefone em todos os textos
    for f in list(DST.rglob("*.json")) + list(DST.rglob("*.md")) + list(DST.rglob("*.py")) + list(DST.rglob("*.txt")):
        try:
            t = f.read_text(encoding="utf-8")
        except Exception:
            continue
        if FONE_REAL in t:
            f.write_text(t.replace(FONE_REAL, FONE_MASK)
                          .replace("21 9XXXX-XXXX", "21 9XXXX-XXXX"), encoding="utf-8")
    print(f"OK! Pasta portfólio em: {DST}")
    print("Arquivos:", sum(1 for _ in DST.rglob('*') if _.is_file()))
    print("\nPróximos passos (na pasta criada):")
    print("  git init -b main && git add . && git commit -m \"Atendente WhatsApp IA — case Diego Sales\"")
    print("  gh repo create atendente-whatsapp-ia --public --source=. --push")

if __name__ == "__main__":
    copiar_limpo()
