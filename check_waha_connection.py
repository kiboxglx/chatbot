
import os
import requests
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("WHATSAPP_API_URL")
API_KEY = "THISISMYSECURETOKEN" # Padrão do WAHA
SESSION = "default"

print(f"--- Diagnóstico de Conexão ---")
print(f"URL Alvo: {URL}")

if not URL:
    print("❌ ERRO: WHATSAPP_API_URL não está no arquivo .env")
    exit(1)

# 1. Verificar se é WAHA e listar sessões
try:
    print("\n1. Testando endpoint /api/sessions (WAHA)...")
    headers = {"X-Api-Key": API_KEY}
    resp = requests.get(f"{URL}/api/sessions", headers=headers, timeout=10)
    
    print(f"   Status Code: {resp.status_code}")
    if resp.status_code == 200:
        print(f"   ✅ Resposta Recebida: {resp.json()}")
        sessions = resp.json()
        
        # Verifica se 'default' existe
        session_found = False
        for s in sessions:
            if s.get('name') == SESSION:
                session_found = True
                print(f"   ✅ Sessão '{SESSION}' encontrada! Status: {s.get('status')}")
                break
        
        if not session_found:
            print(f"   ⚠️ Sessão '{SESSION}' NÃO encontrada. O bot usa 'default' por padrão.")
            
    else:
        print(f"   ❌ Não parece ser WAHA ou chave incorreta. Body: {resp.text}")

except Exception as e:
    print(f"   ❌ Erro ao conectar: {e}")

# 2. Verificar Webhook
try:
    print("\n2. Tentando ler configurações da sessão 'default'...")
    # WAHA não tem endpoint padronizado simples para 'get webhook', mas podemos tentar inferir ou ver logs
    # Se a sessão existe, vamos tentar ver o screenshot para garantir que está rodando
    if resp.status_code == 200:
        resp_screen = requests.get(f"{URL}/api/screenshot?session={SESSION}", headers=headers, timeout=10)
        if resp_screen.status_code == 200:
            print("   ✅ Screenshot disponível (Sessão ativa e navegador rodando).")
        else:
            print(f"   ⚠️ Screenshot indisponível. Status: {resp_screen.status_code}")

except Exception as e:
    print(f"   ❌ Erro no teste de screenshot: {e}")
