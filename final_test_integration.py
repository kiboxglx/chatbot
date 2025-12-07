
import os
import requests
import sys
from dotenv import load_dotenv

# Força recarregar .env
load_dotenv(override=True)

from app.services.ai_service import BrainService
from app.services.whatsapp_service import WhatsAppService

def test_full_integration():
    print("\n🚀 INICIANDO TESTE INTEGRADO (CÉREBRO + ZAP) 🚀\n")
    
    # 1. Verificar Variáveis
    url_zap = os.getenv("WHATSAPP_API_URL")
    print(f"📡 URL do WhatsApp Configurada: {url_zap}")
    
    if "evolution-api" in url_zap:
        print("❌ ALERTA: A URL ainda parece ser da Evolution API. Deveria ser do WAHA.")
    elif "waha" in url_zap:
        print("✅ URL parece correta (contém 'waha').")

    # 2. Testar IA
    print("\n🧠 1. Testando Inteligência Artificial...")
    try:
        brain = BrainService()
        resposta_ia = brain.processar_mensagem("Gostaria de abrir uma empresa", "Cliente Teste")
        print(f"   ✅ IA Respondeu: {resposta_ia.get('response_text')[:100]}...")
    except Exception as e:
        print(f"   ❌ Erro na IA: {e}")
        return

    # 3. Testar Conexão com WhatsApp (WAHA)
    print("\n📱 2. Testando Conexão com o WhatsApp...")
    whatsapp = WhatsAppService()
    
    # Vamos verificar se a sessão existe
    try:
        url_sessions = f"{url_zap}/api/sessions"
        headers = {"X-Api-Key": "THISISMYSECURETOKEN"}
        resp = requests.get(url_sessions, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            sessions = resp.json()
            print(f"   ✅ Conexão com WAHA estabelecida! (Status 200)")
            print(f"   🔍 Sessões encontradas: {len(sessions)}")
            for s in sessions:
                print(f"      - Sessão '{s['name']}': {s['status']}")
                
                if s['status'] == 'WORKING':
                     print("      🎉 ESTA SESSÃO ESTÁ PRONTA PARA ENVIAR MENSAGENS!")
        else:
            print(f"   ❌ Falha ao conectar no WAHA: {resp.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erro de conexão HTTP: {e}")

    print("\n🏁 CONCLUSÃO DO TESTE:")
    if resp.status_code == 200:
        print("✅ TUDO CERTO! A IA está pensando e o WhatsApp está conectado.")
        print("👉 Agora, você DEVE atualizar a variável WHATSAPP_API_URL na Railway para corrigir em produção.")
    else:
        print("❌ Ainda há problemas na conexão com o WhatsApp.")

if __name__ == "__main__":
    test_full_integration()
