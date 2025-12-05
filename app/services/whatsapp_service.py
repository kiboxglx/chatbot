import os
import requests
import json

class WhatsAppService:
    def __init__(self):
        self.base_url = os.getenv("WHATSAPP_API_URL", "http://localhost:3000")
        self.api_key = os.getenv("AUTHENTICATION_API_KEY", "THISISMYSECURETOKEN")
        self.session = "default"  # WAHA usa 'default' como sessão padrão

    def _get_headers(self):
        """WAHA usa X-Api-Key para autenticação"""
        return {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def enviar_texto(self, numero: str, mensagem: str):
        try:
            # WAHA usa chatId no formato: 5511999999999@c.us
            if "@" not in numero:
                numero = f"{numero}@c.us"

            url = f"{self.base_url}/api/sendText"
            payload = {
                "session": self.session,
                "chatId": numero,
                "text": mensagem
            }
            
            headers = self._get_headers()
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            
            if response.status_code == 201:
                print(f"✅ Mensagem enviada para {numero}")
                return response.json()
            else:
                print(f"❌ Erro ao enviar: {response.status_code} - {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem (WAHA): {e}")
            return {"error": str(e)}

    def enviar_arquivo(self, numero: str, caminho_arquivo: str, legenda: str = ""):
        # Implementação futura para arquivos
        pass
