import requests

# Teste de criação de cliente
API_URL = "https://chatbot-production-e324.up.railway.app"

payload = {
    "nome": "Teste Cliente",
    "telefone": "5511999999999",
    "empresa_nome": "Empresa Teste LTDA",
    "cnpj_cpf": "12345678000199"
}

print("Testando criação de cliente...")
try:
    response = requests.post(f"{API_URL}/clients", json=payload, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Erro: {e}")
