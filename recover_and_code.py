
import requests
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"
WEBHOOK_URL = "https://chatbot-production-e324.up.railway.app/webhook"
PHONE_NUMBER = "5538992469902"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("🔧 TENTATIVA DE RECUPERAÇÃO DE SESSÃO 'FAILED'...")

# 1. Stop Session (Force)
print("\n1. Parando sessão...")
try:
    requests.post(f"{WAHA_URL}/api/sessions/stop", json={"name": SESSION}, headers=headers)
except:
    pass
time.sleep(5)

# 2. Start Session
print("2. Iniciando Sessão...")
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
requests.post(f"{WAHA_URL}/api/sessions/start", json=start_payload, headers=headers)

print("   ⏳ Aguardando 15 segundos inicialização...")
time.sleep(15)

# 3. Check Status
print("\n3. Verificando Status...")
resp = requests.get(f"{WAHA_URL}/api/sessions/{SESSION}", headers=headers)
status = resp.json().get('status')
print(f"   Status Atual: {status}")

if status != 'SCAN_QR_CODE':
    print(f"❌ A sessão não entrou no modo QR Code. Status: {status}")
    print("   Tentando logout forçado...")
    requests.post(f"{WAHA_URL}/api/sessions/{SESSION}/logout", headers=headers)
    time.sleep(5)

# 4. Get Code
print(f"\n4. Solicitando Código para {PHONE_NUMBER}...")
resp = requests.post(f"{WAHA_URL}/api/sessions/{SESSION}/pairing-code", json={"phoneNumber": PHONE_NUMBER}, headers=headers)

if resp.status_code == 200:
    print("\n" + "="*40)
    print(f"🔢 CÓDIGO: {resp.json().get('code')}")
    print("="*40)
else:
    print(f"❌ Falha: {resp.text}")
