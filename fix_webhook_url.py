
import requests
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
WEBHOOK_URL = "https://chatbot-production-e324.up.railway.app/webhook"
SESSION = "default"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("🔧 CORRIGINDO URL DO WEBHOOK NA SESSÃO WAHA...")

# Payload para atualizar o webhook SEM reiniciar a sessão (se o motor permitir)
# Na dúvida, usamos set webhook endpoint se disponível, ou patch
# A documentação oficial sugere POST /api/sessions/{session}/update-config ou restart com config
# Vamos tentar o caminho mais seguro: PARAR e RECONFIGURAR apenas os eventos e URLs, mantendo o auth.

url_stop = f"{WAHA_URL}/api/sessions/stop"
requests.post(url_stop, json={"name": SESSION}, headers=headers)
time.sleep(2)

# Start com config explícita
url_start = f"{WAHA_URL}/api/sessions/start"
payload = {
    "name": SESSION,
    "config": {
        "webhooks": [
            {
                "url": WEBHOOK_URL,
                "events": ["message", "message.any", "message.create"],
            }
        ]
    }
}

print(f"👉 Resetando sessão com Webhook alvo: {WEBHOOK_URL}")
resp = requests.post(url_start, json=payload, headers=headers)

print(f"Status Start: {resp.status_code}")
print(f"Body: {resp.text}")

if resp.status_code in [200, 201]:
    print("\n✅ Webhook corrigido! A sessão deve voltar como WORKING.")
    print("Teste enviando mensagens de outro celular agora.")
else:
    print("\n❌ Falha ao configurar. Verifique o log.")
