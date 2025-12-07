from fastapi import APIRouter, Request, BackgroundTasks
from app.services.ai_service import BrainService
from app.services.whatsapp_service import WhatsAppService
import json
import time

router = APIRouter()
brain_service = BrainService()
whatsapp_service = WhatsAppService()

# --- Cache de Idempotência em Memória ---
# Estrutura: {message_id: timestamp_processamento}
processed_messages = {}
CACHE_TTL = 300  # 5 minutos em segundos

def clean_cache():
    """Remove mensagens antigas do cache para liberar memória"""
    now = time.time()
    # Cria lista de keys para deletar (não pode iterar e deletar ao mesmo tempo)
    to_remove = [mid for mid, ts in processed_messages.items() if now - ts > CACHE_TTL]
    for mid in to_remove:
        del processed_messages[mid]

def process_message_background(numero_cliente: str, body: str, media_url: str = None):
    """Processa a mensagem em background para não travar o webhook"""
    try:
        print(f"🔄 [Background] Processando mensagem de {numero_cliente}...")
        
        # 1. Processar com IA (BrainService)
        contexto = f"Cliente WhatsApp: {numero_cliente}"
        decisao = brain_service.processar_mensagem(body, contexto)
        
        resposta_texto = decisao.get("response_text", "")
        acao = decisao.get("action", "REPLY")

        print(f"🧠 Decisão da IA: {acao}")

        # 2. Envia a resposta via WAHA
        if resposta_texto:
            print(f"📤 Enviando resposta para {numero_cliente}...")
            whatsapp_service.enviar_texto(numero_cliente, resposta_texto)
            print(f"✅ [Background] Ciclo concluído para {numero_cliente}!")
        else:
            print("⚠️ A IA não gerou resposta de texto.")
            
    except Exception as e:
        print(f"❌ Erro no processamento background: {e}")
        import traceback
        traceback.print_exc()

@router.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook para receber mensagens do WAHA com Proteção de Duplicidade (Idempotência)
    """
    try:
        raw_body = await request.body()
        data = json.loads(raw_body)
        
        # Validação Básica WAHA
        event = data.get("event")
        if not event:
            return {"status": "ignored", "reason": "No event field"}

        # WAHA envia 'message' e 'message.any'. Vamos restringir para 'message'.
        if event != "message":
            return {"status": "ignored", "reason": f"Event {event} ignored"}

        # Extrai payload
        payload = data.get("payload", {})
        
        # 1. Verificação de ID Único da Mensagem (Idempotência)
        message_id = payload.get("id")
        if not message_id:
            return {"status": "error", "reason": "No message ID"}

        # Limpeza preguiçosa do cache antes de verificar
        clean_cache()

        if message_id in processed_messages:
            print(f"⛔ Mensagem {message_id} ignorada (Duplicada)")
            return {"status": "ignored", "reason": "Duplicate message"}

        # Adiciona ao cache IMEDIATAMENTE antes de processar
        processed_messages[message_id] = time.time()

        # Verificações de segurança
        if payload.get("fromMe", False):
            # Mesmo mensagem enviada por mim tem ID, então já foi cacheada acima, 
            # mas retornamos ignored aqui por lógica de negócio
            return {"status": "ignored", "reason": "fromMe"}
            
        # Extração de dados
        remote_jid = payload.get("from", "") # Ex: 551199999999@c.us
        if not remote_jid:
            return {"status": "error", "reason": "No 'from' field"}
            
        chat_id = remote_jid.replace("@c.us", "")
        message_body = payload.get("body", "")
        
        if not message_body:
             return {"status": "ignored", "reason": "Empty body"}

        print(f"📩 MENSAGEM RECEBIDA [{chat_id}] (ID: {message_id}): {message_body}")

        # Enfileirar processamento
        background_tasks.add_task(process_message_background, chat_id, message_body)

        return {"status": "queued"}

    except json.JSONDecodeError:
        print("❌ Erro: Webhook recebeu payload que não é JSON válido")
        return {"status": "error", "reason": "Invalid JSON"}
    except Exception as e:
        print(f"❌ Erro genérico no webhook: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "details": str(e)}
