import os
import json
from datetime import datetime, timedelta
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
