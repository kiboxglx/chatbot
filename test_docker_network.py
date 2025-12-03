"""
Script para validar a conectividade entre os containers Docker.
Execute DENTRO do container do n8n ou chatbot.
"""

import requests
import sys

def test_connection(service_name: str, url: str) -> bool:
    """Testa conexão com um serviço."""
    try:
        print(f"🔍 Testando {service_name}...")
        response = requests.get(url, timeout=5)
        print(f"✅ {service_name} - Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name} - ERRO: {e}")
        return False

def main():
    """Executa todos os testes de conectividade."""
    print("=" * 60)
    print("🐳 VALIDAÇÃO DE CONECTIVIDADE - DOCKER NETWORK")
    print("=" * 60)
    
    tests = [
        ("Evolution API", "http://evolution-api:8080"),
        ("Chatbot Backend", "http://chatbot:8000/health"),
        ("n8n", "http://n8n:5678"),
    ]
    
    results = []
    for service, url in tests:
        results.append(test_connection(service, url))
        print()
    
    print("=" * 60)
    if all(results):
        print("✅ TODOS OS SERVIÇOS ESTÃO ACESSÍVEIS!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ ALGUNS SERVIÇOS ESTÃO INACESSÍVEIS!")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
