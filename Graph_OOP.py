from neo4j import GraphDatabase
import networkx as nx
import pandas as pd
import textwrap as tw

class Graph_n4(object):
    """
    Импортирование графа из Neo4j
    """
    def __init__(self):
        self.driver = GraphDatabase.driver("neo4j://10.220.75.45:7687", auth=("neo4j", "q1w2e3r4"))

    def get_nodes(self, query) -> list:
        """
        Получение НОД из Neo4j
        :param query: запрос для Neo4j
        :return: список из словарей с НОДАМИ
        """
        result = self.driver.session().run(query)
        records = result.data()
        return records

    def get_edges(self, query) -> list:
        """
        Получение отношений между НОДАМИ графа Neo4j
        :param query: запрос для Neo4j
        :return: список из словарей с со связями
        """
        result = self.driver.session().run(query)
        records = result.data()
        df = pd.DataFrame(records)
        edges = [{'data': {'source': row[0]['id'], 'target': row[2]['id'], 'edge_type': row[1]}} for row in df['r']]
        return edges

    def get_full_graph(self) -> list:
        """
        Получить полный граф со всеми НОДАМИ и отношениями
        :return: сформированный список из списков словарей НОД и отношений
        """
        nodes = self.get_nodes('MATCH (data) RETURN data')
        nodes = self.wrap_text_in_nodes(nodes)
        edges = self.get_edges('MATCH (n)-[r]->(m) RETURN n, r ,m')
        elements = nodes + edges
        return elements

    def get_node_names(self) -> list:
        """
        Получить наименования всех НОД и их id
        :return: сформированный список из наименований НОД
        """
        names = self.driver.session().run('MATCH (n) RETURN distinct n.id, n.name')
        records = names.data()
        df = pd.DataFrame(records)

        return df

    def get_node_and_her_links(self, node_id) -> list:
        """
        Получить НОДУ, её связи (последующие)
        :param node_id: идентификатор НОДЫ
        :return: сформированный список из ноды и ее связей
        """
        nodes = self.get_nodes(f'MATCH (n {{id:\'{node_id}\'}})-->(m) RETURN n, m')
        df = pd.DataFrame(nodes)
        print(df)
        edges = self.get_edges(f'MATCH (n {{id:\'{node_id}\'}})-[r]->(m) RETURN n, r, m')
        print(f'MATCH (n {{id:\'{node_id}\'}})-->(m) RETURN n,m')
        return nodes+edges

    def wrap_text_in_nodes(self, nodes) -> list:
        """
        Добавить отступы строк в названия НОД
        :param nodes: список из словарей НОД
        :return: такой же список НОД, но с переносом текста по строкам
        """
        for node in nodes:
            node['data']['name'] = tw.fill(node['data']['name'], width=35)
        return nodes

# if __name__ == '__main__':
#     test_graph = Graph_n4()
#     nodes_li = test_graph.get_nodes('MATCH (data) RETURN data')
    # for nd in nodes_li:
    #     nd['data']['name'] = tw.fill(nd['data']['name'], width=35)
    #     print(nd['data']['name'])
#     print(test_graph.get_node_and_her_links('circuses'))
#     # nodes = test_graph.get_nodes('MATCH (data) RETURN data')
#     # edges = test_graph.get_edges('MATCH (n)-[r]->(m) RETURN n, r ,m')
#     # print(nodes)
#     # print(edges)
#     names = test_graph.get_node_names()
#     print(names)