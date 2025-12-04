import requests

EVOLUTION_URL = "https://evolution-api-production-e43e.up.railway.app"
API_KEY = "123Cartoon*"  # API Key correta
INSTANCE = "chatbot"
WEBHOOK_URL = "https://chatbot-production-e324.up.railway.app/webhook"

headers = {"apikey": API_KEY}

print("=== CONFIGURAÇÃO AUTOMÁTICA DO WEBHOOK ===\n")
print(f"Evolution API: {EVOLUTION_URL}")
print(f"Webhook URL: {WEBHOOK_URL}")
print(f"Instância: {INSTANCE}\n")

# 1. Testar conexão
print("1. Testando conexão com Evolution API...")
try:
    resp = requests.get(f"{EVOLUTION_URL}/", headers=headers, timeout=5)
    print(f"   ✅ Conectado! Status: {resp.status_code}")
except Exception as e:
    print(f"   ❌ Erro de conexão: {e}")
    exit(1)

# 2. Verificar instância
print("\n2. Verificando instância 'chatbot'...")
try:
    resp = requests.get(f"{EVOLUTION_URL}/instance/connectionState/{INSTANCE}", headers=headers, timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        state = data.get('instance', {}).get('state', data.get('state', 'unknown'))
        print(f"   ✅ Instância encontrada! Estado: {state}")
    else:
        print(f"   Resposta: {resp.text}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. Verificar webhook atual
print("\n3. Verificando configuração atual do webhook...")
try:
    resp = requests.get(f"{EVOLUTION_URL}/webhook/find/{INSTANCE}", headers=headers, timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        config = resp.json()
        print(f"   Configuração atual:")
        print(f"   URL: {config.get('url', 'N/A')}")
    else:
        print(f"   Nenhuma configuração encontrada")
except Exception as e:
    print(f"   Info: Sem configuração prévia")

# 4. Configurar webhook
print(f"\n4. Configurando webhook...")
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
    
    if resp.status_code in [200, 201]:
        print("\n" + "="*60)
        print("   ✅ WEBHOOK CONFIGURADO COM SUCESSO!")
        print("="*60)
        print(f"\n🎉 PRONTO! O bot agora está 100% funcional!")
        print("\n📱 TESTE AGORA:")
        print("   1. Envie uma mensagem para o WhatsApp conectado")
        print("   2. O bot deve responder automaticamente")
        print("\n💡 FUNCIONALIDADES:")
        print("   - Responde perguntas sobre contabilidade")
        print("   - Identifica clientes cadastrados")
        print("   - Pausa automaticamente se você responder manualmente")
    else:
        print(f"   Resposta: {resp.text}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "="*60)
