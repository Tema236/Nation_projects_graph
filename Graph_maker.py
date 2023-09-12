from neo4j import GraphDatabase
import pandas as pd
from dash import Dash, html
from dash import dcc
from dash import html
import dash_cytoscape as cyto
from Graph_OOP import Graph_n4
from dash import Dash, html, dcc, Input, Output, callback


graphn4 = Graph_n4()
elements = graphn4.get_full_graph()

dict_of_layouts = {
        'cose': {
            'name': 'cose',
            # 'roots': '[id = "system"]',
            'idealEdgeLength': 100,
            'nodeOverlap': 20,
            'refresh': 5,
            'fit': True,
            'padding': 30,
            'randomize': False,
            'componentSpacing': 800,
            'nodeRepulsion': 400000000,
            'edgeElasticity': 1000,
            'nestingFactor': 5,
            'gravity': 80,
            'numIter': 1000,
            'initialTemp': 200,
            'coolingFactor': 0.95,
            'minTemp': 1.0
        },

        'breadthfirst': {
            'name': 'breadthfirst',
            'fit': True,
            # 'directed': 'True',
            'padding': 1,
            'roots': '[id = "system"]',
            # 'circle': 'False',
            # 'grid': 'True',
            'spacingFactor': 11, #расстояние между нодам
            'avoidOverlap': 'True',
            # 'depthSort': "function(a, b){ return a.data('node_type').length - b.data('node_type').length }"
        }}

default_stylesheet = [
            {
                'selector': 'node',
                'style': {
                    'label': 'data(name)',
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


app = Dash(__name__)

app.layout = html.Div([
    # dcc.Dropdown(
    #         id='dropdown-update-layout',
    #         value='cose',
    #         clearable=False,
    #         options=[
    #         {'label': name.capitalize(), 'value': name}
    #         for name in ['cose', 'breadthfirst']
    #     ]
    # ),
    html.Div([
            html.Div(style={'width': '50%', 'display': 'inline'}, children=[
                'Edge Color:',
                dcc.Input(id='input-line-color', type='text')
            ]),
            html.Div(style={'width': '50%', 'display': 'inline'}, children=[
                'Node Color:',
                dcc.Input(id='input-bg-color', type='text')
            ]),
            html.Div(style={'width': '50%', 'display': 'inline'}, children=[
                'Node fontsize:',
                dcc.Input(id='input-f-size', type='text')
            ]),
            html.Div(style={'width': '50%', 'display': 'inline'}, children=[
                'Node width:',
                dcc.Input(id='input-node-width', type='text')
            ]),
            html.Div(style={'width': '50%', 'display': 'inline'}, children=[
                'Node height:',
                dcc.Input(id='input-node-height', type='text')
            ]),
            html.Div(style={'width': '50%', 'display': 'inline'}, children=[
                'Edge width:',
                dcc.Input(id='input-edge-width', type='text')
            ]),
                ]),

    dcc.Dropdown(
        id='edge-curvestyle-layout',
        value='bezier',
        clearable=False,
        options=[
            {'label': name.capitalize(), 'value': name}
            for name in ['haystack', 'straight', 'straight-triangle', 'bezier', 'unbundled-bezier', 'segments', 'taxi']
        ]
    ),

    dcc.Slider(1, 30, id='nodes-spacing-factor', updatemode='drag', value=11),

    cyto.Cytoscape(
        id='cytoscape-layout-6',
        # layout={'name': 'preset'},
        style={'width': '100%', 'height': '1500px', 'line-color': 'red'},
        elements=elements,
        stylesheet=default_stylesheet,
        layout=dict_of_layouts['breadthfirst'],
        # {
        #     'name': 'breadthfirst',
        #     'fit': True,
        #     # 'directed': 'True',
        #     'padding': 1,
        #     'roots': '[id = "system"]',
        #     # 'circle': 'False',
        #     # 'grid': 'True',
        #     'spacingFactor': 11, #расстояние между нодам
        #     'avoidOverlap': 'True',
        #     # 'depthSort': "function(a, b){ return a.data('node_type').length - b.data('node_type').length }"
        # },
        responsive=True
    )
])

# @callback(Output('cytoscape-layout-6', 'layout'),
#           Input('dropdown-update-layout', 'value'))
# def change_layout(layout):
#     return dict_of_layouts[layout]

@callback(Output('cytoscape-layout-6', 'stylesheet'),
              Input('input-line-color', 'value'),
               Input('input-bg-color', 'value'),
                Input('input-f-size', 'value'),
                Input('input-node-width', 'value'),
                Input('input-node-height', 'value'),
                Input('edge-curvestyle-layout', 'value'),
                Input('input-edge-width', 'value'))
def update_stylesheet(line_color, bg_color, fontsize, node_w, node_h, curvestyle, edge_width):
    if line_color is None:
        line_color = 'transparent'

    if bg_color is None:
        bg_color = 'transparent'
    #
    # if fontsize is None:
    #     fontsize = 'transparent'

    new_styles = [
            {
                'selector': 'node',
                'style': {
                    'label': 'data(name)',
                    'font-size': fontsize,
                    'background-color': bg_color,
                    'width': node_w,
                    'height': node_h
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
                    'curve-style': curvestyle,
                    'label': 'data(edge_type)',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': line_color,
                    'line-color': line_color,
                    # 'font-size': fontsize,
                    'width': edge_width
                }
            },
        ]

    return default_stylesheet + new_styles

@callback(Output('cytoscape-layout-6', 'layout'),
          Input('nodes-spacing-factor', 'value'))
def update_layout(spacingfactor):
    return {
            'name': 'breadthfirst',
            'fit': True,
            # 'directed': 'True',
            'padding': 1,
            'roots': '[id = "system"]',
            # 'circle': 'False',
            # 'grid': 'True',
            'spacingFactor': spacingfactor, #расстояние между нодам
            'avoidOverlap': 'True',
            # 'depthSort': "function(a, b){ return a.data('node_type').length - b.data('node_type').length }"
        }

if __name__ == '__main__':
    app.run(debug=True)