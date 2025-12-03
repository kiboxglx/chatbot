"""
Expõe o backend Python usando Cloudflare Tunnel (cloudflared)
Alternativa gratuita ao ngrok que não precisa de conta.
"""
import subprocess
import time
import re
import sys

print("="*60)
print("EXPOSIÇÃO DO BACKEND - CLOUDFLARE TUNNEL")
print("="*60)

print("\n[1/2] Verificando cloudflared...")
try:
    result = subprocess.run(["cloudflared", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        raise FileNotFoundError
    print(f"✅ cloudflared encontrado")
except FileNotFoundError:
    print("❌ cloudflared não está instalado!")
    print("\nINSTALAÇÃO RÁPIDA:")
    print("Execute no PowerShell (como Administrador):")
    print("winget install --id Cloudflare.cloudflared")
    print("\nOu baixe de: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/")
    sys.exit(1)

print("\n[2/2] Iniciando tunnel...")
print("⚠️  Aguarde alguns segundos...")

# Inicia cloudflared
process = subprocess.Popen(
    ["cloudflared", "tunnel", "--url", "http://localhost:8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

print("\n" + "="*60)
print("PROCURANDO URL PÚBLICA...")
print("="*60)

# Lê a saída em tempo real procurando pela URL
url_found = False
for line in process.stdout:
    print(line.strip())
    
    # Procura pela URL na saída
    if "trycloudflare.com" in line or "https://" in line:
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            public_url = match.group(0)
            url_found = True
            print("\n" + "="*60)
            print("✅ BACKEND EXPOSTO COM SUCESSO!")
            print("="*60)
            print(f"\nURL PÚBLICA:")
            print(f"{public_url}")
            print(f"\nUSE NO N8N:")
            print(f"{public_url}/webhook")
            print("="*60)
            print("\n⚠️  Mantenha esta janela aberta!")
            print("⏸️  Pressione Ctrl+C para parar")
            break
    
    # Limite de linhas para evitar loop infinito
    if not url_found and "INF" in line:
        continue

if not url_found:
    print("\n⚠️  URL não encontrada automaticamente")
    print("Verifique a saída acima para a URL que começa com https://")

# Mantém o processo rodando
try:
    process.wait()
except KeyboardInterrupt:
    print("\n\n🛑 Encerrando tunnel...")
    process.terminate()
    print("✅ Finalizado!")
