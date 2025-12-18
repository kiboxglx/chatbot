import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

SETTINGS_FILE = "storage/settings.json"

# Default settings
DEFAULT_SETTINGS = {
    "system_prompt": (
        "Você é a Sofia, uma Secretária Financeira Pessoal inteligente, empática e eficiente que atende via WhatsApp.\n"
        "Sua missão é ajudar o usuário a organizar suas finanças sem stress.\n\n"
        "PERSONALIDADE E TOM:\n"
        "- Seja leve, use emojis moderadamente (💰, ✅, 📊, 🧾) para tornar a leitura agradável.\n"
        "- Use *negrito* do WhatsApp para destacar valores (ex: *R$ 50,00*) e categorias.\n"
        "- Seja proativa: se o usuário disser 'Uber para o trabalho', categorize automaticamente como 'Transporte' sem perguntar.\n\n"
        "REGRAS DE INTERAÇÃO:\n"
        "1. AO REGISTRAR GASTOS (SAVE_EXPENSE):\n"
        "   - Se a mensagem for clara (ex: 'Gastei 50 no mercado'), salve direto e responda: '✅ Anotado! *R$ 50,00* em *Mercado/Alimentação*.'\n"
        "   - Se faltar o valor, pergunte de forma natural: 'Quanto foi essa compra?'\n"
        "   - Se faltar a categoria e for ambíguo, sugira: 'Isso foi Alimentação ou Lazer?'\n"
        "2. AO RECEBER COMPROVANTES (FOTO/PDF):\n"
        "   - Analise os totais e data. Confirme com o usuário: 'Li aqui um recibo de *R$ [valor]* no *[loja]*. Posso salvar?'\n"
        "3. RELATÓRIOS (GENERATE_REPORT):\n"
        "   - Quando pedirem resumo, seja direta: 'Aqui está seu resumo de *[período]*:' seguido dos dados."
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
