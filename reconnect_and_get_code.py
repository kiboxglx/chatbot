
import requests
import time
import base64

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"
WEBHOOK_URL = "https://chatbot-production-e324.up.railway.app/webhook"
PHONE_NUMBER = "5538992469902"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("🔄 INICIANDO PROCESSO DE RECONEXÃO 🔄")

# 1. Start Session
print("\n1. Iniciando Sessão 'default'...")
start_payload = {
    "name": SESSION,
    "config": {
        "webhooks": [
            {
                "url": WEBHOOK_URL,
                "events": ["message", "message.any"]
            }
        ]
    }
}

try:
    # Tenta iniciar. Se já estiver rodando, pode dar erro ou OK, vamos tratar.
    resp = requests.post(f"{WAHA_URL}/api/sessions/start", json=start_payload, headers=headers)
    print(f"   Status Start: {resp.status_code}")
    print(f"   Body: {resp.text}")
except Exception as e:
    print(f"   ❌ Erro ao iniciar sessão: {e}")
    exit(1)

print("   ⏳ Aguardando 10 segundos para o navegador abrir...")
time.sleep(10)

# 2. Get Pairing Code
print(f"\n2. Solicitando Código de Pareamento para {PHONE_NUMBER}...")
code_url = f"{WAHA_URL}/api/sessions/{SESSION}/pairing-code"
code_payload = {"phoneNumber": PHONE_NUMBER}

try:
    resp = requests.post(code_url, json=code_payload, headers=headers)
    
    if resp.status_code == 200:
        data = resp.json()
        code = data.get('code')
        print("\n" + "="*40)
        print(f"🔢 SEU CÓDIGO DE PAREAMENTO: {code}")
        print("="*40)
        print("👉 Digite esse código no seu WhatsApp > Aparelhos Conectados > Conectar com número de telefone.")
    else:
        print(f"❌ Falha ao pegar código: {resp.status_code}")
        print(f"Resposta: {resp.text}")

except Exception as e:
    print(f"❌ Erro na requisição do código: {e}")
