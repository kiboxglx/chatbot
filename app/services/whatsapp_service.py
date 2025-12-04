import os
import requests
from typing import Optional

            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "apikey": self.api_token
        }

        try:
            # Timeout curto para não travar a thread se a API estiver fora
            response = requests.post(endpoint, json=payload, headers=headers, timeout=5)
            print(f"Evolution API Response [{response.status_code}]: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Fallback / Mock conforme solicitado
            print(f"[MOCK SEND] Enviando para {numero}: {mensagem}")
            return {"status": "mock_sent", "error": str(e)}

    def enviar_arquivo(self, numero: str, caminho_arquivo: str) -> dict:
        """
        Envia um arquivo (PDF, Imagem, etc) para o número especificado.
        
        Args:
            numero (str): Número do destinatário.
            caminho_arquivo (str): Caminho absoluto ou relativo do arquivo local.
            
        Returns:
            dict: Resposta da API ou dicionário de mock em caso de erro.
        """
        instance_name = "chatbot"
        endpoint = f"{self.api_url}/message/sendMedia/{instance_name}"
        
        # Verifica se o arquivo existe antes de tentar enviar
        if not os.path.exists(caminho_arquivo):
            print(f"[ERRO] Arquivo não encontrado: {caminho_arquivo}")
            return {"status": "error", "message": "File not found"}

        try:
            # Para enviar media na Evolution API v1, geralmente usamos JSON com base64 ou URL,
            # mas se for multipart/form-data (upload), o endpoint pode ser diferente.
            # Vamos assumir envio via arquivo (multipart) se suportado, ou adaptar.
            # A Evolution API v1.7.4 suporta multipart em /message/sendMedia/{instance}
            
            with open(caminho_arquivo, "rb") as f:
                # O campo 'number' deve ir no form-data também
                files = {
                    "file": (os.path.basename(caminho_arquivo), f, "application/pdf") 
                }
                data = {
                    "number": numero,
                    "mediatype": "document", # ou image, video, etc. Vamos assumir document para PDF
                    "mimetype": "application/pdf",
                    "caption": "Segue seu documento."
                }
                headers = {"apikey": self.api_token}
                
                response = requests.post(endpoint, files=files, data=data, headers=headers, timeout=15)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            # Fallback / Mock conforme solicitado
            print(f"[MOCK SEND] Enviando arquivo para {numero}: {caminho_arquivo}")
            return {"status": "mock_sent", "error": str(e)}
