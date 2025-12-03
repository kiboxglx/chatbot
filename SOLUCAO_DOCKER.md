# 🔧 SOLUÇÃO: Conectividade Docker - n8n ↔ Evolution API

## ❌ PROBLEMA IDENTIFICADO

O `docker-compose.yml` original **NÃO tinha uma rede compartilhada** definida. Isso causava:

- ❌ n8n não conseguia acessar `http://evolution_api:8080`
- ❌ Erro: "Could not resolve host: evolution_api"
- ❌ Cada container ficava em uma rede isolada

## ✅ SOLUÇÃO IMPLEMENTADA

### 1. Rede Compartilhada

```yaml
networks:
  chatbot_network:
    driver: bridge
```

Todos os serviços agora estão na mesma rede:

```yaml
services:
  chatbot:
    networks:
      - chatbot_network
  
  n8n:
    networks:
      - chatbot_network
  
  evolution-api:
    networks:
      - chatbot_network
```

### 2. Comunicação Interna

Agora os containers se comunicam pelos **nomes dos serviços**:

| De → Para | URL Interna |
|-----------|-------------|
| n8n → Evolution API | `http://evolution-api:8080` |
| n8n → Chatbot | `http://chatbot:8000` |
| Chatbot → Evolution API | `http://evolution-api:8080` |

### 3. Novo Serviço: Chatbot FastAPI

Adicionado o serviço do chatbot ao Docker Compose:

```yaml
chatbot:
  build: .
  container_name: chatbot_backend
  ports:
    - "8000:8000"
  environment:
    - WHATSAPP_API_URL=http://evolution-api:8080  # ← Nome do container!
  networks:
    - chatbot_network
  depends_on:
    - evolution-api
```

## 📋 ARQUIVOS CRIADOS/MODIFICADOS

### ✅ Modificados

1. **`docker-compose.yml`**
   - ✅ Adicionada rede `chatbot_network`
   - ✅ Todos os serviços conectados à rede
   - ✅ Adicionado serviço `chatbot`

2. **`.env`**
   - ✅ `WHATSAPP_API_URL=http://evolution-api:8080` (nome do container)
   - ✅ Adicionada `OPENAI_API_KEY`

### 🆕 Criados

3. **`Dockerfile`** - Para containerizar o FastAPI
4. **`DOCKER_GUIDE.md`** - Guia completo de uso
5. **`docker_manager.bat`** - Menu interativo Windows
6. **`test_docker_network.py`** - Script de validação

## 🚀 COMO USAR

### Opção 1: Menu Interativo (Recomendado)

```bash
docker_manager.bat
```

### Opção 2: Comandos Manuais

```bash
# Iniciar tudo
docker-compose up -d

# Ver status
docker-compose ps

# Ver logs
docker-compose logs -f

# Testar conectividade
docker exec -it chatbot_backend python test_docker_network.py
```

## 🧪 VALIDAÇÃO

### Teste 1: Verificar Rede

```bash
docker network inspect chatbot_chatbot_network
```

Deve mostrar todos os containers conectados.

### Teste 2: Ping Entre Containers

Entre no n8n:
```bash
docker exec -it chatbot_n8n /bin/sh
```

Teste:
```bash
curl http://evolution-api:8080
curl http://chatbot:8000/health
```

### Teste 3: Script Automático

```bash
docker exec -it chatbot_backend python test_docker_network.py
```

## 📊 ARQUITETURA FINAL

```
┌─────────────────────────────────────────────────┐
│         chatbot_network (bridge)                │
│                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │   n8n    │   │ Chatbot  │   │Evolution │   │
│  │  :5678   │◄─►│  :8000   │◄─►│   API    │   │
│  │          │   │          │   │  :8080   │   │
│  └──────────┘   └──────────┘   └──────────┘   │
│                                                 │
│  ┌──────────┐   ┌──────────┐                   │
│  │PostgreSQL│   │  Redis   │                   │
│  │  :5432   │   │  :6379   │                   │
│  └──────────┘   └──────────┘                   │
└─────────────────────────────────────────────────┘
```

## ⚠️ IMPORTANTE: Configuração do n8n

No n8n, ao criar workflows que chamam a Evolution API, use:

✅ **CORRETO (dentro do Docker):**
```
http://evolution-api:8080/message/sendText/chatbot
```

❌ **ERRADO:**
```
http://localhost:8080/message/sendText/chatbot
http://evolution_api:8080/message/sendText/chatbot  (underscore)
```

## 🎯 PRÓXIMOS PASSOS

1. ✅ Configurar `OPENAI_API_KEY` no `.env`
2. ✅ Executar `docker-compose up -d`
3. ✅ Validar conectividade
4. ✅ Configurar workflows no n8n
5. ✅ Testar fluxo completo do chatbot

## 📞 TROUBLESHOOTING

### Erro: "Could not resolve host"

**Causa:** Container não está na rede `chatbot_network`

**Solução:**
```bash
docker-compose down
docker-compose up -d
docker network inspect chatbot_chatbot_network
```

### Erro: "Connection refused"

**Causa:** Serviço não está rodando

**Solução:**
```bash
docker-compose ps
docker-compose logs evolution-api
docker-compose restart evolution-api
```

### Erro: "No such container"

**Causa:** Containers não foram criados

**Solução:**
```bash
docker-compose up -d --build
```

---

**✅ PROBLEMA RESOLVIDO!** Agora todos os containers podem se comunicar internamente. 🎉
