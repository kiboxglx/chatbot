import requests

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"

# Teste 1: Health check
print("1. Testando health check...")
try:
    resp = requests.get(f"{WAHA_URL}/health", timeout=10)
    print(f"   Status: {resp.status_code}")
    print(f"   Body: {resp.text}")
except Exception as e:
    print(f"   Erro: {e}")

# Teste 2: Listar sessões
print("\n2. Listando sessões...")
try:
    headers = {"X-Api-Key": API_KEY}
    resp = requests.get(f"{WAHA_URL}/api/sessions", headers=headers, timeout=10)
    print(f"   Status: {resp.status_code}")
    print(f"   Body: {resp.text}")
except Exception as e:
    print(f"   Erro: {e}")

# Teste 3: Ver sessão default
print("\n3. Verificando sessão 'default'...")
try:
    headers = {"X-Api-Key": API_KEY}
    resp = requests.get(f"{WAHA_URL}/api/sessions/default", headers=headers, timeout=10)
    print(f"   Status: {resp.status_code}")
    print(f"   Body: {resp.text}")
except Exception as e:
    print(f"   Erro: {e}")
