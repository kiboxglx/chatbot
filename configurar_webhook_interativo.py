"""
Script para configurar o webhook da Evolution API.

IMPORTANTE: Você precisa fornecer a URL da Evolution API no Railway.

Opções:
1. Se a Evolution API está no Railway, a URL deve ser algo como:
   https://evolution-api-production-XXXX.up.railway.app

2. Se você está usando um serviço externo de Evolution API, use essa URL.

3. Para encontrar a URL no Railway:
   - Acesse o dashboard do Railway
   - Clique no serviço "evolution-api"
   - Copie a URL pública (Settings > Domains)
"""

import requests

print(__doc__)

# Solicita a URL ao usuário
print("\n" + "="*60)
evolution_url = input("Digite a URL da Evolution API (sem / no final): ").strip()

if not evolution_url:
    print("❌ URL não fornecida. Abortando.")
    exit(1)

API_KEY = input("Digite a API Key da Evolution API: ").strip() or "429683C4C977415CAAFCCE10F7D57E11"
INSTANCE = "chatbot"
WEBHOOK_URL = "https://chatbot-production-e324.up.railway.app/webhook"

headers = {"apikey": API_KEY}

print("\n=== CONFIGURAÇÃO DO WEBHOOK ===\n")
print(f"Evolution API: {evolution_url}")
print(f"Webhook URL: {WEBHOOK_URL}")
print(f"Instância: {INSTANCE}\n")

# 1. Testar conexão
print("1. Testando conexão com Evolution API...")
try:
    resp = requests.get(f"{evolution_url}/", headers=headers, timeout=5)
    print(f"   ✅ Conectado! Status: {resp.status_code}")
except Exception as e:
    print(f"   ❌ Erro de conexão: {e}")
    print("\n💡 Verifique se a URL está correta e se a Evolution API está online.")
    exit(1)

# 2. Verificar instância
print("\n2. Verificando instância 'chatbot'...")
try:
    resp = requests.get(f"{evolution_url}/instance/connectionState/{INSTANCE}", headers=headers, timeout=5)
    if resp.status_code == 200:
        state = resp.json().get('instance', {}).get('state', 'unknown')
        print(f"   ✅ Instância encontrada! Estado: {state}")
    else:
        print(f"   ⚠️  Status: {resp.status_code}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. Configurar webhook
print(f"\n3. Configurando webhook...")
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
    resp = requests.post(f"{evolution_url}/webhook/set/{INSTANCE}", json=payload, headers=headers, timeout=10)
    print(f"   Status: {resp.status_code}")
    
    if resp.status_code in [200, 201]:
        print("   ✅ Webhook configurado com sucesso!")
        print(f"\n🎉 Pronto! Agora o bot deve responder automaticamente.")
        print("💡 Envie uma mensagem para o WhatsApp conectado para testar!")
    else:
        print(f"   Resposta: {resp.text}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "="*60)
