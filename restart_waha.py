import requests
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("1. Parando sessão travada...")
requests.post(f"{WAHA_URL}/api/sessions/stop", json={"name": SESSION}, headers=headers)
time.sleep(3)

print("2. Iniciando nova sessão limpa...")
payload = {
    "name": SESSION,
    "config": {
        "webhooks": [
            {
                "url": "https://chatbot-production-e324.up.railway.app/webhook",
                "events": ["message"]
            }
        ]
    }
}
requests.post(f"{WAHA_URL}/api/sessions/start", json=payload, headers=headers)

print("✅ Sessão reiniciada! Aguarde 10 segundos e tente gerar o código novamente.")
