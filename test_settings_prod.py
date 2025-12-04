import requests

API_URL = "https://chatbot-production-e324.up.railway.app"

def test_settings():
    print(f"Testando API em: {API_URL}")
    
    # 1. GET Settings
    try:
        print("GET /settings...")
        resp = requests.get(f"{API_URL}/settings")
        if resp.status_code == 200:
            print(f"✅ Sucesso! Dados: {resp.json().keys()}")
        else:
            print(f"❌ Falha GET: {resp.status_code} - {resp.text}")
            return
    except Exception as e:
        print(f"❌ Erro de conexão GET: {e}")
        return

    # 2. POST Settings
    new_settings = {
        "system_prompt": "Teste de atualização via script.",
        "active": True
    }
    
    try:
        print("POST /settings...")
        resp = requests.post(f"{API_URL}/settings", json=new_settings)
        if resp.status_code == 200:
            print(f"✅ Sucesso POST! Resposta: {resp.json()}")
        else:
            print(f"❌ Falha POST: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"❌ Erro de conexão POST: {e}")

if __name__ == "__main__":
    test_settings()
