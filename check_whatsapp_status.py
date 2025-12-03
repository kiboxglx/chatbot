import requests
import json

API_URL = "http://localhost:8080"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"

def connect_instance():
    headers = {"apikey": API_KEY}
    try:
        print("Tentando conectar instância 'chatbot'...")
        response = requests.get(f"{API_URL}/instance/connect/chatbot", headers=headers)
        if response.status_code == 200:
            data = response.json()
            # O QR code vem em 'base64' ou 'code'
            if 'base64' in data:
                print("QR Code gerado com sucesso (base64 recebido).")
                print("O backend está funcionando. Tente recarregar a página do Manager.")
            else:
                print("Resposta recebida:")
                print(json.dumps(data, indent=2))
        else:
            print(f"Erro ao conectar: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erro de conexão: {e}")

if __name__ == "__main__":
    connect_instance()
