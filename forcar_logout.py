import requests

EVOLUTION_URL = "https://evolution-api-production-e43e.up.railway.app"
API_KEY = "123Cartoon*"
INSTANCE = "chatbot"

headers = {"apikey": API_KEY}

print("=== FORÇAR LOGOUT DA INSTÂNCIA ===\n")
print(f"Evolution API: {EVOLUTION_URL}")
print(f"Instância: {INSTANCE}\n")

# 1. Verificar status atual
print("1. Verificando status atual...")
try:
    resp = requests.get(f"{EVOLUTION_URL}/instance/connectionState/{INSTANCE}", headers=headers, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        state = data.get('instance', {}).get('state', data.get('state', 'unknown'))
        print(f"   Estado atual: {state}\n")
except Exception as e:
    print(f"   Erro: {e}\n")

# 2. Forçar logout
print("2. Forçando logout...")
try:
    resp = requests.delete(f"{EVOLUTION_URL}/instance/logout/{INSTANCE}", headers=headers, timeout=10)
    print(f"   Status: {resp.status_code}")
    print(f"   Resposta: {resp.text}\n")
    
    if resp.status_code in [200, 201]:
        print("   ✅ Logout realizado com sucesso!")
    else:
        print("   ⚠️  Possível erro, mas vamos tentar deletar a instância...")
except Exception as e:
    print(f"   Erro: {e}\n")

# 3. Deletar a instância completamente (opcional, mas garante limpeza total)
print("3. Deletando a instância completamente...")
try:
    resp = requests.delete(f"{EVOLUTION_URL}/instance/delete/{INSTANCE}", headers=headers, timeout=10)
    print(f"   Status: {resp.status_code}")
    print(f"   Resposta: {resp.text}\n")
    
    if resp.status_code in [200, 201]:
        print("   ✅ Instância deletada com sucesso!")
except Exception as e:
    print(f"   Erro: {e}\n")

print("="*60)
print("\n✅ PRONTO! A instância foi limpa.")
print("\n📱 PRÓXIMOS PASSOS:")
print("   1. Acesse o dashboard no Vercel")
print("   2. Vá em 'Conexão WhatsApp'")
print("   3. Clique em 'Gerar QR Code'")
print("   4. Escaneie com o WhatsApp do escritório")
print("\n" + "="*60)
