import requests

URLS = [
    "https://chatbot-production.up.railway.app",
    "https://chatbot-production-e324.up.railway.app"
]

def check_urls():
    print("🔍 Verificando URLs do Backend...\n")
    
    for url in URLS:
        try:
            print(f"Testando: {url} ...")
            response = requests.get(f"{url}/", timeout=5)
            if response.status_code == 200:
                print(f"✅ ONLINE! Resposta: {response.json()}")
            else:
                print(f"❌ Erro: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Falha: {e}")
        print("-" * 30)

if __name__ == "__main__":
    check_urls()
