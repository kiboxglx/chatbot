# 📋 PASSO 2: EXTRAÇÃO DE DADOS FINANCEIROS - GUIA COMPLETO

## ✅ O QUE FOI IMPLEMENTADO

### 1. **Serviço de IA (`app/services/ai_service.py`)**
Método: `analisar_documento_financeiro(media_path: str)`

**Funcionalidade:**
- Recebe o caminho de um arquivo (JPEG, PNG ou PDF).
- Faz upload para o Gemini Vision API.
- Usa um prompt especializado para extrair dados financeiros.
- Retorna JSON padronizado.

**Prompt Usado:**
```
Analise este documento financeiro (Recibo, Nota Fiscal, Boleto, Extrato).
Extraia os dados com precisão e retorne APENAS um JSON com este formato:
{
  "data_compra": "DD/MM/AAAA",
  "estabelecimento": "Nome da Loja/Banco",
  "valor_total": 0.00,
  "descricao_resumida": "Ex: Almoço, Gasolina, Boleto Internet",
  "categoria_sugerida": "Ex: Alimentação, Transporte, Custos Fixos"
}
```

---

### 2. **Endpoint da API (`app/api/tools.py`)**
Rota: `POST /tools/analisar_documento`

**Como funciona:**
1. Recebe um arquivo via `multipart/form-data`.
2. Valida o tipo (JPEG, PNG, PDF).
3. Salva temporariamente em `storage/temp/`.
4. Chama `BrainService.analisar_documento_financeiro()`.
5. Retorna o JSON estruturado.

**Exemplo de Resposta:**
```json
{
  "data_compra": "15/11/2024",
  "estabelecimento": "Restaurante Sabor & Arte",
  "valor_total": 85.50,
  "descricao_resumida": "Almoço executivo",
  "categoria_sugerida": "Alimentação"
}
```

---

## 🔧 COMO USAR NO N8N

### Opção 1: Nó HTTP Request (Recomendado)

```json
{
  "nodes": [
    {
      "name": "Analisar Documento",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://chatbot:8000/tools/analisar_documento",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "file",
              "value": "={{ $binary.data }}"
            }
          ]
        },
        "options": {
          "bodyContentType": "multipart-form-data"
        }
      }
    }
  ]
}
```

**Fluxo Completo no n8n:**
```
[Webhook Evolution] 
    → [Download Media] 
    → [HTTP Request: /tools/analisar_documento] 
    → [Google Sheets: Append Row]
```

---

### Opção 2: Teste Manual (cURL)

```bash
curl -X POST http://localhost:8000/tools/analisar_documento \
  -F "file=@/caminho/para/nota_fiscal.jpg"
```

---

## 📊 SCHEMA DE SAÍDA PADRONIZADO

| Campo                | Tipo   | Exemplo                          | Descrição                                    |
|----------------------|--------|----------------------------------|----------------------------------------------|
| `data_compra`        | string | "15/11/2024"                     | Data da transação (DD/MM/AAAA)               |
| `estabelecimento`    | string | "Posto Shell"                    | Nome do estabelecimento/banco                |
| `valor_total`        | float  | 250.00                           | Valor total da transação                     |
| `descricao_resumida` | string | "Abastecimento Gasolina Comum"   | Resumo do que foi comprado/pago              |
| `categoria_sugerida` | string | "Transporte"                     | Categoria contábil sugerida pela IA          |

**Categorias Possíveis:**
- Alimentação
- Transporte
- Custos Fixos (Aluguel, Luz, Internet)
- Material de Escritório
- Impostos e Taxas
- Outros

---

## 🧪 TESTANDO A IMPLEMENTAÇÃO

### 1. Verificar se o endpoint está ativo:
```bash
curl http://localhost:8000/docs
```
Procure por `/tools/analisar_documento` na documentação Swagger.

### 2. Testar com uma imagem de teste:
```bash
# Baixe uma nota fiscal de exemplo da internet ou tire uma foto
curl -X POST http://localhost:8000/tools/analisar_documento \
  -F "file=@nota_exemplo.jpg"
```

### 3. Verificar logs do backend:
```bash
docker logs chatbot_backend --tail 50
```

Você deve ver:
```
📄 Arquivo recebido: nota_exemplo.jpg (image/jpeg)
💾 Salvo em: storage/temp/doc_1733097234.567.jpg
Enviando documento para análise financeira: storage/temp/doc_1733097234.567.jpg
```

---

## 🔄 PRÓXIMOS PASSOS (PASSO 3)

Agora que a extração está pronta, você pode:

1. **Integrar com Google Sheets:**
   - Criar um nó no n8n que pega o JSON retornado.
   - Adiciona uma linha na planilha com os dados extraídos.

2. **Adicionar Validação Humana:**
   - Enviar o JSON para o contador revisar antes de gravar.
   - Criar um painel no frontend para aprovar/editar extrações.

3. **Melhorar a Precisão:**
   - Adicionar exemplos de documentos ao prompt (Few-Shot Learning).
   - Criar regras de validação (ex: data não pode ser futura).

---

## 📝 NOTAS TÉCNICAS

- **PDF vs Imagem:** O Gemini Vision lida com ambos nativamente. PDFs são convertidos internamente.
- **OCR:** Não é necessário OCR separado, o Gemini já faz isso.
- **Custo:** Cada análise consome ~1 requisição da API Gemini (~$0.001-0.005 por documento).
- **Segurança:** Arquivos são salvos em `storage/temp/` e podem ser deletados após processamento.

---

## 🐛 TROUBLESHOOTING

**Erro: "GEMINI_API_KEY não encontrada"**
→ Verifique se a chave está no `.env` e reinicie o Docker.

**Erro: "Tipo de arquivo não suportado"**
→ Certifique-se de enviar JPEG, PNG ou PDF.

**JSON incompleto ou com campos null**
→ Normal para documentos ilegíveis. A IA tenta inferir, mas pode falhar.

**Timeout na requisição**
→ Documentos grandes (PDFs de 10+ páginas) podem demorar. Aumente o timeout do n8n.
