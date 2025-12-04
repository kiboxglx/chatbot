import requests
import os
from dotenv import load_dotenv

load_dotenv()

# URL do Railway
RAILWAY_URL = "https://chatbot-production-e324.up.railway.app"

print("=== DIAGNÓSTICO COMPLETO ===\n")

# 1. Verificar se o backend está online
print("1. Verificando se o backend está online...")
try:
    resp = requests.get(f"{RAILWAY_URL}/", timeout=5)
    print(f"   ✅ Backend online! Status: {resp.status_code}")
except Exception as e:
    print(f"   ❌ Backend offline: {e}")
    exit(1)

# 2. Verificar endpoint de clientes (GET)
print("\n2. Verificando endpoint GET /clients...")
try:
    resp = requests.get(f"{RAILWAY_URL}/clients", timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        clients = resp.json()
        print(f"   ✅ {len(clients)} clientes encontrados")
    else:
        print(f"   ⚠️  Resposta: {resp.text}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 3. Tentar criar um cliente
print("\n3. Tentando criar um cliente de teste...")
payload = {
    "nome": "Cliente Teste Diagnóstico",
    "telefone": "5511988887777",
    "empresa_nome": "Teste LTDA",
    "cnpj_cpf": "99999999000199"
}
try:
    resp = requests.post(f"{RAILWAY_URL}/clients", json=payload, timeout=10)
    print(f"   Status: {resp.status_code}")
    print(f"   Resposta: {resp.text[:200]}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

# 4. Verificar webhook
print("\n4. Verificando status do WhatsApp...")
try:
    resp = requests.get(f"{RAILWAY_URL}/management/status", timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        state = data.get('instance', {}).get('state', data.get('state', 'unknown'))
        print(f"   Estado: {state}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n=== FIM DO DIAGNÓSTICO ===")
