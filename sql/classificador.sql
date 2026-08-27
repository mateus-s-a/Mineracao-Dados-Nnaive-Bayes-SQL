WITH
-- Passo 1: Cálculo das probabilidades a priori P(classe) para 'Sim' e 'Não'
Totais AS (
    SELECT
        CAST(COUNT(*) AS REAL) AS total_geral,
        CAST(SUM(CASE WHEN cancelou = 'Sim' THEN 1 ELSE 0 END) AS REAL) AS total_sim,
        CAST(SUM(CASE WHEN cancelou = 'Não' THEN 1 ELSE 0 END) AS REAL) AS total_nao
    FROM treino
),

-- Passo 2.1: Determinação do tamanho do vocabulário (número de categorias distintas) de cada feature
Vocabulario AS (
    SELECT
        CAST(COUNT(DISTINCT metodo_pagamento) AS REAL) AS v_metodo,
        CAST(COUNT(DISTINCT proporcao_frete) AS REAL) AS v_frete,
        CAST(COUNT(DISTINCT prazo_entrega) AS REAL) AS v_prazo,
        CAST(COUNT(DISTINCT historico_cliente) AS REAL) AS v_historico,
        CAST(COUNT(DISTINCT dispositivo_compra) AS REAL) AS v_dispositivo,
        CAST(COUNT(DISTINCT horario_compra) AS REAL) AS v_horario,
        CAST(COUNT(DISTINCT tipo_autenticacao) AS REAL) AS v_autenticacao
    FROM treino
),

-- Garante a existência de ambas as classes estruturais para evitar perda de linhas na contagem
Classes_Base AS (
    SELECT 'Sim' AS cancelou
    UNION ALL
    SELECT 'Não' AS cancelou
),

-- Passo 2.2: Contagem de ocorrências dos valores do caso de teste na base, agrupadas por classe
Contagens_Teste AS (
    SELECT
        cb.cancelou,
        CAST(SUM(CASE WHEN t.metodo_pagamento = 'Assíncrono (Boleto)' THEN 1 ELSE 0 END) AS REAL) AS c_metodo,
        CAST(SUM(CASE WHEN t.proporcao_frete = 'Alta' THEN 1 ELSE 0 END) AS REAL) AS c_frete,
        CAST(SUM(CASE WHEN t.prazo_entrega = 'Longo' THEN 1 ELSE 0 END) AS REAL) AS c_prazo,
        CAST(SUM(CASE WHEN t.historico_cliente = 'Risco' THEN 1 ELSE 0 END) AS REAL) AS c_historico,
        CAST(SUM(CASE WHEN t.dispositivo_compra = 'Mobile Web' THEN 1 ELSE 0 END) AS REAL) AS c_dispositivo,
        CAST(SUM(CASE WHEN t.horario_compra = 'Noturno' THEN 1 ELSE 0 END) AS REAL) AS c_horario,
        CAST(SUM(CASE WHEN t.tipo_autenticacao = 'Visitante' THEN 1 ELSE 0 END) AS REAL) AS c_autenticacao
    FROM Classes_Base cb
    LEFT JOIN treino t ON cb.cancelou = t.cancelou
    GROUP BY cb.cancelou
),

-- Passo 3: Cálculo das log-probabilidades (priori e verossimilhanças aplicando a Suavização de Laplace)
Log_Probabilidades AS (
    SELECT
        ct.cancelou,
        -- Log da probabilidade a priori: LN( P(Classe) )
        LN(CASE WHEN ct.cancelou = 'Sim' THEN tot.total_sim ELSE tot.total_nao END / tot.total_geral) AS log_prior,
        
        -- Log das verossimilhanças com Laplace: LN( (contagem + 1) / (total da classe + vocabulário) )
        LN((ct.c_metodo + 1.0) / (CASE WHEN ct.cancelou = 'Sim' THEN tot.total_sim ELSE tot.total_nao END + v.v_metodo)) AS log_metodo,
        LN((ct.c_frete + 1.0) / (CASE WHEN ct.cancelou = 'Sim' THEN tot.total_sim ELSE tot.total_nao END + v.v_frete)) AS log_frete,
        LN((ct.c_prazo + 1.0) / (CASE WHEN ct.cancelou = 'Sim' THEN tot.total_sim ELSE tot.total_nao END + v.v_prazo)) AS log_prazo,
        LN((ct.c_historico + 1.0) / (CASE WHEN ct.cancelou = 'Sim' THEN tot.total_sim ELSE tot.total_nao END + v.v_historico)) AS log_historico,
        LN((ct.c_dispositivo + 1.0) / (CASE WHEN ct.cancelou = 'Sim' THEN tot.total_sim ELSE tot.total_nao END + v.v_dispositivo)) AS log_dispositivo,
        LN((ct.c_horario + 1.0) / (CASE WHEN ct.cancelou = 'Sim' THEN tot.total_sim ELSE tot.total_nao END + v.v_horario)) AS log_horario,
        LN((ct.c_autenticacao + 1.0) / (CASE WHEN ct.cancelou = 'Sim' THEN tot.total_sim ELSE tot.total_nao END + v.v_autenticacao)) AS log_autenticacao
    FROM Contagens_Teste ct
    CROSS JOIN Totais tot
    CROSS JOIN Vocabulario v
),

-- Passo 3 (Continuação): Soma dos logaritmos para representar a multiplicação de probabilidades sem underflow
Soma_Logs AS (
    SELECT
        cancelou,
        (log_prior + log_metodo + log_frete + log_prazo + log_historico + log_dispositivo + log_horario + log_autenticacao) AS soma_log_total
    FROM Log_Probabilidades
),

-- Pivota os scores logarítmicos das duas classes em uma única linha para normalização
Pivot_Resultados AS (
    SELECT
        MAX(CASE WHEN cancelou = 'Sim' THEN soma_log_total END) AS log_sim,
        MAX(CASE WHEN cancelou = 'Não' THEN soma_log_total END) AS log_nao
    FROM Soma_Logs
)

-- Passo 4 e 5: Normalização via EXP() convertendo para porcentagem e gerando a recomendação textual
SELECT
    ROUND((1.0 / (1.0 + EXP(log_nao - log_sim))) * 100, 2) AS probabilidade_sim_pct,
    ROUND((1.0 / (1.0 + EXP(log_sim - log_nao))) * 100, 2) AS probabilidade_nao_pct,
    CASE
        WHEN (1.0 / (1.0 + EXP(log_nao - log_sim))) > 0.50 
        THEN 'ALTO RISCO DE CANCELAMENTO - Recomenda-se medidas preventivas (ofertas direcionadas ou suporte).'
        ELSE 'BAIXO RISCO - Seguir com o fluxo normal de processamento do pedido.'
    END AS recomendacao_decisao
FROM Pivot_Resultados;