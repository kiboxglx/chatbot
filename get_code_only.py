
import requests

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"
PHONE_NUMBER = "5538992469902"

headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

print(f"Solicitando código para {PHONE_NUMBER}...")
resp = requests.post(f"{WAHA_URL}/api/sessions/{SESSION}/pairing-code", json={"phoneNumber": PHONE_NUMBER}, headers=headers)

if resp.status_code == 200:
    print(f"✅ CÓDIGO: {resp.json().get('code')}")
else:
    print(f"❌ Erro: {resp.status_code} - {resp.text}")
