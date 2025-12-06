import requests
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"
PHONE = "553892469902"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("Aguardando sessão inicializar (15s)...")
time.sleep(15)

print(f"Solicitando Pairing Code para {PHONE}...")
url = f"{WAHA_URL}/api/{SESSION}/auth/request-code"
payload = {"phoneNumber": PHONE}

try:
    resp = requests.post(url, json=payload, headers=headers, timeout=120)
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text}")
    if resp.status_code == 201:
        print(f"✅ SUCESSO! Código: {resp.json().get('code')}")
except Exception as e:
    print(f"Erro: {e}")
