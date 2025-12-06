import requests
import os

# Configurações (Hardcoded para teste local)
BASE_URL = "https://server-production-c7e4.up.railway.app"
SESSION = "bot_whatsapp"

KEYS_TO_TEST = [
    "minhasenha123",
    "123Cartoon*",
    "THISISMYSECURETOKEN", # Default do WPPConnect
    "mysecretkey"
]

def test_connection():
    print(f"--- DEBUG WPPCONNECT ---")
    print(f"URL Base: {BASE_URL}")
    print(f"Session: {SESSION}")

    for key in KEYS_TO_TEST:
        url = f"{BASE_URL}/api/{SESSION}/{key}/generate-token"
        print(f"\n[?] Testando Key: '{key}'")
        
        try:
            resp = requests.post(url, json={"secret": key}, timeout=10)
            print(f"   Status: {resp.status_code}")
            
            if resp.status_code in [200, 201]:
                print(f"   ✅ SUCESSO! A senha correta é: {key}")
                print(f"   Body: {resp.text}")
                return
            else:
                print(f"   ❌ Falhou: {resp.json().get('message', 'Erro desconhecido')}")
                
        except Exception as e:
            print(f"   ❌ ERRO DE CONEXÃO: {e}")


if __name__ == "__main__":
    test_connection()
