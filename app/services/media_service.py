import os
import base64
import requests
import mimetypes
from datetime import datetime

class MediaService:
    def __init__(self):
        self.storage_dir = "storage/temp"
        os.makedirs(self.storage_dir, exist_ok=True)
import os
import base64
import requests
import mimetypes
from datetime import datetime

class MediaService:
    def __init__(self):
        self.storage_dir = "storage/temp"
        os.makedirs(self.storage_dir, exist_ok=True)

    def salvar_base64(self, base64_data: str, mime_type: str) -> str:
        """Salva uma string base64 como arquivo."""
        ext = mimetypes.guess_extension(mime_type) or ".bin"
        filename = f"media_{datetime.now().timestamp()}{ext}"
        filepath = os.path.join(self.storage_dir, filename)
        
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(base64_data))
            
        return filepath

    def processar_midia(self, mensagem_data: dict) -> str:
        """
        Processa mídia recebida (Áudio ou Imagem) e converte para texto se possível.
        WAHA envia mídia via URL ou Base64.
        """
        tipo_mensagem = mensagem_data.get("type")
        
        # 1. Tenta pegar URL da mídia (Padrão WAHA)
        media_url = mensagem_data.get("mediaUrl") or mensagem_data.get("body")
        
        # 2. Se não for URL válida, ignora processamento pesado por enquanto
        if not media_url or not media_url.startswith("http"):
            return f"[Mídia do tipo {tipo_mensagem} recebida]"

        try:
            # TODO: Implementar download real da mídia se necessário
            # Por enquanto retornamos apenas um marker identificando o tipo
            return f"[Áudio recebido - Transcrição pendente]" if tipo_mensagem == "audio" else f"[Imagem recebida]"

        except Exception as e:
            print(f"❌ Erro ao processar mídia: {e}")
            return "[Erro ao processar mídia]"
