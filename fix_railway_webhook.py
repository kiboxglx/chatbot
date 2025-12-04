import requests

# Configurações
EVOLUTION_API_URL = "https://evolution-api-production-e43e.up.railway.app"
BACKEND_URL = "https://chatbot-production.up.railway.app"
INSTANCE = "chatbot"
API_KEY = "123Cartoon*"

def fix_webhook():
    print(f"🔧 Configurando Webhook para instância '{INSTANCE}'...")
    
    url = f"{EVOLUTION_API_URL}/webhook/set/{INSTANCE}"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": f"{BACKEND_URL}/webhook",
        "webhookUrl": f"{BACKEND_URL}/webhook",
        "webhookByEvents": False,
        "events": ["MESSAGES_UPSERT"],
        "enabled": True
    }
    
    try:
        print(f"Enviando payload para {url}...")
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Webhook configurado com sucesso!")
            print(f"Status: {data.get('status')}")
            print(f"Mensagem: {data.get('message')}")
        else:
            print(f"\n❌ Erro ao configurar: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"\n❌ Erro de conexão: {e}")

if __name__ == "__main__":
    fix_webhook()
