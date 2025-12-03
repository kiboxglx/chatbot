import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("Listando modelos disponíveis...")
with open("models.txt", "w") as f:
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
        print("Modelos salvos em models.txt")
    except Exception as e:
        print(f"Erro ao listar modelos: {e}")
