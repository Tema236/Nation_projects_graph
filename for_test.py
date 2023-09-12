# import re
#
# test_str = '1._creation_and_improvement_of_the_quality_of_tourism_infrastructure'
#
# print(re.sub(r'\d.', '', test_str))

from dash import Dash, html
import dash_cytoscape as cyto

app = Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=[
            {'data': {'id': 'on _e', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'two_treoo', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'on _e', 'target': 'two_treoo'}}
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)