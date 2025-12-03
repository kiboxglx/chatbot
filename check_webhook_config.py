import requests

API_URL = "http://localhost:8080"
INSTANCE = "chatbot"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"

def check_webhook():
    url = f"{API_URL}/webhook/find/{INSTANCE}"
    headers = {"apikey": API_KEY}
    
    try:
        print(f"Consultando webhook para instância '{INSTANCE}'...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Configuração Atual do Webhook:")
            print(f"URL: {data.get('webhookUrl')}")
            print(f"Habilitado: {data.get('enabled')}")
            print(f"Eventos: {data.get('events')}")
            
            # Validação
            expected_url = "http://chatbot_n8n:5678/webhook/whatsapp"
            # Nota: O n8n pode ser acessado por 'chatbot_n8n' ou 'n8n' dependendo do nome do serviço no docker-compose
            # No seu docker-compose o nome do serviço é 'n8n' e container_name é 'chatbot_n8n'
            # Na rede interna, o host é 'chatbot_n8n' (nome do container) ou 'n8n' (nome do serviço)
            
            if not data.get('enabled'):
                print("\n❌ ALERTA: O webhook está DESABILITADO!")
            elif not data.get('webhookUrl'):
                print("\n❌ ALERTA: Nenhuma URL de webhook configurada!")
            else:
                print("\nℹ️ Verifique se a URL acima corresponde ao seu container n8n.")
                
        else:
            print(f"\n❌ Erro ao consultar: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"\n❌ Erro de conexão: {e}")

if __name__ == "__main__":
    check_webhook()
