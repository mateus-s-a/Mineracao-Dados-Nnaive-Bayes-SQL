# Análise dos Resultados e Reflexão Crítica — Etapa 4

**Disciplina:** Mineração de Dados  
**Professor:** Orlando Júnior  
**Dupla:** Lorena Strobel Campos & Mateus de Souza Arruda  
**Atividade:** ATIVIDADE PRÁTICA 1 — Algoritmo Classificador Bayesiano  
**Repositório:** https://github.com/mateus-s-a/Mineracao-Dados-Nnaive-Bayes-SQL  
**Data:** 27/08/2026  

---

## 1. Contexto dos Experimentos

O algoritmo Naive Bayes implementado em SQL (`sql/classificador.sql` e `sql/testes.sql`) foi submetido à avaliação contra o banco de dados relacional `data/atividade.db`, contendo a massa de treinamento curada com **120 registros de pedidos de e-commerce** (56.7% classe `Não` / 43.3% classe `Sim`).

Foram executados **5 casos de teste** cobrindo perfis pragmáticos (baixo risco), transações de atrito (alto risco), perfis ambíguos (sinais conflitantes) e testes de resiliência com a Suavização de Laplace.

---

## 2. Resposta às Perguntas Obrigatórias do Enunciado

### 2.1 Pergunta 1: O modelo classificou corretamente conforme a intuição sobre o domínio?

**Resposta:** **Sim, perfeitamente.** As classificações preditas pelo modelo em SQL demonstraram total aderência à psicologia do consumidor no comércio eletrônico e às hipóteses estabelecidas na Etapa 1:

1. **Caso 1 (Perfil Pragmático / Baixo Risco):** Obteve **$99.91\%$ de probabilidade para `Não` (manter pedido)** e apenas $0.09\%$ para `Sim`. A intuição de que uma compra em Cartão de Crédito feita por cliente antigo, com frete baixo e prazo expresso em horário comercial representa uma transação segura foi inteiramente confirmada pelos dados.
2. **Caso 2 (Perfil de Alto Atrito / Alto Risco):** Obteve **$99.57\%$ de probabilidade para `Sim` (cancelar pedido)**. O acúmulo de fatores desfavoráveis (pagamento assíncrono por Boleto pendente, frete caro, entrega demorada, compra na madrugada via Mobile Web por usuário visitante) confirmou a hipótese de arrependimento pós-compra e abandono passivo.
3. **Caso 3 (Perfil Ambíguo / Sinais Conflitantes):** Obteve **$64.71\%$ para `Sim` (cancelar pedido)**. A presença do Cartão de Crédito e do Mobile App atuaram como forças protetoras contra o cancelamento, mas o peso do frete alto e o horário da madrugada superaram os fatores positivos, resultando em uma classificação de alto risco com margem moderada, exatamente como esperado para um perfil limítrofe.
4. **Caso 4 (Combinação Rara / Laplace):** Classificado como **$86.54\%$ para `Sim`**, demonstrando resiliência probabilística.
5. **Caso 5 (Risco Moderado Transacional):** Obteve **$52.65\%$ para `Sim`**, situando-se muito próximo do ponto de decisão neutro (50%), refletindo a ambiguidade natural de transações via Pix em contas recentes.

---

### 2.2 Pergunta 2: Quais features tiveram maior log-odds (maior poder discriminativo)?

**Resposta:** O poder discriminativo de cada categoria de feature foi quantificado através do cálculo do **Log-Odds** (logaritmo da razão de verossimilhanças entre as classes):

$$\text{Log-Odds}(F = v) = \ln \left( \frac{P(F = v \mid \text{Sim})}{P(F = v \mid \text{Não})} \right)$$

Valores positivos indicam que a característica impulsiona a probabilidade de cancelamento (`Sim`), enquanto valores negativos indicam que a característica é protetora contra o cancelamento (`Não`).

#### Tabela de Poder Discriminativo (Log-Odds Calculado no Dataset de Treino):

| Posição | Feature | Categoria | $P(F=v \mid \text{Sim})$ | $P(F=v \mid \text{Não})$ | Log-Odds | Efeito no Modelo |
|---|---|---|---|---|---|---|
| **1º** | `tipo_autenticacao` | **Conta Antiga** | $0.0909$ | $0.4366$ | **-1.5692** | Forte Protetor (Reduz Risco) |
| **2º** | `proporcao_frete` | **Alta** | $0.5455$ | $0.1690$ | **+1.1716** | Forte Indutor de Risco |
| **3º** | `metodo_pagamento` | **Síncrono (Cartão)** | $0.1636$ | $0.5070$ | **-1.1309** | Forte Protetor |
| **4º** | `historico_cliente` | **Impecável** | $0.1818$ | $0.4648$ | **-0.9386** | Forte Protetor |
| **5º** | `historico_cliente` | **Risco** | $0.5273$ | $0.2113$ | **+0.9146** | Forte Indutor de Risco |
| **6º** | `horario_compra` | **Comercial** | $0.1818$ | $0.4507$ | **-0.9078** | Protetor |
| **7º** | `metodo_pagamento` | **Assíncrono (Boleto)** | $0.5091$ | $0.2113$ | **+0.8795** | Indutor de Risco |
| **8º** | `prazo_entrega` | **Longo** | $0.4727$ | $0.1972$ | **+0.8744** | Indutor de Risco |
| **9º** | `dispositivo_compra` | **Desktop** | $0.1636$ | $0.3803$ | **-0.8433** | Protetor |

**Conclusão dos Log-Odds:**
- A variável de **maior poder discriminativo absoluto** foi `tipo_autenticacao = 'Conta Antiga'` ($\text{Log-Odds} = -1.5692$). A fidelidade do cliente provou ser o maior fator de retenção do e-commerce.
- Dentre as variáveis indutoras de cancelamento, `proporcao_frete = 'Alta'` apresentou o **maior impacto isolado** ($\text{Log-Odds} = +1.1716$), confirmando a hipótese de que o custo desproporcional do envio gera forte atrito e arrependimento pós-compra.

---

### 2.3 Pergunta 3: O que acontece quando se testa um perfil com valores não vistos no treinamento?

**Resposta:** Em um classificador Naive Bayes tradicional sem suavização, se uma determinada categoria $v$ nunca tiver sido observada para a classe $C$ na base de treinamento ($k = 0$), a verossimilhança $P(F=v \mid C) = \frac{0}{N_C} = 0$. Na multiplicação das probabilidades, esse zero "zeraria" todo o score da classe, independentemente de quão favoráveis fossem todas as outras 6 features (problema da probabilidade zero).

No nosso classificador SQL, **esse problema foi completamente resolvido com a Suavização de Laplace ($\alpha = 1.0$)**, implementada na CTE `Log_Probabilidades`:

$$P(F_i = v_i \mid C) = \frac{c_i + 1.0}{N_C + V_i}$$

Onde:
- $c_i$ é a contagem observada da categoria na classe;
- $1.0$ é a pseudo-contagem de Laplace;
- $N_C$ é o total de registros da classe (52 para `Sim`, 68 para `Não`);
- $V_i$ é o número de categorias distintas da feature $i$ (tamanho do vocabulário).

**Resultado Prático no Caso 4:** Mesmo ao submeter um pedido com combinação inédita no treinamento, a pseudo-contagem garantiu um valor mínimo não-nulo no numerador ($0 + 1 = 1$), permitindo que o modelo calculasse log-scores estáveis sem erros numéricos ou divisão por zero, resultando em uma classificação robusta ($86.54\%$ `Sim`).

---

### 2.4 Pergunta 4: Quais são as limitações do Naive Bayes neste domínio específico (e-commerce)?

**Resposta:** A principal limitação do Naive Bayes é a sua **premissa de independência condicional forte** (a hipótese "ingênua"). O algoritmo assume que, dada a classe do pedido (cancelado ou não), a ocorrência de qualquer feature é estatisticamente independente de qualquer outra.

No domínio do e-commerce real, essa suposição é **frequentemente violada**:

1. **Correlação entre Dispositivo, Horário e Forma de Pagamento:** Compras realizadas de madrugada (`horario_compra = 'Madrugada'`) via dispositivo móvel (`dispositivo_compra = 'Mobile Web'`) possuem altíssima correlação com a opção por boleto bancário (`metodo_pagamento = 'Assíncrono (Boleto)'`). O Naive Bayes trata essas três evidências como independentes e multiplica (soma nos logs) o peso de cada uma, o que pode levar a um **superdimensionamento da probabilidade** (superconfiança estatística em valores de borda próximos a 99.9%).
2. **Ausência de Captura de Interações Não-Lineares:** O modelo não consegue aprender regras condicionais compostas (ex: *"Boleto só é perigoso se o prazo for Longo, mas é seguro se o frete for Grátis"*). Cada feature contribui de forma aditiva no espaço logarítmico, sem considerar sinergias ou neutralizações entre pares de variáveis.

---

## 3. Reflexão Crítica (Mínimo de 1 Parágrafo)

> **Reflexão Crítica sobre a Solução Desenvolvida:**
> 
> O algoritmo Naive Bayes demonstrou ser uma técnica de mineração de dados surpreendentemente eficaz, elegante e computacionalmente leve para o problema de decisão binária no e-commerce. A sua capacidade de ser totalmente codificado dentro de um SGBD relacional (SQLite) utilizando consultas SQL estruturadas em CTEs evidencia sua viabilidade prática para sistemas de recomendação e mitigação de risco em tempo real no momento do checkout, sem a necessidade de infraestruturas complexas de aprendizado de máquina. A inclusão da suavização de Laplace e a computação em escala logarítmica conferiram ao modelo total resiliência contra instabilidades numéricas e dados não vistos. Por outro lado, a principal fragilidade da abordagem reside na sua premissa ingênua de independência condicional entre as variáveis preditivas. No e-commerce, comportamentos de compra são intrinsecamente correlacionados (como a associação entre compras noturnas por dispositivos móveis e pagamentos assíncronos), o que faz com que o modelo acumule evidências redundantes e produza probabilidades extremas nas extremidades do espectro. Apesar dessa limitação teórica, para a finalidade de ordenação de risco e tomada de decisão operacional (como acionar cupons de retenção ou abrir chats de suporte), o Naive Bayes cumpre seu papel com alta explicabilidade e excelente relação custo-benefício.

---

*Documento de análise e reflexão crítica elaborado para a Etapa 4 da Atividade Prática 1.*
