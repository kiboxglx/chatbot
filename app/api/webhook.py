from fastapi import APIRouter, Request
from app.services.ai_service import BrainService
from app.services.whatsapp_service import WhatsAppService

router = APIRouter()
brain_service = BrainService()
whatsapp_service = WhatsAppService()

@router.post("/webhook")
async def webhook(request: Request):
    """
    Webhook para receber mensagens do WPPConnect Server
    """
    try:
        data = await request.json()
        
        # WPPConnect: Verifica evento
        # O evento principal de mensagem é 'onMessage'
        if data.get("event") != "onMessage":
            return {"status": "ignored", "reason": "Not a message event"}

        message_data = data.get("data", {})
        
        # Ignora mensagens enviadas por mim mesmo (fromMe) e mensagens de grupo (isGroup)
        if message_data.get("fromMe", False) or message_data.get("isGroup", False):
            return {"status": "ignored"}

        # Extrai dados principais
        # WPPConnect usa 'from' para o remetente (ex: 5511999999999@c.us)
        remote_jid = message_data.get("from", "")
        # Remove o sufixo @c.us para ficar só o número limpo
        numero_cliente = remote_jid.replace("@c.us", "")
        
        body = message_data.get("body", "") or message_data.get("content", "")
        
        if not body:
            return {"status": "ignored", "reason": "Empty body"}

        print(f"📩 Mensagem recebida de {numero_cliente}: {body}")

        # --- LÓGICA DO BOT ---
        
        # 1. Processar com IA (BrainService)
        contexto = f"Cliente WhatsApp: {numero_cliente}"
        
        # O método processar_mensagem retorna um dict com 'response_text' e 'action'
        decisao = brain_service.processar_mensagem(body, contexto)
        
        resposta_texto = decisao.get("response_text", "")
        acao = decisao.get("action", "REPLY")

        # 2. Envia a resposta via WPPConnect
        if resposta_texto:
            whatsapp_service.enviar_texto(numero_cliente, resposta_texto)

        return {"status": "processed", "action": acao}

    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        # Retorna 200 mesmo com erro para o WPPConnect não ficar tentando reenviar infinitamente
        return {"status": "error", "details": str(e)}
