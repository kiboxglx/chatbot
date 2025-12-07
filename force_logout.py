
import requests
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("🔓 FORÇANDO LOGOUT DA SESSÃO...")

# 1. Tentar Logout
url_logout = f"{WAHA_URL}/api/sessions/{SESSION}/logout"
try:
    print(f"   Enviando pedido de logout para {url_logout}...")
    resp = requests.post(url_logout, headers=headers, timeout=20)
    print(f"   Status: {resp.status_code}")
    print(f"   Resposta: {resp.text}")
except Exception as e:
    print(f"   Erro no logout: {e}")

# 2. Verificar Status
time.sleep(2)
print("\n🔍 Verificando status pós-logout...")
resp_status = requests.get(f"{WAHA_URL}/api/sessions/{SESSION}", headers=headers)
print(f"   Status Atual: {resp_status.json()['status']}")

print("\n👉 Se o status for 'SCAN_QR_CODE' ou 'STOPPED', deu certo.")
print("👉 Agora você PRECISARÁ escanear o QR Code novamente.")
