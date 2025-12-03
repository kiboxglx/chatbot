import sys
import os
from dotenv import load_dotenv

# Add current directory to sys.path
sys.path.append(os.getcwd())

from app.services.ai_service import BrainService

def test_openai():
    print("Iniciando teste de conexão com OpenAI...")
    try:
        brain = BrainService()
        # Mascarar a chave para segurança no log
        key = brain.client.api_key
        if key:
            print(f"Chave API configurada: {key[:8]}...{key[-4:]}")
        else:
            print("ERRO: Chave API não encontrada!")
            return

        print("Enviando requisição de teste...")
        # A mensagem é clara para gerar 2_VIA_BOLETO
        intencao = brain.classificar_intencao("Quero a segunda via do boleto")
        print(f"Resultado da Classificação: {intencao}")
        
    except Exception as e:
        print(f"\nERRO FATAL NO SCRIPT DE TESTE: {e}")

if __name__ == "__main__":
    test_openai()
