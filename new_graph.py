from dash import Dash, html
import dash_cytoscape as cyto
from parce_rtf import rtf_file

file_path = r"C:\Users\a.danilov\Downloads\Telegram Desktop\FP_Turisticheskaya_infrastruktura.rtf"
fp_su = rtf_file(file_path=file_path)
result = fp_su.parce_rtf_file()

nodes = result[0]
edges = result[1]

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
            'roots': '[id = "tourism_and_hospitality_industry"]',
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