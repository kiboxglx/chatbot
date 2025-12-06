import requests
import os

# Configurações
WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"
CHATBOT_URL = "https://chatbot-production-e324.up.railway.app"

def configurar_webhook():
    url = f"{WAHA_URL}/api/sessions/start"
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": SESSION,
        "config": {
            "webhooks": [
                {
                    "url": f"{CHATBOT_URL}/webhook",
                    "events": ["message"],
                }
            ]
        }
    }
    
    print(f"Iniciando sessão com webhook: {CHATBOT_URL}/webhook")
    resp = requests.post(url, json=payload, headers=headers)
    
    if resp.status_code in [200, 201]:
        print("✅ Sessão iniciada e webhook configurado!")
        print(resp.json())
    else:
        print(f"❌ Erro: {resp.status_code}")
        print(resp.text)

if __name__ == "__main__":
    configurar_webhook()
