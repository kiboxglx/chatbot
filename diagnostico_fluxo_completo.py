"""
DIAGNÓSTICO COMPLETO DO FLUXO DE MENSAGENS

Este script verifica cada etapa do processo:
1. Cliente envia mensagem
2. Evolution API recebe
3. Webhook é acionado
4. Backend processa
5. IA responde
6. Resposta é enviada de volta
"""

import requests
import json

print("="*70)
print("DIAGNÓSTICO COMPLETO DO CHATBOT")
print("="*70)

BACKEND_URL = "https://chatbot-production-e324.up.railway.app"
EVOLUTION_URL = "https://evolution-api-production-e43e.up.railway.app"
API_KEY = "123Cartoon*"
INSTANCE = "chatbot"

headers = {"apikey": API_KEY}

# 1. Verificar se o WhatsApp está conectado
print("\n1. Verificando conexão do WhatsApp...")
try:
    resp = requests.get(f"{EVOLUTION_URL}/instance/connectionState/{INSTANCE}", headers=headers, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        state = data.get('instance', {}).get('state', data.get('state', 'unknown'))
        print(f"   ✅ WhatsApp conectado! Estado: {state}")
        
        # Pegar informações da conta conectada
        if 'instance' in data and 'owner' in data['instance']:
            owner = data['instance']['owner']
            print(f"   📱 Número conectado: {owner}")
    else:
        print(f"   ❌ Erro: {resp.status_code}")
        exit(1)
except Exception as e:
    print(f"   ❌ Erro: {e}")
    exit(1)

# 2. Verificar configuração do webhook
print("\n2. Verificando configuração do webhook...")
try:
    resp = requests.get(f"{EVOLUTION_URL}/webhook/find/{INSTANCE}", headers=headers, timeout=5)
    if resp.status_code == 200:
        config = resp.json()
        webhook_url = config.get('url', 'N/A')
        events = config.get('events', [])
        print(f"   ✅ Webhook configurado!")
        print(f"   URL: {webhook_url}")
        print(f"   Events: {', '.join(events)}")
        
        if webhook_url != f"{BACKEND_URL}/webhook":
            print(f"   ⚠️  ATENÇÃO: URL do webhook está diferente!")
            print(f"   Esperado: {BACKEND_URL}/webhook")
    else:
        print(f"   ❌ Webhook não configurado")
except Exception as e:
    print(f"   ⚠️  Erro ao verificar: {e}")

# 3. Testar se o backend está online
print("\n3. Verificando se o backend está online...")
try:
    resp = requests.get(f"{BACKEND_URL}/", timeout=5)
    print(f"   ✅ Backend online! Status: {resp.status_code}")
except Exception as e:
    print(f"   ❌ Backend offline: {e}")
    exit(1)

# 4. Testar o webhook com uma mensagem simulada
print("\n4. Testando webhook com mensagem simulada...")
webhook_payload = {
    "event": "messages.upsert",
    "instance": INSTANCE,
    "data": {
        "key": {
            "remoteJid": "5511999999999@s.whatsapp.net",
            "fromMe": False,
            "id": "TEST_MSG_123"
        },
        "message": {
            "conversation": "Teste de mensagem"
        },
        "messageTimestamp": "1234567890"
    }
}

try:
    resp = requests.post(f"{BACKEND_URL}/webhook", json=webhook_payload, timeout=30)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        result = resp.json()
        print(f"   ✅ Webhook processou a mensagem!")
        print(f"   Ação da IA: {result.get('ai_action', 'N/A')}")
        print(f"   Cliente identificado: {result.get('client', 'N/A')}")
    else:
        print(f"   ❌ Erro: {resp.text}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n" + "="*70)
print("CONCLUSÃO:")
print("="*70)
print("""
Se todos os testes acima passaram (✅), o bot DEVE estar funcionando!

COMO TESTAR:
1. Pegue seu celular pessoal
2. Envie uma mensagem para o WhatsApp do escritório (o que foi conectado)
3. Aguarde 5-10 segundos
4. O bot deve responder automaticamente

SE NÃO FUNCIONAR:
- Verifique se você está enviando para o número CORRETO (o que foi conectado)
- Verifique se o número que enviou não está pausado (você respondeu manualmente?)
- Verifique os logs do Railway para ver se há erros

NÚMERO CONECTADO:
- O número que apareceu no item 1 acima é o que deve RECEBER as mensagens
- Qualquer pessoa pode enviar mensagem para esse número
- Não precisa cadastrar nada no código
""")
print("="*70)
