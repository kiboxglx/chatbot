# Imagem base Python 3.11
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto
COPY . .

# Cria o diretório de storage se não existir
RUN mkdir -p /app/storage/boletos

# Expõe a porta 8000
EXPOSE 8000

# Comando para iniciar o servidor
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
