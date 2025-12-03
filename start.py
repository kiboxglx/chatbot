import os
import subprocess
import sys

# Adiciona o diretório atual ao PYTHONPATH
sys.path.append(os.getcwd())

# Inicializa o banco de dados
print("Inicializando banco de dados...")
try:
    from app.core.init_db import init_db
    init_db()
except Exception as e:
    print(f"Erro ao inicializar banco de dados: {e}")

port = os.getenv("PORT", "8000")
subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", port])
