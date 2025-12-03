@echo off
echo ============================================================
echo NGROK - EXPOSICAO DO BACKEND
echo ============================================================
echo.
echo O ngrok esta rodando!
echo.
echo ACESSE: http://localhost:4040
echo.
echo Nessa pagina voce vera a URL publica do seu backend.
echo Exemplo: https://abc123.ngrok.io
echo.
echo COPIE A URL E USE NO N8N:
echo https://SUA-URL-NGROK.ngrok.io/webhook
echo.
echo Pressione qualquer tecla para abrir o painel do ngrok...
pause
start http://localhost:4040
