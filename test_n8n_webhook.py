import requests
import json

print("="*60)
print("TESTE DO N8N CLOUD COM NGROK")
print("="*60)

N8N_WEBHOOK_URL = "https://evelure.app.n8n.cloud/webhook-test/chatbot"

# Payload de teste simulando mensagem do WhatsApp
payload = {
    "body": {
        "key": {
            "remoteJid": "5531982119605@s.whatsapp.net",
            "fromMe": False
        },
        "message": {
            "conversation": "Preciso da segunda via do DAS"
        },
        "pushName": "Gabriel Nunes"
    }
}

print(f"\n📤 Enviando mensagem de teste para n8n Cloud...")
print(f"URL n8n: {N8N_WEBHOOK_URL}")
print(f"Mensagem: {payload['body']['message']['conversation']}")

try:
    response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
    
    print(f"\n📥 Resposta recebida:")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Sucesso! O fluxo completo funcionou!")
        try:
            data = response.json()
            print(f"\nResposta JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Verifica se a IA classificou corretamente
            if 'intent' in str(data):
                print("\n🎯 A IA classificou a intenção!")
            if '2_VIA_BOLETO' in str(data):
                print("✅ Intent correto: 2_VIA_BOLETO")
                
        except:
            print(f"\nResposta (texto):")
            print(response.text)
    else:
        print(f"⚠️  Status inesperado: {response.status_code}")
        print(f"Resposta: {response.text}")
        
except requests.exceptions.Timeout:
    print("❌ Timeout! O n8n demorou muito para responder.")
    print("   Isso pode acontecer se:")
    print("   1. O workflow não está ativo")
    print("   2. O backend Python não está rodando")
    print("   3. O ngrok está offline")
    
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "="*60)
print("VERIFICAÇÕES:")
print("="*60)
print("✓ Backend Python rodando? (http://localhost:8000)")
print("✓ ngrok ativo? (https://emelda-misapplied-accustomably.ngrok-free.dev)")
print("✓ Workflow n8n ativo? (toggle verde)")
print("="*60)
