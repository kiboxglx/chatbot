import requests
import json

print("="*60)
print("TESTE COMPLETO - CHATBOT LOCAL")
print("="*60)

# 1. Testar Backend Python
print("\n[1/3] Testando Backend Python...")
try:
    response = requests.get("http://localhost:8000")
    if response.status_code == 200:
        print("✅ Backend Python online")
    else:
        print(f"⚠️  Backend respondeu: {response.status_code}")
except Exception as e:
    print(f"❌ Backend offline: {e}")

# 2. Testar n8n Local
print("\n[2/3] Testando n8n Local...")
try:
    response = requests.get("http://localhost:5678")
    if response.status_code == 200:
        print("✅ n8n Local online")
    else:
        print(f"⚠️  n8n respondeu: {response.status_code}")
except Exception as e:
    print(f"❌ n8n offline: {e}")

# 3. Testar Evolution API
print("\n[3/3] Testando Evolution API...")
try:
    response = requests.get("http://localhost:8080")
    if response.status_code == 200:
        print("✅ Evolution API online")
    else:
        print(f"⚠️  Evolution respondeu: {response.status_code}")
except Exception as e:
    print(f"❌ Evolution offline: {e}")

print("\n" + "="*60)
print("STATUS FINAL")
print("="*60)
print("\n✅ Todos os serviços devem estar online para funcionar!")
print("\nPróximo passo:")
print("1. Configure o webhook na Evolution API")
print("2. Envie uma mensagem de teste do WhatsApp")
print("="*60)
