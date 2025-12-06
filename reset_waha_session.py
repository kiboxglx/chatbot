import requests

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

# 1. Para a sessão atual
print("1. Parando sessão atual...")
stop_url = f"{WAHA_URL}/api/sessions/stop"
payload = {"name": SESSION}
resp = requests.post(stop_url, json=payload, headers=headers, timeout=10)
print(f"   Status: {resp.status_code}")
print(f"   Body: {resp.text}")

# 2. Aguarda um pouco
import time
time.sleep(2)

# 3. Inicia uma nova sessão
print("\n2. Iniciando nova sessão...")
start_url = f"{WAHA_URL}/api/sessions/start"
payload = {
    "name": SESSION,
    "config": {
        "webhooks": [
            {
                "url": "https://chatbot-production-e324.up.railway.app/webhook",
                "events": ["message"],
            }
        ]
    }
}
resp = requests.post(start_url, json=payload, headers=headers, timeout=30)
print(f"   Status: {resp.status_code}")
print(f"   Body: {resp.text}")

print("\n✅ Pronto! Agora tente gerar o QR Code no frontend novamente.")
