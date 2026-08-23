# Mineração de Dados — Classificador Naive Bayes em SQL

Implementação da **Atividade Prática 1 — Algoritmo Classificador Bayesiano**, da disciplina de **Mineração de Dados**.

* **Lorena Strobel Campos**
* **Mateus de Souza Arruda**

**Professor:** Antônio Braz

**Data de entrega:** 28/08/2026

---

## Sobre a atividade

A atividade consiste em modelar, implementar e avaliar um classificador **Naive Bayes** aplicado a um problema real de **classificação binária**.

O trabalho envolve todo o fluxo de desenvolvimento de uma solução de mineração de dados: definição do problema, seleção e discretização das features, geração e validação dos dados, implementação do algoritmo e análise crítica dos resultados.

A implementação do classificador é realizada **em SQL**, utilizando **SQLite**, com:

* Probabilidades a priori;
* Verossimilhanças condicionais;
* Suavização de Laplace;
* Log-probabilidades;
* Normalização dos scores em probabilidades;
* Recomendação da classe com maior probabilidade.

A atividade também exige a utilização documentada de uma ferramenta de IA generativa como parceira durante o processo de modelagem e desenvolvimento. O uso da IA deve ser acompanhado de revisão e compreensão do código produzido.

---

## Objetivos

* Aplicar conceitos de **Mineração de Dados** em um problema real;
* Compreender o funcionamento do algoritmo **Naive Bayes**;
* Trabalhar com **aprendizado supervisionado** e classificação binária;
* Aplicar as etapas do processo de **KDD**;
* Implementar o classificador utilizando SQL;
* Avaliar o comportamento do modelo em diferentes perfis de teste;
* Analisar criticamente as limitações e os resultados obtidos;
* Documentar o processo de interação com a IA utilizada durante o desenvolvimento.

---

## Metodologia

O desenvolvimento segue quatro etapas principais:

### 1. Modelagem do problema

Definição de:

* Domínio da aplicação;
* Rótulo alvo binário;
* 6 a 8 features preditivas;
* Discretização das features;
* Padrões esperados de classificação.

### 2. Geração da massa de dados

Criação de pelo menos **100 registros de treinamento**, contendo:

* Features discretizadas;
* Padrões intencionais e coerentes;
* Distribuição razoável entre as classes;
* Curadoria e validação dos registros gerados.

### 3. Implementação do Naive Bayes

O classificador é implementado em SQL utilizando:

1. Cálculo das probabilidades a priori `P(classe)`;
2. Cálculo das verossimilhanças `P(feature | classe)`;
3. Suavização de Laplace;
4. Cálculo utilizando log-probabilidades;
5. Conversão dos scores em probabilidades normalizadas;
6. Recomendação da classe mais provável.

### 4. Testes e análise

São utilizados pelo menos **5 perfis de teste**, incluindo:

* Perfil de baixo risco;
* Perfil de alto risco;
* Perfil ambíguo;
* Perfil contendo valor não observado no treinamento;
* Perfil de fronteira.

Os resultados são analisados considerando a classificação, os **log-odds** das features, o efeito da suavização de Laplace e as limitações do Naive Bayes.

---

## Tecnologias

| Tecnologia        | Utilização                                            |
| ----------------- | ----------------------------------------------------- |
| **SQLite**        | Banco de dados e execução do classificador            |
| **SQL**           | Implementação do Naive Bayes                          |
| **Markdown**      | Documentação do projeto                               |
| **Git/GitHub**    | Versionamento e organização do trabalho               |
| **IA generativa** | Apoio à modelagem, geração de dados e desenvolvimento |

O uso de SQLite foi escolhido por permitir que todo o experimento seja executado a partir de um único arquivo de banco de dados, facilitando também a demonstração da atividade.

---

## Estrutura do projeto (NÃO GARANTIDO, AINDA EM PROGRESSO)

```text
.
├── README.md
├── docs/
│   ├── modelagem.md
│   ├── prompts.md
│   └── analise-resultados.md
│
├── data/
│   ├── treino.csv
│   └── atividade.db
│
├── sql/
│   ├── schema.sql
│   ├── dados.sql
│   ├── classificador.sql
│   └── testes.sql
│
└── resultados/
    └── resultados-testes.md
```

> A estrutura pode ser ajustada conforme a organização final dos arquivos da dupla.

---

## Dados de treinamento

A base de treinamento deve conter **100 ou mais registros**, utilizando exclusivamente as categorias definidas durante a etapa de modelagem.

Os dados são gerados com auxílio de IA, mas passam por **curadoria e validação** antes de serem utilizados no treinamento.

Entre as verificações realizadas estão:

* Quantidade mínima de registros;
* Balanceamento entre as classes;
* Validade das categorias;
* Coerência dos registros;
* Identificação de possíveis duplicidades.

---

## Naive Bayes

De forma simplificada, para cada classe, o modelo calcula:

```text
P(classe) ×
P(feature1 | classe) ×
P(feature2 | classe) ×
...
P(featureN | classe)
```

Para evitar probabilidades iguais a zero quando determinado valor não aparece no treinamento, é utilizada a **suavização de Laplace**.

O cálculo também utiliza **log-probabilidades**, transformando multiplicações em somas e reduzindo problemas de underflow numérico.

Por fim, os scores das classes são normalizados para obter probabilidades entre **0% e 100%**.

---

## Casos de teste

Os testes seguem diferentes perfis para avaliar o comportamento do classificador:

| Caso | Perfil              | Objetivo                                             |
| ---- | ------------------- | ---------------------------------------------------- |
| 1    | Baixo risco         | Verificar alta probabilidade para a classe esperada  |
| 2    | Alto risco          | Verificar alta probabilidade para a classe oposta    |
| 3    | Ambíguo             | Avaliar situações com evidências conflitantes        |
| 4    | Valor não observado | Avaliar o efeito da suavização de Laplace            |
| 5    | Perfil de fronteira | Identificar features com maior influência na decisão |

---

## Análise dos resultados (4 PERGUNTAS)

A análise busca responder:

1. O modelo classificou os casos de acordo com a intuição do domínio?
2. Quais features apresentaram maior **log-odds**?
3. O que acontece quando um valor não é observado no treinamento?
4. Quais são as principais limitações do Naive Bayes para o problema escolhido?

Também será realizada uma reflexão crítica sobre os pontos fortes e as limitações do modelo.

---

## Uso de Inteligência Artificial

A IA generativa faz parte do processo de desenvolvimento da atividade.

Seu uso contempla, entre outras etapas:

* Escolha e modelagem do domínio;
* Definição das features;
* Discretização das variáveis;
* Geração da massa de dados;
* Apoio na implementação do SQL;
* Interpretação dos resultados.

Todos os **prompts relevantes** utilizados durante a atividade serão documentados no projeto.

O código gerado por IA será revisado, adaptado e compreendido pela dupla. Nenhum output será utilizado de forma bruta sem curadoria.

---

## Conteúdos relacionados

A atividade está relacionada aos seguintes conceitos da disciplina:

* Mineração de Dados;
* Classificação;
* Aprendizado supervisionado;
* KDD;
* Teorema de Bayes;
* Naive Bayes;
* Discretização;
* Probabilidade condicional;
* Suavização de Laplace;
* Log-probabilidade;
* Log-odds;
* Avaliação de modelos.

---

