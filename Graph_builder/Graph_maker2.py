import dash_cytoscape as cyto
from neo4j_py.Graph_OOP import Graph_n4
from dash import Dash, html, Input, Output, callback
import os
from rtf_parce.parce_rtf import rtf_file

# graphn4 = Graph_n4()
# elements = graphn4.get_full_graph()

def delete_dubles_in_list(list):
    new_list = []
    for item in list:
        if item not in new_list:
            new_list.append(item)
    return new_list

# Указываем путь к директории
directory = r"C:\PY\Nation_projects_graph\files"

# Получаем список файлов
files = os.listdir(directory)

nodes = []
edges = []

for file in files:

    file_path = f'{directory}\{file}'
    fp_su = rtf_file(file_path=file_path)
    result = fp_su.parce_rtf_file()

    nodes += result[0]
    edges += result[1]

nodes = delete_dubles_in_list(nodes)
edges = delete_dubles_in_list(edges)

elements = nodes+edges

default_stylesheet = [
            {
              "selector": "core",
              "style": {
                "selection-box-color": "#AAD8FF",
                "selection-box-border-color": "#8BB0D0",
                "selection-box-opacity": "0.5"
              },
            },

            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'font-size': 'large',
                    'background-color': '#00bfff',
                    'text-wrap': 'wrap'
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
                    'label': 'data(edge_type)',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': 'black',
                    'line-color': 'black'
                }
            },
        ]

styles = {
    'container': {
        'position': 'fixed',
        'display': 'flex',
        'flex-direction': 'column',
        'height': '100%',
        'width': '100%'
    },
    'cy-container': {
        'flex': '1',
        'position': 'relative'
    },
    'cytoscape': {
        'position': 'absolute',
        'width': '100%',
        'height': '100%',
        'z-index': 999
    }
}

app = Dash(__name__)

app.layout = html.Div(style=styles['container'], children=[
    html.Div([
        html.Button("Responsive Toggle", id='toggle-button'),
        html.Div(id='toggle-text')
    ]),
    html.Div(className='cy-container', style=styles['cy-container'], children=[
        cyto.Cytoscape(
            id='cytoscape-responsive-layout',
            elements=elements,
            stylesheet=default_stylesheet,
            style=styles['cytoscape'],
            layout={
                'name': 'cose',
                'idealEdgeLength': 100,
                'nodeOverlap': 20,
                'refresh': 20,
                'fit': True,
                'padding': 30,
                'randomize': False,
                'componentSpacing': 100,
                'nodeRepulsion': 400000,
                'edgeElasticity': 100,
                'nestingFactor': 5,
                'gravity': 80,
                'numIter': 1000,
                'initialTemp': 200,
                'coolingFactor': 0.95,
                'minTemp': 1.0
            },
            responsive=True
        )
    ])
])

@callback(Output('cytoscape-responsive-layout', 'responsive'), Input('toggle-button', 'n_clicks'))
def toggle_responsive(n_clicks):
    n_clicks = 2 if n_clicks is None else n_clicks
    toggle_on = n_clicks % 2 == 0
    return toggle_on

@callback(Output('toggle-text', 'children'), Input('cytoscape-responsive-layout', 'responsive'))
def update_toggle_text(responsive):
    return '\t' + 'Responsive ' + ('On' if responsive else 'Off')

if __name__ == '__main__':
    app.run(debug=True)