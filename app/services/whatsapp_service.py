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

        except Exception as e:
            print(f"❌ Erro CRÍTICO ao enviar mensagem (WAHA): {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}

    def enviar_texto(self, numero: str, mensagem: str):
        try:
            # WAHA usa chatId no formato: 5511999999999@c.us
            if "@" not in numero:
                numero = f"{numero}@c.us"

            url = f"{self.base_url}/api/sendText"
            
            # --- LOG DE DIAGNÓSTICO ---
            print(f"🚀 TENTATIVA DE ENVIO DE MENSAGEM:")
            print(f"   URL: {url}")
            print(f"   Destino: {numero}")
            print(f"   Key Configurada: {self.api_key[:3]}***{self.api_key[-3:]}")
            # --------------------------

            payload = {
                "session": self.session,
                "chatId": numero,
                "text": mensagem
            }
            
            headers = self._get_headers()
            
            print(f"   Enviando request...")
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            
            print(f"   ⬅️ Resposta WAHA: Status {response.status_code}")
            print(f"   📄 Body: {response.text}")

            if response.status_code == 201:
                print(f"✅ Mensagem enviada com sucesso para {numero}")
                return response.json()
            else:
                print(f"❌ WAHA rejeitou o envio: {response.status_code} - {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem (WAHA Exception): {e}")
            return {"error": str(e)}

    def enviar_arquivo(self, numero: str, caminho_arquivo: str, legenda: str = ""):
        # Implementação futura para arquivos
        pass
