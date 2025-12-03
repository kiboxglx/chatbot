# 🤖 Chatbot WhatsApp com IA (Versão Python)

Este é um sistema de atendimento automático para WhatsApp que utiliza Inteligência Artificial (Google Gemini) para responder clientes.

## ✨ Diferenciais
- **100% Python**: Sem custos mensais de plataformas como n8n ou Typebot.
- **Pausa Inteligente**: Se um humano responder pelo celular, o bot para de responder aquele cliente por 30 minutos.
- **Multimodal**: Entende texto, áudio (transcrição futura) e analisa imagens/documentos.

## 🚀 Como Rodar

### 1. Pré-requisitos
- Python 3.11+ instalado
- Docker (para a Evolution API)
- Chave de API do Google Gemini (Grátis)

### 2. Configuração
Crie um arquivo `.env` na pasta raiz com:
```env
GEMINI_API_KEY="sua_chave_aqui"
AUTHENTICATION_API_KEY="sua_senha_evolution"
```

### 3. Iniciar a API do WhatsApp (Evolution API)
```bash
docker-compose up -d evolution-api
```
Acesse `http://localhost:8080/manager` para escanear o QR Code.

### 4. Iniciar o Cérebro (Python)
```bash
python -m uvicorn main:app --port 8000 --reload
```

### 5. Conectar
No painel da Evolution API, configure o Webhook:
- **URL**: `http://localhost:8000/webhook` (ou sua URL pública/ngrok)
- **Eventos**: Marque `MESSAGES_UPSERT`
- **Ativo**: Sim

## ⚙️ Personalização

Para mudar a personalidade do bot (ex: Pizzaria, Clínica, Loja), edite o arquivo `storage/settings.json` (será criado automaticamente na primeira execução) ou use a API `/settings`.

Exemplo de Prompt:
> "Você é o atendente da Pizzaria Bella Napoli. Seja divertido e anote os pedidos. Nosso cardápio é..."

## 🛑 Como o Humano assume?
Basta responder qualquer mensagem do cliente pelo próprio WhatsApp (celular ou web). O bot detectará sua mensagem e ficará em silêncio por 30 minutos para aquele cliente.
