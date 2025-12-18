from fastapi import APIRouter, Request, BackgroundTasks
import json
import time

router = APIRouter()

# Instanciação preguiçosa (Lazy) para evitar erros no import
_brain = None
_wa = None
_exp = None

# Lista global para diagnóstico de produção
RECENT_EVENTS = []

def get_brain():
    global _brain
    if not _brain:
        from app.services.ai_service import BrainService
        _brain = BrainService()
    return _brain

def get_whatsapp():
    global _wa
    if not _wa:
        from app.services.whatsapp_service import WhatsAppService
        _wa = WhatsAppService()
    return _wa

def get_expense():
    global _exp
    if not _exp:
        from app.services.expense_service import ExpenseService
        _exp = ExpenseService()
    return _exp

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
        RECENT_EVENTS.append({"time": time.strftime("%H:%M:%S"), "event": "BG_START", "for": numero_cliente})
        
        # Carrega serviços sob demanda
        brain_service = get_brain()
        whatsapp_service = get_whatsapp()
        expense_service = get_expense()

        RECENT_EVENTS.append({"time": time.strftime("%H:%M:%S"), "event": "BG_SERVICES_LOADED"})

        # 1. Processar com IA (BrainService)
        contexto = f"Cliente WhatsApp: {numero_cliente}"
        decisao = brain_service.processar_mensagem(body, contexto)
        
        RECENT_EVENTS.append({"time": time.strftime("%H:%M:%S"), "event": "BG_AI_DECISION", "action": decisao.get("action")})
        
        resposta_texto = decisao.get("response_text", "")
        acao = decisao.get("action", "REPLY")
        params = decisao.get("parameters", {})

        print(f"🧠 Decisão da IA: {acao}")

        # 2. Executar Ações Específicas
        if acao == "SAVE_EXPENSE":
            amount = params.get("amount", 0)
            desc = params.get("description", "Gasto não especificado")
            cat = params.get("category", "Geral")
            expense_service.save_expense(desc, float(amount), cat, numero_cliente)
            print(f"💰 Gasto salvo: {desc} - R$ {amount}")

        elif acao == "GENERATE_REPORT":
        elif acao == "GENERATE_REPORT":
            data = expense_service.get_summary(numero_cliente)
            
            # Cabeçalho Técnico
            report_text = (
                f"📊 *Relatório Financeiro Analítico*\n"
                f"📅 *Período:* Geral (All-time)\n\n"
                f"💰 *Total Acumulado:* *R$ {data['total']:,.2f}*\n"
                f"📉 *Média p/ Transação:* R$ {data['average']:,.2f}\n"
                f"📝 *Registros:* {data['count']}\n"
            )

            # Top Gasto
            if data['top_category']:
                top = data['top_category']
                report_text += f"🏆 *Ofensor Principal:* {top['name']} ({(top['percentage']):.0f}%)\n"

            report_text += "\n*Detalhamento por Categoria:*\n"
            
            # Gráfico ASCII
            # Ex: ██████░░░░ 60%
            def make_bar(pct):
                filled = int(pct / 10)
                return "█" * filled + "░" * (10 - filled)

            for cat in data['categories']:
                bar = make_bar(cat['percentage'])
                report_text += (
                    f"\n🔹 *{cat['name']}*\n"
                    f"`{bar}` {cat['percentage']:.1f}%  (R$ {cat['amount']:,.2f})"
                )
            
            # Substitui resposta da IA
            if "Total" not in resposta_texto: 
                resposta_texto += f"\n\n{report_text}"
            else:
                 resposta_texto = report_text

        # 3. Envia a resposta via WAHA
        if resposta_texto:
            print(f"📤 Enviando resposta para {numero_cliente}...")
            whatsapp_service.enviar_texto(numero_cliente, resposta_texto)
            print(f"✅ [Background] Ciclo concluído para {numero_cliente}!")
        else:
            print("⚠️ A IA não gerou resposta de texto.")
            
    except Exception as e:
        RECENT_EVENTS.append({"time": time.strftime("%H:%M:%S"), "event": "BG_ERROR", "error": str(e)})
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
        
        # Log para diagnóstico
        event_info = {
            "time": time.strftime("%H:%M:%S"),
            "event": data.get("event"),
            "payload_id": data.get("payload", {}).get("id"),
            "from": data.get("payload", {}).get("from"),
            "fromMe": data.get("payload", {}).get("fromMe")
        }
        RECENT_EVENTS.append(event_info)
        if len(RECENT_EVENTS) > 20: RECENT_EVENTS.pop(0)

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
        remote_jid = payload.get("from", "") # Ex: 551199999999@c.us, 551199999999@lid
        if not remote_jid:
            return {"status": "error", "reason": "No 'from' field"}
            
        # Usa o JID completo para garantir que @lid e @g.us sejam respeitados
        chat_id = remote_jid
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
