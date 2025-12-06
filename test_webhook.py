import requests
import os

# SUBSTITUA PELO SEU DOMÍNIO REAL DO CHATBOT
CHATBOT_URL = "https://chatbot-production-e324.up.railway.app" 

def test_webhook():
    url = f"{CHATBOT_URL}/webhook"
    
    # Payload simulando o formato do WPPConnect
    payload = {
        "event": "onMessage",
        "session": "bot_whatsapp",
        "data": {
            "id": "false_123456789@c.us_ABCDEF",
            "from": "5511999999999@c.us",
            "to": "5511888888888@c.us",
            "body": "Olá, preciso de ajuda com meu DAS",
            "isGroup": False,
            "sender": {
                "name": "Cliente Teste",
                "pushname": "Cliente Teste"
            },
            "timestamp": 1700000000
        }
    }
    
    print(f"📡 Enviando mensagem de teste para: {url}")
    try:
        resp = requests.post(url, json=payload, timeout=60)
        print(f"Status: {resp.status_code}")
        print(f"Resposta: {resp.text}")
        
        if resp.status_code == 200:
            print("✅ Webhook recebeu a mensagem com sucesso!")
        else:
            print("❌ Webhook rejeitou ou deu erro.")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_webhook()
