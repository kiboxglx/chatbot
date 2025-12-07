
import requests
import base64

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

headers = {"X-Api-Key": API_KEY}

print("📸 Capturando QR Code...")

try:
    resp = requests.get(f"{WAHA_URL}/api/screenshot?session={SESSION}", headers=headers)
    
    if resp.status_code == 200:
        with open("qrcode_connect.png", "wb") as f:
            f.write(resp.content)
        print("✅ QR Code salvo em 'qrcode_connect.png'")
        print("👉 Como o código de texto falhou (404), por favor use o QR Code.")
    else:
        print(f"❌ Falha ao pegar QR Code: {resp.status_code}")
        print(resp.text)

except Exception as e:
    print(f"Erro: {e}")
