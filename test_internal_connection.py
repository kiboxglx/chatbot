import requests

# URL interna do Docker
URL = "http://chatbot:8000/tools/consultar_pendencias/00000000000191"

def test_connection():
    try:
        print(f"Tentando conectar em {URL}...")
        response = requests.get(URL, timeout=5)
        
        if response.status_code == 200:
            print("✅ Conexão n8n -> Python OK!")
            print(response.json())
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Erro de Conexão: {e}")

if __name__ == "__main__":
    test_connection()
