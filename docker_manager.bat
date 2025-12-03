@echo off
chcp 65001 >nul
echo ========================================
echo 🐳 DOCKER COMPOSE - CHATBOT CONTÁBIL
echo ========================================
echo.

:menu
echo Escolha uma opção:
echo.
echo [1] 🚀 Iniciar todos os serviços
echo [2] 🛑 Parar todos os serviços
echo [3] 📊 Ver status dos containers
echo [4] 📝 Ver logs (todos)
echo [5] 📝 Ver logs do Chatbot
echo [6] 📝 Ver logs da Evolution API
echo [7] 📝 Ver logs do n8n
echo [8] 🔄 Reiniciar o Chatbot
echo [9] 🔨 Reconstruir o Chatbot
echo [10] 🧪 Testar conectividade
echo [11] 🗑️ Limpar tudo (CUIDADO!)
echo [0] ❌ Sair
echo.

set /p opcao="Digite o número da opção: "

if "%opcao%"=="1" goto iniciar
if "%opcao%"=="2" goto parar
if "%opcao%"=="3" goto status
if "%opcao%"=="4" goto logs_todos
if "%opcao%"=="5" goto logs_chatbot
if "%opcao%"=="6" goto logs_evolution
if "%opcao%"=="7" goto logs_n8n
if "%opcao%"=="8" goto reiniciar
if "%opcao%"=="9" goto rebuild
if "%opcao%"=="10" goto testar
if "%opcao%"=="11" goto limpar
if "%opcao%"=="0" goto sair

echo Opção inválida!
pause
cls
goto menu

:iniciar
echo.
echo 🚀 Iniciando todos os serviços...
docker-compose up -d
echo.
echo ✅ Serviços iniciados!
echo.
echo Acesse:
echo - Chatbot API: http://localhost:8000/docs
echo - n8n: http://localhost:5678
echo - Evolution API: http://localhost:8080
echo.
pause
cls
goto menu

:parar
echo.
echo 🛑 Parando todos os serviços...
docker-compose down
echo ✅ Serviços parados!
pause
cls
goto menu

:status
echo.
echo 📊 Status dos containers:
docker-compose ps
echo.
pause
cls
goto menu

:logs_todos
echo.
echo 📝 Logs de todos os serviços (Ctrl+C para sair):
docker-compose logs -f
cls
goto menu

:logs_chatbot
echo.
echo 📝 Logs do Chatbot (Ctrl+C para sair):
docker-compose logs -f chatbot
cls
goto menu

:logs_evolution
echo.
echo 📝 Logs da Evolution API (Ctrl+C para sair):
docker-compose logs -f evolution-api
cls
goto menu

:logs_n8n
echo.
echo 📝 Logs do n8n (Ctrl+C para sair):
docker-compose logs -f n8n
cls
goto menu

:reiniciar
echo.
echo 🔄 Reiniciando o Chatbot...
docker-compose restart chatbot
echo ✅ Chatbot reiniciado!
pause
cls
goto menu

:rebuild
echo.
echo 🔨 Reconstruindo o Chatbot...
docker-compose up -d --build chatbot
echo ✅ Chatbot reconstruído!
pause
cls
goto menu

:testar
echo.
echo 🧪 Testando conectividade...
echo.
echo Entrando no container do chatbot...
docker exec -it chatbot_backend python test_docker_network.py
echo.
pause
cls
goto menu

:limpar
echo.
echo ⚠️ ATENÇÃO: Isso vai APAGAR TODOS OS DADOS!
set /p confirma="Tem certeza? (S/N): "
if /i "%confirma%"=="S" (
    echo.
    echo 🗑️ Limpando tudo...
    docker-compose down -v
    docker system prune -a -f
    echo ✅ Tudo limpo!
) else (
    echo ❌ Operação cancelada.
)
pause
cls
goto menu

:sair
echo.
echo 👋 Até logo!
exit
