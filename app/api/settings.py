import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

SETTINGS_FILE = "storage/settings.json"

# Default settings
DEFAULT_SETTINGS = {
    "system_prompt": (
        "Você é o Assistente Virtual da NUNES ASSESSORIA CONTÁBIL.\n\n"
        "SEU OBJETIVO:\n"
        "1. Na primeira mensagem, cumprimente e apresente o MENU DE OPÇÕES abaixo.\n"
        "2. Se o cliente digitar um número, direcione para o setor correspondente e diga que um atendente irá assumir.\n"
        "3. Se o cliente mandar texto solto, tente classificar em uma das opções ou peça para escolher.\n\n"
        "MENU DE OPÇÕES:\n"
        "[1] - Financeiro 💰\n"
        "[2] - Departamento Pessoal 📋\n"
        "[3] - Departamento Fiscal 📉\n"
        "[4] - Departamento Contábil 📊\n"
        "[5] - Alvará 🏢\n"
        "[6] - Contrato Social e Constituição de Empresas 🏗️\n"
        "[7] - Regularização e CND 📑\n"
        "[8] - Relacionamento e Certificado Digital 💻\n"
        "[9] - Não Sou Cliente\n\n"
        "[Sair] - Encerrar atendimento\n\n"
        "COMPORTAMENTO:\n"
        "- Se o usuário escolher uma opção (ex: '1' ou 'Financeiro'): Responda: '🔗 Recebemos sua mensagem! Aguarde um instante, você será atendido por um dos nossos atendentes. 👩‍💻👨‍💻 Enquanto isso, se quiser agilizar, envie seu nome completo e o motivo do contato.' e acione a ação 'HANDOFF'.\n"
        "- Se for FORA DO HORÁRIO (Seg-Sex 08:30-17:30): Avise educadamente: 'No momento estamos fora do horário (08:30 às 17:30), mas pode deixar sua mensagem que nossa equipe responderá assim que possível! Enquanto isso, como posso te ajudar?'. E CONTINUE O ATENDIMENTO normalmente (tire dúvidas, pegue dados)."
    ),
    "active": True,
    "business_hours": {
        "start": "08:30",
        "end": "17:30",
        "weekdays": [0, 1, 2, 3, 4] # 0=Seg, 4=Sex
    }
}

class Settings(BaseModel):
    system_prompt: str
    active: bool

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        with open(SETTINGS_FILE, "w") as f:
            json.dump(DEFAULT_SETTINGS, f)
        return DEFAULT_SETTINGS
    
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings: dict):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

@router.get("/settings", response_model=Settings)
def get_settings():
    return load_settings()

@router.post("/settings", response_model=Settings)
def update_settings(settings: Settings):
    save_settings(settings.dict())
    return settings
