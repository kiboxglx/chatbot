# Integração com n8n - Chatbot Contábil

## Credenciais de Acesso

### n8n (Automação)
- **URL**: http://localhost:5678
- **Usuário**: admin
- **Senha**: chatbot2024

### Evolution API (WhatsApp)
- **URL**: http://localhost:8080/manager
- **API Key**: 429683C4C977415CAAFCCE10F7D57E11

### Backend Python (FastAPI)
- **URL**: http://localhost:8000
- **Docs**: http://localhost:8000/docs

## Passo a Passo para Configuração

### 1. Iniciar os Serviços
```bash
docker-compose up -d
```

Aguarde 30 segundos para todos os containers iniciarem.

### 2. Acessar n8n
1. Abra http://localhost:5678
2. Login: admin / chatbot2024
3. Você verá a interface do n8n

### 3. Criar Workflow no n8n

#### Estrutura do Workflow:
```
[Webhook] → [HTTP Request ao Backend] → [Processar Resposta] → [Enviar WhatsApp]
```

#### Configuração Detalhada:

**Node 1: Webhook (Trigger)**
- Tipo: Webhook
- Path: `whatsapp-message`
- Método: POST
- Responder: Immediately

**Node 2: HTTP Request (Chamar Backend Python)**
- Método: POST
- URL: `http://host.docker.internal:8000/webhook`
- Body JSON:
```json
{
  "remoteJid": "{{ $json.body.remoteJid }}",
  "conversation": "{{ $json.body.message }}"
}
```

**Node 3: Processar Resposta**
- Tipo: Code (JavaScript)
- Código:
```javascript
const response = $input.all()[0].json;
return [{
  json: {
    telefone: response.client || "Cliente",
    intencao: response.intent,
    status: response.status
  }
}];
```

**Node 4: Enviar Resposta WhatsApp**
- Tipo: HTTP Request
- Método: POST
- URL: `http://evolution_api:8080/message/sendText/chatbot`
- Headers:
  - `apikey`: `429683C4C977415CAAFCCE10F7D57E11`
- Body JSON:
```json
{
  "number": "{{ $json.telefone }}",
  "text": "Mensagem processada! Intent: {{ $json.intencao }}"
}
```

### 4. Conectar Evolution API ao n8n

No painel da Evolution API:
1. Acesse a instância `chatbot`
2. Vá em **Webhooks**
3. Configure:
   - **URL**: `http://chatbot_n8n:5678/webhook/whatsapp-message`
   - **Events**: `MESSAGES_UPSERT`
   - **Enabled**: ✅

### 5. Testar o Fluxo

Envie uma mensagem para o WhatsApp conectado:
```
Preciso da segunda via do DAS
```

O fluxo será:
1. WhatsApp → Evolution API
2. Evolution API → n8n (webhook)
3. n8n → Backend Python (classificação IA)
4. Backend Python → n8n (resposta)
5. n8n → Evolution API → WhatsApp (mensagem final)

## Estrutura de Dados

### Payload que o n8n recebe da Evolution:
```json
{
  "remoteJid": "5531982119605@s.whatsapp.net",
  "message": "Preciso da segunda via do DAS",
  "pushName": "Nome do Cliente",
  "messageType": "conversation"
}
```

### Payload que o Backend Python espera:
```json
{
  "remoteJid": "5531982119605",
  "conversation": "Preciso da segunda via do DAS"
}
```

### Resposta do Backend Python:
```json
{
  "status": "processed",
  "client": "Empresa Teste Ltda",
  "intent": "2_VIA_BOLETO"
}
```

## Troubleshooting

### n8n não inicia
```bash
docker logs chatbot_n8n
```

### Webhook não recebe dados
- Verifique se a URL do webhook no Evolution está correta
- Teste manualmente: `curl -X POST http://localhost:5678/webhook/whatsapp-message -d '{"test": true}'`

### Backend Python não responde
```bash
# Verificar se está rodando
curl http://localhost:8000

# Ver logs
docker logs -f chatbot_n8n
```

## Próximos Passos

1. ✅ Subir n8n
2. ✅ Criar workflow
3. ✅ Conectar Evolution API
4. ⏳ Testar com WhatsApp real
5. ⏳ Adicionar mais automações (envio de PDF, etc)
