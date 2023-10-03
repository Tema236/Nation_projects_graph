# from neo4j import GraphDatabase
# import pandas as pd
# import dash
# from dash import dcc
# from dash import html
# import dash_cytoscape as cyto
# from Graph_OOP import Graph_n4
#
# app = dash.Dash(__name__)
# graphn4 = Graph_n4()
# elements = graphn4.get_full_graph()
#
# app.layout = html.Div([
#     cyto.Cytoscape(
#         id='cytoscape-two-nodes',
#         layout={'name': 'preset'},
#         style={'width': '100%', 'height': '400px'},
#         elements=elements,
#         # [
#             # {'data': {'object_in_db': 'True', 'node_type': 'structural_element', 'name': 'Кинотеатры', 'id': 'cinemas'}, 'position': {'x': 75, 'y': 75}},
#             # {'data': {'node_type': 'structural_element', 'name': 'Образование и духовный рост', 'id': 'national_development_goal2'}, 'position': {'x': 200, 'y': 200}},
#             # {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
#             # {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
#             # {'data': {'source': 'one', 'target': 'two'}}
#         # ],
#         stylesheet=[
#         {
#             'selector': 'node',
#             'style': {
#                 'label': 'data(name)',
#                 'font-size': 'small',
#                 'background-color': '#00bfff',
#             }
#         }
# ])])
#
# if __name__ == '__main__':
#     app.run(debug=True)

# pd.set_option('display.max_rows', 550)
# # pd.set_option('expand_frame_repr', True)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
# pd.set_option('max_colwidth', 70)
#
# # Подключение к базе данных Neo4j
# driver = GraphDatabase.driver("neo4j://10.220.75.45:7687", auth=("neo4j", "q1w2e3r4"))
#
# # Запрос к базе данных Neo4j
# def runquery(query):
#     with driver.session() as session:
#         result = session.run(query)
#         records = result.data()
#     return records
#
# # Выполнение запроса к базе данных Neo4j и создание DataFrame
# query_egdes = "MATCH (n)-[r]->(m) RETURN n, r ,m"
# records_e = runquery(query_egdes)
# df_e = pd.DataFrame(records_e)
#
# # print(df_e)
# print(df_e['r'][0])
#
# print(f'source: {df_e["r"][0][0]["id"]} -{df_e["r"][0][1]}-> {df_e["r"][0][2]["id"]}')
#
# edges_li = [{'data': {'source': row[0]['id'], 'target': row[2]['id'], 'edge_type': row[1]}} for row in df_e['r']]
#
# print(edges_li)
# edges = [dict({'data': dict({'source': link['target'], 'target': link['source']})}) for link in templates['links']]

# dict_of_layouts = {
#         'cose': {
#             'name': 'cose',
#             # 'roots': '[id = "system"]',
#             'idealEdgeLength': 100,
#             'nodeOverlap': 20,
#             'refresh': 5,
#             'fit': True,
#             'padding': 30,
#             'randomize': False,
#             'componentSpacing': 800,
#             'nodeRepulsion': 400000000,
#             'edgeElasticity': 1000,
#             'nestingFactor': 5,
#             'gravity': 80,
#             'numIter': 1000,
#             'initialTemp': 200,
#             'coolingFactor': 0.95,
#             'minTemp': 1.0
#         },
#
#         'breadthfirst': {
#             'name': 'breadthfirst',
#             'fit': True,
#             # 'directed': 'True',
#             'padding': 1,
#             'roots': '[id = "system"]',
#             # 'circle': 'False',
#             # 'grid': 'True',
#             'spacingFactor': 11, #расстояние между нодам
#             'avoidOverlap': 'True',
#             # 'depthSort': "function(a, b){ return a.data('node_type').length - b.data('node_type').length }"
#         }}
#
# print(dict_of_layouts['breadthfirst'])

# import textwrap as tw
#
# str_1 = 'возвращает 2 строки - первая часть максимальной длины не больше n и остаток строки, разделители - пробелы. Повторять с остатком, пока он не пуст. Если пуста первая возвращаемая строка - разбиение невозможно.'
#
# print(tw.fill(str_1, width=20))

# a = ['', 'dwada', '', '21321', 'dqwd1']
a = ['', '']
# if '#5' in a:
#     index = a.index('#5')
#     a = a[:index]
print(set(a))
if set(a) == {''}:
    print(')')