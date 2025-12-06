import requests
import base64

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("🔍 Verificando status do WAHA...")

# 1. Status da Sessão
try:
    resp = requests.get(f"{WAHA_URL}/api/sessions/{SESSION}", headers=headers, timeout=10)
    print(f"Status Code: {resp.status_code}")
    print(f"Body: {resp.text}")
except Exception as e:
    print(f"Erro ao pegar status: {e}")

# 2. Tentando pegar screenshot (para ver o que o navegador está vendo)
print("\n📸 Tentando capturar tela do navegador...")
try:
    resp = requests.get(f"{WAHA_URL}/api/screenshot?session={SESSION}", headers=headers, timeout=20)
    if resp.status_code == 200:
        print("✅ Screenshot capturado! Salvando como 'waha_debug.png'...")
        with open("waha_debug.png", "wb") as f:
            f.write(resp.content)
    else:
        print(f"❌ Falha no screenshot: {resp.status_code} - {resp.text}")
except Exception as e:
    print(f"Erro ao pegar screenshot: {e}")
