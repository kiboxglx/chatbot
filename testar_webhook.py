import requests
import json

# Simula uma mensagem chegando no webhook
WEBHOOK_URL = "https://chatbot-production-e324.up.railway.app/webhook"

# Payload simulando uma mensagem real da Evolution API
payload = {
    "event": "messages.upsert",
    "instance": "chatbot",
    "data": {
        "key": {
            "remoteJid": "5511999999999@s.whatsapp.net",
            "fromMe": False,
            "id": "TEST123"
        },
        "message": {
            "conversation": "Olá, preciso de ajuda"
        },
        "messageTimestamp": "1234567890"
    }
}

print("=== TESTE DO WEBHOOK ===\n")
print(f"Enviando mensagem de teste para: {WEBHOOK_URL}\n")
print(f"Payload: {json.dumps(payload, indent=2)}\n")

try:
    response = requests.post(WEBHOOK_URL, json=payload, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.text}\n")
    
    if response.status_code == 200:
        print("✅ Webhook recebeu a mensagem!")
        print("\n💡 Se o bot não respondeu no WhatsApp, o problema pode ser:")
        print("   1. GEMINI_API_KEY não configurada no Railway")
        print("   2. Erro ao enviar resposta de volta para a Evolution API")
        print("   3. Verifique os logs do Railway para ver o erro exato")
    else:
        print("⚠️  Webhook retornou erro")
        
except Exception as e:
    print(f"❌ Erro ao conectar no webhook: {e}")

print("\n" + "="*60)
