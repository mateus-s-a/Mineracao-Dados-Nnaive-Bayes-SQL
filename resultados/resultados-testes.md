# Resultados dos Casos de Teste — Etapa 4

**Disciplina:** Mineração de Dados  
**Atividade:** ATIVIDADE PRÁTICA 1 — Algoritmo Classificador Bayesiano  
**Banco de dados:** `data/atividade.db` (120 registros de treinamento)  

---

## Tabela Comparativa de Resultados

| ID | Caso de Teste / Perfil | Prob. Cancelar (Sim) | Prob. Manter (Não) | Classificação Predita | Recomendação de Decisão |
|---|---|---|---|---|---|
| 1 | Perfil 1 — Baixo Risco (Transação Pragmática) | **0.09%** | **99.91%** | `BAIXO RISCO DE CANCELAMENTO` | Manter fluxo normal de processamento e faturamento do pedido |
| 2 | Perfil 2 — Alto Risco (Transação de Alto Atrito) | **99.57%** | **0.43%** | `ALTO RISCO DE CANCELAMENTO` | Acionar medida preventiva (cupom frete, oferta direcionada ou suporte em tempo real) |
| 3 | Perfil 3 — Ambíguo (Sinais Conflitantes) | **64.71%** | **35.29%** | `ALTO RISCO DE CANCELAMENTO` | Acionar medida preventiva (cupom frete, oferta direcionada ou suporte em tempo real) |
| 4 | Perfil 4 — Valor/Combinação Rara (Suavização Laplace) | **86.54%** | **13.46%** | `ALTO RISCO DE CANCELAMENTO` | Acionar medida preventiva (cupom frete, oferta direcionada ou suporte em tempo real) |
| 5 | Perfil 5 — Risco Moderado Transacional | **52.65%** | **47.35%** | `ALTO RISCO DE CANCELAMENTO` | Acionar medida preventiva (cupom frete, oferta direcionada ou suporte em tempo real) |

---

## Detalhamento por Caso de Teste

### Caso 1: Perfil 1 — Baixo Risco (Transação Pragmática)
- **Características do Pedido:** `Pagamento Síncrono (Cartão) + Frete Baixo + Prazo Expresso + Cliente Impecável + Desktop + Comercial + Conta Antiga`
- **Probabilidade P(Sim):** 0.09%
- **Probabilidade P(Não):** 99.91%
- **Veredito:** `BAIXO RISCO DE CANCELAMENTO`
- **Análise do Resultado:** Confirmou a intuição teórica de baixo risco. O cartão de crédito aliado à alta fidelidade do cliente e frete insignificante geraram probabilidade esmagadora a favor da manutenção do pedido.

### Caso 2: Perfil 2 — Alto Risco (Transação de Alto Atrito)
- **Características do Pedido:** `Pagamento Assíncrono (Boleto) + Frete Alto + Prazo Longo + Cliente Risco + Mobile Web + Madrugada + Visitante`
- **Probabilidade P(Sim):** 99.57%
- **Probabilidade P(Não):** 0.43%
- **Veredito:** `ALTO RISCO DE CANCELAMENTO`
- **Análise do Resultado:** Confirmou a intuição teórica de alto risco. O acúmulo de fatores de atrito (boleto pendente, frete caro, compra impulsiva de madrugada por visitante) elevou drasticamente a probabilidade de cancelamento.

### Caso 3: Perfil 3 — Ambíguo (Sinais Conflitantes)
- **Características do Pedido:** `Pagamento Síncrono (Cartão) + Frete Alto + Prazo Padrão + Cliente Aceitável + Mobile App + Madrugada + Nova Conta`
- **Probabilidade P(Sim):** 64.71%
- **Probabilidade P(Não):** 35.29%
- **Veredito:** `ALTO RISCO DE CANCELAMENTO`
- **Análise do Resultado:** Apresentou probabilidade intermediária. O uso do Cartão de Crédito e do App Móvel reduziram o risco, contrabalançando o frete alto e o horário da madrugada.

### Caso 4: Perfil 4 — Valor/Combinação Rara (Suavização Laplace)
- **Características do Pedido:** `Pagamento Síncrono (Pix) + Frete Alto + Prazo Expresso + Cliente Risco + Desktop + Madrugada + Visitante`
- **Probabilidade P(Sim):** 86.54%
- **Probabilidade P(Não):** 13.46%
- **Veredito:** `ALTO RISCO DE CANCELAMENTO`
- **Análise do Resultado:** Demonstrou a eficácia da Suavização de Laplace (alpha=1). Mesmo contendo uma combinação não vista exatamente nesta forma no treinamento, a constante pseudo-contagem evitou indeterminação por divisão por zero e produziu uma estimativa probabilística estável.

### Caso 5: Perfil 5 — Risco Moderado Transacional
- **Características do Pedido:** `Pagamento Síncrono (Pix) + Frete Média + Prazo Padrão + Cliente Aceitável + Mobile Web + Noturno + Nova Conta`
- **Probabilidade P(Sim):** 52.65%
- **Probabilidade P(Não):** 47.35%
- **Veredito:** `ALTO RISCO DE CANCELAMENTO`
- **Análise do Resultado:** Mostrou perfil moderado com leve tendência a não cancelamento, refletindo um comportamento de compra rotineiro em e-commerce via Pix.
