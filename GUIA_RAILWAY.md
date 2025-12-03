# 🚂 Guia Detalhado de Deploy no Railway

Siga esta ordem exata para evitar erros de conexão.

## 1️⃣ Criar os Bancos de Dados
No painel do Railway (botão "New" ou clique direito na tela):
1.  **Add Service** → **Database** → **PostgreSQL**.
2.  **Add Service** → **Database** → **Redis**.

*Aguarde eles ficarem verdes (Online).*

---

## 2️⃣ Subir o Cérebro (Python Backend)
1.  **Add Service** → **GitHub Repo** → Selecione seu repositório `chatbot`.
2.  O Railway vai começar a construir. **Cancele** ou espere falhar (pois faltam variáveis).
3.  Clique no bloco do **Python Backend** → Aba **Variables**.
4.  Adicione:
    -   `GEMINI_API_KEY`: (Sua chave do Google)
    -   `AUTHENTICATION_API_KEY`: `SuaSenhaForte123` (Invente uma senha)
    -   `DATABASE_URL`: Digite `${{Postgres` e selecione a opção que aparecer (o Railway preenche automático).
    -   `PORT`: `8000`
5.  Vá na aba **Settings** → **Networking** → **Public Domain** → Clique em **Generate Domain**.
    -   *Copie esse domínio!* (Ex: `chatbot-production.up.railway.app`). Vamos chamar de **URL_DO_PYTHON**.

---

## 3️⃣ Subir o WhatsApp (Evolution API)
1.  **Add Service** → **Docker Image**.
2.  Image Name: `atendai/evolution-api:v1.7.4` (Dê Enter).
3.  Clique no bloco criado → Aba **Variables**.
4.  Adicione (Essa é a parte mais importante):
    -   `SERVER_URL`: `https://` + (Gere um domínio na aba Settings primeiro e cole aqui).
    -   `AUTHENTICATION_API_KEY`: `SuaSenhaForte123` (A mesma do Python).
    -   `DATABASE_PROVIDER`: `postgresql`
    -   `DATABASE_CONNECTION_URI`: Digite `${{Postgres` e selecione a URL.
    -   `REDIS_ENABLED`: `true`
    -   `REDIS_URI`: Digite `${{Redis` e selecione a URL.
    -   `QRCODE_LIMIT`: `30`
    -   **WEBHOOK_GLOBAL_ENABLED**: `true`
    -   **WEBHOOK_GLOBAL_URL**: `https://URL_DO_PYTHON/webhook` (Cole a URL que você gerou no passo 2).
    -   `WEBHOOK_EVENTS_MESSAGES_UPSERT`: `true`
5.  Vá na aba **Settings** → **Networking** → **Public Domain** → Gere o domínio (se não gerou antes).
    -   *Copie esse domínio!* (Ex: `evolution-production.up.railway.app`). Vamos chamar de **URL_DO_ZAP**.

---

## 4️⃣ Conectar o Cérebro ao WhatsApp
Agora que o WhatsApp tem uma URL, precisamos avisar o Python.

1.  Volte no bloco do **Python Backend** → Aba **Variables**.
2.  Adicione:
    -   `WHATSAPP_API_URL`: `https://URL_DO_ZAP` (A URL que você gerou no passo 3).
3.  O Railway vai reiniciar o Python automaticamente.

---

## 5️⃣ Frontend (Vercel)
Agora que o backend está online e tem uma URL (`URL_DO_PYTHON`):

1.  Vá no Vercel.
2.  Importe o projeto `frontend`.
3.  Environment Variables:
    -   `VITE_API_URL`: `https://URL_DO_PYTHON`
4.  Deploy!

---

### 🎉 Resumo da Arquitetura
-   **Vercel** (Frontend) → fala com → **Railway Python**
-   **Railway Python** → fala com → **Railway Evolution**
-   **Railway Evolution** → manda mensagens para → **Railway Python** (via Webhook)
