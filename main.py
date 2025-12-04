from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from app.api import webhook, clients, settings, error_handler, management

app = FastAPI(title="Chatbot Contábil", version="0.1.0")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook.router)
app.include_router(clients.router)
app.include_router(settings.router)
app.include_router(error_handler.router)
app.include_router(management.router)

# --- Frontend Integration (Production) ---
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Verifica se a pasta de build existe (criada no deploy)
if os.path.exists("frontend/dist"):
    # Monta assets estáticos (JS, CSS, Imagens)
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

    # Rota Catch-All para SPA (React)
    # Qualquer rota que não seja API, retorna o index.html
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Se for arquivo conhecido na raiz (ex: favicon.ico), tenta servir
        file_path = f"frontend/dist/{full_path}"
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # Senão, retorna o index.html (React Router assume)
        return FileResponse("frontend/dist/index.html")

@app.get("/api/health")
def health_check():
    return {"status": "online"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
