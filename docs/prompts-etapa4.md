# Documentação do Diálogo com IA — Etapa 4: Análise dos Resultados e Aplicação

**Disciplina:** Mineração de Dados  
**Atividade:** ATIVIDADE PRÁTICA 1 — Algoritmo Classificador Bayesiano  
**Responsável:** Mateus de Souza Arruda & Lorena Strobel Campos  
**Data:** 27/08/2026  

---

## 1. Contexto dos Prompts da Etapa 4

Para atender às exigências da **Etapa 4 — Aplicação e Análise dos Resultados**, conduzimos diálogos orientados com a IA para:
1. Formular os 5 perfis de teste representativos de cenários reais de e-commerce.
2. Calcular e interpretar os Log-Odds das variáveis para identificar o ranking de poder discriminativo.
3. Avaliar matematicamente a Suavização de Laplace diante de dados não vistos.
4. Fundamentar as limitações do Naive Bayes (hipótese de independência condicional) e a reflexão crítica.

---

## 2. Prompt Utilizado para a Análise de Resultados e Log-Odds

```text
Atue como um Especialista em Mineração de Dados e Machine Learning.

Estou finalizando a Etapa 4 do projeto acadêmico de Classificador Naive Bayes em SQL para E-commerce.
Possuímos um banco SQLite populado com 120 registros de treinamento e implementamos a classificação 
via CTEs com suavização de Laplace e log-probabilidades.

Preciso elaborar um relatório técnico com as respostas para 4 perguntas fundamentais:
1. O modelo classificou corretamente conforme a intuição sobre o domínio de e-commerce? 
   (Avaliar os 5 perfis de teste submetidos)
2. Quais features tiveram maior log-odds (maior poder discriminativo)? 
   (Calcular o Log-Odds = LN( P(Feature=v | Sim) / P(Feature=v | Não) ) para as categorias da base)
3. O que acontece ao testar um perfil com valores/combinações não vistos no treinamento? 
   (Explicar o papel da Suavização de Laplace alpha=1.0)
4. Quais são as limitações teóricas e práticas do Naive Bayes no e-commerce? 
   (Focar na premissa ingênua de independência condicional entre variáveis correlacionadas)

Também elabore uma Reflexão Crítica (mínimo 1 parágrafo) destacando onde o modelo acerta, onde falha e por quê.

Mantenha o rigor matemático e a linguagem técnica adequada para a disciplina de Mineração de Dados.
```

---

## 3. Síntese das Respostas da IA e Adaptações no Projeto

- A IA forneceu a fórmula formal do Log-Odds $\ln\left(\frac{P(F=v \mid \text{Sim})}{P(F=v \mid \text{Não})}\right)$, que executamos diretamente no banco de dados `data/atividade.db` via Python para obter o ranking exato de poder discriminativo.
- A análise identificou que `tipo_autenticacao = 'Conta Antiga'` é o maior fator de retenção (Log-Odds $-1.5692$) e `proporcao_frete = 'Alta'` é o maior indutor de cancelamento (Log-Odds $+1.1716$).
- Os resultados foram consolidados no documento oficial `docs/analise-resultados.md` e na tabela comparativa `resultados/resultados-testes.md`.
