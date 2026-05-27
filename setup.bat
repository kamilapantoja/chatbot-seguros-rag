@echo off
echo.
echo  Setup do Dracarys Chatbot
echo  ===========================
echo.

cd /d "%~dp0"

if not exist ".venv" (
    echo  Criando virtual environment...
    python -m venv .venv
)

echo  Ativando venv e instalando dependencias...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo  Setup concluido. Proximos passos:
echo    1. Aguardar gemma2:27b terminar download na Spark
echo    2. Rodar: python ingest.py (popula o Chroma)
echo    3. Rodar: start_chatbot.bat (sobe o Chainlit)
echo.
pause
