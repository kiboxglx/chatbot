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
        print(f"Tentando gerar token em: {url}")
        resp = requests.post(url, json={"secret": SECRET_KEY}, timeout=10)
        
        if resp.status_code in [200, 201]:
            data = resp.json()
            if 'token' in data: return data['token']
            if 'session' in data: return data['session']['token']
            
        # Se não for 200, retorna o erro
        error_msg = f"WPPConnect retornou {resp.status_code}: {resp.text}"
        print(error_msg)
        raise Exception(error_msg)
        
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
    """
    WPPConnect Server ainda não tem suporte nativo robusto para Pairing Code via API pública
    na versão stable. Mas vamos deixar preparado caso usem uma versão beta que suporte.
    """
    raise HTTPException(status_code=400, detail="WPPConnect ainda não suporta Código de Pareamento via API. Use o QR Code.")
