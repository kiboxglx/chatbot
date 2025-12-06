import requests
import json

CHATBOT_URL = "https://chatbot-production-e324.up.railway.app"

print("🔍 Testando endpoint de QR Code (V2)...")
try:
    resp = requests.get(f"{CHATBOT_URL}/management/qrcode", timeout=30)
    
    print(f"📥 Status Code: {resp.status_code}")
    print(f"📥 Content-Type: {resp.headers.get('content-type')}")
    
    if resp.status_code == 200:
        try:
            data = resp.json()
            if "base64" in data:
                print("✅ QR Code recebido com sucesso (Base64 presente)")
                print(f"   Início do Base64: {data['base64'][:50]}...")
            elif "message" in data:
                print(f"⚠️ Mensagem recebida: {data['message']}")
            else:
                print(f"⚠️ JSON inesperado: {data}")
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON. Corpo bruto:\n{resp.text}")
    else:
        print(f"❌ Erro na requisição: {resp.status_code}")
        print(f"   Corpo: {resp.text}")

except Exception as e:
    print(f"❌ Exceção: {e}")
