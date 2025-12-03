# 🚂 Guia de Deploy no Railway (Backend + WhatsApp)

Este guia vai colocar seu "Cérebro" (Python) e o "WhatsApp" (Evolution API) online 24h.

## Passo 1: Preparar o GitHub
1.  Crie um repositório no GitHub (ex: `chatbot-contabil`).
2.  Suba todos os arquivos desta pasta para lá.
    ```bash
    git init
    git add .
    git commit -m "Primeiro deploy"
    git branch -M main
    git remote add origin https://github.com/SEU_USUARIO/chatbot-contabil.git
    git push -u origin main
    ```

## Passo 2: Criar Projeto no Railway
1.  Acesse [railway.app](https://railway.app) e faça login com GitHub.
2.  Clique em **"New Project"** -> **"Deploy from GitHub repo"**.
3.  Selecione o repositório `chatbot-contabil`.
4.  Clique em **"Add Variables"** antes de fazer o deploy.

## Passo 3: Configurar Variáveis (Environment Variables)
Adicione as seguintes variáveis no Railway:

| Variável | Valor |
| :--- | :--- |
| `AUTHENTICATION_API_KEY` | Crie uma senha forte (ex: `MinhaSenhaSegura123`) |
| `GEMINI_API_KEY` | Sua chave do Google Gemini |
| `PORT` | `8080` |

## Passo 4: Adicionar Banco de Dados (Postgres + Redis)
No painel do Railway (Graph View):
1.  Clique com botão direito -> **Add Service** -> **Database** -> **PostgreSQL**.
2.  Clique com botão direito -> **Add Service** -> **Database** -> **Redis**.

O Railway vai criar automaticamente as variáveis `PGHOST`, `PGUSER`, `PGPASSWORD`, etc. O nosso `docker-compose.railway.yml` já está configurado para ler isso!

## Passo 5: Deploy
O Railway vai detectar o `docker-compose.railway.yml` (ou você pode apontar para ele nas configurações se ele tentar usar o Dockerfile direto).
Se ele tentar usar o Dockerfile, vá em **Settings** -> **Build** -> **Watch Paths** e aponte para o arquivo compose, ou simplesmente deixe ele construir o Python e adicione a Evolution como um serviço extra (Docker Image).

**DICA DE OURO**: O jeito mais fácil no Railway é subir **Serviço por Serviço**:
1.  **Python**: Conecte o Repo. Ele vai usar o `Dockerfile`.
2.  **Evolution**: Adicione um serviço "Docker Image" com a imagem `atendai/evolution-api:v1.7.4` e configure as variáveis de ambiente apontando para o Postgres/Redis que você criou.

---

# 🚀 Frontend (Vercel/Netlify)

1.  Vá no [Vercel](https://vercel.com).
2.  Importe o mesmo repositório do GitHub.
3.  Nas configurações de **Build**, aponte a pasta raiz para `frontend`.
4.  Adicione a variável de ambiente:
    -   `VITE_API_URL`: A URL que o Railway gerou para o seu Python Backend (ex: `https://chatbot-production.up.railway.app`).
5.  Deploy!
