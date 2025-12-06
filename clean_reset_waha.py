import requests
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("1. Excluindo sessão 'default' para limpar dados antigos...")
delete_url = f"{WAHA_URL}/api/sessions/{SESSION}"
try:
    resp = requests.delete(delete_url, headers=headers, timeout=20)
    print(f"   Status Code: {resp.status_code}")
    print(f"   Body: {resp.text}")
except Exception as e:
    print(f"   Erro ao excluir: {e}")

print("\n2. Aguardando 5 segundos...")
time.sleep(5)

print("\n3. Criando nova sessão limpa...")
start_url = f"{WAHA_URL}/api/sessions/start"
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
try:
    resp = requests.post(start_url, json=payload, headers=headers, timeout=30)
    print(f"   Status Code: {resp.status_code}")
    print(f"   Body: {resp.text}")
except Exception as e:
    print(f"   Erro ao iniciar: {e}")
