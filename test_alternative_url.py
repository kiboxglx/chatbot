
import requests

POTENTIAL_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"

print(f"Testando URL alternativa: {POTENTIAL_URL}")

try:
    resp = requests.get(f"{POTENTIAL_URL}/api/sessions", headers={"X-Api-Key": API_KEY}, timeout=10)
    print(f"Status: {resp.status_code}")
    print(f"Body: {resp.text}")
    
    if resp.status_code == 200:
        print("✅ SUCESSO! Esta parece ser a URL correta do WAHA.")
    else:
        print("❌ Falha na URL alternativa.")

except Exception as e:
    print(f"Erro: {e}")
