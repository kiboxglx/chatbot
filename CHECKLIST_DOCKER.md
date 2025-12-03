# ✅ CHECKLIST DE IMPLANTAÇÃO - DOCKER

## 📋 PRÉ-REQUISITOS

- [ ] Docker Desktop instalado e rodando
- [ ] Docker Compose disponível (`docker-compose --version`)
- [ ] Porta 8000, 5678 e 8080 livres
- [ ] Chave da OpenAI em mãos

---

## 🔧 CONFIGURAÇÃO INICIAL

### 1. Configurar Variáveis de Ambiente

- [ ] Abrir arquivo `.env`
- [ ] Substituir `sua_chave_openai_aqui` pela chave real
- [ ] Verificar se `WHATSAPP_API_URL=http://evolution-api:8080`
- [ ] Salvar o arquivo

### 2. Validar Arquivos

- [ ] `Dockerfile` existe na raiz
- [ ] `docker-compose.yml` tem a rede `chatbot_network`
- [ ] `requirements.txt` está atualizado
- [ ] Pasta `storage/boletos` existe

---

## 🚀 PRIMEIRA EXECUÇÃO

### 3. Iniciar Containers

```bash
docker-compose up -d
```

- [ ] Comando executado sem erros
- [ ] Aguardar download das imagens (pode demorar)
- [ ] Build do chatbot concluído

### 4. Verificar Status

```bash
docker-compose ps
```

Verificar se estão rodando:
- [ ] `chatbot_backend` (Up)
- [ ] `chatbot_n8n` (Up)
- [ ] `evolution_api` (Up)
- [ ] `evolution_postgres` (Up)
- [ ] `evolution_redis` (Up)

### 5. Acessar Serviços

- [ ] http://localhost:8000/docs → Swagger do Chatbot
- [ ] http://localhost:5678 → n8n (login: admin/chatbot2024)
- [ ] http://localhost:8080 → Evolution API

---

## 🧪 TESTES DE CONECTIVIDADE

### 6. Teste Interno (Dentro do Container)

```bash
docker exec -it chatbot_backend python test_docker_network.py
```

- [ ] Evolution API acessível
- [ ] n8n acessível
- [ ] Todos os testes passaram

### 7. Teste Manual (Curl)

Entre no container do n8n:
```bash
docker exec -it chatbot_n8n /bin/sh
```

Dentro do container:
```bash
curl http://evolution-api:8080
curl http://chatbot:8000/health
```

- [ ] Evolution API respondeu
- [ ] Chatbot respondeu

### 8. Verificar Rede Docker

```bash
docker network inspect chatbot_chatbot_network
```

- [ ] Todos os 5 containers aparecem na lista
- [ ] Cada um tem um IP na subnet

---

## 📱 CONFIGURAR WHATSAPP

### 9. Conectar WhatsApp na Evolution API

Acesse: http://localhost:8080

- [ ] Criar instância "chatbot"
- [ ] Gerar QR Code
- [ ] Escanear com WhatsApp
- [ ] Status: "open"

### 10. Testar Envio de Mensagem

```bash
python test_simulator.py
```

- [ ] Mensagem enviada com sucesso
- [ ] Resposta recebida do bot

---

## 🔄 CONFIGURAR N8N

### 11. Criar Workflow no n8n

Acesse: http://localhost:5678

- [ ] Login realizado (admin/chatbot2024)
- [ ] Importar workflow `n8n-workflow-chatbot.json`
- [ ] Ativar workflow

### 12. Configurar Webhook no n8n

No nó HTTP Request, usar:
```
http://evolution-api:8080/message/sendText/chatbot
```

- [ ] URL configurada (SEM localhost!)
- [ ] Header `apikey` configurado
- [ ] Testar execução manual

---

## 🎯 TESTE COMPLETO (E2E)

### 13. Fluxo Completo

1. Enviar mensagem via WhatsApp
2. Evolution API recebe
3. n8n processa
4. Chatbot classifica intenção
5. Resposta enviada

- [ ] Cliente identificado no banco
- [ ] Intenção classificada corretamente
- [ ] Resposta enviada via WhatsApp
- [ ] Logs sem erros

### 14. Testar Intenções

Enviar mensagens de teste:

- [ ] "Quero a 2ª via do boleto" → Envia arquivo
- [ ] "Quero falar com atendente" → Mensagem de encaminhamento
- [ ] "Olá" → Mensagem genérica

---

## 📊 MONITORAMENTO

### 15. Ver Logs em Tempo Real

```bash
docker-compose logs -f
```

- [ ] Logs do chatbot aparecem
- [ ] Logs da Evolution API aparecem
- [ ] Logs do n8n aparecem
- [ ] Sem erros críticos

### 16. Verificar Recursos

```bash
docker stats
```

- [ ] CPU < 50%
- [ ] Memória < 2GB
- [ ] Sem containers reiniciando

---

## 🔒 SEGURANÇA

### 17. Validar Configurações

- [ ] `.env` NÃO está no Git
- [ ] Senhas fortes configuradas
- [ ] API Keys não expostas nos logs
- [ ] Portas expostas apenas as necessárias

---

## 📚 DOCUMENTAÇÃO

### 18. Ler Guias

- [ ] `DOCKER_GUIDE.md` - Guia de uso
- [ ] `SOLUCAO_DOCKER.md` - Solução de conectividade
- [ ] `README_FINAL.md` - Documentação geral

---

## 🎉 FINALIZAÇÃO

### 19. Backup

- [ ] Exportar workflows do n8n
- [ ] Backup do banco `contabilidade.db`
- [ ] Backup da pasta `storage/`

### 20. Produção (Opcional)

- [ ] Trocar SQLite por PostgreSQL
- [ ] Configurar domínio e SSL
- [ ] Configurar variáveis de produção
- [ ] Deploy em servidor (AWS/Azure/GCP)

---

## 🆘 TROUBLESHOOTING

### Se algo der errado:

```bash
# Parar tudo
docker-compose down

# Ver logs
docker-compose logs chatbot
docker-compose logs evolution-api

# Reconstruir
docker-compose up -d --build

# Limpar tudo (CUIDADO!)
docker-compose down -v
docker system prune -a
```

---

## ✅ STATUS FINAL

- [ ] Todos os containers rodando
- [ ] Conectividade validada
- [ ] WhatsApp conectado
- [ ] n8n configurado
- [ ] Testes E2E passando
- [ ] Documentação lida
- [ ] Backup realizado

**🎊 PARABÉNS! Sistema 100% operacional!**
