import requests
import json
import base64
import time

API_URL = "http://localhost:8080"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"
INSTANCE = "chatbot"

def get_qr():
    headers = {"apikey": API_KEY}
    
    # 1. Tenta conectar (gera o QR)
    print(f"Solicitando QR Code para '{INSTANCE}'...")
    try:
        response = requests.get(f"{API_URL}/instance/connect/{INSTANCE}", headers=headers)
        data = response.json()
        
        if 'base64' in data:
            # Salva a imagem
            b64_data = data['base64'].replace("data:image/png;base64,", "")
            with open("qrcode.png", "wb") as f:
                f.write(base64.b64decode(b64_data))
            print("SUCESSO: QR Code salvo em 'qrcode.png'. Abra este arquivo para escanear!")
            return True
        elif 'code' in data:
             # Às vezes retorna apenas o código para pareamento
             print(f"Código de Pareamento recebido: {data['code']}")
        else:
            print("QR Code não recebido na primeira tentativa. Tentando novamente em 2 segundos...")
            print(f"Resposta: {data}")
            
    except Exception as e:
        print(f"Erro: {e}")
        
    return False

if __name__ == "__main__":
    # Tenta 3 vezes
    for i in range(3):
        if get_qr():
            break
        time.sleep(2)
