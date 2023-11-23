from neo4j import GraphDatabase

# # Подключение к базе данных Neo4j
driver = GraphDatabase.driver("neo4j://10.220.75.45:7687", auth=("neo4j", "q1w2e3r4"))
print(driver)

