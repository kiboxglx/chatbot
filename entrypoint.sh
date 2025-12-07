#!/bin/sh

# Entrypoint Script para garantir expansão correta da variável PORT
# Se PORT não estiver definida, usa 8000
PORT_TO_USE=${PORT:-8000}

echo "🚀 Iniciando Chatbot na porta $PORT_TO_USE..."
exec uvicorn main:app --host 0.0.0.0 --port $PORT_TO_USE
