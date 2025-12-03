import requests
import json
import time

API_URL = "http://localhost:8080"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"
INSTANCE = "chatbot"
PHONE = "5531982119605"

def get_code():
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}
    
    # 1. Deleta
    print(f"Limpando instância '{INSTANCE}'...")
    requests.delete(f"{API_URL}/instance/delete/{INSTANCE}", headers=headers)
    time.sleep(2)
    
    # 2. Cria
    print("Criando nova instância...")
    body = {
        "instanceName": INSTANCE,
        "token": "",
        "qrcode": False,
        "integration": "WHATSAPP-BAILEYS",
        "number": PHONE
    }
    create_res = requests.post(f"{API_URL}/instance/create", json=body, headers=headers)
    print(f"Criação Status: {create_res.status_code}")
    
    if create_res.status_code != 201:
        return

    # 3. Connect (com delay)
    print("Aguardando 5 segundos para inicialização...")
    time.sleep(5)
    
    print(f"Solicitando código...")
    # Tenta endpoint específico de pairing code se existir (algumas versoes usam /instance/pairingCode/{instance})
    # Mas vamos tentar o connect padrao novamente
    connect_res = requests.get(f"{API_URL}/instance/connect/{INSTANCE}", headers=headers)
    print(f"Connect Body: {connect_res.text}")

if __name__ == "__main__":
    get_code()
