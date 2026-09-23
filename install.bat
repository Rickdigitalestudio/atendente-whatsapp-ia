@echo off
REM Instalador Windows — 1 clique
echo === Atendente WhatsApp IA — instalando ===
python --version || (echo Instale o Python 3.11+ em python.org e rode de novo & pause & exit)
if not exist .env copy .env.example .env
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo OK! Agora edite o .env (chave Gemini/OpenAI) e o config\config.json (nome, precos).
echo Depois rode start.bat
pause
