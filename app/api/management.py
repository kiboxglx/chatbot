import requests
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class PairingRequest(BaseModel):
    number: str

router = APIRouter()

# Configurações do WPPConnect
BASE_URL = os.getenv("WHATSAPP_API_URL", "http://localhost:8080")
SECRET_KEY = os.getenv("AUTHENTICATION_API_KEY", "123Cartoon*")
SESSION = "bot_whatsapp"

def get_token():
    """Gera token para operações administrativas"""
    url = f"{BASE_URL}/api/{SESSION}/{SECRET_KEY}/generate-token"
    try:
    except Exception as e:
        print(f"Erro fatal ao conectar no WPPConnect: {e}")
        # Retorna o erro original para aparecer no frontend
        raise Exception(f"Falha de Conexão: {str(e)}")

def get_headers():
    # Agora get_token lança exceção se falhar, que será capturada pelo endpoint
    token = get_token()
    return {"Authorization": f"Bearer {token}"}

@router.get("/management/status")
def get_status():
    """Verifica status da sessão"""
    try:
        # WPPConnect: GET /api/{session}/status-session
        url = f"{BASE_URL}/api/{SESSION}/status-session"
        headers = get_headers()
        
        if not headers:
            return {"state": "DISCONNECTED", "message": "Sem token"}

        resp = requests.get(url, headers=headers, timeout=5)
        
        if resp.status_code == 200:
            data = resp.json()
            status = data.get('status', 'DISCONNECTED')
            # Mapeia status do WPPConnect para o nosso frontend
            if status in ['CONNECTED', 'inChat', 'isLogged']:
                return {"state": "open", "status": status}
            if status in ['qrReadError', 'browserClose']:
                return {"state": "close", "status": status}
            return {"state": "connecting", "status": status}
            
        return {"state": "close", "details": "Sessão não iniciada"}
    except Exception as e:
        return {"state": "ERROR", "details": str(e)}

@router.get("/management/qrcode")
def get_qrcode():
    """Inicia sessão e retorna QR Code"""
    try:
        headers = get_headers()
        if not headers:
            raise HTTPException(status_code=500, detail="Falha na autenticação com WPPConnect")

        # 1. Inicia Sessão (Start Session)
        start_url = f"{BASE_URL}/api/{SESSION}/start-session"
        # webhook é importante para receber mensagens
        webhook_url = os.getenv("WEBHOOK_GLOBAL_URL", "")
        payload = {
            "webhook": webhook_url,
            "waitQrCode": True
        }
        requests.post(start_url, json=payload, headers=headers, timeout=10)
        
        # 2. Pega o QR Code (que vem no status ou endpoint específico)
        # O WPPConnect retorna o QR Code em base64 no status se estiver aguardando leitura
        status_url = f"{BASE_URL}/api/{SESSION}/status-session"
        resp = requests.get(status_url, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('qrcode'):
                return {"base64": data.get('qrcode')}
                
        return {"message": "Aguardando geração do QR Code..."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/management/logout")
def logout():
    """Fecha a sessão"""
    try:
        headers = get_headers()
        url = f"{BASE_URL}/api/{SESSION}/close-session"
        requests.post(url, headers=headers)
        return {"status": "logged_out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/management/pairing-code")
def get_pairing_code(request: PairingRequest):
    """
    WPPConnect Server ainda não tem suporte nativo robusto para Pairing Code via API pública
    na versão stable. Mas vamos deixar preparado caso usem uma versão beta que suporte.
    """
    raise HTTPException(status_code=400, detail="WPPConnect ainda não suporta Código de Pareamento via API. Use o QR Code.")
