-- sql/schema.sql
-- Definição da estrutura da tabela de treinamento para o classificador Naive Bayes em SQL

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS treino;

CREATE TABLE treino (
    id_pedido          INTEGER PRIMARY KEY AUTOINCREMENT,
    metodo_pagamento   TEXT NOT NULL CHECK (metodo_pagamento IN ('Síncrono (Cartão)', 'Síncrono (Pix)', 'Assíncrono (Boleto)')),
    proporcao_frete    TEXT NOT NULL CHECK (proporcao_frete IN ('Baixa', 'Média', 'Alta')),
    prazo_entrega      TEXT NOT NULL CHECK (prazo_entrega IN ('Expresso', 'Padrão', 'Longo')),
    historico_cliente  TEXT NOT NULL CHECK (historico_cliente IN ('Impecável', 'Aceitável', 'Risco')),
    dispositivo_compra TEXT NOT NULL CHECK (dispositivo_compra IN ('Desktop', 'Mobile App', 'Mobile Web')),
    horario_compra     TEXT NOT NULL CHECK (horario_compra IN ('Comercial', 'Noturno', 'Madrugada')),
    tipo_autenticacao  TEXT NOT NULL CHECK (tipo_autenticacao IN ('Visitante', 'Nova Conta', 'Conta Antiga')),
    cancelou           TEXT NOT NULL CHECK (cancelou IN ('Sim', 'Não'))
);
