import requests
import time

EVOLUTION_URL = "https://evolution-api-production-e43e.up.railway.app"
API_KEY = "123Cartoon*"
INSTANCE = "chatbot"

headers = {"apikey": API_KEY}

print("=== MONITORAMENTO DE CONEXÃO ===\n")
print("Verificando status a cada 10 segundos...")
print("Pressione Ctrl+C para parar\n")

try:
    while True:
        try:
            resp = requests.get(f"{EVOLUTION_URL}/instance/connectionState/{INSTANCE}", headers=headers, timeout=5)
            
            if resp.status_code == 200:
                data = resp.json()
                state = data.get('instance', {}).get('state', data.get('state', 'unknown'))
                
                timestamp = time.strftime("%H:%M:%S")
                
                if state == 'open':
                    print(f"[{timestamp}] ✅ Conectado")
                elif state == 'close':
                    print(f"[{timestamp}] ❌ DESCONECTADO - Tentando reconectar...")
                    
                    # Tenta reconectar
                    connect_resp = requests.get(f"{EVOLUTION_URL}/instance/connect/{INSTANCE}", headers=headers, timeout=10)
                    if connect_resp.status_code == 200:
                        print(f"[{timestamp}] 🔄 Novo QR Code gerado! Escaneie novamente.")
                    else:
                        print(f"[{timestamp}] ⚠️  Erro ao gerar QR Code: {connect_resp.status_code}")
                else:
                    print(f"[{timestamp}] ⏳ Estado: {state}")
            else:
                print(f"[{time.strftime('%H:%M:%S')}] ⚠️  Erro ao verificar status: {resp.status_code}")
                
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] ❌ Erro: {e}")
        
        time.sleep(10)  # Verifica a cada 10 segundos
        
except KeyboardInterrupt:
    print("\n\nMonitoramento encerrado.")
