from dash import Dash, html
import dash_cytoscape as cyto
from rtf_parce.parce_rtf import rtf_file
# from rtf_parce import parce_rtf
import os

# file_path = r"C:\PY\Nation_projects_graph\files\FP_Sovershenstvovanie_upravleniya.rtf"
# file_path = r"C:\PY\Nation_projects_graph\files\FP_Turisticheskaya_infrastruktura.rtf"
# file_path = r"C:\PY\Nation_projects_graph\files\FP_Dostupnost'_turisticheskogo_produkta.rtf"

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

    file_path = f'{directory}\{file}'
    fp_su = rtf_file(file_path=file_path)
    result = fp_su.parce_rtf_file()

    nodes += result[0]
    edges += result[1]

nodes = delete_dubles_in_list(nodes)
edges = delete_dubles_in_list(edges)

app = Dash(__name__)

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
        ],
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


if __name__ == '__main__':
    app.run(debug=True)