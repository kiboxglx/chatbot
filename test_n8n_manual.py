import requests
import json

# URL do n8n (acessível do host)
N8N_URL = "http://localhost:5678/webhook/whatsapp"

def test_n8n_webhook():
    payload = {
        "data": {
            "key": {
                "remoteJid": "5511999999999@s.whatsapp.net",
                "fromMe": False
            },
            "message": {
                "conversation": "Teste manual do script Python"
            }
        }
    }
    
    try:
        print(f"Enviando POST para {N8N_URL}...")
        response = requests.post(N8N_URL, json=payload)
        
        if response.status_code == 200:
            print("✅ Sucesso! O n8n recebeu a mensagem.")
            print("Resposta:", response.text)
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_n8n_webhook()
