from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

app = FastAPI(
    title="Secretária Financeira Virtual",
    description="Bot de Gestão de Gastos e Relatórios via WhatsApp",
    version="1.0.0"
)

# 1. HEALTHCHECK (Sempre no topo para Railway)
@app.get("/api/health")
def health_check():
    return {"status": "online", "message": "Secretária Financeira Ativa"}

@app.get("/api/debug/events")
def get_debug_events():
    from app.api.webhook import RECENT_EVENTS
    return {"recent_events": RECENT_EVENTS}

# 2. EVENTOS DE STARTUP
@app.on_event("startup")
async def startup_event():
    import threading
    from app.core.init_db import init_db
    print("🚀 Verificando Banco de Dados...")
    # Executa em thread separada para não travar o loop principal (importante para Railway)
    threading.Thread(target=init_db).start()

# 3. MIDDLEWARES
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. ROTEADORES DE API
from app.api import webhook, clients, settings, error_handler, management, tools

app.include_router(webhook.router)
app.include_router(clients.router)
app.include_router(settings.router)
app.include_router(error_handler.router)
app.include_router(management.router)
app.include_router(tools.router)

# 5. SERVINDO O FRONTEND (SPA)
# Verifica se a pasta de build existe
frontend_path = "frontend/dist"
if os.path.exists(frontend_path):
    print("✅ Frontend detectado. Configurando rotas SPA...")
    app.mount("/assets", StaticFiles(directory=f"{frontend_path}/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Tenta servir arquivo estático se existir
        file_path = os.path.join(frontend_path, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        # Fallback para index.html (React Router)
        return FileResponse(os.path.join(frontend_path, "index.html"))
else:
    print("ℹ️ Frontend não encontrado (frontend/dist). Servindo roteador raiz.")
    @app.get("/")
    def read_root():
        return {"status": "Online", "mode": "API Only"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
