import os
import sys
from dotenv import load_dotenv

# Força o carregamento do .env
load_dotenv()

# SOBRESCREVE a chave com a nova fornecida pelo usuário para garantir
os.environ["GEMINI_API_KEY"] = "AIzaSyCZTrQmZQt_qqYeT3nGB09BJjAJNn3mGyM"
os.environ["WHATSAPP_API_URL"] = "https://server-production-c7e4.up.railway.app"
os.environ["AUTHENTICATION_API_KEY"] = "THISISMYSECURETOKEN"

# Adiciona o diretório atual ao path para importar os módulos
sys.path.append(os.getcwd())

from app.services.ai_service import BrainService
from app.services.whatsapp_service import WhatsAppService

def diagnose():
    print("🔍 INICIANDO DIAGNÓSTICO DE FLUXO COMPLETO (LOCAL)...")
    
    # 1. Teste BrainService (IA)
    print("\n🧠 1. Testando BrainService (IA)...")
    try:
        brain = BrainService()
        print(f"   Chave usada: {os.environ['GEMINI_API_KEY'][:5]}...")
        
        # Simula uma mensagem de "Oi"
        resultado = brain.processar_mensagem("Oi, tudo bem?")
        print(f"   ✅ Resposta da IA: {resultado}")
        
        if not resultado.get("response_text"):
            print("   ⚠️ ALERTA: IA retornou resposta vazia!")
            
    except Exception as e:
        print(f"   ❌ ERRO CRÍTICO NA IA: {e}")
        return

    # 2. Teste WhatsAppService (Envio)
    print("\n📤 2. Testando WhatsAppService (Envio)...")
    try:
        wpp = WhatsAppService()
        # Usa um número de teste (o seu próprio ou um fictício)
        # O ideal seria o usuário ver se chega no celular dele
        numero_teste = "5511999999999" 
        
        print(f"   URL WPPConnect: {wpp.base_url}")
        print(f"   Tentando enviar para: {numero_teste}")
        
        resp = wpp.enviar_texto(numero_teste, "Teste de Diagnóstico: Se você ler isso, o envio funciona.")
        print(f"   ✅ Resultado do Envio: {resp}")
        
    except Exception as e:
        print(f"   ❌ ERRO CRÍTICO NO ENVIO: {e}")

if __name__ == "__main__":
    diagnose()
