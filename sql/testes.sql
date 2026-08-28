-- ==============================================================================
-- sql/testes.sql
-- Classificação dos 5 Casos de Teste da Etapa 4 usando Naive Bayes em SQL
-- Disciplina: Mineração de Dados
-- ==============================================================================

WITH
-- Passo 1: Totais gerais e contagens a priori P(classe)
Totais AS (
    SELECT
        CAST(COUNT(*) AS REAL) AS total_geral,
        CAST(SUM(CASE WHEN cancelou = 'Sim' THEN 1 ELSE 0 END) AS REAL) AS total_sim,
        CAST(SUM(CASE WHEN cancelou = 'Não' THEN 1 ELSE 0 END) AS REAL) AS total_nao
    FROM treino
),

-- Passo 2: Tamanho do vocabulário (número de categorias distintas por feature)
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

-- Passo 3: Definição dos 5 Perfis de Teste da Etapa 4
Casos_Teste AS (
    SELECT 
        1 AS id_teste, 
        'Perfil 1 — Baixo Risco (Transação Pragmática)' AS nome_perfil,
        'Síncrono (Cartão)' AS metodo_pagamento, 
        'Baixa' AS proporcao_frete, 
        'Expresso' AS prazo_entrega, 
        'Impecável' AS historico_cliente, 
        'Desktop' AS dispositivo_compra, 
        'Comercial' AS horario_compra, 
        'Conta Antiga' AS tipo_autenticacao
    UNION ALL
    SELECT 
        2, 
        'Perfil 2 — Alto Risco (Transação de Alto Atrito)',
        'Assíncrono (Boleto)', 'Alta', 'Longo', 'Risco', 'Mobile Web', 'Madrugada', 'Visitante'
    UNION ALL
    SELECT 
        3, 
        'Perfil 3 — Ambíguo (Sinais Conflitantes)',
        'Síncrono (Cartão)', 'Alta', 'Padrão', 'Aceitável', 'Mobile App', 'Madrugada', 'Nova Conta'
    UNION ALL
    SELECT 
        4, 
        'Perfil 4 — Valor/Combinação Rara (Suavização Laplace)',
        'Síncrono (Pix)', 'Alta', 'Expresso', 'Risco', 'Desktop', 'Madrugada', 'Visitante'
    UNION ALL
    SELECT 
        5, 
        'Perfil 5 — Risco Moderado Transacional',
        'Síncrono (Pix)', 'Média', 'Padrão', 'Aceitável', 'Mobile Web', 'Noturno', 'Nova Conta'
),

-- Suporte para avaliação de ambas as classes (Sim e Não) para cada perfil
Classes_Base AS (
    SELECT 'Sim' AS cancelou
    UNION ALL
    SELECT 'Não' AS cancelou
),

-- Cruzamento dos casos de teste com as classes
Casos_Classes AS (
    SELECT c.id_teste, c.nome_perfil, cb.cancelou,
           c.metodo_pagamento, c.proporcao_frete, c.prazo_entrega,
           c.historico_cliente, c.dispositivo_compra, c.horario_compra, c.tipo_autenticacao
    FROM Casos_Teste c
    CROSS JOIN Classes_Base cb
),

-- Passo 4: Contagem de ocorrências das características na base treino agrupadas por caso e por classe
Contagens_Teste AS (
    SELECT
        cc.id_teste,
        cc.nome_perfil,
        cc.cancelou,
        CAST(SUM(CASE WHEN t.metodo_pagamento = cc.metodo_pagamento THEN 1 ELSE 0 END) AS REAL) AS c_metodo,
        CAST(SUM(CASE WHEN t.proporcao_frete = cc.proporcao_frete THEN 1 ELSE 0 END) AS REAL) AS c_frete,
        CAST(SUM(CASE WHEN t.prazo_entrega = cc.prazo_entrega THEN 1 ELSE 0 END) AS REAL) AS c_prazo,
        CAST(SUM(CASE WHEN t.historico_cliente = cc.historico_cliente THEN 1 ELSE 0 END) AS REAL) AS c_historico,
        CAST(SUM(CASE WHEN t.dispositivo_compra = cc.dispositivo_compra THEN 1 ELSE 0 END) AS REAL) AS c_dispositivo,
        CAST(SUM(CASE WHEN t.horario_compra = cc.horario_compra THEN 1 ELSE 0 END) AS REAL) AS c_horario,
        CAST(SUM(CASE WHEN t.tipo_autenticacao = cc.tipo_autenticacao THEN 1 ELSE 0 END) AS REAL) AS c_autenticacao
    FROM Casos_Classes cc
    LEFT JOIN treino t ON cc.cancelou = t.cancelou
    GROUP BY cc.id_teste, cc.nome_perfil, cc.cancelou
),

-- Passo 5: Cálculo das log-probabilidades com Suavização de Laplace (alpha = 1)
Log_Probabilidades AS (
    SELECT
        ct.id_teste,
        ct.nome_perfil,
        ct.cancelou,
        
        -- Log Priori: LN( P(Classe) )
        LN(CASE WHEN ct.cancelou = 'Sim' THEN tot.total_sim ELSE tot.total_nao END / tot.total_geral) AS log_prior,
        
        -- Log Verossimilhanças com Laplace: LN( (contagem + 1) / (total_classe + V_i) )
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

-- Passo 6: Soma das log-probabilidades por perfil e por classe (evita underflow)
Soma_Logs AS (
    SELECT
        id_teste,
        nome_perfil,
        cancelou,
        (log_prior + log_metodo + log_frete + log_prazo + log_historico + log_dispositivo + log_horario + log_autenticacao) AS soma_log_total
    FROM Log_Probabilidades
),

-- Passo 7: Pivoteamento dos scores logarítmicos das duas classes por perfil
Pivot_Resultados AS (
    SELECT
        id_teste,
        nome_perfil,
        MAX(CASE WHEN cancelou = 'Sim' THEN soma_log_total END) AS log_sim,
        MAX(CASE WHEN cancelou = 'Não' THEN soma_log_total END) AS log_nao
    FROM Soma_Logs
    GROUP BY id_teste, nome_perfil
)

-- Passo 8: Normalização Softmax/EXP() e decisão recomendada
SELECT
    id_teste,
    nome_perfil,
    ROUND((1.0 / (1.0 + EXP(log_nao - log_sim))) * 100, 2) AS probabilidade_sim_pct,
    ROUND((1.0 / (1.0 + EXP(log_sim - log_nao))) * 100, 2) AS probabilidade_nao_pct,
    CASE
        WHEN (1.0 / (1.0 + EXP(log_nao - log_sim))) > 0.50 
        THEN 'ALTO RISCO DE CANCELAMENTO'
        ELSE 'BAIXO RISCO DE CANCELAMENTO'
    END AS classificacao_predita,
    CASE
        WHEN (1.0 / (1.0 + EXP(log_nao - log_sim))) > 0.50 
        THEN 'Acionar medida preventiva (cupom frete, oferta direcionada ou suporte em tempo real)'
        ELSE 'Manter fluxo normal de processamento e faturamento do pedido'
    END AS recomendacao_acao
FROM Pivot_Resultados
ORDER BY id_teste;
