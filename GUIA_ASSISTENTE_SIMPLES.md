# 🤖 GUIA: Assistente IA Simples (WhatsApp)

Este guia vai te ajudar a colocar no ar um robô que responde seus clientes automaticamente, mas fica quieto quando você (contador) entra na conversa.

## 📋 Passo 1: Importar no n8n

1.  Acesse seu n8n: `http://localhost:5678`
2.  Vá em **Workflows** > **Add Workflow**.
3.  Clique nos 3 pontinhos (canto superior direito) > **Import from File**.
4.  Selecione o arquivo `n8n-workflow-simple-agent.json` que acabei de criar na sua área de trabalho (pasta chatbot).

## 🔑 Passo 2: Configurar OpenAI

1.  No n8n, vá em **Credentials** (menu esquerdo).
2.  Clique em **Add Credential** e procure por **OpenAI API**.
3.  Cole sua API Key da OpenAI (se não tiver, crie em platform.openai.com).
4.  Salve.

## 🔗 Passo 3: Conectar WhatsApp

1.  No workflow importado, clique no primeiro nó (**Webhook WhatsApp**).
2.  Copie a URL que aparece em **Production URL** (algo como `http://localhost:5678/webhook/whatsapp-simple`).
3.  Acesse o Evolution Manager: `http://localhost:8080/manager`.
4.  Clique na sua instância (`chatbot`).
5.  Vá em **Webhooks**.
6.  Cole a URL que você copiou (⚠️ **Atenção**: Se estiver usando Docker, troque `localhost` por `chatbot_n8n`. Ex: `http://chatbot_n8n:5678/webhook/whatsapp-simple`).
7.  Marque a opção **MESSAGES_UPSERT**.
8.  Salve.

## ▶️ Passo 4: Ativar

1.  Volte no n8n.
2.  No topo direito do workflow, mude de **Inactive** para **Active** (verde).

## 🧪 Como Testar

1.  Peça para um amigo mandar "Oi" para o número do escritório.
    -   ✅ O robô deve responder.
2.  Pegue seu celular (do escritório) e responda seu amigo manualmente.
    -   ✅ O robô NÃO deve responder sua mensagem.
3.  Peça para seu amigo responder de volta.
    -   ⚠️ **Atenção**: Nesta versão simples, o robô vai tentar responder de novo. Se quiser que ele pare, você precisa instruir a IA no prompt (dentro do nó AI Agent) ou simplesmente ignorar.

## 📝 Personalizar a IA

Para mudar como o robô fala:
1.  Abra o nó **AI Agent**.
2.  Edite o texto em **System Message**.
    -   Ex: "Você é o assistente do Escritório Silva..."
