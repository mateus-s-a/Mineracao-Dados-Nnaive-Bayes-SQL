import sqlite3

# Conecta ao banco de dados
conn = sqlite3.connect("data/atividade.db")

# Lê e executa o script SQL
with open("sql/classificador.sql", encoding="utf-8") as f:
    query = f.read()

# Exibe o resultado
for row in conn.execute(query):
    print("Probabilidade Sim (%):", row[0])
    print("Probabilidade Não (%):", row[1])
    print("Recomendação:", row[2])

conn.close()