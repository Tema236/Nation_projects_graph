import json

from neo4j import GraphDatabase
import networkx as nx

driver = GraphDatabase.driver("neo4j://10.220.75.45:7687", auth=("neo4j", "q1w2e3r4"))

with open('../files/factor_hierarchy.json', encoding='utf-8') as f:
    templates = json.load(f)

nodes = [dict({'data': dict({'id': node['id'], 'label': node['name'], 'node_type': node['node_type']}), 'selected': False}) for node in templates['nodes']]
# print(nodes)

query_nodes = """
MATCH (n) RETURN n
"""

query_edges = """
MATCH (n)-[r]->(c) RETURN r
"""

results_nodes = driver.session().run(query_nodes)
nodes = list(results_nodes.graph()._nodes.values())

nodes_2 = [dict({'data': node._properties}) for node in nodes]
# nodes_2 = [dict({'data': node._properties}) for node in nodes]
print(nodes_2[0])

results_edges = driver.session().run(query_edges)
rels = list(results_edges.graph()._relationships.values())
print(rels[0])

# for rel in rels:
#     print(rel._properties)