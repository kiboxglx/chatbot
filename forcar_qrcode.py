import requests
import json
import time

API_URL = "http://localhost:8080"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"
INSTANCE = "chatbot"

print("="*60)
print("FORÇAR GERAÇÃO DE QR CODE")
print("="*60)

headers = {"apikey": API_KEY}

# 1. Verificar status da instância
print("\n[1/3] Verificando status da instância...")
response = requests.get(f"{API_URL}/instance/fetchInstances", headers=headers)
instances = response.json()

for inst in instances:
    if inst['name'] == INSTANCE:
        print(f"Status: {inst['connectionStatus']}")
        if inst['connectionStatus'] != 'close':
            print("⚠️  Instância não está no estado 'close'")
            print("Vou desconectar e reconectar...")
            
            # Logout
            requests.delete(f"{API_URL}/instance/logout/{INSTANCE}", headers=headers)
            time.sleep(3)

# 2. Deletar e recriar
print("\n[2/3] Recriando instância...")
requests.delete(f"{API_URL}/instance/delete/{INSTANCE}", headers=headers)
time.sleep(2)

body = {
    "instanceName": INSTANCE,
    "token": "",
    "qrcode": True,
    "integration": "WHATSAPP-BAILEYS"
}
response = requests.post(f"{API_URL}/instance/create", json=body, headers=headers)
print(f"Criação: {response.status_code}")

# 3. Aguardar e tentar conectar
print("\n[3/3] Aguardando 5 segundos...")
time.sleep(5)

print("\n" + "="*60)
print("AGORA TENTE NOVAMENTE NO MANAGER:")
print("="*60)
print("1. Feche o modal (X)")
print("2. Atualize a página (F5)")
print("3. Clique novamente na instância 'chatbot'")
print("4. O QR Code deve aparecer!")
print("="*60)
