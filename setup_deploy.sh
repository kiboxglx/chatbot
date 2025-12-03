#!/bin/bash

# Script de Instalação Automática para Deploy (Ubuntu 22.04)
# Uso: chmod +x setup_deploy.sh && ./setup_deploy.sh

echo "🚀 Iniciando Setup do Chatbot Contábil..."

# 1. Atualizar Sistema
echo "📦 Atualizando pacotes..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Instalar Docker e Docker Compose
echo "🐳 Instalando Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker instalado!"
else
    echo "✅ Docker já estava instalado."
fi

# 3. Clonar Repositório (se não existir)
echo "🐙 Verificando repositório..."
if [ ! -d "chatbot" ]; then
    git clone https://github.com/kiboxglx/chatbot.git
    echo "✅ Repositório clonado!"
else
    echo "ℹ️ Pasta 'chatbot' já existe. Pulando clone."
fi

# 4. Entrar na pasta
cd chatbot

# 5. Criar .env se não existir
if [ ! -f ".env" ]; then
    echo "⚠️ Arquivo .env não encontrado!"
    echo "Crie o arquivo .env com suas credenciais antes de rodar o docker-compose."
    echo "Exemplo: cp .env.example .env"
    # cp .env.example .env (opcional, se tiver example)
fi

echo "---------------------------------------------------"
echo "🎉 Setup finalizado!"
echo "PRÓXIMOS PASSOS:"
echo "1. Entre na pasta: cd chatbot"
echo "2. Edite o .env: nano .env (Cole suas chaves API)"
echo "3. Suba o sistema: docker compose up -d --build"
echo "---------------------------------------------------"
