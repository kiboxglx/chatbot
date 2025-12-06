import requests
import time
import json

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("1. Verificando status atual...")
status_url = f"{WAHA_URL}/api/sessions/{SESSION}"
try:
    resp = requests.get(status_url, headers=headers, timeout=10)
    print(f"   Status Code: {resp.status_code}")
    print(f"   Body: {resp.text}")
    
    if resp.status_code == 200:
        status = resp.json().get('status')
        print(f"   Estado da sessão: {status}")
        
except Exception as e:
    print(f"   Erro ao verificar status: {e}")

print("\n2. Tentando realizar Logout (Stop Session)...")
stop_url = f"{WAHA_URL}/api/sessions/stop"
payload = {"name": SESSION}
try:
    resp = requests.post(stop_url, json=payload, headers=headers, timeout=20)
    print(f"   Status Code: {resp.status_code}")
    print(f"   Body: {resp.text}")
except Exception as e:
    print(f"   Erro ao realizar logout: {e}")

print("\n3. Verificando novamente após 5 segundos...")
time.sleep(5)
try:
    resp = requests.get(status_url, headers=headers, timeout=10)
    print(f"   Status Code: {resp.status_code}")
    print(f"   Body: {resp.text}")
except Exception as e:
    print(f"   Erro ao verificar status final: {e}")

print("\n4. Logout físico (Logout do WhatsApp) - Opcional se Stop não bastar")
# WAHA tem endpoint /api/{session}/auth/logout para desconectar do WhatsApp mesmo
logout_auth_url = f"{WAHA_URL}/api/{SESSION}/auth/logout"
try:
    print(f"   Tentando endpoint: {logout_auth_url}")
    resp = requests.post(logout_auth_url, headers=headers, timeout=10)
    print(f"   Status Code: {resp.status_code}")
    print(f"   Body: {resp.text}")
except Exception as e:
    print(f"   Erro logout auth: {e}")
