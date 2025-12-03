"""
Error Handler para o Chatbot
Gerencia erros e envia mensagens de fallback
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ErrorRequest(BaseModel):
    remoteJid: str
    error_type: str
    error_message: str = ""

@router.post("/error/handle")
async def handle_error(request: ErrorRequest):
    """
    Endpoint para tratar erros do fluxo e gerar mensagens de fallback
    """
    logger.error(f"Erro no fluxo: {request.error_type} - {request.error_message}")
    
    # Mensagens de erro personalizadas
    error_messages = {
        "image_processing": "⚠️ *Ops!* Não consegui processar sua imagem.\n\n"
                           "Por favor, tente:\n"
                           "• Enviar uma foto mais nítida\n"
                           "• Verificar se o texto está legível\n"
                           "• Ou digite manualmente os dados do gasto",
        
        "pdf_processing": "⚠️ *Problema com o PDF*\n\n"
                         "Não consegui ler o arquivo. Tente:\n"
                         "• Enviar uma imagem ao invés do PDF\n"
                         "• Ou digite os dados manualmente",
        
        "sheets_error": "⚠️ *Erro ao salvar*\n\n"
                       "Tive um problema técnico ao salvar seu gasto.\n"
                       "Por favor, tente novamente em alguns instantes.",
        
        "ai_error": "⚠️ *Não entendi*\n\n"
                   "Não consegui processar sua mensagem.\n"
                   "Pode reformular ou enviar uma foto do comprovante?",
        
        "timeout": "⏱️ *Tempo esgotado*\n\n"
                  "O processamento demorou muito.\n"
                  "Por favor, tente novamente.",
        
        "default": "⚠️ *Erro técnico*\n\n"
                  "Tive um problema para processar seu pedido.\n"
                  "Tente novamente ou entre em contato com o suporte."
    }
    
    # Seleciona a mensagem apropriada
    message = error_messages.get(request.error_type, error_messages["default"])
    
    # Adiciona detalhes se houver
    if request.error_message:
        message += f"\n\n_Detalhes técnicos: {request.error_message}_"
    
    return {
        "status": "error_handled",
        "remoteJid": request.remoteJid,
        "responseMessage": message,
        "error_type": request.error_type
    }

@router.post("/error/notify-support")
async def notify_support(request: ErrorRequest):
    """
    Notifica o suporte sobre erros críticos
    """
    logger.critical(f"Erro crítico: {request.error_type} - {request.error_message}")
    
    # Aqui você pode integrar com:
    # - Email
    # - Slack
    # - Telegram
    # - Sistema de tickets
    
    return {
        "status": "support_notified",
        "message": "Suporte foi notificado sobre o erro"
    }
