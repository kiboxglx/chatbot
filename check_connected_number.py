
import requests

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"
SESSION = "default"

print(f"🔍 Verificando número conectado na sessão '{SESSION}'...")

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

try:
    # 1. Obter informações de "ME" (Quem sou eu?)
    url_me = f"{WAHA_URL}/api/sessions/{SESSION}/me"
    resp = requests.get(url_me, headers=headers, timeout=10)
    
    if resp.status_code == 200:
        me_data = resp.json()
        print("\n✅ CONECTADO COM SUCESSO!")
        print(f"📱 Número: {me_data.get('id', 'Desconhecido')}")
        print(f"👤 Nome (PushName): {me_data.get('pushName', 'Sem nome')}")
        print(f"📸 Foto de Perfil: {me_data.get('profilePicUrl', 'Sem foto')}")
    else:
        print(f"❌ Não foi possível obter dados do número. Status: {resp.status_code}")
        print(f"Resposta: {resp.text}")

        # Fallback: Checar status da sessão
        resp_session = requests.get(f"{WAHA_URL}/api/sessions/{SESSION}", headers=headers)
        print(f"\nStatus da Sessão: {resp_session.json()}")

except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
