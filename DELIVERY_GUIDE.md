# Guia de Entrega e Negócio: Agente de IA para Contabilidade

Este guia detalha como transformar o protótipo atual em um produto comercializável para escritórios de contabilidade.

## 1. O Produto: "Secretária Contábil Inteligente"

### Funcionalidades para Vender (O que ela faz?)
1.  **Atendimento 24/7**: Responde clientes instantaneamente, sábado, domingo e feriados.
2.  **Triagem Automática**: Identifica quem é o cliente (pelo telefone) e qual a empresa dele.
3.  **Envio de Documentos (Self-Service)**:
    *   "Me manda o DAS?" -> A IA busca o PDF e envia.
    *   "Cadê o boleto do honorário?" -> Envia na hora.
4.  **Tira-Dúvidas Tributárias (Nível 1)**:
    *   "Qual a alíquota do Simples?"
    *   "Quando vence o IR?"
    *   *Nota: A IA responde com base em uma base de conhecimento controlada.*
5.  **Leitura de Documentos (Multimodal)**:
    *   Cliente manda foto de um recibo -> IA lê o valor e data e já lança no sistema (ou avisa o contador).
6.  **Transbordo Inteligente**:
    *   Se a IA não souber ou o cliente estiver bravo, ela passa para um humano e avisa no painel.

---

## 2. O Painel de Controle (O que o Contador vê?)

Para o cliente (contador) sentir controle, o painel precisa ter:

### A. Gestão de Clientes (Já criamos!)
- Lista de quem pode falar com o bot.
- Cadastro rápido de novos clientes.

### B. "Cérebro da IA" (Configurações)
- **Personalidade**: "Edite aqui como a IA deve se comportar (mais formal, mais amiga)".
- **Base de Conhecimento**: "Faça upload de PDFs (leis internas, manuais) para a IA estudar".
- **Horário de Funcionamento**: "Defina quando a IA atende sozinha".

### C. Histórico e Auditoria
- Ver todas as conversas.
- Ver onde a IA "errou" para corrigir.

---

## 3. Roadmap de Entrega (Passo a Passo)

### Fase 1: O Piloto (Gratuito ou Custo Reduzido)
*   **Objetivo**: Validar com 1 escritório parceiro.
*   **Setup**:
    *   Instale em um servidor VPS (ex: DigitalOcean, Hetzner) ~R$ 40/mês.
    *   Use um número de WhatsApp de teste (ou um secundário do escritório).
*   **Funcionalidades**: Apenas Triagem + Tira-Dúvidas Básico.
*   **Duração**: 15 a 30 dias.

### Fase 2: O Produto (Cobrança Mensal)
*   **Objetivo**: Vender para outros escritórios.
*   **Setup**: Multi-tenant (um painel para vários escritórios) ou Instâncias separadas (Docker facilita isso).
*   **Preço Sugerido**:
    *   **Setup Inicial**: R$ 1.000 - R$ 3.000 (Configuração, Treinamento da IA).
    *   **Mensalidade**: R$ 500 - R$ 1.500 (Manutenção, Custos de API).

### Fase 3: Escala (SaaS)
*   **Objetivo**: Venda automática.
*   **Integrações**: Conectar com sistemas contábeis reais (Domínio, ContaAzul) para puxar guias de verdade.

---

## 4. Estratégia de Venda
*   **Dor do Contador**: "Perco muito tempo enviando 2ª via de boleto e respondendo coisa boba no WhatsApp".
*   **Solução**: "Nossa IA faz isso por você. Você só atende o que for complexo."
*   **Segurança**: "A IA só responde o que está na base de dados. Ela não inventa leis."

---

## 5. Próximos Passos Técnicos (Agora)
Para entregar o que você pediu ("Painel de fácil uso"), vamos:
1.  Criar a aba **Configurações** no Front-end.
2.  Permitir que o contador edite o **Prompt do Sistema** (Personalidade) direto pelo site.
3.  Criar uma aba **Logs** para ver as conversas recentes.
