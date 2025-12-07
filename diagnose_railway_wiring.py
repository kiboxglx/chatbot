
import requests
import json

WAHA_URL = "https://devlikeaprowaha-production-69c9.up.railway.app"
CHATBOT_URL = "https://chatbot-production-e324.up.railway.app"
API_KEY = "THISISMYSECURETOKEN"

print(f"🕵️‍♂️ INICIANDO DIAGNÓSTICO DE INTEGRAÇÃO (RAILWAY)\n")

# 1. Verificar se o Chatbot está no ar
print(f"1. Verificando saúde do Chatbot ({CHATBOT_URL})...")
try:
    # Tenta bater no root ou docs
    resp_bot = requests.get(f"{CHATBOT_URL}/docs", timeout=10)
    if resp_bot.status_code == 200:
        print("   ✅ Chatbot está ONLINE e acessível.")
    else:
        print(f"   ⚠️ Chatbot respondeu com status: {resp_bot.status_code}")
except Exception as e:
    print(f"   ❌ Erro ao acessar Chatbot: {e}")
    print("   (Isso pode indicar que o deploy falhou ou o serviço está fora do ar)")

# 2. Verificar Configuração do Webhook no WAHA
print(f"\n2. Verificando configuração do Webhook no WAHA...")
try:
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }
    # Endpoint para pegar sessões e configs
    resp_waha = requests.get(f"{WAHA_URL}/api/sessions?all=true", headers=headers, timeout=10)
    
    if resp_waha.status_code == 200:
        sessions = resp_waha.json()
        print(f"   ✅ WAHA Acessível. Analisando sessões...")
        
        found_problem = False
        for session in sessions:
            name = session.get('name')
            status = session.get('status')
            config = session.get('config', {})
            webhooks = config.get('webhooks', [])
            
            print(f"\n   [Sessão: {name} | Status: {status}]")
            
            if not webhooks:
                print("   ❌ ALERTA: Nenhum webhook configurado nesta sessão!")
                found_problem = True
            else:
                for hook in webhooks:
                    url = hook.get('url')
                    print(f"      🔗 Webhook alvo: {url}")
                    
                    expected_url = f"{CHATBOT_URL}/webhook"
                    if url != expected_url:
                        print(f"      ❌ ERRADO! Deveria ser: {expected_url}")
                        found_problem = True
                    else:
                        print(f"      ✅ URL Correta.")
                        
            # Verificar eventos
            # (WAHA geralmente envia tudo se não especificado, ou podemos checar 'events')
            
        if not found_problem:
            print("\n   ✅ A configuração do Webhook parece PERFEITA.")
        else:
            print("\n   ❌ FORAM ENCONTRADOS ERROS NA CONFIGURAÇÃO DO WEBHOOK.")
            
            # Tentar corrigir automaticamente
            print("   🔧 Tentando corrigir webhook automaticamente...")
            correct_webhook_payload = {
                "url": f"{CHATBOT_URL}/webhook",
                "events": ["message", "message.any"] # Eventos padrão WAHA
            }
            # OBS: WAHA set webhook é via POST /api/sessions/{session}/webhook ou PATCH config
            # Vamos tentar setar para a sessão 'default'
            
            url_set = f"{WAHA_URL}/api/sessions/default/webhook" 
            # Nota: Endpoint exato pode variar na versão, tentando set config
            patch_payload = {
                "config": {
                    "webhooks": [correct_webhook_payload]
                }
            }
             # Tentar PATCH session config
            resp_patch = requests.patch(f"{WAHA_URL}/api/sessions/default", json=patch_payload, headers=headers)
            if resp_patch.status_code == 200:
                 print("   ✅ Webhook corrigido com sucesso!")
            else:
                 print(f"   ⚠️ Falha ao corrigir webhook: {resp_patch.text}")

    else:
        print(f"   ❌ Erro ao acessar WAHA: {resp_waha.status_code}")

except Exception as e:
    print(f"   ❌ Erro na verificação do WAHA: {e}")

print("\n🏁 FIM DO DIAGNÓSTICO")
