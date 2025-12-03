import os
import base64
import requests
import mimetypes
from datetime import datetime

class MediaService:
    def __init__(self):
        self.storage_dir = "storage/temp"
        os.makedirs(self.storage_dir, exist_ok=True)
        # Headers para baixar da Evolution API se necessário (usando a mesma key)
        self.api_key = os.getenv("WHATSAPP_API_TOKEN", "")
        self.headers = {"apikey": self.api_key}

    def salvar_base64(self, base64_data: str, mime_type: str) -> str:
        """Salva uma string base64 como arquivo."""
        ext = mimetypes.guess_extension(mime_type) or ".bin"
        filename = f"media_{datetime.now().timestamp()}{ext}"
        filepath = os.path.join(self.storage_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(base64_data))
            
        return filepath

    def download_media(self, message_data: dict) -> str:
        """
        Tenta baixar a mídia da mensagem.
        Suporta Base64 direto no payload ou URL de download.
        """
        try:
            # 1. Tenta pegar Base64 direto (se habilitado no webhook)
            media_data = message_data.get('base64')
            if media_data:
                # O Evolution manda algo como "data:image/jpeg;base64,..."
                if "," in media_data:
                    header, base64_str = media_data.split(",", 1)
                    mime_type = header.split(":")[1].split(";")[0]
                else:
                    base64_str = media_data
                    mime_type = message_data.get('mimetype', 'application/octet-stream')
                
                return self.salvar_base64(base64_str, mime_type)

            # 2. Se não tiver base64, tenta URL (Evolution v2 ou v1 configurado)
            # A estrutura varia, vamos tentar achar uma URL
            # Em mensagens de mídia, geralmente tem 'url' ou 'directPath' mas o download real
            # na Evolution v1 costuma ser via endpoint específico se não vier o base64.
            
            # NOTA: Se o webhook não estiver mandando base64, precisamos buscar o base64
            # usando o ID da mensagem. Vamos assumir que vamos configurar o webhook para mandar base64
            # ou que vamos implementar a busca depois.
            
            # Por enquanto, vamos retornar None se não tiver base64, 
            # e instruir o usuário a ativar "Webhook Base64" na Evolution se falhar.
            print("AVISO: Nenhum base64 encontrado na mensagem. Ative 'Webhook Base64' na Evolution API.")
            return None

        except Exception as e:
            print(f"Erro ao baixar mídia: {e}")
            return None
