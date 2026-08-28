# Mineração de Dados — Classificador Naive Bayes em SQL

Implementação completa da **Atividade Prática 1 — Algoritmo Classificador Bayesiano**, da disciplina de **Mineração de Dados**.

* **Lorena Strobel Campos**
* **Mateus de Souza Arruda**

**Professor:** Orlando Júnior  
**Instituição:** Instituto Federal de Educação, Ciência e Tecnologia de Mato Grosso (IFMT)  
**Data de entrega:** 28/08/2026  

<br>

---

<br>

## Sobre a Atividade

A atividade consiste em modelar, implementar e avaliar um classificador **Naive Bayes** aplicado a um problema real de **classificação binária no e-commerce** (previsão de cancelamento de pedidos no checkout).

O trabalho contempla todo o fluxo de desenvolvimento de uma solução de mineração de dados (KDD - Descoberta de Conhecimento em Bancos de Dados):
- definição do problema,
- seleção e discretização de 7 features preditivas,
- geração e validação de 120 registros de treinamento,
- implementação do algoritmo em SQL relacional e
- análise crítica dos resultados.

A implementação do classificador é realizada em **SQL nativo** utilizando **SQLite**, englobando:

* Probabilidades a priori $P(\text{classe})$;
* Verossimilhanças condicionais com **Suavização de Laplace** ($\alpha = 1.0$);
* Classificação em escala de **log-probabilidades** para prevenir *underflow* numérico;
* Normalização dos scores em probabilidades ($0\%$ a $100\%$) via exponenciação $\text{EXP}()$;
* Recomendação de decisão operacional textual.

<br>

---

<br>

## Estrutura do Projeto

```text
.
├── README.md                           # Documentação principal do projeto
├── etapa1.md                           # Modelagem do domínio de e-commerce e 7 features discretizadas
├── data/
│   ├── atividade.db                    # Banco de dados SQLite populado com os 120 registros de treino
│   └── treino.csv                      # Base de dados de treinamento em CSV (120 registros)
├── docs/
│   ├── analise-resultados.md           # Respostas às 4 perguntas do professor + Reflexão Crítica
│   ├── prompts-etapa1.md               # Registro dos prompts da Etapa 1 (Modelagem)
│   ├── prompts-etapa2.md               # Registro dos prompts da Etapa 2 (Geração de Dados)
│   ├── prompts-etapa3.md               # Registro dos prompts da Etapa 3 (Algoritmo SQL)
│   ├── prompts-etapa4.md               # Registro dos prompts da Etapa 4 (Log-Odds e Análise)
│   ├── Enunciado - Atividade.pdf       # Especificação oficial da atividade fornecida pelo professor
│   └── Etapa 1 - Escolha do domínio... # Documento complementar de fundamentação da Etapa 1
├── resultados/
│   └── resultados-testes.md            # Relatório formal e tabela dos 5 casos de teste executados
├── scripts/
│   ├── executar_classificador.py       # Runner Python para executar sql/classificador.sql no SQLite
│   ├── executar_testes_etapa4.py       # Automation runner Python para executar sql/testes.sql
│   ├── gera_dados.py                   # Script Python reprodutível de geração do dataset (120 linhas)
│   ├── gera_sql_dados.py               # Script Python de conversão CSV -> dados.sql e carga no SQLite
│   └── valida_etapa2.py                # Script Python de validação automatizada das regras do dataset
└── sql/
    ├── schema.sql                      # DDL da tabela treino com restrições CHECK por categoria
    ├── dados.sql                       # 120 instruções INSERT INTO treino (...)
    ├── classificador.sql               # Algoritmo Naive Bayes completo em SQL via CTEs
    └── testes.sql                      # Consulta SQL que classifica os 5 perfis de teste em lote
```

<br>

---

<br>

## Como Executar o Projeto

Todo o projeto utiliza unicamente a **biblioteca padrão do Python 3** (sem dependências externas) e o **SQLite 3**.

### 1. Gerar o Dataset (Etapa 2)
- Para alterar a distribuição e gerar um novo dataset, altere `random.seed()` em `scripts/gera_dados.py`.
- Para gerar o dataset com 120 registros, utilize o comando:
```bash
python3 scripts/gera_dados.py
```

### 2. Validar a Massa de Dados de Treinamento
Para rodar a bateria de testes automatizados sobre `data/treino.csv`:
```bash
python3 scripts/valida_etapa2.py
```

### 3. Recriar o Banco de Dados e Carga SQL
Para regerar o script `sql/dados.sql` e reconstruir a base `data/atividade.db`:
```bash
python3 scripts/gera_sql_dados.py
```

### 4. Executar o Classificador Naive Bayes em SQL (Caso Individual)
Para rodar o script SQL oficial (`sql/classificador.sql`) via Python:
```bash
python3 scripts/executar_classificador.py
```

### 5. Executar os 5 Casos de Teste e Regerar Relatórios (Etapa 4)
Para rodar a bateria dos 5 perfis de teste (`sql/testes.sql`) e compilar `resultados/resultados-testes.md`:
```bash
python3 scripts/executar_testes_etapa4.py
```

<br>

---

<br>

## Detalhamento Técnico dos Arquivos (`data/`, `scripts/` e `sql/`)

### Diretório `data/` (Armazenamento dos Dados)

* **`data/treino.csv`:** A base de dados de treinamento bruta contendo **120 registros de pedidos de e-commerce** em formato CSV (UTF-8). Possui cabeçalho estrito com as 7 features preditivas (`metodo_pagamento`, `proporcao_frete`, `prazo_entrega`, `historico_cliente`, `dispositivo_compra`, `horario_compra`, `tipo_autenticacao`) e o rótulo alvo `cancelou` (`Sim` / `Não`).
* **`data/atividade.db`:** O arquivo do banco de dados relacional **SQLite 3**. Armazena a tabela `treino` populada e pronta para receber as consultas relacionais do classificador Bayesiano.

### Diretório `scripts/` (Automação em Python)

Todos os scripts utilizam **exclusivamente a biblioteca padrão do Python 3** (módulos `csv`, `sqlite3`, `random`, `sys`, `os`), garantindo que o projeto execute em qualquer ambiente sem necessidade de instalar dependências de terceiros (`pip`).

* **`scripts/gera_dados.py`:** Script responsável pela geração determinística (com semente estatística `seed=42`) da massa de 120 registros de treinamento em `data/treino.csv`. Ele embutiu na geração a probabilidade dos 3 perfis intuitivos definidos na Etapa 1 (baixo risco, alto risco e perfil ambíguo).
* **`scripts/valida_etapa2.py`:** Inspetor e validador de qualidade automatizado. Lê `data/treino.csv` e valida 4 critérios de aceite do professor:
  1. Registros $\ge 100$ (obteve 120);
  2. Distribuição da classe `Não` entre $50\%$ e $70\%$ (obteve $56.7\%$);
  3. Pertencimento estrito das categorias às 7 variáveis discretizadas;
  4. Ausência total de valores nulos, vazios ou linhas duplicadas.
* **`scripts/gera_sql_dados.py`:** Converte `data/treino.csv` no arquivo `sql/dados.sql` (gerando 120 comandos `INSERT INTO`) e conecta ao SQLite (`data/atividade.db`) para executar o `sql/schema.sql` e carregar os dados no banco de forma totalmente automatizada.
* **`scripts/executar_classificador.py`:** Runner de execução simples que lê o script `sql/classificador.sql`, executa a consulta no `data/atividade.db` e exibe a classificação e recomendação do caso individual no terminal.
* **`scripts/executar_testes_etapa4.py`:** Runner automático de testes que conecta ao `data/atividade.db`, executa a bateria de 5 perfis de teste simultâneos (`sql/testes.sql`) e gera automaticamente o relatório em Markdown `resultados/resultados-testes.md`.

### Diretório `sql/` (Algoritmo e Banco de Dados)

* **`sql/schema.sql`:** Script DDL (*Data Definition Language*) de criação da tabela `treino` no SQLite. Inclui restrições `CHECK (...)` para cada uma das 7 colunas, garantindo que o banco de dados rejeite valores fora do domínio discreto oficial.
* **`sql/dados.sql`:** Script DML (*Data Manipulation Language*) contendo as 120 instruções `INSERT INTO treino (...)` para popular a tabela relacional.
* **`sql/classificador.sql`:** O script SQL principal desenvolvido para a Etapa 3. Utiliza 7 Common Table Expressions (`WITH CTEs`) para calcular:
  - Probabilidades a priori $P(\text{classe})$;
  - Vocabulário $V_i$ por feature;
  - Verossimilhança com **Suavização de Laplace** ($\alpha = 1.0$);
  - Soma dos logaritmos $\text{LN}()$ para evitar *underflow* numérico;
  - Normalização exponencial $\text{EXP}()$ em probabilidades de $0\%$ a $100\%$ e recomendação textual.
* **`sql/testes.sql`:** O script SQL expandido para a Etapa 4. Adapta a estrutura de CTEs do classificador para avaliar em lote uma matriz com **5 perfis de teste com características distintas**, retornando o diagnóstico completo para cada caso.

<br>

---

<br>

## Resumo dos Resultados dos Testes (Etapa 4)

| ID | Perfil de Teste | $P(\text{Sim})$ | $P(\text{Não})$ | Veredito Predito | Recomendação Operacional |
|---|---|---|---|---|---|
| **1** | **Perfil 1 — Baixo Risco (Transação Pragmática)** | **0.09%** | **99.91%** | `BAIXO RISCO` | Manter fluxo normal de faturamento do pedido |
| **2** | **Perfil 2 — Alto Risco (Transação de Alto Atrito)** | **99.57%** | **0.43%** | `ALTO RISCO` | Acionar medida preventiva (cupom frete/suporte) |
| **3** | **Perfil 3 — Ambíguo (Sinais Conflitantes)** | **64.71%** | **35.29%** | `ALTO RISCO` | Acionar medida preventiva (cupom frete/suporte) |
| **4** | **Perfil 4 — Valor Raro (Suavização Laplace)** | **86.54%** | **13.46%** | `ALTO RISCO` | Acionar medida preventiva (cupom frete/suporte) |
| **5** | **Perfil 5 — Risco Moderado Transacional** | **52.65%** | **47.35%** | `ALTO RISCO` | Acionar medida preventiva (cupom frete/suporte) |

<br>

---

<br>

## Principais Descobertas Técnicas (Log-Odds)

Foi calculado o Log-Odds $\ln\left(\frac{P(F=v \mid \text{Sim})}{P(F=v \mid \text{Não})}\right)$ para todas as categorias do dataset:

* **Maior fator de retenção (Menor Log-Odds):** `tipo_autenticacao = 'Conta Antiga'` ($\text{Log-Odds} = -1.5692$). A fidelidade histórica é o maior sinal protetor contra o cancelamento.
* **Maior indutor de cancelamento (Maior Log-Odds):** `proporcao_frete = 'Alta'` ($\text{Log-Odds} = +1.1716$). O custo relativo do envio é o principal fator de atrito e desistência no e-commerce.

<br>

---

<br>

## Tecnologias e Ferramentas

| Tecnologia | Utilização |
| --- | --- |
| **![SQLite 3](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=SQLite&logoColor=white) / ![SQL](https://shields.io/badge/SQL-003545?style=for-the-badge&logo=sql&logoColor=white)** | Banco de dados e implementação nativa do algoritmo Naive Bayes via CTEs |
| **![Python 3](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)** | Scripts autônomos de automação, geração determinística, validação e execução |
| **![Markdown](https://img.shields.io/badge/Markdown-003545?style=for-the-badge&logo=markdown&logoColor=white)** | Documentação técnica, logs de prompts, artefatos de controle e relatórios |
| **![Git](https://shields.io/badge/Git-003545?style=for-the-badge&logo=git&logoColor=white) / ![GitHub](https://shields.io/badge/GitHub-003545?style=for-the-badge&logo=github&logoColor=white)** | Controlabilidade e versionamento do código-fonte |
| **IA Generativa (Gemini & Genspark)** | Parceira documentada nas etapas de modelagem, geração de dados e análise crítica |

<br>

---

<br>

## Integrantes e Responsabilidade

* **Lorena Strobel Campos:** Modelagem do problema (Etapa 1), implementação do algoritmo Naive Bayes em SQL (Etapa 3) e documentação de prompts (`etapa1.md`, `prompts-etapa3.md`).
* **Mateus de Souza Arruda:** Geração e validação automatizada da massa de dados (Etapa 2), execução da bateria dos 5 perfis de teste e análise dos log-odds/reflexão crítica (Etapa 4).
