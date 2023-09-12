import dash
from dash import dcc
from dash import html
import dash_cytoscape as cyto

from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://10.220.75.45:7687", auth=("neo4j", "q1w2e3r4"))

query_nodes = """
MATCH (n) RETURN n
"""

query_edges = """
MATCH (n)-[r]->(c) RETURN r
"""

results_nodes = driver.session().run(query_nodes)
results_edges = driver.session().run(query_edges)
nds = list(results_nodes.graph()._nodes.values())
eds = list(results_edges.graph()._relationships.values())

nodes = [dict({'data':node._properties}) for node in nds]
edges = [dict({'data':rel._properties}) for rel in eds]

print(nodes)
print(edges)

app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-layout-6',
        # layout={'name': 'preset'},
        style={'width': '100%', 'height': '1500px', 'line-color': 'red'},
        elements=nodes+edges,
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'font-size': 'large',
                    'background-color': '#00bfff',
                }
            },
            {
                'selector': '[firstname *= "ert"]',
                'style': {
                    'background-color': '#FF4136',
                    'shape': 'rectangle'
                }
            },

            {
                'selector': '[node_type = "structural_element"]',
                'style': {
                    'background-color': '#FF4136',
                    'shape': 'rectangle'
                }
            },

            {
                'selector': '[node_type = "observed_indicator"]',
                'style': {
                    'background-color': '#8be553',
                    'background-fit': 'cover',
                    # 'background-image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/' + '4/45/Spongilla_lacustris.jpg' + '/150px-' + '4/45/Spongilla_lacustris.jpg'.split('/')[-1]
                    'shape': 'triangle'
                }
            },

            {
                'selector': 'edge',
                'style': {
                    # The default curve style does not work with certain arrows
                    'curve-style': 'bezier',
                    'source-arrow-shape': 'triangle',
                    'source-arrow-color': 'black',
                    'line-color': 'black'
                }
            },
        ],
        layout={
            'name': 'breadthfirst',
            'fit': True,
            'directed': False,
            'padding': 100,
            'roots': '[id = "system"]',
            'circle': False,
            'grid': False,
            'spacingFactor': 5,
           ' avoidOverlap': True,
        },
        responsive=True
    )
])

# app.layout = html.Div(
#     children=[
#         html.H1("Моделирование национальной проектной деятельности", style={'text-align': 'center'}),
#         dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
#                           ['Montréal']),
#         dcc.Graph(
#             id="example-graph",
#             figure={
#                 "data": [
#                     {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "Нью-Йорк"},
#                     {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": u"Монреаль"},
#                 ],
#                 "layout": {"title": "Столбчатая диаграмма"},
#             },
#         ),
#     ]
# )

if __name__ == "__main__":
    app.run_server(debug=True)

# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#    dcc.Dropdown(
#        options=[
#            {'label': 'FC Barcelona', 'value': 'FCB'},
#            {'label': 'Real Madrid', 'value': 'RM'},
#            {'label': 'Manchester United', 'value': 'MU'}
#        ],
#        multi=True,
#        value="FCB"
#    )
# ], style={"width": 200})
#
# if __name__ == '__main__':
#    app.run_server(debug=True)

# from dash import Dash, dcc, html
#
# app = Dash(__name__)
#
# app.layout = html.Div([
#     dcc.Checklist(['New York City', 'Montréal', 'San Francisco'],
#                   ['Montréal'])
# ])
#
# if __name__ == '__main__':
#     app.run(debug=True)