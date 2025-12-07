
import os
import time
from app.services.whatsapp_service import WhatsAppService

# Força as variáveis corretas para o teste local, caso o .env não tenha pego
os.environ["WHATSAPP_API_URL"] = "https://devlikeaprowaha-production-69c9.up.railway.app"
os.environ["AUTHENTICATION_API_KEY"] = "THISISMYSECURETOKEN"

def teste_envio_ativo():
    print("🚀 Iniciando teste de ENVIO ATIVO...")
    
    zap = WhatsAppService()
    target = "5538992469902" # Número conectado identificado anteriormente
    
    msg = (
        "🤖 *Teste de Diagnóstico do Bot*\n\n"
        "Se você está lendo isso, significa que:\n"
        "1. O servidor está rodando.\n"
        "2. A conexão com o WhatsApp está ativa.\n"
        "3. O sistema de envio está funcionando.\n\n"
        "🕒 Hora: " + time.strftime("%H:%M:%S")
    )
    
    print(f"📨 Tentando enviar mensagem para o próprio número ({target})...")
    
    try:
        resp = zap.enviar_texto(target, msg)
        print("Resultado:")
        print(resp)
    except Exception as e:
        print(f"❌ Falha crítica no teste: {e}")

if __name__ == "__main__":
    teste_envio_ativo()
