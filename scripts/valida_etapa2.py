#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Validação Automatizada — Etapa 2
Mineração de Dados (Naive Bayes em SQL)
Utiliza apenas a biblioteca padrão do Python (sem dependências externas).
"""

import csv
import sys
from collections import Counter

CATEGORIAS = {
    "metodo_pagamento":   {"Síncrono (Cartão)", "Síncrono (Pix)", "Assíncrono (Boleto)"},
    "proporcao_frete":    {"Baixa", "Média", "Alta"},
    "prazo_entrega":      {"Expresso", "Padrão", "Longo"},
    "historico_cliente":  {"Impecável", "Aceitável", "Risco"},
    "dispositivo_compra": {"Desktop", "Mobile App", "Mobile Web"},
    "horario_compra":     {"Comercial", "Noturno", "Madrugada"},
    "tipo_autenticacao":  {"Visitante", "Nova Conta", "Conta Antiga"},
    "cancelou":           {"Sim", "Não"},
}

def validar_csv(caminho_csv="data/treino.csv"):
    print("=" * 60)
    print("INICIANDO VALIDAÇÃO DA MASSA DE DADOS DA ETAPA 2")
    print("=" * 60)

    try:
        with open(caminho_csv, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            linhas = list(reader)
            fieldnames = reader.fieldnames
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao ler o arquivo {caminho_csv}: {e}")
        sys.exit(1)

    erros = []
    
    # 1. Total de registros
    total = len(linhas)
    print(f"Total de registros: {total}")
    if total < 100:
        erros.append(f"Total de registros ({total}) é inferior ao mínimo exigido (100).")

    # 2. Distribuição das classes
    if fieldnames and "cancelou" in fieldnames:
        contagem = Counter(row["cancelou"] for row in linhas)
        print("\nDistribuição por classe ('cancelou'):")
        for k, v in contagem.items():
            pct = v / total if total > 0 else 0
            print(f"  - {k}: {v} ({pct:.1%})")
        
        nao_cnt = contagem.get("Não", 0)
        nao_pct = nao_cnt / total if total > 0 else 0
        if not (0.50 <= nao_pct <= 0.70):
            erros.append(f"Proporção da classe 'Não' ({nao_pct:.1%}) fora da faixa esperada (50% a 70%).")
    else:
        erros.append("Coluna alvo 'cancelou' não encontrada no CSV.")

    # 3. Validação de Categorias por Feature
    print("\nVerificando categorias por feature:")
    for col, permitidos in CATEGORIAS.items():
        if fieldnames and col not in fieldnames:
            erros.append(f"Coluna ausente: {col}")
            continue
        
        usados = set(row[col] for row in linhas if row.get(col) is not None)
        invalidos = usados - permitidos
        if invalidos:
            erros.append(f"Coluna '{col}': valores fora do domínio -> {invalidos}")
        else:
            print(f"  [OK] {col}: {len(usados)} categorias válidas ({', '.join(sorted(usados))})")

    # 4. Duplicatas e Nulos
    vistos = set()
    duplicatas = 0
    nulos = 0

    for row in linhas:
        # Tupla com os valores para checar duplicata de linha completa
        tpl = tuple(row[col] for col in fieldnames) if fieldnames else ()
        if tpl in vistos:
            duplicatas += 1
        else:
            vistos.add(tpl)
            
        for col in fieldnames or []:
            if not row[col] or row[col].strip() == "":
                nulos += 1

    print(f"\nDuplicatas de linhas completas: {duplicatas}")
    print(f"Valores nulos/vazios: {nulos}")

    if duplicatas > 0:
        erros.append(f"Foram encontradas {duplicatas} linhas duplicadas no dataset.")
    if nulos > 0:
        erros.append(f"Foram encontrados {nulos} valores nulos no dataset.")

    # Resultado final
    print("\n" + "=" * 60)
    if erros:
        print("[FALHA] Foram encontrados erros na validação:")
        for err in erros:
            print(f"  - {err}")
        return False
    else:
        print("[SUCESSO] Todos os critérios de aceite da Etapa 2 foram atendidos!")
        print("=" * 60)
        return True

if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else "data/treino.csv"
    sucesso = validar_csv(caminho)
    sys.exit(0 if sucesso else 1)
