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

@app.get("/")
def read_root():
    """Rota de verificação de saúde da API."""
    return {"status": "online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
