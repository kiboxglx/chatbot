import requests
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class PairingRequest(BaseModel):
    number: str

router = APIRouter()

# Configurações do WAHA
BASE_URL = os.getenv("WHATSAPP_API_URL", "http://localhost:3000")
API_KEY = os.getenv("AUTHENTICATION_API_KEY", "THISISMYSECURETOKEN")
SESSION = "default"

def get_headers():
    return {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json"
    }

@router.get("/management/status")
def get_status():
    """Verifica status da sessão"""
    try:
        url = f"{BASE_URL}/api/sessions/{SESSION}"
        headers = get_headers()
        
        resp = requests.get(url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            status = data.get('status', 'STOPPED')
            
            # Mapeia status do WAHA
            if status == 'WORKING':
                return {"state": "open", "status": "CONNECTED"}
            elif status == 'SCAN_QR_CODE':
                return {"state": "connecting", "status": "WAITING_QR"}
            elif status == 'STOPPED':
                return {"state": "close", "status": "DISCONNECTED"}
            
            return {"state": "connecting", "status": status}
            
        return {"state": "close", "details": "Sessão não encontrada"}
    except Exception as e:
        return {"state": "ERROR", "details": str(e)}

@router.get("/management/qrcode")
def get_qrcode():
    """Inicia sessão e retorna QR Code"""
    try:
        headers = get_headers()

        # 1. Inicia a sessão
        start_url = f"{BASE_URL}/api/sessions/start"
        payload = {"name": SESSION}
        
        resp = requests.post(start_url, json=payload, headers=headers, timeout=30)
        
        if resp.status_code not in [200, 201]:
            raise HTTPException(status_code=500, detail=f"Erro ao iniciar sessão: {resp.text}")

        # 2. Aguarda um pouco para o QR Code ser gerado
        import time
        time.sleep(2)
        
        # 3. Pega o QR Code
        qr_url = f"{BASE_URL}/api/{SESSION}/auth/qr"
        qr_resp = requests.get(qr_url, headers=headers, timeout=10)
        
        if qr_resp.status_code == 200:
            data = qr_resp.json()
            # WAHA retorna {qr: "base64..."}
            if data.get('qr'):
                return {"base64": data.get('qr')}
                
        return {"message": "Aguardando geração do QR Code..."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/management/logout")
def logout():
    """Fecha a sessão"""
    try:
        headers = get_headers()
        url = f"{BASE_URL}/api/sessions/stop"
        payload = {"name": SESSION}
        
        requests.post(url, json=payload, headers=headers, timeout=10)
        return {"status": "logged_out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/management/pairing-code")
def get_pairing_code(request: PairingRequest):
    """
    WAHA não suporta Pairing Code nativamente
    """
    raise HTTPException(status_code=400, detail="WAHA não suporta Código de Pareamento. Use o QR Code.")
