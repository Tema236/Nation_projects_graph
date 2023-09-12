from neo4j import GraphDatabase
import networkx as nx
import matplotlib.pyplot as plt

# # Подключение к базе данных Neo4j
driver = GraphDatabase.driver("neo4j://10.220.75.45:7687", auth=("neo4j", "q1w2e3r4"))
print(driver)

query_nodes = """
MATCH (n) RETURN n
"""

query_edges = """
MATCH (n)-[r]->(c) RETURN r
"""

results_nodes = driver.session().run(query_nodes)
results_edges = driver.session().run(query_edges)

G = nx.MultiDiGraph()

nodes = list(results_nodes.graph()._nodes.values())

# print(nodes)
for node in nodes:
    G.add_node(node.id, labels=node._labels, properties=node._properties)
    print({node._properties})

rels = list(results_edges.graph()._relationships.values())
# print(rels)
for rel in rels:
    G.add_edge(rel.start_node.id, rel.end_node.id, key=rel.id, type=rel.type, properties=rel._properties)
    print(rel)

print(G)

# nx.draw(G)
# plt.figure(figsize=(100,100))
#
# plt.show()
# with driver.session() as session:
#     result = session.run(query)
#     session.close()
#
# print(result.consume())
#
# # print(result.graph()._nodes.values())
#
# dtf_data = pd.DataFrame([dict(_) for _ in result.consume()])
# print(dtf_data)