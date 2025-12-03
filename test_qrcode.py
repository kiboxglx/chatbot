import requests
import json
import base64
import time

API_URL = "http://localhost:8080"
API_KEY = "429683C4C977415CAAFCCE10F7D57E11"
INSTANCE = "chatbot"

print("="*60)
print("TESTE DE QR CODE - EVOLUTION API")
print("="*60)

headers = {"apikey": API_KEY, "Content-Type": "application/json"}

# 1. Deletar instância antiga
print("\n[1/4] Limpando instâncias antigas...")
try:
    requests.delete(f"{API_URL}/instance/delete/{INSTANCE}", headers=headers)
    time.sleep(2)
    print("✅ Instância antiga removida")
except:
    print("⚠️  Nenhuma instância para remover")

# 2. Criar nova instância
print("\n[2/4] Criando nova instância...")
body = {
    "instanceName": INSTANCE,
    "token": "",
    "qrcode": True,
    "integration": "WHATSAPP-BAILEYS"
}
response = requests.post(f"{API_URL}/instance/create", json=body, headers=headers)
print(f"Status: {response.status_code}")

if response.status_code in [200, 201]:
    print("✅ Instância criada com sucesso!")
else:
    print(f"❌ Erro ao criar instância: {response.text}")
    exit(1)

# 3. Aguardar inicialização
print("\n[3/4] Aguardando inicialização (10 segundos)...")
time.sleep(10)

# 4. Solicitar QR Code
print("\n[4/4] Solicitando QR Code...")
response = requests.get(f"{API_URL}/instance/connect/{INSTANCE}", headers=headers)

print(f"Status: {response.status_code}")

try:
    data = response.json()
    
    if 'base64' in data:
        print("\n" + "="*60)
        print("✅ QR CODE GERADO COM SUCESSO!")
        print("="*60)
        
        # Salvar QR Code como imagem
        b64_data = data['base64'].replace("data:image/png;base64,", "")
        with open("qrcode_whatsapp.png", "wb") as f:
            f.write(base64.b64decode(b64_data))
        
        print("\n📱 QR Code salvo em: qrcode_whatsapp.png")
        print("\nABRA O ARQUIVO E ESCANEIE COM SEU WHATSAPP!")
        print("\nComo escanear:")
        print("1. Abra o WhatsApp no celular")
        print("2. Vá em 'Aparelhos Conectados'")
        print("3. Toque em 'Conectar um aparelho'")
        print("4. Escaneie o QR Code do arquivo qrcode_whatsapp.png")
        
    elif 'code' in data:
        print("\n" + "="*60)
        print("✅ CÓDIGO DE PAREAMENTO GERADO!")
        print("="*60)
        print(f"\nCÓDIGO: {data['code']}")
        print("\nComo usar:")
        print("1. Abra o WhatsApp no celular")
        print("2. Vá em 'Aparelhos Conectados'")
        print("3. Toque em 'Conectar com número de telefone'")
        print("4. Digite o código acima")
        
    else:
        print("\n⚠️  Resposta inesperada:")
        print(json.dumps(data, indent=2))
        
        # Tentar via Manager
        print("\n💡 ALTERNATIVA:")
        print("Acesse o Manager da Evolution API:")
        print(f"URL: {API_URL}/manager")
        print(f"API Key: {API_KEY}")
        print("Lá você pode ver o QR Code visualmente!")
        
except Exception as e:
    print(f"\n❌ Erro ao processar resposta: {e}")
    print(f"Resposta: {response.text}")

print("\n" + "="*60)
