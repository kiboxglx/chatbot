import requests
import json

# URL base do chatbot (ajuste se necessário)
BASE_URL = "http://localhost:8000"

def test_gerar_relatorio():
    print("\n--- Testando Gerar Relatório (DAS) ---")
    url = f"{BASE_URL}/tools/gerar_relatorio"
    payload = {
        "cnpj": "00000000000191",
        "tipo": "das",
        "mes": 5,
        "ano": 2025
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Sucesso!")
            print(f"URL Download Local: {data['download_url']}")
            print(f"URL Download Docker: {data['internal_url']}")
            
            # Tenta baixar o arquivo para verificar se a rota estática funciona
            file_url = data['download_url']
            file_resp = requests.get(file_url)
            if file_resp.status_code == 200:
                print("✅ Arquivo acessível via HTTP!")
            else:
                print(f"❌ Erro ao baixar arquivo: {file_resp.status_code}")
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

def test_consultar_pendencias():
    print("\n--- Testando Consultar Pendências ---")
    cnpj = "00000000000191"
    url = f"{BASE_URL}/tools/consultar_pendencias/{cnpj}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("✅ Sucesso!")
            print(f"Pendências: {data['pendencias']}")
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    print("Iniciando testes das ferramentas...")
    test_gerar_relatorio()
    test_consultar_pendencias()
