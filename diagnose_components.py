import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega envs (mas vamos forçar a chave nova para testar)
load_dotenv()

# CONFIGURAÇÕES
NEW_GEMINI_KEY = "AIzaSyCZTrQmZQt_qqYeT3nGB09BJjAJNn3mGyM" # Chave fornecida pelo usuário
WPP_URL = os.getenv("WHATSAPP_API_URL", "https://chatbot-production-e324.up.railway.app")
WPP_KEY = os.getenv("AUTHENTICATION_API_KEY", "THISISMYSECURETOKEN") # Senha correta
WPP_SESSION = "bot_whatsapp"
TEST_PHONE = "5511999999999" # Número fictício só para ver se a API aceita

def test_gemini():
    print("\n🤖 --- TESTE GEMINI (IA) ---")
    try:
        genai.configure(api_key=NEW_GEMINI_KEY)
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        response = model.generate_content("Responda apenas: OK")
        print(f"✅ Gemini respondeu: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Erro no Gemini: {e}")
        return False

def test_wpp_send():
    print("\n📤 --- TESTE WPPCONNECT (ENVIO) ---")
    
    # 1. Gerar Token
    token_url = f"{WPP_URL}/api/{WPP_SESSION}/{WPP_KEY}/generate-token"
    token = None
    try:
        print(f"1. Gerando token em: {token_url}")
        resp = requests.post(token_url, json={"secret": WPP_KEY}, timeout=60)
        
        if resp.status_code in [200, 201]:
            data = resp.json()
            token = data.get('token') or data.get('session', {}).get('token')
            print("✅ Token gerado com sucesso!")
        else:
            print(f"❌ Falha ao gerar token: {resp.status_code} - {resp.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão ao gerar token: {e}")
        return False

    # 2. Enviar Mensagem
    if not token:
        print("❌ Sem token, pulando envio.")
        return False
        
    send_url = f"{WPP_URL}/api/{WPP_SESSION}/send-message"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "phone": f"{TEST_PHONE}@c.us",
        "message": "Teste de diagnóstico do Chatbot",
        "isGroup": False
    }
    
    try:
        print(f"2. Enviando mensagem para {TEST_PHONE}...")
        resp = requests.post(send_url, json=payload, headers=headers, timeout=120)
        
        if resp.status_code in [200, 201]:
            print(f"✅ Mensagem enviada/aceita! Status: {resp.status_code}")
            return True
        else:
            print(f"❌ Falha ao enviar mensagem: {resp.status_code} - {resp.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro de conexão ao enviar mensagem: {e}")
        return False

if __name__ == "__main__":
    print("🔍 INICIANDO DIAGNÓSTICO COMPLETO...")
    ai_ok = test_gemini()
    wpp_ok = test_wpp_send()
    
    print("\n" + "="*30)
    print("📊 RELATÓRIO FINAL")
    print(f"IA (Gemini): {'✅ OK' if ai_ok else '❌ FALHOU'}")
    print(f"WPPConnect:  {'✅ OK' if wpp_ok else '❌ FALHOU'}")
    print("="*30)
