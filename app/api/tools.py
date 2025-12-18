from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
import os

# Importamos o gerador de PDF existente
from app.services.pdf_generator import gerar_das_pdf

router = APIRouter()

# --- Schemas ---
class RelatorioRequest(BaseModel):
    cnpj: str
    tipo: str  # 'faturamento', 'impostos', 'balancete', 'das'
    mes: int | str
    ano: int
    email_destino: Optional[str] = None

    def get_mes_int(self) -> int:
        if isinstance(self.mes, int):
            return self.mes
        
        mes_str = self.mes.lower().strip()
        if mes_str.isdigit():
            return int(mes_str)
            
        meses = {
            "janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3,
            "abril": 4, "maio": 5, "junho": 6, "julho": 7,
            "agosto": 8, "setembro": 9, "outubro": 10,
            "novembro": 11, "dezembro": 12
        }
        return meses.get(mes_str, 0)

class PendenciaResponse(BaseModel):
    status: str
    pendencias: List[str]

# --- Endpoints ---

@router.post("/tools/gerar_relatorio")
async def api_gerar_relatorio(request: RelatorioRequest):
    """
    Ferramenta para gerar relatórios contábeis em PDF.
    Retorna a URL do arquivo gerado para download.
    """
    try:
        print(f"[TOOL] Gerando relatório {request.tipo} para {request.cnpj} ({request.mes}/{request.ano})")
        
        # Por enquanto, só temos implementação real para DAS
        # Se for outro tipo, podemos simular ou usar o mesmo gerador por enquanto
        
        caminho_arquivo = gerar_das_pdf(
            nome_empresa="Empresa Cliente", # Idealmente buscaria no banco pelo CNPJ
            cnpj=request.cnpj,
            mes_referencia=f"{request.get_mes_int():02d}/{request.ano}"
        )
        
        # O caminho retornado é absoluto (ex: /app/storage/boletos/DAS_...)
        # Precisamos converter para URL acessível externamente
        # Como o n8n vai acessar via rede Docker, usamos o nome do serviço ou localhost mapeado
        # Mas para o n8n enviar para o usuário, o ideal é uma URL pública.
        # Como estamos em ambiente local/Docker, vamos retornar a URL relativa ao container 'chatbot'
        # O n8n pode usar essa URL se estiver na mesma rede, ou podemos montar a URL externa.
        
        filename = os.path.basename(caminho_arquivo)
        
        # URL acessível de fora (pelo navegador do usuário se ele clicar, ou pelo n8n para download)
        # Nota: 'localhost' aqui refere-se à máquina do usuário. 
        # Se o n8n for baixar, ele deve usar http://chatbot:8000/...
        # Se o usuário for clicar, http://localhost:8000/...
        
        # Vamos retornar ambos para flexibilidade
        download_url_local = f"http://localhost:8000/storage/boletos/{filename}"
        download_url_docker = f"http://chatbot:8000/storage/boletos/{filename}"
        
        return {
            "status": "success",
            "message": f"Relatório de {request.tipo} gerado com sucesso.",
            "download_url": download_url_local,
            "internal_url": download_url_docker,
            "meta": {"mes": request.mes, "ano": request.ano, "tipo": request.tipo}
        }
        
    except Exception as e:
        print(f"[TOOL ERROR] {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools/consultar_pendencias/{cnpj}")
async def api_consultar_pendencias(cnpj: str):
    """
    Ferramenta para verificar se a empresa tem impostos atrasados.
    """
    print(f"[TOOL] Consultando pendências para {cnpj}")
    
    # Simulação de lógica de banco de dados
    # Aqui você conectaria no seu Service de Contabilidade real
    
    pendencias_mock = [
        f"DAS {cnpj[-4:]} - 05/2025 - R$ 150,00",
        f"ISSQN {cnpj[-4:]} - 04/2025 - R$ 50,00"
    ]
    
    return {
        "status": "success",
        "pendencias": pendencias_mock,
        "total_pendente": len(pendencias_mock)
    }

@router.post("/tools/analisar_documento")
async def api_analisar_documento(file: UploadFile = File(...)):
    """
    Endpoint para análise de documentos financeiros (Imagens ou PDFs).
    
    **Fluxo:**
    1. Recebe o arquivo (JPEG, PNG, PDF).
    2. Salva temporariamente no storage.
    3. Envia para o Gemini Vision para extração de dados.
    4. Retorna JSON estruturado com: data_compra, estabelecimento, valor_total, descricao_resumida, categoria_sugerida.
    
    **Uso no n8n:**
    - Nó HTTP Request (POST Multipart)
    - Campo: `file` (Binary Data)
    """
    from fastapi import UploadFile, File
    import shutil
    from datetime import datetime
    from app.services.ai_service import BrainService
    
    # Validação de tipo de arquivo
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Tipo de arquivo não suportado: {file.content_type}. Use JPEG, PNG ou PDF."
        )
    
    # Salva o arquivo temporariamente
    storage_dir = "storage/temp"
    os.makedirs(storage_dir, exist_ok=True)
    
    timestamp = datetime.now().timestamp()
    ext = os.path.splitext(file.filename)[1] or ".bin"
    temp_filename = f"doc_{timestamp}{ext}"
    temp_path = os.path.join(storage_dir, temp_filename)
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"📄 Arquivo recebido: {file.filename} ({file.content_type})")
        print(f"💾 Salvo em: {temp_path}")
        
        # Chama o serviço de IA
        brain = BrainService()
        resultado = brain.analisar_documento_financeiro(temp_path)
        
        # Limpeza do arquivo temporário (opcional, pode manter para auditoria)
        # os.remove(temp_path)
        
        return resultado
    
    except Exception as e:
        print(f"❌ Erro ao processar documento: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar documento: {str(e)}")

