# Documentação do Diálogo com IA — Etapa 3: Implementação do Classificador Naive Bayes

**Disciplina:** Mineração de Dados  
**Atividade:** ATIVIDADE PRÁTICA 1 — Algoritmo Classificador Bayesiano  
**Responsável:** Mateus de Souza Arruda & Lorena Strobel Campos  
**Data:** 26/08/2026  

---

## Contexto do Prompt

Implemente o classificador na linguagem SQL. O algoritmo deve conter obrigatoriamente:
1. Cálculo das probabilidades a priori P(classe)
2. Cálculo das verossimilhanças P(feature = valor | classe) com suavização de Laplace
3. Classificação usando log-probabilidades — para evitar underflow numérico
4. Normalização do score final em probabilidade entre 0 % e 100 %
5. Saída com a probabilidade de cada classe e uma recomendação de decisão

---

## Prompt Utizado para o algoritmo de Naive Bayes

```text
Atue como um Engenheiro de Dados Sênior especialista em SQL e Machine Learning.

O contexto do nosso projeto é de E-commerce, com o objetivo de prever se um pedido será cancelado.

Possuo uma tabela SQLite chamada `treino`, populada com 120 registros gerados e validados na Etapa 2.

Utilize exclusivamente as colunas e categorias já definidas na massa de dados, sem criar novas features, alterar nomes das colunas ou adicionar novas variáveis.

Estrutura da tabela:

* Tabela: `treino`
* Coluna alvo: `cancelou` — valores possíveis: `'Sim'` ou `'Não'`
* Features:

  * `metodo_pagamento`
  * `proporcao_frete`
  * `prazo_entrega`
  * `historico_cliente`
  * `dispositivo_compra`
  * `horario_compra`
  * `tipo_autenticacao`

Categorias utilizadas na Etapa 2:

* `metodo_pagamento`: `'Síncrono (Cartão)'`, `'Síncrono (Pix)'`, `'Assíncrono (Boleto)'`
* `proporcao_frete`: `'Baixa'`, `'Média'`, `'Alta'`
* `prazo_entrega`: `'Expresso'`, `'Padrão'`, `'Longo'`
* `historico_cliente`: `'Impecável'`, `'Aceitável'`, `'Risco'`
* `dispositivo_compra`: `'Desktop'`, `'Mobile App'`, `'Mobile Web'`
* `horario_compra`: `'Comercial'`, `'Noturno'`, `'Madrugada'`
* `tipo_autenticacao`: `'Visitante'`, `'Nova Conta'`, `'Conta Antiga'`

O caso de teste que desejo classificar possui os seguintes valores:

* `metodo_pagamento = 'Assíncrono (Boleto)'`
* `proporcao_frete = 'Alta'`
* `prazo_entrega = 'Longo'`
* `historico_cliente = 'Risco'`
* `dispositivo_compra = 'Mobile Web'`
* `horario_compra = 'Noturno'`
* `tipo_autenticacao = 'Visitante'`

Escreva um único script SQL compatível com SQLite, utilizando consultas estruturadas passo a passo, para implementar o algoritmo Classificador Naive Bayes.

O script deve obrigatoriamente conter:

1. Cálculo das probabilidades a priori P(classe), para as classes `'Sim'` e `'Não'`.
2. Cálculo das verossimilhanças P(feature = valor | classe) utilizando suavização de Laplace, com a fórmula `(contagem + 1) / (total da classe + tamanho do vocabulário da feature)`.
3. Classificação utilizando log-probabilidades, com `LN()` ou outra função compatível com SQLite, evitando a multiplicação direta de várias probabilidades pequenas.
4. Normalização dos scores em probabilidades entre 0% e 100%, utilizando exponenciação (`EXP()`).
5. Uma saída final contendo a probabilidade de cancelamento (`Sim`), a probabilidade de não cancelamento (`Não`) e uma recomendação de decisão em texto.

Organize o script em CTEs (`WITH`) ou outra estrutura equivalente que permita identificar claramente cada etapa do cálculo.

Adicione comentários curtos explicando a finalidade de cada etapa do código.

Não altere a lógica matemática do Naive Bayes e não introduza métodos de classificação diferentes do solicitado.
```

---
