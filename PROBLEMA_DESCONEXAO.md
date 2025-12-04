# PROBLEMA: WhatsApp Desconectando Sozinho

## Causas Possíveis

1. **Evolution API sem persistência de dados** (mais provável)
   - O Railway pode estar reiniciando o container
   - Os dados da sessão não estão sendo salvos

2. **Múltiplas conexões simultâneas**
   - WhatsApp Web aberto em outro lugar
   - Outro sistema tentando conectar

3. **Timeout de inatividade**
   - WhatsApp desconecta após muito tempo sem uso

## Solução 1: Verificar Variáveis de Ambiente da Evolution API

No Railway, serviço **evolution-api**, adicione/verifique:

```
DATABASE_CONNECTION_URI=postgresql://...  (se tiver PostgreSQL)
DATABASE_SAVE_DATA_INSTANCE=true
DATABASE_SAVE_DATA_NEW_MESSAGE=true
```

## Solução 2: Adicionar Volume Persistente (Recomendado)

A Evolution API precisa salvar os dados da sessão em um volume persistente.

### No Railway:

1. Vá no serviço **evolution-api**
2. Clique em **"Variables"**
3. Adicione:
   ```
   STORE_MESSAGES=true
   STORE_CONTACTS=true
   STORE_CHATS=true
   ```

## Solução 3: Usar Redis para Sessões

Adicione no Railway (evolution-api):
```
REDIS_ENABLED=true
REDIS_URI=redis://...  (se tiver Redis configurado)
```

## Solução Temporária (Enquanto Configuramos)

Execute este script para reconectar automaticamente:

```bash
py reconectar_automatico.py
```

## Verificação

Execute para ver os logs da Evolution API:
1. Acesse Railway
2. Clique em evolution-api
3. Vá em "Deployments"
4. Clique no deploy atual
5. Veja os logs

Procure por:
- "Session lost"
- "Connection closed"
- "Logout"
