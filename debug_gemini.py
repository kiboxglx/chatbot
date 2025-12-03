import sys
import os
from dotenv import load_dotenv

# Add current directory to sys.path
sys.path.append(os.getcwd())

from app.services.ai_service import BrainService

def test_gemini():
    print("Iniciando teste de conexão com Google Gemini...")
    try:
        brain = BrainService()
        key = os.getenv("GEMINI_API_KEY")
        
        if key:
            print(f"Chave API configurada: {key[:8]}...{key[-4:]}")
        else:
            print("ERRO: Chave API não encontrada!")
            return

        print("Enviando requisição de teste...")
        # A mensagem é a mesma do simulador
        intencao = brain.classificar_intencao("Preciso da segunda via do DAS")
        print(f"Resultado da Classificação: {intencao}")
        
    except Exception as e:
        print(f"\nERRO FATAL NO SCRIPT DE TESTE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini()
