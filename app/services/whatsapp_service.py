import os
import requests
import json

class WhatsAppService:
    def __init__(self):
        self.base_url = os.getenv("WHATSAPP_API_URL", "http://localhost:8080")
        self.api_key = os.getenv("AUTHENTICATION_API_KEY", "123Cartoon*") # Usado como SECRET_KEY no WPPConnect
        self.session = "chatbot"
        self.token = None

    def _get_token(self):
        """Gera o token de autenticação do WPPConnect"""
        if self.token:
            return self.token
            
        try:
            url = f"{self.base_url}/api/{self.session}/{self.api_key}/generate-token"
            payload = {"secret": self.api_key}
            
            # WPPConnect às vezes precisa iniciar a sessão antes de gerar token
            # Mas vamos tentar gerar direto. Se falhar, o management.py cuida do start.
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if 'token' in data:
                    self.token = data['token']
                    return self.token
                if 'session' in data and 'token' in data['session']: # Estrutura varia
                    self.token = data['session']['token']
                    return self.token
            
            print(f"Erro ao gerar token WPPConnect: {response.text}")
            return None
        except Exception as e:
            print(f"Erro de conexão WPPConnect (Token): {e}")
            return None

    def _get_headers(self):
        token = self._get_token()
        if not token:
            return {}
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def enviar_texto(self, numero: str, mensagem: str):
        try:
            # Formata número (WPPConnect gosta de 5511999999999@c.us)
            if "@" not in numero:
                numero = f"{numero}@c.us"

            url = f"{self.base_url}/api/{self.session}/send-message"
            payload = {
                "phone": numero,
                "message": mensagem,
                "isGroup": False
            }
            
            headers = self._get_headers()
            if not headers:
                print("Falha: Sem token de autenticação")
                return {"error": "No auth token"}

            response = requests.post(url, json=payload, headers=headers, timeout=20)
            return response.json()
        except Exception as e:
            print(f"Erro ao enviar mensagem (WPPConnect): {e}")
            return {"error": str(e)}

    def enviar_arquivo(self, numero: str, caminho_arquivo: str, legenda: str = ""):
        # Implementação futura para arquivos
        pass
