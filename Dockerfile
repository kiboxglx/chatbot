# Imagem base Python 3.11 (Versão estável e leve)
FROM python:3.11-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Instala dependências do sistema necessárias para compilar pacotes Python (como psycopg2 e outros)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o requirements.txt primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Atualiza o pip e instala as dependências do projeto
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto
COPY . .

# Garante que o diretório de storage existe
RUN mkdir -p /app/storage/boletos

# Define a porta padrão (Railway injeta a variável PORT, mas aqui expomos por documentação)
EXPOSE 8000

# Comando para iniciar a aplicação usando uvicorn diretamente
# Usamos a variável de ambiente $PORT injetada pela Railway
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
