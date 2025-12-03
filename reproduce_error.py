import requests
import json

N8N_URL = "http://localhost:5678/webhook/whatsapp"

# Payload reconstruído a partir do seu relato
payload = [
  {
    "event": "messages.upsert",
    "instance": "chatbot",
    "data": {
      "key": {
        "remoteJid": "553182119605@s.whatsapp.net",
        "fromMe": False,
        "id": "3A46..."
      },
      "pushName": "Cliente",
      "message": {
        "extendedTextMessage": {
          "text": "Preciso do DAS de maio de 2025 para o CNPJ 00000000000191",
          "contextInfo": {
             "stanzaId": "...",
             "participant": "..."
          }
        },
        "messageContextInfo": {
          "deviceListMetadata": {
             "senderKeyHash": "..."
          }
        }
      },
      "messageType": "extendedTextMessage",
      "messageTimestamp": 1764623037,
      "owner": "chatbot",
      "source": "ios"
    },
    "destination": "http://host.docker.internal:5678/webhook/whatsapp",
    "date_time": "2025-12-01T18:03:58.422Z",
    "sender": "553182119605@s.whatsapp.net",
    "server_url": "http://localhost:8080",
    "apikey": "FF12A686..."
  }
]

def test_repro():
    try:
        print(f"Enviando payload complexo para {N8N_URL}...")
        # O n8n recebe o payload como JSON body
        response = requests.post(N8N_URL, json=payload)
        
        if response.status_code == 200:
            print("✅ Enviado com sucesso! Verifique se o n8n processou ou deu erro.")
            print(response.text)
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_repro()
