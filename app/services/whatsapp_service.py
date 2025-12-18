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
            # WAHA Exige chatId no formato number@c.us
            # Tratamento robusto de JID
            # Se já tem @ (ex: @c.us, @g.us, @lid), confiamos no caller
            if "@" in numero:
                 chat_id = numero
            else:
                 # Se vier sem nada, assumimos usuário padrão
                 chat_id = f"{numero}@c.us"

            url = f"{self.base_url}/api/sendText"
            
            # --- LOG AVANÇADO ---
            print(f"👉 [Outbound] Enviando para: {chat_id}")
            # --------------------

            payload = {
                "session": self.session,
                "chatId": chat_id,
                "text": mensagem
            }
            
            headers = self._get_headers()
            
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            
            # Log em RECENT_EVENTS para diagnóstico
            try:
                from app.api.webhook import RECENT_EVENTS
                import time
                RECENT_EVENTS.append({
                    "time": time.strftime("%H:%M:%S"),
                    "event": "OUTBOUND_SEND",
                    "to": chat_id,
                    "status": response.status_code,
                    "body_snippet": mensagem[:50]
                })
            except: pass

            if response.status_code == 201:
                print(f"✅ [Outbound] Sucesso: {response.json().get('id', 'SEM_ID')}")
                return response.json()
            else:
                print(f"❌ [Outbound] Erro WAHA ({response.status_code}): {response.text}")
                return {"error": response.text}
                
        except requests.exceptions.Timeout:
            print("❌ [Outbound] Timeout ao conectar com WAHA")
            return {"error": "timeout"}
        except Exception as e:
            print(f"❌ [Outbound] Exception: {e}")
            import traceback
            traceback.print_exc()
            return {"error": str(e)}

    def enviar_arquivo(self, numero: str, caminho_arquivo: str, legenda: str = ""):
        # Implementação futura para arquivos
        pass
