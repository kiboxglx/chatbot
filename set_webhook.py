import requests

API_URL = "http://localhost:8080"
INSTANCE = "chatbot"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"

# URL interna do Docker para o n8n
# O nome do container é 'chatbot_n8n' e a porta interna é 5678
WEBHOOK_URL = "http://chatbot_n8n:5678/webhook/whatsapp"

def set_webhook():
    url = f"{API_URL}/webhook/set/{INSTANCE}"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "webhookUrl": WEBHOOK_URL,
        "webhookByEvents": False, # Envia tudo para a mesma URL
        "events": ["MESSAGES_UPSERT"],
        "enabled": True
    }
    
    try:
        print(f"Configurando webhook para: {WEBHOOK_URL}")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("✅ Webhook configurado com sucesso!")
            print(response.json())
        else:
            print(f"❌ Erro ao configurar: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    set_webhook()
