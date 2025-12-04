import requests
import os

# Configurações do Railway (Recuperadas do contexto anterior)
EVOLUTION_API_URL = "https://evolution-api-production-e43e.up.railway.app"
BACKEND_URL = "https://chatbot-production.up.railway.app"
INSTANCE = "chatbot"
API_KEY = "123Cartoon*" # Chave configurada no serviço Evolution API

def check_webhook():
    print(f"🔍 Verificando Webhook na Evolution API: {EVOLUTION_API_URL}")
    
    url = f"{EVOLUTION_API_URL}/webhook/find/{INSTANCE}"
    headers = {
        "apikey": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Configuração Atual:")
            print(f"URL do Webhook: {data.get('webhookUrl')}")
            print(f"Habilitado: {data.get('enabled')}")
            print(f"Eventos: {data.get('events')}")
            
            # Verificação
            expected_url = f"{BACKEND_URL}/webhook"
            current_url = data.get('webhookUrl')
            
            if current_url != expected_url:
                print(f"\n⚠️ AVISO: A URL do webhook parece incorreta!")
                print(f"Esperado: {expected_url}")
                print(f"Atual:    {current_url}")
                print("\n💡 Execute 'python fix_webhook.py' para corrigir.")
            else:
                print("\n✅ A URL do webhook está correta!")
                
        else:
            print(f"\n❌ Erro ao consultar API: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Erro de conexão: {e}")

if __name__ == "__main__":
    check_webhook()
