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

        # 1. Verifica se a sessão já existe
        status_url = f"{BASE_URL}/api/sessions/{SESSION}"
        status_resp = requests.get(status_url, headers=headers, timeout=10)
        
        session_exists = False
        if status_resp.status_code == 200:
            session_data = status_resp.json()
            current_status = session_data.get('status', 'STOPPED')
            session_exists = current_status != 'STOPPED'
            
            print(f"Status atual da sessão: {current_status}")
            
            # Se já está conectado, retorna mensagem
            if current_status == 'WORKING':
                return {"message": "Sessão já está conectada!"}

        # 2. Se não existe ou está parada, inicia
        if not session_exists:
            start_url = f"{BASE_URL}/api/sessions/start"
            webhook_url = os.getenv("WEBHOOK_GLOBAL_URL", "https://chatbot-production-e324.up.railway.app/webhook")
            
            payload = {
                "name": SESSION,
                "config": {
                    "webhooks": [
                        {
                            "url": webhook_url,
                            "events": ["message"],
                        }
                    ]
                }
            }
            
            resp = requests.post(start_url, json=payload, headers=headers, timeout=30)
            
            if resp.status_code not in [200, 201]:
                raise HTTPException(status_code=500, detail=f"Erro ao iniciar sessão: {resp.text}")

        # 3. Aguarda um pouco para o QR Code ser gerado
        import time
        time.sleep(3)
        
        # 4. Pega o QR Code - WAHA retorna a imagem PNG diretamente
        qr_url = f"{BASE_URL}/api/{SESSION}/auth/qr"
        qr_resp = requests.get(qr_url, headers=headers, timeout=10)
        
        if qr_resp.status_code == 200:
            # WAHA retorna a imagem PNG, precisamos converter para base64
            import base64
            qr_base64 = base64.b64encode(qr_resp.content).decode('utf-8')
            return {"base64": f"data:image/png;base64,{qr_base64}"}
                
        return {"message": "Aguardando geração do QR Code..."}
        
    except Exception as e:
        import traceback
        print(f"Erro completo: {traceback.format_exc()}")
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
    Gera código de pareamento no WAHA
    """
    try:
        headers = get_headers()
        
        # 1. Garante que a sessão está iniciada (semelhante ao QR Code)
        # Mas para pairing code, a sessão precisa estar em SCAN_QR_CODE
        status_url = f"{BASE_URL}/api/sessions/{SESSION}"
        status_resp = requests.get(status_url, headers=headers, timeout=10)
        
        if status_resp.status_code == 200:
            status = status_resp.json().get('status')
            if status == 'STOPPED':
                # Inicia a sessão se estiver parada
                start_url = f"{BASE_URL}/api/sessions/start"
                webhook_url = os.getenv("WEBHOOK_GLOBAL_URL", "https://chatbot-production-e324.up.railway.app/webhook")
                payload = {
                    "name": SESSION,
                    "config": {"webhooks": [{"url": webhook_url, "events": ["message"]}]}
                }
                requests.post(start_url, json=payload, headers=headers, timeout=30)
                import time
                time.sleep(3) # Aguarda iniciar
        
        # 2. Solicita o código
        url = f"{BASE_URL}/api/{SESSION}/auth/request-code"
        payload = {"phoneNumber": request.number.replace("+", "").replace("-", "").strip()}
        
        print(f"Solicitando Pairing Code para: {payload['phoneNumber']}")
        # Aumentando timeout para 120s (2 min)
        resp = requests.post(url, json=payload, headers=headers, timeout=120)
        
        if resp.status_code in [200, 201]:
            data = resp.json()
            # WAHA retorna {"code": "XYZ-123"}
            # Frontend espera {"pairingCode": "XYZ-123"}
            return {"pairingCode": data.get("code")}
            
        raise HTTPException(status_code=resp.status_code, detail=f"Erro WAHA: {resp.text}")
        
    except Exception as e:
        print(f"Erro Pairing Code: {e}")
        raise HTTPException(status_code=500, detail=str(e))
