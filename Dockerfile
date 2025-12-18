# Imagem base Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para o psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto
COPY . .

# Cria o diretório de storage se não existir
RUN mkdir -p /app/storage/boletos

# Configura Entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Porta (Documentação)
EXPOSE 8000

# Executar via script
CMD ["./entrypoint.sh"]
