import requests

API_URL = "http://localhost:8080"
INSTANCE = "chatbot"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"

# Usando host.docker.internal para garantir conectividade via host
WEBHOOK_URL = "http://host.docker.internal:5678/webhook/whatsapp"

def set_webhook():
    url = f"{API_URL}/webhook/set/{INSTANCE}"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "enabled": True,
        "url": WEBHOOK_URL,
        "webhookByEvents": False,
        "events": ["MESSAGES_UPSERT"]
    }
    
    try:
        print(f"Tentando configurar webhook para: {WEBHOOK_URL}")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Webhook configurado com sucesso!")
            print(response.json())
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    set_webhook()
