# 🎯 PASSO 5: RESPOSTA E TRATAMENTO DE ERROS

## 1. NÓ DE RESPOSTA UNIFICADO

### Configuração no n8n:

**Node: HTTP Request (Enviar WhatsApp)**
- **Method**: POST
- **URL**: `http://evolution_api:8080/message/sendText/chatbot`
- **Headers**:
  ```
  apikey: 429683C4C977415CAAFCCE10F7D57E11
  Content-Type: application/json
  ```
- **Body (JSON)**:
  ```json
  {
    "number": "{{ $json.remoteJid || $json.body.key.remoteJid.replace('@s.whatsapp.net', '') }}",
    "text": "{{ $json.responseMessage || $json.message }}"
  }
  ```

### Formatação Markdown WhatsApp:

A IA deve formatar as respostas usando:
- **Negrito**: `*texto*`
- **Itálico**: `_texto_`
- **Tachado**: `~texto~`
- **Monoespaçado**: `` `texto` ``

**Exemplo de resposta formatada:**
```
✅ *Gasto salvo com sucesso!*

📊 *Detalhes:*
• Valor: *R$ 45,90*
• Estabelecimento: _Supermercado ABC_
• Data: 01/12/2025
• Categoria: Alimentação

_Registrado em 01/12/2025 às 19:00_
```

---

## 2. TRATAMENTO DE ERROS

### Arquitetura de Error Handling:

```
Qualquer Node
    ↓ (em caso de erro)
Error Trigger
    ↓
HTTP Request → /error/handle
    ↓
Enviar Resposta WhatsApp (Fallback)
```

### Configuração no n8n:

#### A. Adicionar Error Trigger:

1. **Em cada node crítico**, clique em "Settings" (⚙️)
2. Ative **"Continue On Fail"**
3. Conecte a saída de erro a um node "Error Trigger"

#### B. Node Error Trigger:

```json
{
  "name": "Error Handler",
  "type": "n8n-nodes-base.errorTrigger",
  "position": [x, y]
}
```

#### C. Node HTTP Request (Error Handler):

- **Method**: POST
- **URL**: `http://host.docker.internal:8000/error/handle`
- **Body**:
  ```json
  {
    "remoteJid": "{{ $json.remoteJid }}",
    "error_type": "{{ $json.error.name || 'default' }}",
    "error_message": "{{ $json.error.message || '' }}"
  }
  ```

### Tipos de Erro Suportados:

| Tipo | Quando Ocorre | Mensagem |
|------|---------------|----------|
| `image_processing` | Falha ao processar imagem | Pede foto mais nítida |
| `pdf_processing` | Falha ao ler PDF | Sugere enviar imagem |
| `sheets_error` | Erro ao salvar no Sheets | Pede para tentar novamente |
| `ai_error` | IA não conseguiu processar | Pede reformulação |
| `timeout` | Processamento demorou muito | Pede nova tentativa |
| `default` | Qualquer outro erro | Mensagem genérica |

---

## 3. RESPOSTA ASSÍNCRONA (Evitar Timeout)

### Problema:
WhatsApp espera resposta em até 30 segundos. Se a IA demorar mais, o webhook dá timeout.

### Solução: Resposta Imediata + Processamento Assíncrono

#### No n8n:

**Opção A: Respond to Webhook (Recomendado)**

1. Logo após o node "Webhook", adicione:
   ```
   Node: Respond to Webhook
   - Response Code: 200
   - Response Body: {"status": "processing"}
   ```

2. Continue o fluxo normalmente (IA, Sheets, etc)

3. No final, envie a resposta real via Evolution API

**Fluxo Correto:**
```
Webhook
    ↓
Respond to Webhook (200 OK imediato)
    ↓
[Processamento IA - pode demorar]
    ↓
Salvar no Sheets
    ↓
Enviar Resposta WhatsApp (assíncrono)
```

#### No Backend Python (Alternativa):

Se preferir controlar pelo backend:

```python
from fastapi import BackgroundTasks

@router.post("/webhook")
async def webhook(request: WebhookRequest, background_tasks: BackgroundTasks):
    # Responde imediatamente
    background_tasks.add_task(process_message, request)
    return {"status": "processing"}

async def process_message(request):
    # Processa a IA (pode demorar)
    # Salva no Sheets
    # Envia resposta via Evolution API
    pass
```

---

## 4. CONFIGURAÇÃO COMPLETA DO FLUXO

### Estrutura Final do Workflow n8n:

```
1. Webhook (Recebe mensagem)
    ↓
2. Respond to Webhook (200 OK)
    ↓
3. Switch (Tipo de mensagem)
    ├─→ Imagem → Processar Imagem
    ├─→ PDF → Processar PDF
    └─→ Texto → Processar Texto
    ↓
4. HTTP Request (Backend Python)
    ↓
5. Google Sheets (Salvar)
    ↓
6. HTTP Request (Enviar WhatsApp)

[Error Trigger conectado em todos os nodes]
    ↓
Error Handler
    ↓
HTTP Request (Error Endpoint)
    ↓
Enviar Resposta WhatsApp (Fallback)
```

---

## 5. CHECKLIST DE PRODUÇÃO

### Antes de ir para produção:

- [ ] Todos os nodes têm "Continue On Fail" ativado
- [ ] Error Trigger está conectado
- [ ] Webhook responde imediatamente (200 OK)
- [ ] Timeout configurado (30s máximo por node)
- [ ] Mensagens de erro são amigáveis
- [ ] Logs estão sendo salvos
- [ ] Teste com imagens borradas
- [ ] Teste com PDFs corrompidos
- [ ] Teste com Google Sheets offline
- [ ] Teste com mensagens inválidas

---

## 6. EXEMPLO DE IMPLEMENTAÇÃO

### JSON Completo do Node de Resposta:

```json
{
  "nodes": [
    {
      "parameters": {
        "method": "POST",
        "url": "http://evolution_api:8080/message/sendText/chatbot",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            {
              "name": "apikey",
              "value": "429683C4C977415CAAFCCE10F7D57E11"
            }
          ]
        },
        "sendBody": true,
        "bodyContentType": "json",
        "jsonBody": "={\n  \"number\": \"{{ $json.remoteJid }}\",\n  \"text\": \"{{ $json.responseMessage }}\"\n}",
        "options": {
          "timeout": 10000
        }
      },
      "name": "Enviar Resposta WhatsApp",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [1200, 300],
      "onError": "continueErrorOutput"
    }
  ]
}
```

---

## 7. MONITORAMENTO E LOGS

### Adicionar Logging:

No backend Python, adicione logs detalhados:

```python
import logging

logger = logging.getLogger(__name__)

@router.post("/webhook")
async def webhook(request: WebhookRequest):
    logger.info(f"Mensagem recebida de {request.remoteJid}")
    
    try:
        # Processamento
        logger.info("Processamento iniciado")
        result = await process_ai(request.conversation)
        logger.info(f"IA retornou: {result}")
        
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        raise
```

### Visualizar Logs:

```bash
# Docker
docker logs chatbot_n8n -f

# Python
tail -f app.log
```

---

## ENTREGÁVEIS DO PASSO 5:

✅ **Arquivo**: `n8n-response-node.json` - Configuração do node de resposta
✅ **Arquivo**: `app/api/error_handler.py` - Endpoint de tratamento de erros
✅ **Documentação**: Este guia completo

### Próximos Passos:

1. Importe o node de resposta no n8n
2. Configure o Error Trigger
3. Teste com mensagens inválidas
4. Monitore os logs
5. Ajuste as mensagens de erro conforme necessário

---

**Dúvidas ou precisa de ajuda para implementar?**
