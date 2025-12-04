import requests
import os

# Configurações
EVOLUTION_URL = os.getenv("WHATSAPP_API_URL", "http://localhost:8080")
API_KEY = os.getenv("AUTHENTICATION_API_KEY", "429683C4C977415CAAFCCE10F7D57E11")
INSTANCE = "chatbot"
WEBHOOK_URL = "https://chatbot-production-e324.up.railway.app/webhook"

headers = {"apikey": API_KEY}

print("=== CONFIGURAÇÃO DO WEBHOOK ===\n")

# 1. Verificar configuração atual
print("1. Verificando webhook atual...")
try:
    resp = requests.get(f"{EVOLUTION_URL}/webhook/find/{INSTANCE}", headers=headers, timeout=5)
    if resp.status_code == 200:
        config = resp.json()
        print(f"   Configuração atual: {config}")
    else:
        print(f"   Nenhuma configuração encontrada (Status: {resp.status_code})")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 2. Configurar webhook
print(f"\n2. Configurando webhook para: {WEBHOOK_URL}")
payload = {
    "url": WEBHOOK_URL,
    "webhook_by_events": False,
    "webhook_base64": False,
    "events": [
        "MESSAGES_UPSERT",
        "MESSAGES_UPDATE",
        "SEND_MESSAGE"
    ]
}

try:
    resp = requests.post(f"{EVOLUTION_URL}/webhook/set/{INSTANCE}", json=payload, headers=headers, timeout=10)
    print(f"   Status: {resp.status_code}")
    print(f"   Resposta: {resp.text}")
    
    if resp.status_code in [200, 201]:
        print("\n   ✅ Webhook configurado com sucesso!")
    else:
        print(f"\n   ⚠️  Possível erro na configuração")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n=== FIM DA CONFIGURAÇÃO ===")
print("\n💡 Agora envie uma mensagem para o WhatsApp conectado e veja se o bot responde!")
