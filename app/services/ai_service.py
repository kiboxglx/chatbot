import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

from app.api.settings import load_settings

class BrainService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("ERRO: GEMINI_API_KEY não encontrada no .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.0-flash')

    def processar_mensagem(self, mensagem: str, contexto_cliente: str = "", media_path: str = None) -> dict:
        """
        Processa a mensagem do usuário (texto e/ou arquivo) e retorna uma ação estruturada.
        """
        settings = load_settings()
        
        if not settings.get("active", True):
            return {
                "action": "HANDOFF",
                "response_text": "O atendimento automático está temporariamente desativado. Um atendente irá responder em breve.",
                "parameters": {}
            }

        system_prompt = (
            f"{settings['system_prompt']}\n\n"
            
            "CAPACIDADE VISUAL:\n"
            "Você pode ver arquivos enviados pelo usuário (Imagens, PDFs). "
            "Se receber um arquivo, analise-o como um documento financeiro (recibo, nota, etc).\n\n"
            
            "FORMATO DE RESPOSTA (JSON OBRIGATÓRIO):\n"
            "Responda APENAS um JSON válido com esta estrutura:\n"
            "{\n"
            '  "action": "REPLY" | "SAVE_EXPENSE" | "GENERATE_REPORT" | "HANDOFF",\n'
            '  "response_text": "Sua resposta amigável para o cliente aqui",\n'
            '  "parameters": {\n'
            '     "amount": 0.0, "description": "nome do gasto", "category": "categoria" (Obrigatório se action for SAVE_EXPENSE),\n'
            '     "period": "today" | "month" | "all" (Opcional se action for GENERATE_REPORT)\n'
            '  }\n'
            "}"
        )

        try:
            # Prepara o conteúdo da mensagem
            user_content = [f"System: {system_prompt}\nUser: {mensagem}"]
            
            # Se tiver arquivo, faz upload e adiciona ao conteúdo
            if media_path:
                print(f"Enviando arquivo para o Gemini: {media_path}")
                arquivo = genai.upload_file(media_path)
                user_content.append(arquivo)
                user_content.append("Analise este arquivo enviado pelo usuário.")

            # Envia para o modelo
            # Nota: Para multimodal, usamos generate_content ou start_chat com history
            # Aqui vamos usar generate_content direto para simplificar o envio de arquivos no turno
            response = self.model.generate_content(user_content)
            
            # Limpeza básica para garantir JSON válido
            raw_text = response.text.replace("```json", "").replace("```", "").strip()
            
            import json
            resultado = json.loads(raw_text)
            return resultado

        except Exception as e:
            print(f"Erro no BrainService: {e}")
            return {
                "action": "HANDOFF",
                "response_text": "Desculpe, tive um erro ao ler o arquivo. Vou chamar um humano. 👷‍♂️",
                "parameters": {}
            }

    def classificar_intencao(self, mensagem: str) -> str:
        # Mantendo compatibilidade temporária (depreciado)
        res = self.processar_mensagem(mensagem)
        if res['action'] == 'SEND_DOC': return '2_VIA_BOLETO'
        if res['action'] == 'HANDOFF': return 'FALAR_HUMANO'
        return 'OUTROS'

    def analisar_documento_financeiro(self, media_path: str) -> dict:
        """
        Analisa um documento (Imagem/PDF) e extrai dados financeiros estruturados.
        """
        prompt = (
            "Analise este documento financeiro (Recibo, Nota Fiscal, Boleto, Extrato).\n"
            "Extraia os dados com precisão e retorne APENAS um JSON com este formato:\n"
            "{\n"
            '  "data_compra": "DD/MM/AAAA",\n'
            '  "estabelecimento": "Nome da Loja/Banco",\n'
            '  "valor_total": 0.00,\n'
            '  "descricao_resumida": "Ex: Almoço, Gasolina, Boleto Internet",\n'
            '  "categoria_sugerida": "Ex: Alimentação, Transporte, Custos Fixos"\n'
            "}\n"
            "Se algum campo não estiver claro, tente inferir pelo contexto ou deixe null.\n"
            "O valor_total deve ser um float (ex: 150.50)."
        )

        try:
            print(f"Enviando documento para análise financeira: {media_path}")
            arquivo = genai.upload_file(media_path)
            
            response = self.model.generate_content([prompt, arquivo])
            
            # Limpeza do JSON
            raw_text = response.text.replace("```json", "").replace("```", "").strip()
            import json
            return json.loads(raw_text)

        except Exception as e:
            print(f"Erro na análise financeira: {e}")
            return {
                "error": "Falha ao processar documento",
                "details": str(e)
            }
