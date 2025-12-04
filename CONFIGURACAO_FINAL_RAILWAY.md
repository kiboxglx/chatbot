# GUIA DE CONFIGURAÇÃO FINAL - RAILWAY

## ✅ O QUE JÁ ESTÁ FUNCIONANDO
- ✅ QR Code (Vercel Proxy configurado)
- ✅ Banco de Dados (tabela clientes criada)
- ✅ WhatsApp conectado (estado: open)
- ✅ Webhook configurado na Evolution API

## ⚠️ O QUE FALTA FAZER

### 1. Configurar Variáveis de Ambiente no Railway

Acesse o Railway e configure as variáveis no serviço **chatbot** (backend):

**Variáveis Obrigatórias:**
```
WHATSAPP_API_URL=https://evolution-api-production-e43e.up.railway.app
AUTHENTICATION_API_KEY=123Cartoon*
```

**Variáveis Opcionais (se ainda não tiver):**
```
DATABASE_URL=(Railway configura automaticamente se você adicionou PostgreSQL)
OPENAI_API_KEY=(sua chave da OpenAI)
```

### 2. Como Adicionar no Railway

1. Acesse: https://railway.app
2. Vá no projeto do chatbot
3. Clique no serviço **"chatbot"** (o backend Python)
4. Clique em **"Variables"** no menu lateral
5. Clique em **"+ New Variable"**
6. Adicione cada variável (nome e valor)
7. Clique em **"Deploy"** ou aguarde o redeploy automático

### 3. Verificar Deploy

Após o deploy (leva 1-2 minutos):

1. Execute o diagnóstico:
   ```bash
   py diagnostico_completo.py
   ```

2. Teste enviando uma mensagem para o WhatsApp

### 4. Se Ainda Não Funcionar

Execute este comando para verificar se o backend está usando as variáveis corretas:
```bash
py verificar_config_railway.py
```

## 🎯 RESULTADO ESPERADO

Depois dessas configurações, o bot deve:
- ✅ Receber mensagens via webhook
- ✅ Processar com IA
- ✅ Responder automaticamente no WhatsApp
- ✅ Identificar clientes cadastrados
- ✅ Pausar quando você responder manualmente

## 📞 SUPORTE

Se após configurar ainda não funcionar, verifique:
1. Logs do Railway (aba "Deployments" > clique no deploy > "View Logs")
2. Se o webhook está realmente configurado (já fizemos isso ✅)
3. Se a instância do WhatsApp está conectada (já está ✅)
