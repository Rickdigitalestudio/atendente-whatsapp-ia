@echo off
REM Sobe a Evolution API (WhatsApp real). Precisa do Docker Desktop instalado.
echo === Subindo Evolution API (WhatsApp real) ===
docker compose up -d
echo Aguarde 20s e abra http://localhost:8080
echo Depois gere o QR: python conectar_whatsapp.py
pause
