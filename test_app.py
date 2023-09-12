from neo4j import GraphDatabase
import pandas as pd
# import dash
# import dashcytoscape as cyto
# import dashhtmlcomponents as html

pd.set_option('display.max_rows', 550)
# pd.set_option('expand_frame_repr', True)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 70)

# Подключение к базе данных Neo4j
driver = GraphDatabase.driver("neo4j://10.220.75.45:7687", auth=("neo4j", "q1w2e3r4"))

# Запрос к базе данных Neo4j
def runquery(query):
    with driver.session() as session:
        result = session.run(query)
        records = result.data()
    return records

# Выполнение запроса к базе данных Neo4j и создание DataFrame
query_egdes = "MATCH (n)-[r]->(m) RETURN n, r ,m"
records_e = runquery(query_egdes)
df_e = pd.DataFrame(records_e)

query_nodes = """
MATCH (data) RETURN data
"""
records_n = runquery(query_nodes)
# print(records_n)
df_n = pd.DataFrame(records_n)

print(df_e['n'][0]['id'], df_e['m'][0]['id'])
print(df_e['r'][20])
print(df_e['r'][20][0])
print(df_e['r'][20][1])
print(df_e['r'][20][2])
print(df_n)
print(records_n)