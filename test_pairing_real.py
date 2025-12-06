import requests

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"
# Coloque seu número aqui para testar se quiser, ou use um fictício para ver se a API responde
PHONE = "5511999999999" 

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

print(f"Solicitando código para {PHONE}...")
url = f"{WAHA_URL}/api/{SESSION}/auth/request-code"
payload = {"phoneNumber": PHONE}

try:
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"Status: {resp.status_code}")
    print(f"Resposta: {resp.text}")
except Exception as e:
    print(f"Erro: {e}")
