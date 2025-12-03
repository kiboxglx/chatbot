# 🎯 GUIA: n8n LOCAL - Chatbot Contábil

## 📋 Passo a Passo

### 1. Acessar n8n Local

Abra seu navegador em:
```
http://localhost:5678
```

**Credenciais (primeira vez):**
- Email: admin@chatbot.local
- Senha: chatbot2024

### 2. Importar Workflow

1. No n8n, clique em **"Workflows"** (menu lateral)
2. Clique em **"Import from File"**
3. Selecione o arquivo: `n8n-workflow-local.json`
4. O workflow será carregado

### 3. Ativar Workflow

1. Abra o workflow importado
2. Clique no toggle **"Inactive"** → **"Active"** (canto superior direito)
3. O workflow ficará verde

### 4. Copiar URL do Webhook

1. Clique no node **"Webhook WhatsApp"**
2. Copie a **Production URL**
3. Será algo como: `http://localhost:5678/webhook/whatsapp`

### 5. Atualizar Webhook na Evolution API

1. Acesse: http://localhost:8080/manager
2. Faça login com API Key: `429683C4C977415CAAFCCE10F7D57E11`
3. Clique na instância **"chatbot"**
4. Vá em **"Webhook"**
5. Configure:
   - **URL**: `http://chatbot_n8n:5678/webhook/whatsapp`
   - **Events**: Marque `MESSAGES_UPSERT` ou `messages.upsert`
   - **Enabled**: ✅

6. Salve

## 🔄 Fluxo Completo (Local)

```
WhatsApp
    ↓
Evolution API (localhost:8080)
    ↓
n8n Local (localhost:5678)
    ↓
Backend Python (localhost:8000)
    ↓
Gemini AI
    ↓
n8n Local
    ↓
Evolution API
    ↓
WhatsApp (Resposta)
```

## ✅ Vantagens do n8n Local

- ✅ Não precisa de ngrok
- ✅ Mais rápido (tudo local)
- ✅ Sem limites de requisições
- ✅ Acesso direto à Evolution API
- ✅ Mais fácil de debugar

## 🧪 Testar

Envie mensagem do WhatsApp:
```
Preciso da segunda via do DAS
```

Você deve receber:
```
✅ Mensagem processada!

Cliente: Empresa Teste Ltda
Intenção: 2_VIA_BOLETO
```

## 🔧 URLs Importantes

- **n8n Local**: http://localhost:5678
- **Evolution Manager**: http://localhost:8080/manager
- **Backend Python**: http://localhost:8000
- **Backend Docs**: http://localhost:8000/docs

## ⚠️ Observações

### Webhook URL no Evolution:

Use `http://chatbot_n8n:5678/webhook/whatsapp` (nome do container Docker)

**NÃO use** `http://localhost:5678` porque a Evolution API está em outro container.

### Backend URL no n8n:

Use `http://host.docker.internal:8000/webhook`

Isso permite o n8n (Docker) acessar o backend (sua máquina).

## 🆘 Troubleshooting

### n8n não inicia:
```bash
docker-compose restart n8n
docker logs chatbot_n8n
```

### Webhook não funciona:
- Verifique se workflow está **Active**
- Teste manualmente: `curl -X POST http://localhost:5678/webhook/whatsapp -d '{"test": true}'`

### Evolution não chama webhook:
- Use `http://chatbot_n8n:5678` (nome do container)
- Verifique se está na mesma rede Docker

## 📊 Monitorar Execuções

No n8n:
1. Clique em **"Executions"** (menu lateral)
2. Veja todas as execuções do workflow
3. Clique em uma para ver detalhes

---

**Pronto! Agora tudo está rodando localmente sem depender de serviços externos!**
