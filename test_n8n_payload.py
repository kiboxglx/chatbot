import requests
import json

# URL do Webhook do n8n (ajuste se necessário)
N8N_URL = "http://localhost:5678/webhook/whatsapp"

def test_workflow():
    # Payload simulando Evolution API v1.6+
    payload = {
        "data": {
            "key": {
                "remoteJid": "5511999999999@s.whatsapp.net",
                "fromMe": False
            },
            "pushName": "Cliente Teste",
            "message": {
                "conversation": "Olá, preciso emitir um boleto DAS para o CNPJ 00000000000191 referente a maio de 2025"
            }
        },
        "sender": "5511999999999@s.whatsapp.net"
    }
    
    try:
        print(f"Enviando mensagem de teste para {N8N_URL}...")
        response = requests.post(N8N_URL, json=payload)
        
        if response.status_code == 200:
            print("✅ Mensagem enviada! Verifique o n8n.")
            print("Se o workflow rodar verde, o problema é apenas o formato do JSON da Evolution.")
        else:
            print(f"❌ Erro no n8n: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_workflow()
