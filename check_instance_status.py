import requests

EVOLUTION_API_URL = "https://evolution-api-production-e43e.up.railway.app"
INSTANCE = "chatbot"
API_KEY = "123Cartoon*"

def check_instance():
    url = f"{EVOLUTION_API_URL}/instance/fetchInstances"
    headers = {"apikey": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            instances = response.json()
            found = False
            for inst in instances:
                if inst.get('instance', {}).get('instanceName') == INSTANCE:
                    found = True
                    print(f"✅ Instância '{INSTANCE}' encontrada!")
                    print(f"Status: {inst.get('instance', {}).get('status')}")
                    break
            
            if not found:
                print(f"❌ Instância '{INSTANCE}' NÃO encontrada na listagem.")
                
        else:
            print(f"Erro ao listar instâncias: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    check_instance()
