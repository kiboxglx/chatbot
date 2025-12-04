import requests

print("=== VERIFICAÇÃO DA CHAVE DA IA ===\n")

BACKEND_URL = "https://chatbot-production-e324.up.railway.app"

# Testa se a IA está funcionando enviando uma mensagem de teste
webhook_payload = {
    "event": "messages.upsert",
    "instance": "chatbot",
    "data": {
        "key": {
            "remoteJid": "5511999999999@s.whatsapp.net",
            "fromMe": False,
            "id": "TEST_IA_123"
        },
        "message": {
            "conversation": "Olá, preciso de ajuda"
        },
        "messageTimestamp": "1234567890"
    }
}

print("Enviando mensagem de teste para o webhook...")
print("Mensagem: 'Olá, preciso de ajuda'\n")

try:
    resp = requests.post(f"{BACKEND_URL}/webhook", json=webhook_payload, timeout=30)
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        result = resp.json()
        print(f"Resposta: {result}\n")
        
        ai_action = result.get('ai_action', 'N/A')
        
        if ai_action == 'HANDOFF':
            print("⚠️  A IA retornou 'HANDOFF' (passar para humano)")
            print("   Isso pode significar que a GEMINI_API_KEY não está configurada!")
            print("\n📝 SOLUÇÃO:")
            print("   1. Acesse o Railway")
            print("   2. Vá no serviço 'chatbot'")
            print("   3. Clique em 'Variables'")
            print("   4. Adicione: GEMINI_API_KEY=sua_chave_aqui")
            print("   5. Aguarde o redeploy")
        elif ai_action == 'REPLY':
            print("✅ A IA está funcionando!")
            print("   O problema deve ser no envio da resposta de volta")
        else:
            print(f"🤔 Ação inesperada: {ai_action}")
    else:
        print(f"❌ Erro: {resp.text}")
        
except Exception as e:
    print(f"❌ Erro: {e}")

print("\n" + "="*60)
