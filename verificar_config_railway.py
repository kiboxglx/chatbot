import requests

print("=== VERIFICAÇÃO DE CONFIGURAÇÃO DO RAILWAY ===\n")

BACKEND_URL = "https://chatbot-production-e324.up.railway.app"

print("Verificando se o backend está usando as variáveis corretas...\n")

# Teste 1: Verificar se o backend está online
print("1. Backend online?")
try:
    resp = requests.get(f"{BACKEND_URL}/", timeout=5)
    print(f"   ✅ Sim! Status: {resp.status_code}\n")
except Exception as e:
    print(f"   ❌ Não: {e}\n")
    exit(1)

# Teste 2: Verificar endpoint de status do WhatsApp
print("2. Backend consegue acessar a Evolution API?")
try:
    resp = requests.get(f"{BACKEND_URL}/management/status", timeout=10)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        state = data.get('instance', {}).get('state', data.get('state', 'unknown'))
        print(f"   ✅ Sim! Estado do WhatsApp: {state}\n")
    else:
        print(f"   ⚠️  Resposta: {resp.text[:200]}\n")
        print("   💡 Isso significa que o backend NÃO está conseguindo")
        print("      acessar a Evolution API. Verifique as variáveis:\n")
        print("      - WHATSAPP_API_URL")
        print("      - AUTHENTICATION_API_KEY\n")
except Exception as e:
    print(f"   ❌ Erro: {e}\n")

# Teste 3: Verificar se o webhook está recebendo mensagens
print("3. Para testar se o webhook funciona:")
print("   - Envie uma mensagem para o WhatsApp conectado")
print("   - Aguarde 5 segundos")
print("   - Se o bot responder = ✅ TUDO FUNCIONANDO!")
print("   - Se não responder = ⚠️ Verifique os logs do Railway\n")

print("="*60)
print("\n💡 PRÓXIMOS PASSOS:\n")
print("1. Vá no Railway > chatbot > Variables")
print("2. Adicione/Atualize:")
print("   WHATSAPP_API_URL=https://evolution-api-production-e43e.up.railway.app")
print("   AUTHENTICATION_API_KEY=123Cartoon*")
print("3. Aguarde o redeploy (1-2 min)")
print("4. Execute este script novamente")
print("\n" + "="*60)
