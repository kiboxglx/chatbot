import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def test_ai():
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"Chave carregada: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")
    
    if not api_key:
        print("❌ Sem chave API")
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        
        print("🤖 Enviando mensagem para o Gemini...")
        response = model.generate_content("Olá, diga 'Estou funcionando' se você me ouvir.")
        
        print(f"✅ Resposta: {response.text}")
        
    except Exception as e:
        print(f"❌ Erro ao conectar no Gemini: {e}")

if __name__ == "__main__":
    test_ai()
