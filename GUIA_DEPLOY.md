# 🚀 Guia de Deploy (Colocando no Ar)

Seu projeto tem 3 partes:
1.  **Frontend (Painel)**: React/Vite.
2.  **Backend (Cérebro)**: Python FastAPI.
3.  **WhatsApp API**: Evolution API (Docker).

## ⚠️ Importante sobre o Vercel
O **Vercel** é excelente para o **Frontend**, mas **NÃO suporta** a Evolution API (WhatsApp) porque ela precisa ficar ligada 24h (e o Vercel desliga servidores inativos).

### ✅ A Melhor Estratégia (Híbrida)

1.  **Frontend no Vercel** (Grátis e Rápido).
2.  **Backend + WhatsApp numa VPS** (DigitalOcean, Hetzner, Railway ou Render).

---

## 1️⃣ Subindo o Backend (VPS/Railway)
Você precisa de um servidor que suporte Docker.
Sugestão: **Railway** (mais fácil) ou **DigitalOcean** (mais barato, $6/mês).

### No Servidor:
1.  Copie a pasta do projeto.
2.  Rode `docker-compose up -d --build`.
3.  Seu backend ficará acessível em `http://IP-DO-SERVIDOR:8000`.
4.  Configure o domínio (ex: `api.seusite.com`).

---

## 2️⃣ Subindo o Frontend no Vercel

1.  Crie uma conta no [Vercel](https://vercel.com).
2.  Instale o Vercel CLI ou conecte seu GitHub.
3.  Na pasta `frontend`, crie um arquivo `.env.production`:
    ```env
    VITE_API_URL=https://api.seusite.com
    ```
    *(Substitua pela URL do seu backend)*

4.  No arquivo `frontend/src/App.tsx`, altere a linha da API para usar a variável de ambiente:
    ```javascript
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    ```

5.  Rode o deploy:
    ```bash
    cd frontend
    vercel
    ```

---

## 💡 Opção "Tudo em Um" (Mais Simples)
Se não quiser usar Vercel separado, você pode hospedar **TUDO** numa VPS (ex: Coolify).
Assim, o Frontend, Backend e WhatsApp rodam no mesmo lugar e se comunicam localmente. É mais fácil de gerenciar para quem está começando.
