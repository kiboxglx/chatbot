import requests

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"
PHONE = "553182119605" 

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print(f"Solicitando código para {PHONE}...")
url = f"{WAHA_URL}/api/{SESSION}/auth/request-code"
payload = {"phoneNumber": PHONE}

try:
    # Timeout de 120s
    resp = requests.post(url, json=payload, headers=headers, timeout=120)
    print(f"Status: {resp.status_code}")
    print(f"Resposta: {resp.text}")
except Exception as e:
    print(f"Erro: {e}")
