import json
from neo4j import GraphDatabase

# # Подключение к базе данных Neo4j
driver = GraphDatabase.driver("neo4j://10.220.75.45:7687", auth=("neo4j", "q1w2e3r4"))
print(driver)

with open('../drafts/factor_hierarchy.json', encoding='utf-8') as f:
    templates = json.load(f)

with driver.session() as session:
    for node in templates['nodes']:
        node_attrs = ""
        for key, value in node.items():
            new_value = str(value).replace('"','')
            node_attrs += f'{key}: "{new_value}", '
        node_attrs = node_attrs.strip(', ')
        print(f'CREATE (node:{node["node_type"]} {{{node_attrs}}})')
        session.run(f'CREATE (node:{node["node_type"]} {{{node_attrs}}})')

    id_and_node_type = {node['id']: node['node_type'] for node in templates['nodes']}

    for link in templates['links']:
        print(link)
        session.run(f"MATCH (a:{id_and_node_type[link['source']]} {{id: '{link['source']}'}}), (b:{id_and_node_type[link['target']]} {{id: '{link['target']}'}}) CREATE (a)-[:{link['edge_type'].replace(' ','_')}]->(b)")

    session.close()
# print(templates)