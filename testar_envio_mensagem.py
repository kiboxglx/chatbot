import requests

print("=== TESTE DE ENVIO DE MENSAGEM ===\n")

EVOLUTION_URL = "https://evolution-api-production-e43e.up.railway.app"
API_KEY = "123Cartoon*"
INSTANCE = "chatbot"

# Número de teste (substitua pelo SEU número de celular)
NUMERO_TESTE = input("Digite seu número de celular (com DDD, ex: 5511999999999): ").strip()

if not NUMERO_TESTE:
    print("❌ Número não fornecido")
    exit(1)

headers = {"apikey": API_KEY}

print(f"\nTentando enviar mensagem de teste para: {NUMERO_TESTE}")
print("Aguarde...\n")

# Tenta enviar uma mensagem de teste
endpoint = f"{EVOLUTION_URL}/message/sendText/{INSTANCE}"
payload = {
    "number": NUMERO_TESTE,
    "textMessage": {
        "text": "🤖 TESTE: Se você recebeu esta mensagem, o bot está funcionando!"
    }
}

try:
    resp = requests.post(endpoint, json=payload, headers=headers, timeout=10)
    print(f"Status: {resp.status_code}")
    print(f"Resposta: {resp.text}\n")
    
    if resp.status_code in [200, 201]:
        print("✅ Mensagem enviada com sucesso!")
        print("\n📱 Verifique seu WhatsApp agora!")
        print("   Se você recebeu a mensagem, o problema está resolvido!")
        print("   Se NÃO recebeu, o problema pode ser:")
        print("   1. API Key incorreta")
        print("   2. Número formatado errado")
        print("   3. WhatsApp não está realmente conectado")
    else:
        print("❌ Erro ao enviar mensagem")
        print("\n💡 Possíveis causas:")
        print("   - API Key incorreta")
        print("   - Instância não conectada")
        print("   - Número formatado errado (deve ser: 5511999999999)")
        
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "="*60)
