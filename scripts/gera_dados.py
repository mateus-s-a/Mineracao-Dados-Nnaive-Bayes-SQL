#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Geração de Dados de Treinamento — Etapa 2
Mineração de Dados (Naive Bayes em SQL)
Utiliza apenas a biblioteca padrão do Python (sem dependências externas).
"""

import csv
import random

random.seed(42)

FIELDNAMES = [
    "metodo_pagamento",
    "proporcao_frete",
    "prazo_entrega",
    "historico_cliente",
    "dispositivo_compra",
    "horario_compra",
    "tipo_autenticacao",
    "cancelou"
]

METODOS_PAGAMENTO = ["Síncrono (Cartão)", "Síncrono (Pix)", "Assíncrono (Boleto)"]
PROPORCOES_FRETE = ["Baixa", "Média", "Alta"]
PRAZOS_ENTREGA = ["Expresso", "Padrão", "Longo"]
HISTORICOS_CLIENTE = ["Impecável", "Aceitável", "Risco"]
DISPOSITIVOS_COMPRA = ["Desktop", "Mobile App", "Mobile Web"]
HORARIOS_COMPRA = ["Comercial", "Noturno", "Madrugada"]
TIPOS_AUTENTICACAO = ["Visitante", "Nova Conta", "Conta Antiga"]

def gerar_registro():
    tipo_perfil = random.choices([1, 2, 3], weights=[0.45, 0.35, 0.20])[0]

    if tipo_perfil == 1:
        # Perfil Baixo Risco (tendência a cancelou = Não)
        metodo = random.choices(["Síncrono (Cartão)", "Síncrono (Pix)"], weights=[0.7, 0.3])[0]
        frete = random.choices(["Baixa", "Média"], weights=[0.8, 0.2])[0]
        prazo = random.choices(["Expresso", "Padrão"], weights=[0.75, 0.25])[0]
        historico = random.choices(["Impecável", "Aceitável"], weights=[0.8, 0.2])[0]
        dispositivo = random.choices(["Desktop", "Mobile App"], weights=[0.6, 0.4])[0]
        horario = random.choices(["Comercial", "Noturno"], weights=[0.7, 0.3])[0]
        autenticacao = random.choices(["Conta Antiga", "Nova Conta"], weights=[0.8, 0.2])[0]
        cancelou = random.choices(["Não", "Sim"], weights=[0.92, 0.08])[0]

    elif tipo_perfil == 2:
        # Perfil Alto Risco (tendência a cancelou = Sim)
        metodo = random.choices(["Assíncrono (Boleto)", "Síncrono (Pix)"], weights=[0.8, 0.2])[0]
        frete = random.choices(["Alta", "Média"], weights=[0.8, 0.2])[0]
        prazo = random.choices(["Longo", "Padrão"], weights=[0.75, 0.25])[0]
        historico = random.choices(["Risco", "Aceitável"], weights=[0.75, 0.25])[0]
        dispositivo = random.choices(["Mobile Web", "Mobile App"], weights=[0.7, 0.3])[0]
        horario = random.choices(["Madrugada", "Noturno"], weights=[0.7, 0.3])[0]
        autenticacao = random.choices(["Visitante", "Nova Conta"], weights=[0.7, 0.3])[0]
        cancelou = random.choices(["Sim", "Não"], weights=[0.85, 0.15])[0]

    else:
        # Perfil Ambíguo / Mistura
        metodo = random.choice(METODOS_PAGAMENTO)
        frete = random.choice(PROPORCOES_FRETE)
        prazo = random.choice(PRAZOS_ENTREGA)
        historico = random.choice(HISTORICOS_CLIENTE)
        dispositivo = random.choice(DISPOSITIVOS_COMPRA)
        horario = random.choice(HORARIOS_COMPRA)
        autenticacao = random.choice(TIPOS_AUTENTICACAO)
        
        if autenticacao == "Visitante" and historico == "Impecável":
            historico = "Aceitável"
        
        cancelou = random.choices(["Não", "Sim"], weights=[0.5, 0.5])[0]

    return {
        "metodo_pagamento": metodo,
        "proporcao_frete": frete,
        "prazo_entrega": prazo,
        "historico_cliente": historico,
        "dispositivo_compra": dispositivo,
        "horario_compra": horario,
        "tipo_autenticacao": autenticacao,
        "cancelou": cancelou
    }

def gerar_dataset(n_registros=120, caminho_saida="data/treino.csv"):
    registros = []
    vistos = set()
    
    attempts = 0
    while len(registros) < n_registros and attempts < 2000:
        attempts += 1
        reg = gerar_registro()
        key = tuple(reg[col] for col in FIELDNAMES)
        if key not in vistos:
            vistos.add(key)
            registros.append(reg)

    with open(caminho_saida, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(registros)

    print(f"Dataset de {len(registros)} registros gerado com sucesso em {caminho_saida}")

if __name__ == "__main__":
    gerar_dataset(120)
