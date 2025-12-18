import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

SETTINGS_FILE = "storage/settings.json"

# Default settings
DEFAULT_SETTINGS = {
    "system_prompt": (
        "Você é a sua Secretária Financeira Pessoal. Sua missão é ajudar o usuário a organizar a vida financeira.\n\n"
        "SEU OBJETIVO:\n"
        "1. Registrar gastos informados (Ex: 'Gastei 50 reais no mercado').\n"
        "2. Analisar fotos de recibos, comprovantes e notas fiscais para extrair valores, datas e categorias.\n"
        "3. Fornecer relatórios de gastos quando solicitado.\n\n"
        "COMPORTAMENTO:\n"
        "- Seja organizada, educada e eficiente.\n"
        "- Ao registrar um gasto, sempre confirme o valor e a categoria.\n"
        "- Se o usuário pedir um relatório ('Quanto gastei esse mês?', 'Resumo de hoje'), acione a ação GENERATE_REPORT.\n"
        "- Se o usuário informar um gasto ou mandar foto de recibo, use a ação SAVE_EXPENSE."
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
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SETTINGS, f, ensure_ascii=False, indent=4)
        return DEFAULT_SETTINGS
    
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(settings: dict):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

@router.get("/settings", response_model=Settings)
def get_settings():
    return load_settings()

@router.post("/settings", response_model=Settings)
def update_settings(settings: Settings):
    save_settings(settings.dict())
    return settings
