from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente (Importante para DATABASE_URL, etc)
load_dotenv()

app = FastAPI(title="Chatbot Financeiro", version="1.0.0")

@app.get("/api/health")
def health_check():
    return {"status": "online", "message": "Secretária Financeira Ativa"}

@app.on_event("startup")
async def startup_event():
    import threading
    from app.core.init_db import init_db
    print("🚀 Iniciando Banco de Dados...")
    threading.Thread(target=init_db).start()

# Configuração de CORS Básica
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota raiz simples
@app.get("/")
def read_root():
    return {"status": "Chatbot API Barebones", "docs": "/docs"}

# Tentativa de carregar os roteadores de forma silenciada
try:
    from app.api import webhook, clients, settings, error_handler, management
    app.include_router(webhook.router)
    app.include_router(clients.router)
    app.include_router(settings.router)
    app.include_router(error_handler.router)
    app.include_router(management.router)
    print("✅ Roteadores carregados com sucesso.")
except Exception as e:
    print(f"⚠️ ERRO AO CARREGAR ROTEADORES (Continuando em modo seguro): {e}")

# Frontend desativado temporariamente para debugar healthcheck
print("ℹ️ Frontend desativado no modo barebones.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
