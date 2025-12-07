
import requests

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"

headers = {"X-Api-Key": API_KEY}

print("Verificando versão do WAHA...")
try:
    resp = requests.get(f"{WAHA_URL}/api/server/version", headers=headers)
    if resp.status_code == 200:
        print(f"Versão: {resp.json()}")
    else:
        # Fallback getting checking environment or health
        resp2 = requests.get(f"{WAHA_URL}/dashboard", headers=headers)
        print(f"Status Dashboard: {resp2.status_code}")
        # Try finding version in sessions
        resp3 = requests.get(f"{WAHA_URL}/api/sessions?all=true", headers=headers)
        print(f"Sessions Body prefix: {resp3.text[:200]}")

except Exception as e:
    print(f"Erro: {e}")
