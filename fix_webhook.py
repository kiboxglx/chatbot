import requests

API_URL = "http://localhost:8080"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"
INSTANCE = "chatbot"

headers = {
    "apikey": API_KEY
}

try:
    response = requests.get(f"{API_URL}/webhook/find/{INSTANCE}", headers=headers)
    if response.status_code == 200:
        config = response.json()
        print("--- CONFIGURAÇÃO ATUAL DO WEBHOOK ---")
        print(f"URL: {config.get('url')}")
        print(f"Ativo: {config.get('enabled')}")
        
        if "5678" in config.get('url', ''):
            print("\n⚠️ ALERTA: O Webhook ainda está apontando para o n8n (porta 5678)!")
            print("Vou corrigir para o Python (porta 8000)...")
            
            # Corrige para o Python
            new_config = {
                "url": "http://host.docker.internal:8000/webhook",
                "webhookByEvents": False,
                "events": ["MESSAGES_UPSERT"],
                "enabled": True
            }
            res = requests.post(f"{API_URL}/webhook/set/{INSTANCE}", json=new_config, headers=headers)
            print(f"Correção: {res.status_code} - {res.json()}")
        else:
            print("\n✅ O Webhook parece estar correto (não está no n8n).")
            
    else:
        print(f"Erro ao ler webhook: {response.text}")

except Exception as e:
    print(f"Erro de conexão: {e}")
