@echo off
echo.
echo  Dracarys Chatbot - Desafio 2 InsurMinds
echo  ==========================================

echo  Limpando tunnels antigos na porta 11435...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":11435 "') do taskkill /PID %%a /F >nul 2>&1

echo  Abrindo tunnel SSH para Spark (Ollama)...
start /B "" ssh -L 11435:localhost:11434 -N -o ConnectTimeout=5 dgx-spark 2>nul

timeout /t 3 /nobreak >nul

echo  Testando conexao com Spark...
curl -s http://localhost:11435/api/tags >nul 2>&1 && echo  OK - Ollama respondendo via tunnel || echo  AVISO: servidor nao respondeu - VPN conectada?

echo.
echo  Iniciando Chainlit (chatbot)...
echo  Acesse http://localhost:8000 no seu navegador
echo.

cd /d "%~dp0"
chainlit run app.py
