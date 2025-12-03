import requests

API_URL = "http://localhost:8080"
INSTANCE = "chatbot"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"
WEBHOOK_URL = "http://chatbot_n8n:5678/webhook/whatsapp"

def set_webhook():
    url = f"{API_URL}/webhook/set/{INSTANCE}"
    headers = {
        "apikey": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Tentativa com payload simplificado para v1.7+
    payload = {
        "url": WEBHOOK_URL,
        "webhookByEvents": False,
        "events": ["MESSAGES_UPSERT"],
        "enabled": True
    }
    
    try:
        print(f"Tentando configurar webhook para: {WEBHOOK_URL}")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("✅ Webhook configurado com sucesso!")
            print(response.json())
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            
            # Se falhar, tenta o formato antigo 'webhookUrl'
            print("Tentando formato alternativo...")
            payload["webhookUrl"] = WEBHOOK_URL
            del payload["url"]
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                print("✅ Sucesso com formato alternativo!")
            else:
                print(f"❌ Falha total: {response.text}")

    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    set_webhook()
