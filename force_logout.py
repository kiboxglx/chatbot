import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações (pegando do .env local ou definindo manualmente se precisar)
# IMPORTANTE: Se rodar localmente, a URL deve ser a pública do Railway
EVOLUTION_URL = "https://evolution-api-production-e43e.up.railway.app" 
API_KEY = "123Cartoon*" # A chave que definimos
INSTANCE = "chatbot"

headers = {
    "apikey": API_KEY
}

def force_logout():
    print(f"Tentando desconectar a instância '{INSTANCE}' na URL: {EVOLUTION_URL}")
    
    try:
        # 1. Tenta Logout
        url_logout = f"{EVOLUTION_URL}/instance/logout/{INSTANCE}"
        resp = requests.delete(url_logout, headers=headers)
        print(f"Logout Status: {resp.status_code}")
        print(f"Logout Response: {resp.text}")
        
        # 2. Se não funcionar, tenta deletar a instância para recriar limpa
        if resp.status_code != 200:
            print("Logout falhou ou não estava conectado. Tentando deletar a instância...")
            url_delete = f"{EVOLUTION_URL}/instance/delete/{INSTANCE}"
            resp_del = requests.delete(url_delete, headers=headers)
            print(f"Delete Status: {resp_del.status_code}")
            print(f"Delete Response: {resp_del.text}")

    except Exception as e:
        print(f"Erro ao tentar desconectar: {e}")

if __name__ == "__main__":
    force_logout()
