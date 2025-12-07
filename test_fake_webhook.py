
import requests
import json
import time

# URL do seu CHATBOT (O Cérebro) na Railway
WEBHOOK_URL = "https://chatbot-production-e324.up.railway.app/webhook"

# Simulando uma mensagem vinda do WAHA
payload_simulado = {
    "event": "message",
    "payload": {
        "id": "false_AAAAAA",
        "timestamp": int(time.time()),
        "from": "5511999999999@c.us", # Número fake para teste
        "body": "Teste de Vida: Você está me ouvindo?",
        "fromMe": False,
        "_data": {
            "notifyName": "Tester"
        }
    }
}

print(f"🚀 ENVIANDO MENSAGEM FALSA PARA O CÉREBRO...")
print(f"Alvo: {WEBHOOK_URL}")

try:
    resp = requests.post(WEBHOOK_URL, json=payload_simulado, timeout=10)
    
    print(f"\n📨 Status do Envio: {resp.status_code}")
    print(f"📝 Resposta do Servidor: {resp.text}")
    
    if resp.status_code == 200:
        print("\n✅ O Cérebro RECEBEU a mensagem!")
        if "queued" in resp.text:
            print("🕒 O bot colocou na fila para processar (Background Task).")
            print("👉 Isso é BOM! Significa que o fluxo de entrada está funcionando.")
            print("⚠️ Se o WhatsApp real não responde, o problema é no 'WhatsappService.enviar_texto' dentro da Railway.")
    else:
        print("❌ O Cérebro REJEITOU a mensagem.")

except Exception as e:
    print(f"❌ Falha ao conectar no webhook: {e}")
