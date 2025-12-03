# 🐳 Guia Docker Compose - Chatbot Contábil

## 📋 Pré-requisitos

- Docker Desktop instalado
- Docker Compose instalado (geralmente vem com o Docker Desktop)

## 🚀 Como Usar

### 1. Configurar Variáveis de Ambiente

Edite o arquivo `.env` e adicione sua chave da OpenAI:

```bash
OPENAI_API_KEY=sk-proj-sua_chave_aqui
```

### 2. Iniciar Todos os Serviços

```bash
docker-compose up -d
```

Este comando irá:
- ✅ Criar a rede `chatbot_network`
- ✅ Baixar as imagens necessárias
- ✅ Construir o container do chatbot
- ✅ Iniciar todos os serviços

### 3. Verificar Status dos Containers

```bash
docker-compose ps
```

Você deve ver 5 containers rodando:
- `chatbot_backend` (porta 8000)
- `chatbot_n8n` (porta 5678)
- `evolution_api` (porta 8080)
- `evolution_postgres`
- `evolution_redis`

### 4. Acessar os Serviços

- **Chatbot API**: http://localhost:8000/docs
- **n8n**: http://localhost:5678 (user: admin, pass: chatbot2024)
- **Evolution API**: http://localhost:8080

### 5. Ver Logs

Ver logs de todos os serviços:
```bash
docker-compose logs -f
```

Ver logs de um serviço específico:
```bash
docker-compose logs -f chatbot
docker-compose logs -f evolution-api
docker-compose logs -f n8n
```

### 6. Testar Conectividade Entre Containers

Entre no container do n8n:
```bash
docker exec -it chatbot_n8n /bin/sh
```

Teste a conexão com a Evolution API:
```bash
curl http://evolution-api:8080
```

Teste a conexão com o Chatbot:
```bash
curl http://chatbot:8000/health
```

### 7. Parar os Serviços

```bash
docker-compose down
```

Para parar E remover os volumes (⚠️ apaga dados):
```bash
docker-compose down -v
```

## 🔧 Comandos Úteis

### Reiniciar um Serviço Específico

```bash
docker-compose restart chatbot
docker-compose restart evolution-api
```

### Reconstruir o Container do Chatbot

Se você alterou o código:
```bash
docker-compose up -d --build chatbot
```

### Ver Uso de Recursos

```bash
docker stats
```

## 🌐 Comunicação Entre Containers

Dentro da rede `chatbot_network`, os containers se comunicam pelos **nomes dos serviços**:

- `chatbot` → `http://chatbot:8000`
- `evolution-api` → `http://evolution-api:8080`
- `n8n` → `http://n8n:5678`
- `postgres` → `postgres:5432`
- `redis` → `redis:6379`

## 📝 Configuração do n8n

No n8n, ao configurar webhooks HTTP para a Evolution API, use:

```
http://evolution-api:8080/message/sendText/chatbot
```

**NÃO use** `http://localhost:8080` dentro do n8n!

## 🐛 Troubleshooting

### Container não inicia

```bash
docker-compose logs chatbot
```

### Erro de rede

```bash
docker network ls
docker network inspect chatbot_chatbot_network
```

### Limpar tudo e recomeçar

```bash
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

## 📂 Estrutura de Volumes

Os dados persistentes ficam em:

- `n8n_data`: Workflows e configurações do n8n
- `evolution_instances`: Sessões do WhatsApp
- `evolution_store`: Arquivos da Evolution API
- `evolution_pgdata`: Banco PostgreSQL
- `evolution_redis_data`: Cache Redis
- `./storage`: Boletos e arquivos do chatbot (mapeado do host)
- `./contabilidade.db`: Banco SQLite do chatbot (mapeado do host)

## ✅ Checklist de Validação

- [ ] Todos os containers estão rodando (`docker-compose ps`)
- [ ] n8n acessível em http://localhost:5678
- [ ] Evolution API acessível em http://localhost:8080
- [ ] Chatbot API acessível em http://localhost:8000/docs
- [ ] Teste de conectividade entre containers OK
- [ ] Logs sem erros críticos
