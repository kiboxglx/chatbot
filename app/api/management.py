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
        # 1. Tenta criar a instância (se não existir)
        create_url = f"{EVOLUTION_URL}/instance/create"
        create_payload = {
            "instanceName": INSTANCE,
            "qrcode": True,
            "integration": "WHATSAPP-BAILEYS"
        }
        requests.post(create_url, json=create_payload, headers=headers)
        
        # 2. Tenta conectar (gerar QR Code)
        connect_url = f"{EVOLUTION_URL}/instance/connect/{INSTANCE}"
        resp = requests.get(connect_url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            return resp.json()
            
        # Se falhar (ex: já conectado ou erro), tenta verificar o status
        status_url = f"{EVOLUTION_URL}/instance/connectionState/{INSTANCE}"
        status_resp = requests.get(status_url, headers=headers)
        
        if status_resp.status_code == 200:
            state = status_resp.json().get('instance', {}).get('state')
            if state == 'open':
                return {"status": "connected", "message": "WhatsApp já conectado"}
        
        # Se chegou aqui, tenta forçar logout e tentar de novo (recuperação)
        requests.delete(f"{EVOLUTION_URL}/instance/logout/{INSTANCE}", headers=headers)
        
        # Tenta conectar novamente após logout
        resp_retry = requests.get(connect_url, headers=headers, timeout=10)
        if resp_retry.status_code == 200:
            return resp_retry.json()

        raise HTTPException(status_code=400, detail="Não foi possível gerar QR Code. Tente novamente em instantes.")
        
    except Exception as e:
        print(f"Erro QR Code: {e}")
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
