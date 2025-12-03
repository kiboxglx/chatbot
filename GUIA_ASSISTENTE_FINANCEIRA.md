# 🤖 ASSISTENTE FINANCEIRA IA - GUIA COMPLETO

## 📋 O QUE ELA FAZ:

1. **📸 Lê Notas Fiscais/Cupons** - Envia foto → IA extrai dados → Salva automaticamente
2. **💬 Responde Perguntas** - "Quanto gastei esse mês?" → IA consulta planilha → Responde
3. **📊 Salva no Google Sheets** - Todos os gastos organizados automaticamente
4. **✅ Confirma Salvamento** - Mensagem formatada com os detalhes

---

## 🛠️ CONFIGURAÇÃO PASSO A PASSO

### PASSO 1: Criar Planilha no Google Sheets

1. Acesse: https://sheets.google.com
2. Crie uma nova planilha chamada: **"Controle Financeiro"**
3. Renomeie a aba para: **"Gastos"**
4. Crie os cabeçalhos na primeira linha:

| A | B | C | D |
|---|---|---|---|
| Data | Estabelecimento | Valor | Categoria |

5. Copie o **ID da planilha** (está na URL):
   ```
   https://docs.google.com/spreadsheets/d/[ESTE_É_O_ID]/edit
   ```

---

### PASSO 2: Configurar Credenciais no n8n

#### A. OpenAI API:

1. Acesse: https://platform.openai.com/api-keys
2. Crie uma nova API Key
3. No n8n:
   - Vá em **Settings → Credentials**
   - Clique em **"Add Credential"**
   - Selecione **"OpenAI API"**
   - Cole sua API Key
   - Salve como: `openai-credentials`

#### B. Google Sheets:

1. No n8n:
   - Vá em **Settings → Credentials**
   - Clique em **"Add Credential"**
   - Selecione **"Google Sheets OAuth2 API"**
   - Clique em **"Connect my account"**
   - Autorize o acesso
   - Salve como: `google-sheets-credentials`

---

### PASSO 3: Importar Workflow

1. Abra o n8n: http://localhost:5678
2. Clique em **"Workflows" → "Import from File"**
3. Selecione: `n8n-assistente-financeira-COMPLETO.json`
4. O workflow será carregado

---

### PASSO 4: Configurar IDs da Planilha

No workflow, você precisa substituir `SUA_PLANILHA_ID` em 2 nodes:

#### Node "Salvar no Sheets":
1. Clique no node
2. Em **"Document"**, clique em **"From list"**
3. Selecione sua planilha **"Controle Financeiro"**
4. Em **"Sheet"**, selecione **"Gastos"**

#### Node "Ler Planilha":
1. Clique no node
2. Repita o processo acima

---

### PASSO 5: Configurar Evolution API

1. Copie a URL do Webhook (no node "Webhook WhatsApp")
2. Acesse: http://localhost:8080/manager
3. Vá em **Webhook**
4. Configure:
   - **URL**: `http://chatbot_n8n:5678/webhook/financas`
   - **Events**: `MESSAGES_UPSERT`
   - **Enabled**: ✅

---

### PASSO 6: Ativar Workflow

1. No n8n, clique no toggle **"Inactive" → "Active"**
2. O workflow ficará verde

---

## 🎯 COMO USAR

### 1. Salvar Gasto (Foto):

**Você:**
- Envia foto do cupom/nota fiscal

**Assistente:**
```
✅ Gasto salvo com sucesso!

📊 Detalhes:
• Estabelecimento: _Supermercado ABC_
• Valor: *R$ 45,90*
• Data: 01/12/2025
• Categoria: Alimentação

_Registrado em 01/12/2025 19:11_
```

### 2. Consultar Gastos (Texto):

**Você:**
```
Quanto gastei esse mês?
```

**Assistente:**
```
📊 *Resumo de Dezembro/2025*

• *Total gasto:* R$ 1.234,56

*Por categoria:*
• Alimentação: R$ 450,00
• Transporte: R$ 320,00
• Lazer: R$ 150,00
• Outros: R$ 314,56

_Dados atualizados em 01/12/2025_
```

**Você:**
```
Onde gastei mais?
```

**Assistente:**
```
🏆 *Maiores gastos:*

1. *R$ 450,00* - Alimentação
2. *R$ 320,00* - Transporte
3. *R$ 150,00* - Lazer

💡 _Dica: Você gastou 36% do total em alimentação._
```

---

## 🔄 FLUXO COMPLETO

### Quando você envia uma IMAGEM:

```
Foto do Cupom
    ↓
Webhook WhatsApp
    ↓
Tem Imagem? → SIM
    ↓
Baixar Imagem
    ↓
OpenAI Vision (Extrai dados)
    ↓
Parse JSON
    ↓
Salvar no Google Sheets
    ↓
Formatar Mensagem de Sucesso
    ↓
Enviar Resposta WhatsApp
```

### Quando você envia TEXTO:

```
Mensagem de Texto
    ↓
Webhook WhatsApp
    ↓
Tem Imagem? → NÃO
    ↓
AI Agent (Processa pergunta)
    ↓
Ler Planilha (Busca dados)
    ↓
AI Agent (Gera resposta)
    ↓
Enviar Resposta WhatsApp
```

---

## 📊 ESTRUTURA DA PLANILHA

Após alguns gastos salvos, sua planilha ficará assim:

| Data | Estabelecimento | Valor | Categoria |
|------|----------------|-------|-----------|
| 01/12/2025 | Supermercado ABC | 45.90 | Alimentação |
| 01/12/2025 | Posto Shell | 150.00 | Transporte |
| 02/12/2025 | Restaurante XYZ | 85.50 | Alimentação |
| 02/12/2025 | Farmácia | 32.00 | Saúde |

---

## 🎨 FORMATAÇÃO DAS RESPOSTAS

A IA usa Markdown do WhatsApp:

- **Negrito**: `*texto*` → *texto*
- **Itálico**: `_texto_` → _texto_
- **Tachado**: `~texto~` → ~texto~
- **Monoespaçado**: `` `texto` `` → `texto`
- **Lista**: `• item` → • item

---

## ⚙️ CONFIGURAÇÕES AVANÇADAS

### Personalizar Categorias:

No node **"Extrair Dados (OpenAI Vision)"**, edite o prompt:

```
Categorias disponíveis:
- Alimentação
- Transporte
- Saúde
- Lazer
- Educação
- Moradia
- Vestuário
- Outros
```

### Adicionar Mais Campos:

1. Adicione colunas na planilha (ex: "Forma de Pagamento")
2. Atualize o prompt da IA para extrair esse campo
3. Adicione o campo no node "Salvar no Sheets"

### Mudar Modelo da IA:

No node **"Extrair Dados (OpenAI Vision)"**:
- **gpt-4o** - Mais preciso (recomendado)
- **gpt-4o-mini** - Mais rápido e barato
- **gpt-4-turbo** - Alternativa

---

## 🆘 TROUBLESHOOTING

### ❌ "Não consegui processar a imagem"

**Causas:**
- Imagem muito borrada
- Texto ilegível
- Formato não suportado

**Solução:**
- Tire foto mais nítida
- Certifique-se que o texto está legível
- Use JPG ou PNG

### ❌ "Erro ao salvar na planilha"

**Causas:**
- Credenciais do Google expiradas
- ID da planilha incorreto
- Planilha foi deletada

**Solução:**
- Reconecte as credenciais do Google
- Verifique o ID da planilha
- Certifique-se que a aba "Gastos" existe

### ❌ "AI Agent não responde"

**Causas:**
- API Key da OpenAI inválida
- Créditos da OpenAI esgotados
- Planilha vazia

**Solução:**
- Verifique sua API Key
- Adicione créditos na OpenAI
- Adicione alguns gastos manualmente

---

## 💰 CUSTOS

### OpenAI API:

- **gpt-4o**: ~$0.005 por imagem
- **gpt-4o-mini**: ~$0.001 por imagem
- **Texto**: ~$0.0001 por mensagem

**Estimativa mensal:**
- 100 fotos + 200 perguntas = ~$0.70/mês

### Google Sheets:

- **Gratuito** (até 5 milhões de células)

---

## 🎯 PRÓXIMAS MELHORIAS

- [ ] Gráficos automáticos
- [ ] Alertas de gastos excessivos
- [ ] Comparação mês a mês
- [ ] Exportar relatórios em PDF
- [ ] Integração com banco (via Open Finance)
- [ ] Reconhecimento de voz
- [ ] Lembretes de contas a pagar

---

## ✅ CHECKLIST DE CONFIGURAÇÃO

- [ ] Planilha criada no Google Sheets
- [ ] Cabeçalhos configurados (Data, Estabelecimento, Valor, Categoria)
- [ ] API Key da OpenAI obtida
- [ ] Credenciais configuradas no n8n
- [ ] Workflow importado
- [ ] IDs da planilha atualizados
- [ ] Webhook configurado na Evolution API
- [ ] Workflow ativado
- [ ] Teste com foto realizado
- [ ] Teste com pergunta realizado

---

**🎉 Pronto! Sua Assistente Financeira está funcionando!**

Qualquer dúvida, me chame! 😊
