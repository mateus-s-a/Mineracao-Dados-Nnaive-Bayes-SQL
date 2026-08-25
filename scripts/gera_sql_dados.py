#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Geração de dados.sql e Carga no SQLite — Etapa 2
Mineração de Dados (Naive Bayes em SQL)
"""

import csv
import sqlite3
import sys

def csv_para_sql(caminho_csv="data/treino.csv", caminho_sql="sql/dados.sql", caminho_db="data/atividade.db"):
    print("Gerando sql/dados.sql e criando banco SQLite em data/atividade.db...")
    
    with open(caminho_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        linhas = list(reader)

    # 1. Escrever sql/dados.sql
    with open(caminho_sql, mode="w", encoding="utf-8") as f_sql:
        f_sql.write("-- sql/dados.sql\n")
        f_sql.write("-- Inserts da massa de treinamento (120 registros)\n\n")
        
        for row in linhas:
            # Escapar aspas simples se houver (neste dataset não há, mas por garantia)
            mp = row["metodo_pagamento"].replace("'", "''")
            pf = row["proporcao_frete"].replace("'", "''")
            pe = row["prazo_entrega"].replace("'", "''")
            hc = row["historico_cliente"].replace("'", "''")
            dc = row["dispositivo_compra"].replace("'", "''")
            ho = row["horario_compra"].replace("'", "''")
            ta = row["tipo_autenticacao"].replace("'", "''")
            ca = row["cancelou"].replace("'", "''")
            
            sql_line = (
                f"INSERT INTO treino (metodo_pagamento, proporcao_frete, prazo_entrega, "
                f"historico_cliente, dispositivo_compra, horario_compra, tipo_autenticacao, cancelou) "
                f"VALUES ('{mp}', '{pf}', '{pe}', '{hc}', '{dc}', '{ho}', '{ta}', '{ca}');\n"
            )
            f_sql.write(sql_line)

    print(f"[OK] {len(linhas)} instruções INSERT geradas em {caminho_sql}")

    # 2. Carregar no banco SQLite data/atividade.db
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()

    # Executar schema.sql
    with open("sql/schema.sql", mode="r", encoding="utf-8") as f_schema:
        schema_script = f_schema.read()
        cursor.executescript(schema_script)

    # Executar dados.sql
    with open(caminho_sql, mode="r", encoding="utf-8") as f_dados:
        dados_script = f_dados.read()
        cursor.executescript(dados_script)

    conn.commit()

    # Validar contagem no SQLite
    cursor.execute("SELECT COUNT(*) FROM treino;")
    total_db = cursor.fetchone()[0]

    cursor.execute("SELECT cancelou, COUNT(*) FROM treino GROUP BY cancelou;")
    distrib_db = cursor.fetchall()

    conn.close()

    print(f"[OK] Banco de dados {caminho_db} populado com sucesso!")
    print(f"     Total de registros inseridos no SQLite: {total_db}")
    print(f"     Distribuição de classes no SQLite: {distrib_db}")

if __name__ == "__main__":
    csv_para_sql()
