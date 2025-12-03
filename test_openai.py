import os
from openai import OpenAI
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

print(f"Chave encontrada: {api_key[:5]}...{api_key[-4:] if api_key else 'NENHUMA'}")

if not api_key:
    print("❌ ERRO: Nenhuma OPENAI_API_KEY encontrada no arquivo .env")
    exit(1)

client = OpenAI(api_key=api_key)

try:
    print("Tentando falar com a OpenAI (gpt-4o-mini)...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Diga 'Olá, funcionou!' se você estiver me ouvindo."}
        ]
    )
    print("\n✅ SUCESSO! Resposta da IA:")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"\n❌ ERRO ao conectar na OpenAI: {e}")
