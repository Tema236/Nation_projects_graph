from dash import Dash, html, dcc, Input, Output, callback
import dash_cytoscape as cyto
from rtf_parce.parce_rtf import rtf_file
# from rtf_parce import parce_rtf
import os

# Удаление дубликатов в массиве
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

    file_path = fr'{directory}\{file}'
    fp_su = rtf_file(file_path=file_path)
    result = fp_su.parce_rtf_file()

    nodes += result[0]
    edges += result[1]

nodes = delete_dubles_in_list(nodes)
edges = delete_dubles_in_list(edges)

style1 = [
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)',
                    'font-size': 'large',
                    'background-color': '#00bfff',
                    'text-wrap': 'wrap',
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
                'selector': '[node_type = "subprogram"]',
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
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': 'black',
                    'line-color': 'black'
                }
            },
        ]

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div(style={'width': '50%', 'display': 'inline'}, children=[
            'Edge Color:',
            dcc.Input(id='input-line-color', type='text'),
        ]),
        html.Div(style={'width': '50%', 'display': 'inline'}, children=[
            'Node Color:',
            dcc.Input(id='input-bg-color', type='text'),
        ])
    ]),

    cyto.Cytoscape(
        id='cytoscape-layout-6',
        # layout={'name': 'preset'},
        style={'width': '100%', 'height': '1500px', 'line-color': 'red'},
        elements=nodes+edges,
        stylesheet=style1,
        layout={
            'name': 'breadthfirst',
            'fit': True,
            'directed': False,
            'padding': 100,
            'roots': '[node_type = "national_project"]',
            'circle': False,
            'grid': False,
            'spacingFactor': 11,
           ' avoidOverlap': True,
        },
        responsive=True
    )
])

@callback(Output('cytoscape-layout-6', 'stylesheet'),
              Input('input-line-color', 'value'),
               Input('input-bg-color', 'value'))
def update_stylesheet(line_color, bg_color):
    if line_color is None:
        line_color = 'transparent'

    if bg_color is None:
        bg_color = 'transparent'

    new_styles = [
        {
            'selector': 'node',
            'style': {
                'background-color': bg_color
            }
        },
        {
            'selector': 'edge',
            'style': {
                'line-color': line_color
            }
        }
    ]

    return style1 + new_styles

if __name__ == '__main__':
    app.run(debug=True)
