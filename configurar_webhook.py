import requests
import json

# Configurações
API_URL = "http://localhost:8080"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"
INSTANCE = "chatbot"
# URL interna do Docker para o backend Python
NEW_WEBHOOK_URL = "http://host.docker.internal:8000/webhook"

headers = {
    "apikey": API_KEY,
    "Content-Type": "application/json"
}

payload = {
    "url": NEW_WEBHOOK_URL,
    "enabled": True,
    "webhookByEvents": False,
    "events": ["MESSAGES_UPSERT"]
}

print(f"Configurando Webhook para: {NEW_WEBHOOK_URL}...")

try:
    response = requests.post(f"{API_URL}/webhook/set/{INSTANCE}", json=payload, headers=headers)
    
    if response.status_code == 200:
        print("✅ SUCESSO! Webhook atualizado.")
        print(f"Resposta: {response.json()}")
    else:
        print(f"❌ ERRO: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Erro de conexão: {e}")
    print("Verifique se o container 'evolution_api' está rodando.")
