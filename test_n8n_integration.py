import requests
import json
import time

print("="*60)
print("TESTE DE INTEGRAÇÃO n8n + Backend Python")
print("="*60)

# 1. Verificar se n8n está rodando
print("\n[1/4] Verificando n8n...")
try:
    response = requests.get("http://localhost:5678")
    if response.status_code == 200:
        print("✅ n8n está rodando em http://localhost:5678")
        print("   Acesse com: admin / chatbot2024")
    else:
        print(f"⚠️  n8n respondeu com status {response.status_code}")
except Exception as e:
    print(f"❌ n8n não está acessível: {e}")

# 2. Verificar Backend Python
print("\n[2/4] Verificando Backend Python...")
try:
    response = requests.get("http://localhost:8000")
    if response.status_code == 200:
        print("✅ Backend Python está rodando")
    else:
        print(f"⚠️  Backend respondeu com status {response.status_code}")
except Exception as e:
    print(f"❌ Backend não está acessível: {e}")
    print("   Execute: python -m uvicorn main:app --port 8000 --reload")

# 3. Verificar Evolution API
print("\n[3/4] Verificando Evolution API...")
try:
    response = requests.get("http://localhost:8080")
    if response.status_code == 200:
        print("✅ Evolution API está rodando")
    else:
        print(f"⚠️  Evolution respondeu com status {response.status_code}")
except Exception as e:
    print(f"❌ Evolution não está acessível: {e}")

# 4. Testar Backend diretamente
print("\n[4/4] Testando Backend Python...")
try:
    payload = {
        "remoteJid": "5511999999999",
        "conversation": "Preciso da segunda via do DAS"
    }
    response = requests.post("http://localhost:8000/webhook", json=payload)
    if response.status_code == 200:
        data = response.json()
        print("✅ Backend processou a mensagem:")
        print(f"   Status: {data.get('status')}")
        print(f"   Cliente: {data.get('client', 'Não encontrado')}")
        print(f"   Intent: {data.get('intent')}")
    else:
        print(f"⚠️  Backend respondeu com status {response.status_code}")
        print(f"   Resposta: {response.text}")
except Exception as e:
    print(f"❌ Erro ao testar backend: {e}")

print("\n" + "="*60)
print("PRÓXIMOS PASSOS:")
print("="*60)
print("1. Acesse http://localhost:5678")
print("2. Login: admin / chatbot2024")
print("3. Importe o workflow: n8n-workflow-chatbot.json")
print("4. Ative o workflow")
print("5. Configure o webhook na Evolution API")
print("="*60)
