import requests

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"
PHONE = "5511999999999" # Número de teste

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print("Testando Pairing Code no WAHA...")
url = f"{WAHA_URL}/api/{SESSION}/auth/request-code"
payload = {"phoneNumber": PHONE}

try:
    # Tenta o endpoint de pairing code (pode variar dependendo da versão do WAHA)
    # Alguns usam /auth/request-code, outros /auth/pairing-code
    print(f"Tentando POST {url}")
    resp = requests.post(url, json=payload, headers=headers, timeout=10)
    
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text}")
    
except Exception as e:
    print(f"Erro: {e}")
