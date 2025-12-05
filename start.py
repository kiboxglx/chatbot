import os
import subprocess
import sys

# Adiciona o diretório atual ao PYTHONPATH
sys.path.append(os.getcwd())

print("🚀 Iniciando aplicação via start.py...")

# Pega a porta do ambiente ou usa 8000 como fallback
port = os.getenv("PORT", "8000")

# Comando para iniciar o Uvicorn via módulo Python (mais seguro que chamar o binário direto)
# Removemos o init_db daqui pois já está no evento startup do main.py
cmd = [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", port]

print(f"📦 Executando comando: {' '.join(cmd)}")

try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"❌ Erro ao iniciar a aplicação: {e}")
    sys.exit(1)
except KeyboardInterrupt:
    print("🛑 Aplicação interrompida pelo usuário.")
    sys.exit(0)
