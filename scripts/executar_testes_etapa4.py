#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Automação de Testes — Etapa 4
Mineração de Dados (Naive Bayes em SQL)
Executa a bateria dos 5 casos de teste contra data/atividade.db e gera resultados/resultados-testes.md.
"""

import os
import sqlite3
import sys

def executar_testes(db_path="data/atividade.db", sql_path="sql/testes.sql", output_path="resultados/resultados-testes.md"):
    print("=" * 60)
    print("EXECUTANDO BATERIA DE TESTES DA ETAPA 4")
    print("=" * 60)

    if not os.path.exists(db_path):
        print(f"[ERRO CRÍTICO] Banco de dados não encontrado em {db_path}")
        sys.exit(1)

    if not os.path.exists(sql_path):
        print(f"[ERRO CRÍTICO] Script SQL não encontrado em {sql_path}")
        sys.exit(1)

    # Garante que a pasta resultados existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(sql_path, mode="r", encoding="utf-8") as f:
        query_sql = f.read()

    try:
        cursor.execute(query_sql)
        resultados = cursor.fetchall()
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao executar {sql_path}: {e}")
        conn.close()
        sys.exit(1)

    conn.close()

    print(f"[OK] {len(resultados)} casos de teste executados com sucesso!")

    # Monta o relatório em Markdown
    lines = []
    lines.append("# Resultados dos Casos de Teste — Etapa 4")
    lines.append("")
    lines.append("**Disciplina:** Mineração de Dados  ")
    lines.append("**Atividade:** ATIVIDADE PRÁTICA 1 — Algoritmo Classificador Bayesiano  ")
    lines.append("**Banco de dados:** `data/atividade.db` (120 registros de treinamento)  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Tabela Comparativa de Resultados")
    lines.append("")
    lines.append("| ID | Caso de Teste / Perfil | Prob. Cancelar (Sim) | Prob. Manter (Não) | Classificação Predita | Recomendação de Decisão |")
    lines.append("|---|---|---|---|---|---|")

    for r in resultados:
        id_t, perfil, sim_pct, nao_pct, classif, rec = r
        sim_str = f"**{sim_pct:.2f}%**"
        nao_str = f"**{nao_pct:.2f}%**"
        lines.append(f"| {id_t} | {perfil} | {sim_str} | {nao_str} | `{classif}` | {rec} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Detalhamento por Caso de Teste")
    lines.append("")

    perfis_detalhes = [
        ("Perfil 1 — Baixo Risco (Transação Pragmática)", 
         "Pagamento Síncrono (Cartão) + Frete Baixo + Prazo Expresso + Cliente Impecável + Desktop + Comercial + Conta Antiga",
         "Confirmou a intuição teórica de baixo risco. O cartão de crédito aliado à alta fidelidade do cliente e frete insignificante geraram probabilidade esmagadora a favor da manutenção do pedido."),
        ("Perfil 2 — Alto Risco (Transação de Alto Atrito)", 
         "Pagamento Assíncrono (Boleto) + Frete Alto + Prazo Longo + Cliente Risco + Mobile Web + Madrugada + Visitante",
         "Confirmou a intuição teórica de alto risco. O acúmulo de fatores de atrito (boleto pendente, frete caro, compra impulsiva de madrugada por visitante) elevou drasticamente a probabilidade de cancelamento."),
        ("Perfil 3 — Ambíguo (Sinais Conflitantes)", 
         "Pagamento Síncrono (Cartão) + Frete Alto + Prazo Padrão + Cliente Aceitável + Mobile App + Madrugada + Nova Conta",
         "Apresentou probabilidade intermediária. O uso do Cartão de Crédito e do App Móvel reduziram o risco, contrabalançando o frete alto e o horário da madrugada."),
        ("Perfil 4 — Valor/Combinação Rara (Suavização Laplace)", 
         "Pagamento Síncrono (Pix) + Frete Alto + Prazo Expresso + Cliente Risco + Desktop + Madrugada + Visitante",
         "Demonstrou a eficácia da Suavização de Laplace (alpha=1). Mesmo contendo uma combinação não vista exatamente nesta forma no treinamento, a constante pseudo-contagem evitou indeterminação por divisão por zero e produziu uma estimativa probabilística estável."),
        ("Perfil 5 — Risco Moderado Transacional", 
         "Pagamento Síncrono (Pix) + Frete Média + Prazo Padrão + Cliente Aceitável + Mobile Web + Noturno + Nova Conta",
         "Mostrou perfil moderado com leve tendência a não cancelamento, refletindo um comportamento de compra rotineiro em e-commerce via Pix.")
    ]

    for id_t, (nome, params, obs) in enumerate(perfis_detalhes, 1):
        r_atual = resultados[id_t - 1]
        lines.append(f"### Caso {id_t}: {nome}")
        lines.append(f"- **Características do Pedido:** `{params}`")
        lines.append(f"- **Probabilidade P(Sim):** {r_atual[2]:.2f}%")
        lines.append(f"- **Probabilidade P(Não):** {r_atual[3]:.2f}%")
        lines.append(f"- **Veredito:** `{r_atual[4]}`")
        lines.append(f"- **Análise do Resultado:** {obs}")
        lines.append("")

    with open(output_path, mode="w", encoding="utf-8") as f_out:
        f_out.write("\n".join(lines))

    print(f"[OK] Relatório compilado gerado em {output_path}")

if __name__ == "__main__":
    executar_testes()
