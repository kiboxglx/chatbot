import os
import json
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.models.cliente import Cliente
from app.services.ai_service import BrainService
from app.services.whatsapp_service import WhatsAppService
from app.services.media_service import MediaService
from app.services.pdf_generator import gerar_das_pdf

router = APIRouter()

# Instanciação dos serviços
brain_service = BrainService()
whatsapp_service = WhatsAppService()
media_service = MediaService()

# --- CONTROLE DE PAUSA (MEMÓRIA SIMPLES) ---
# Armazena { "numero_telefone": datetime_ultima_intervencao }
PAUSED_CHATS = {}
PAUSE_DURATION_MINUTES = 30

@router.post("/webhook")
async def receive_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint para receber mensagens do WhatsApp (Evolution API).
    Gerencia a lógica de resposta automática e pausa humana.
    """
    try:
        payload = await request.json()
    except Exception:
        return {"status": "error", "reason": "invalid_json"}

    # 1. Extração de Dados (Compatível com Evolution API direto)
    data = payload.get('data')
    if not data:
        # Tenta pegar de 'body' caso venha encapsulado
        data = payload.get('body', {}).get('data')
    
    if not data:
        return {"status": "ignored", "reason": "no_data_field"}

    try:
        key = data.get('key', {})
        remote_jid = key.get('remoteJid', '')
        telefone = remote_jid.replace('@s.whatsapp.net', '')
        from_me = key.get('fromMe', False)
    except:
        return {"status": "error", "reason": "extraction_error"}

    # --- LÓGICA DE HANDOVER (PAUSA INTELIGENTE) ---
    
    # Se a mensagem foi enviada POR MIM (Contador/Humano)
    if from_me:
        print(f"👤 Humano respondeu para {telefone}. Pausando bot por {PAUSE_DURATION_MINUTES} min.")
        PAUSED_CHATS[telefone] = datetime.now()
        return {"status": "ignored", "reason": "human_interaction_detected"}

    # Se a mensagem é do CLIENTE, verifica se está pausado
    if telefone in PAUSED_CHATS:
        last_interaction = PAUSED_CHATS[telefone]
        if datetime.now() - last_interaction < timedelta(minutes=PAUSE_DURATION_MINUTES):
            print(f"⏸️ Bot pausado para {telefone} (Modo Humano Ativo)")
            return {"status": "ignored", "reason": "bot_paused"}
        else:
            # Tempo expirou, remove da pausa
            print(f"▶️ Retomando atendimento automático para {telefone}")
            del PAUSED_CHATS[telefone]

    # 2. Extrai Conteúdo da Mensagem
    message_content = data.get('message', {})
    mensagem = ""
    media_path = None
    
    if 'conversation' in message_content:
        mensagem = message_content['conversation']
    elif 'extendedTextMessage' in message_content:
        mensagem = message_content['extendedTextMessage'].get('text', '')
    elif 'imageMessage' in message_content:
        mensagem = message_content['imageMessage'].get('caption', 'Imagem enviada')
        print("📷 Imagem detectada! Baixando...")
        media_path = media_service.download_media(message_content['imageMessage'])
    elif 'documentMessage' in message_content:
        mensagem = message_content['documentMessage'].get('caption', 'Documento enviado')
        print("📄 Documento detectado! Baixando...")
        media_path = media_service.download_media(message_content['documentMessage'])
    
    if not mensagem and not media_path:
        return {"status": "ignored", "reason": "empty_message"}

    print(f"📩 Cliente: {telefone} | Msg: {mensagem}")

    # --- VERIFICAÇÃO DE HORÁRIO (Apenas Informativo - IA decide o que dizer) ---
    # A lógica de bloqueio foi removida a pedido.
    # A IA será instruída via prompt a avisar sobre o horário se necessário.

    # 3. Identificação do Cliente (Opcional - agora permite não cadastrados)
    nome_cliente = "Cliente"
    contexto_extra = ""
    
    try:
        cliente = db.query(Cliente).filter(Cliente.telefone == telefone).first()
        if cliente:
            nome_cliente = cliente.nome
            contexto_extra = f"Empresa: {cliente.empresa_nome} | CNPJ: {cliente.cnpj_cpf}"
            print(f"Cliente identificado: {cliente.nome}")
        else:
            print(f"Número não cadastrado: {telefone}. Atendendo como visitante.")
    except Exception as e:
        print(f"Erro ao buscar cliente (banco offline?): {e}")

    # 4. Processamento IA (Cérebro)
    agora_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    contexto = f"Cliente: {nome_cliente} | {contexto_extra} | Data/Hora Atual: {agora_str}"
    
    # Envia para o Gemini
    decisao_ia = brain_service.processar_mensagem(mensagem, contexto, media_path)
    
    # Limpa arquivo temporário
    if media_path and os.path.exists(media_path):
        try:
            os.remove(media_path)
        except:
            pass
    
    acao = decisao_ia.get("action")
    texto_resposta = decisao_ia.get("response_text")
    
    print(f"🤖 IA: {acao} | Resp: {texto_resposta}")

    # 5. Executar Ação
    if acao in ['REPLY', 'HANDOFF', 'SEND_DOC']:
        # Envia a resposta
        whatsapp_service.enviar_texto(telefone, texto_resposta)
        
        # Se for HANDOFF, podemos pausar o bot automaticamente também?
        # Opcional: Se a IA decidiu passar para humano, pausa o bot para não atrapalhar
        if acao == 'HANDOFF':
            print(f"🛑 IA solicitou humano. Pausando bot para {telefone}.")
            PAUSED_CHATS[telefone] = datetime.now()

    return {
        "status": "processed",
        "client": nome_cliente,
        "ai_action": acao
    }
