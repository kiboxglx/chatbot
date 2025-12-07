
import requests
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"
PHONE_NUMBER = "5538992469902"
WEBHOOK_URL = "https://chatbot-production-e324.up.railway.app/webhook"

headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

print("⚙️ TROCANDO MOTOR PARA 'NOWEB' E PEDINDO CÓDIGO...")

# 1. Stop & Delete Current Session
print("1. Removendo sessão WEBJS antiga...")
requests.post(f"{WAHA_URL}/api/sessions/stop", json={"name": SESSION}, headers=headers)
time.sleep(2)
requests.delete(f"{WAHA_URL}/api/sessions/{SESSION}", headers=headers)
time.sleep(2)

# 2. Start with NOWEB
print("2. Iniciando nova sessão com motor NOWEB...")
payload = {
    "name": SESSION,
    "config": {
        "engine": "NOWEB", # O Pulo do Gato 🐱
        "webhooks": [
            {
                "url": WEBHOOK_URL,
                "events": ["message", "message.any"]
            }
        ]
    }
}
resp = requests.post(f"{WAHA_URL}/api/sessions/start", json=payload, headers=headers)
print(f"   Status Start: {resp.status_code}")

if resp.status_code != 201:
    print(f"   ❌ Erro ao iniciar: {resp.text}")
    print("   Tentando continuar mesmo assim...")

print("   ⏳ Aguardando 10s para inicialização do motor...")
time.sleep(10)

# 3. Request Code
print(f"\n3. 🤞 SOLICITANDO CÓDIGO PARA {PHONE_NUMBER}...")
code_payload = {"phoneNumber": PHONE_NUMBER}
resp_code = requests.post(f"{WAHA_URL}/api/sessions/{SESSION}/pairing-code", json=code_payload, headers=headers)

if resp_code.status_code == 200:
    data = resp_code.json()
    print("\n" + "█"*40)
    print(f"   CÓDIGO DE PAREAMENTO: {data.get('code')}")
    print("█"*40 + "\n")
    print("👉 DIGITE ISSO NO CELULAR AGORA!")
else:
    print(f"\n❌ FIM DA LINHA. Erro: {resp_code.status_code}")
    print(f"Body: {resp_code.text}")
