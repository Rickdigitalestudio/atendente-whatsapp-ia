"""Login Google 1 vez: python setup_google.py — gera token.pickle"""
from pathlib import Path
print("1) Vá em console.cloud.google.com → ative Google Calendar API")
print("2) Credenciais → OAuth Desktop → baixe como credentials.json nesta pasta")
print("3) Depois rode de novo este script para logar.")
BASE = Path(__file__).parent
cred = BASE / "credentials.json"
if not cred.exists():
    print("FALTANDO credentials.json — siga o passo 2 acima.")
    raise SystemExit(1)
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
flow = InstalledAppFlow.from_client_secrets_file(str(cred), ["https://www.googleapis.com/auth/calendar"])
creds = flow.run_local_server(port=0)
with open(BASE / "token.pickle", "wb") as f:
    pickle.dump(creds, f)
print("OK! token.pickle criado. Agendamentos agora vão para o Google Calendar.")
