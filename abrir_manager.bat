@echo off
echo ============================================================
echo ACESSAR EVOLUTION API MANAGER
echo ============================================================
echo.
echo Abrindo o Manager da Evolution API...
echo.
echo Credenciais:
echo URL: http://localhost:8080/manager
echo API Key: 429683C4C977415CAAFCCE10F7D57E11
echo.
echo Aguarde o navegador abrir...
timeout /t 2
start http://localhost:8080/manager
echo.
echo ============================================================
echo INSTRUÇÕES:
echo ============================================================
echo 1. Faça login com a API Key acima
echo 2. Você verá a instância "chatbot"
echo 3. Clique nela para ver o QR Code
echo 4. Escaneie com seu WhatsApp
echo ============================================================
pause
