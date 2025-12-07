
import requests
import time

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "test_engine"
PHONE_NUMBER = "5538992469902"

headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

print("🧪 TESTANDO NOVO MOTOR (NOWEB) PARA GERAR CÓDIGO...")

# 1. Start Session with NOWEB
print("1. Criando sessão de teste...")
payload = {
    "name": SESSION,
    "config": {
        "engine": "NOWEB", # Tentativa de forçar engine
        "webhooks": []
    }
}

try:
    # Stop first if exists
    requests.post(f"{WAHA_URL}/api/sessions/stop", json={"name": SESSION}, headers=headers)
    time.sleep(2)
    
    resp = requests.post(f"{WAHA_URL}/api/sessions/start", json=payload, headers=headers)
    print(f"   Start Status: {resp.status_code}")
    print(f"   Body: {resp.text}")
    
    print("   ⏳ Aguardando 5s...")
    time.sleep(5)
    
    # Check if logic worked (engine)
    resp_sess = requests.get(f"{WAHA_URL}/api/sessions/{SESSION}", headers=headers)
    print(f"   Session Info: {resp_sess.text}")
    
    # 2. Try Get Code
    print("\n2. Tentando pegar código na sessão de teste...")
    resp_code = requests.post(f"{WAHA_URL}/api/sessions/{SESSION}/pairing-code", json={"phoneNumber": PHONE_NUMBER}, headers=headers)
    
    if resp_code.status_code == 200:
        print("\n" + "="*40)
        print(f"🔢 CÓDIGO (SESSÃO TESTE): {resp_code.json().get('code')}")
        print("   ⚠️ Se funcionou, precisamos migrar a sessão principal para NOWEB.")
        print("="*40)
    else:
        print(f"❌ Falha no código: {resp_code.status_code} - {resp_code.text}")

    # Cleanup
    print("\n3. Limpando sessão de teste...")
    requests.post(f"{WAHA_URL}/api/sessions/stop", json={"name": SESSION}, headers=headers)
    requests.delete(f"{WAHA_URL}/api/sessions/{SESSION}", headers=headers)

except Exception as e:
    print(f"Erro: {e}")
