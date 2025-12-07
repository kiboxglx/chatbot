from fastapi import APIRouter, Request, BackgroundTasks
from app.services.ai_service import BrainService
from app.services.whatsapp_service import WhatsAppService
import json

router = APIRouter()
brain_service = BrainService()
whatsapp_service = WhatsAppService()

def process_message_background(numero_cliente: str, body: str, media_url: str = None):
    """Processa a mensagem em background para não travar o webhook"""
    try:
        print(f"🔄 [Background] Processando mensagem de {numero_cliente}...")
        
        # 1. Processar com IA (BrainService)
        contexto = f"Cliente WhatsApp: {numero_cliente}"
        # Se tiver media, a lógica muda (futuro), por enquanto vamos de texto
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
    Webhook para receber mensagens do WAHA (Compatibilidade Estrita)
    """
    try:
        raw_body = await request.body()
        data = json.loads(raw_body)
        
        # Logar o payload bruto para debug (Temporário)
        # print(f"📥 [Webhook RAW] {data}") 
        
        # Validação Básica WAHA
        event = data.get("event")
        if not event:
            return {"status": "ignored", "reason": "No event field"}

        # WAHA envia 'message' e 'message.any'. Se ouvirmos os dois, processamos duplicado.
        # Vamos restringir apenas para 'message' que é o evento principal.
        if event != "message":
            return {"status": "ignored", "reason": f"Event {event} ignored (duplicate prevention)"}

        # Extrai payload
        payload = data.get("payload", {})
        
        # Verificações de segurança
        if payload.get("fromMe", False):
            # print("⛔ Ignorando mensagem enviada por mim (fromMe=True)")
            return {"status": "ignored", "reason": "fromMe"}
            
        # Extração de dados
        remote_jid = payload.get("from", "") # Ex: 551199999999@c.us
        if not remote_jid:
            return {"status": "error", "reason": "No 'from' field"}
            
        chat_id = remote_jid.replace("@c.us", "")
        
        # WAHA envia o texto no campo 'body'
        message_body = payload.get("body", "")
        
        if not message_body:
             # Pode ser mídia ou sticker
             # print(f"⚠️ Mensagem sem corpo de texto de {chat_id}")
             return {"status": "ignored", "reason": "Empty body"}

        print(f"📩 MENSAGEM RECEBIDA [{chat_id}]: {message_body}")

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
