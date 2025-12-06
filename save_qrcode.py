import requests
import base64
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

headers = {
    "X-Api-Key": API_KEY,
}

# Aguarda a sessão iniciar
print("Aguardando sessão iniciar...")
time.sleep(5)

# Pega o QR Code
print("Obtendo QR Code...")
qr_url = f"{WAHA_URL}/api/{SESSION}/auth/qr"
resp = requests.get(qr_url, headers=headers, timeout=10)

print(f"Status: {resp.status_code}")
print(f"Content-Type: {resp.headers.get('content-type')}")
print(f"Tamanho: {len(resp.content)} bytes")

if resp.status_code == 200:
    # Salva a imagem
    with open("qrcode_test.png", "wb") as f:
        f.write(resp.content)
    print("✅ QR Code salvo em qrcode_test.png")
    print("Abra o arquivo e tente escanear com o WhatsApp!")
else:
    print(f"❌ Erro: {resp.text}")
