import requests

CHATBOT_URL = "https://chatbot-production-e324.up.railway.app"

print("Testando endpoint de QR Code...")
try:
    resp = requests.get(f"{CHATBOT_URL}/management/qrcode", timeout=30)
    print(f"Status: {resp.status_code}")
    print(f"Headers: {resp.headers.get('content-type')}")
    print(f"Body: {resp.text[:500]}")  # Primeiros 500 caracteres
except Exception as e:
    print(f"Erro: {e}")
