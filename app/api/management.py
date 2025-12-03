import requests
import base64
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Configurações da Evolution API
# Usa variável de ambiente se existir, senão usa o padrão do Docker local
EVOLUTION_URL = os.getenv("WHATSAPP_API_URL", "http://evolution_api:8080")
API_KEY = os.getenv("AUTHENTICATION_API_KEY", "429683C4C977415CAAFCCE10F7D57E11")
INSTANCE = "chatbot"

headers = {
    "apikey": API_KEY
}

@router.get("/management/status")
def get_status():
    """Verifica se o WhatsApp está conectado"""
    try:
        url = f"{EVOLUTION_URL}/instance/connectionState/{INSTANCE}"
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            return resp.json()
        return {"instance": INSTANCE, "state": "DISCONNECTED"}
    except Exception as e:
        print(f"Erro ao checar status: {e}")
        return {"state": "ERROR", "details": str(e)}

@router.get("/management/qrcode")
def get_qrcode():
    """Gera o QR Code para conexão"""
    try:
        # Primeiro, garante que a instância existe
        requests.post(
            f"{EVOLUTION_URL}/instance/create", 
            json={"instanceName": INSTANCE, "qrcode": True}, 
            headers=headers
        )
        
        # Pede o connect (retorna base64 ou json)
        url = f"{EVOLUTION_URL}/instance/connect/{INSTANCE}"
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            # Evolution v1.7 retorna { "base64": "..." } ou { "code": "..." }
            return data
        
        raise HTTPException(status_code=400, detail="Não foi possível gerar QR Code")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/management/logout")
def logout():
    """Desconecta o WhatsApp"""
    try:
        url = f"{EVOLUTION_URL}/instance/logout/{INSTANCE}"
        requests.delete(url, headers=headers)
        return {"status": "logged_out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
