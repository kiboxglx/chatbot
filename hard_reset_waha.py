
import requests
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("🧨 REALIZANDO HARD RESET NA SESSÃO WAHA...")

# 1. Deletar Sessão (Isso mata o processo do navegador)
print("\n1. Deletando sessão 'default' (Pode demorar)...")
try:
    resp = requests.delete(f"{WAHA_URL}/api/sessions/{SESSION}", headers=headers, timeout=30)
    print(f"   Status Delete: {resp.status_code}")
except Exception as e:
    print(f"   Erro no Delete: {e}")

time.sleep(5)

# 2. Recriar Sessão Limpa
print("\n2. Recriando Sessão...")
payload = {
    "name": SESSION,
    "config": {
        "webhooks": [
            {
                "url": "https://chatbot-production-e324.up.railway.app/webhook",
                "events": ["message", "message.any"]
            }
        ]
    }
}
try:
    resp = requests.post(f"{WAHA_URL}/api/sessions/start", json=payload, headers=headers, timeout=30)
    print(f"   Status Start: {resp.status_code}")
    print(f"   Body: {resp.text}")
    
    if resp.status_code == 201:
        print("\n✅ Sessão recriada com sucesso!")
        print("📲 PEÇA PARA O CLIENTE ESCANEAR O QR CODE AGORA.")
    else:
        print("❌ Falha ao recriar sessão.")
        
except Exception as e:
    print(f"   Erro no Start: {e}")
