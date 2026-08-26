# Documentação do Diálogo com IA — Etapa 2: Geração da Massa de Dados de Treinamento

**Disciplina:** Mineração de Dados  
**Atividade:** ATIVIDADE PRÁTICA 1 — Algoritmo Classificador Bayesiano  
**Responsável:** Mateus de Souza Arruda & Lorena Strobel Campos  
**Data:** 25/08/2026  

---

## Contexto do Prompt

Para atender aos requisitos da Etapa 2 descritos no enunciado e detalhados nos artefatos de planejamento:
1. Gerar **pelo menos 100 registros** de treinamento (alvo: 120 registros para permitir curadoria).
2. Manter **padrões intencionais e realistas** coerentes com a modelagem definida na Etapa 1 (`etapa1.md`).
3. Manter **distribuição razoável entre as classes** (alvo: ~60% `Não` / ~40% `Sim`).
4. Utilizar estritamente as **7 features discretizadas** e o rótulo binário `cancelou`.

---

## Prompt Utilizado para a Geração dos Dados

```text
Atue como cientista de dados. Preciso gerar uma massa de dados de treinamento para um
classificador Naive Bayes em SQL, para uma atividade acadêmica de mineração de dados.

CONTEXTO: plataforma de e-commerce quer prever, no momento do checkout, se um pedido será
cancelado, para acionar medidas preventivas (ofertas direcionadas, frete facilitado, suporte).

MODELAGEM JÁ FECHADA (use exatamente estas features e categorias):
- metodo_pagamento: "Síncrono (Cartão)" | "Síncrono (Pix)" | "Assíncrono (Boleto)"
- proporcao_frete: "Baixa" | "Média" | "Alta"
- prazo_entrega: "Expresso" | "Padrão" | "Longo"
- historico_cliente: "Impecável" | "Aceitável" | "Risco"
- dispositivo_compra: "Desktop" | "Mobile App" | "Mobile Web"
- horario_compra: "Comercial" | "Noturno" | "Madrugada"
- tipo_autenticacao: "Visitante" | "Nova Conta" | "Conta Antiga"
- rótulo: cancelou = "Sim" | "Não"  (cada linha é UM pedido)

REGRAS DA GERAÇÃO:
1) Gere 120 pedidos distintos.
2) Use SOMENTE os valores listados acima — nada além dessas categorias.
3) Padrões intencionais (não aleatórios):
   - Pedidos com Síncrono (Cartão) + proporcao_frete Baixa + prazo Expresso + Conta Antiga +
     histórico Impecável + Desktop + horário Comercial devem ser, em ~90% dos casos, cancelou=Não.
   - Pedidos com Assíncrono (Boleto) + proporcao_frete Alta + prazo Longo + Visitante +
     histórico Risco + Mobile Web + Madrugada devem ser, em ~85% dos casos, cancelou=Sim.
   - Perfis intermediários (misturas) devem ter resultado misto (~50/50).
4) Distribuição das classes: cerca de 60% "Não" e 40% "Sim" (evitar desbalanceamento).
5) Inclua variedade: todas as categorias de cada feature devem aparecer várias vezes,
   e nenhuma combinação deve dominar a base inteira.
6) Garanta coerência interna: ex.: "Visitante" não combina com "Conta Antiga"; histórico
   "Impecável" não combina com cancelamentos frequentes do próprio cliente.

ENTREGUE: uma tabela CSV com cabeçalho exato:
metodo_pagamento,proporcao_frete,prazo_entrega,historico_cliente,dispositivo_compra,horario_compra,tipo_autenticacao,cancelou
Sem colunas extras. Não explique o código — apenas gere os dados no formato pedido.
```

---

## Síntese do Output Recebido da IA

O modelo gerou a massa de dados inicial com 120 registros no formato CSV, mantendo a correspondência exata com o esquema das 7 features e do rótulo `cancelou`. A massa gerada foi submetida à curadoria manual e à validação automatizada via script Python em `scripts/valida_etapa2.py`.
