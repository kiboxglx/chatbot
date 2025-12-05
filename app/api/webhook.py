from fastapi import APIRouter, Request, BackgroundTasks
from app.services.ai_service import BrainService
from app.services.whatsapp_service import WhatsAppService

router = APIRouter()
brain_service = BrainService()
whatsapp_service = WhatsAppService()

def process_message_background(numero_cliente: str, body: str):
    """Processa a mensagem em background para não travar o webhook"""
    try:
        print(f"🔄 Processando mensagem de {numero_cliente} em background...")
        
        # 1. Processar com IA (BrainService)
        contexto = f"Cliente WhatsApp: {numero_cliente}"
        decisao = brain_service.processar_mensagem(body, contexto)
        
        resposta_texto = decisao.get("response_text", "")
        acao = decisao.get("action", "REPLY")

        # 2. Envia a resposta via WPPConnect
        if resposta_texto:
            print(f"📤 Enviando resposta para {numero_cliente}...")
            whatsapp_service.enviar_texto(numero_cliente, resposta_texto)
            print(f"✅ Resposta enviada para {numero_cliente}!")
            
    except Exception as e:
        print(f"❌ Erro no processamento background: {e}")

@router.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook para receber mensagens do WPPConnect Server
    """
    try:
        data = await request.json()
        
        # WPPConnect: Verifica evento
        if data.get("event") != "onMessage":
            return {"status": "ignored", "reason": "Not a message event"}

        message_data = data.get("data", {})
        
        # Ignora mensagens enviadas por mim mesmo (fromMe) e mensagens de grupo (isGroup)
        if message_data.get("fromMe", False) or message_data.get("isGroup", False):
            return {"status": "ignored"}

        # Extrai dados principais
        remote_jid = message_data.get("from", "")
        numero_cliente = remote_jid.replace("@c.us", "")
        
        body = message_data.get("body", "") or message_data.get("content", "")
        
        if not body:
            return {"status": "ignored", "reason": "Empty body"}

        print(f"📩 Mensagem recebida de {numero_cliente}: {body}")

        # --- LÓGICA DO BOT (BACKGROUND) ---
        # Adiciona o processamento na fila de background do FastAPI
        # Isso retorna 200 OK imediatamente para o WPPConnect
        background_tasks.add_task(process_message_background, numero_cliente, body)

        return {"status": "queued", "message": "Processing in background"}

    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return {"status": "error", "details": str(e)}
