from dash import Dash, html
import dash_cytoscape as cyto
import json
import textwrap as tw

nodes = []

with open('../files/factor_hierarchy.json', encoding='utf-8') as f:
    templates = json.load(f)

# print(templates)
# x = 5
# y = 5
# count = 0
#
# for node in templates['nodes']:
#     # js_gr_1.add_node(node['name'])
#     # elements.append(dict([{'data': dict({'id': node['id'], 'label': node['name']})}, {'position': dict({'x': x, 'y': y})}, dict({'locked': True, 'selected': True})]))
#     nodes.append(dict(
#         {'data': dict({'id': node['id'], 'label': node['name']}), 'position': dict({'x': x, 'y': y}),
#          'selected': True}))
#     x += 20
#     y += 10
#     # if count % 2 == 0:
#     #     y += y
#     # else:
#     #     y -= 2*y
#     # print(node['name'])
#
# edges = []
#
# for link in templates['links']:
#     edges.append(dict({'data': dict({'source': link['target'], 'target': link['source']})}))
#     print(link['source'], '->', link['target'])

nodes = [dict({'data': dict({'id': node['id'], 'label': tw.fill(node['name'], width=35), 'node_type': node['node_type']}), 'selected': False}) for node in templates['nodes']]
edges = [dict({'data': dict({'source': link['target'], 'target': link['source']})}) for link in templates['links']]

print(type(nodes))
print(edges)

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
            'spacingFactor': 11,
           ' avoidOverlap': True,
        },
        responsive=True
    )
])


if __name__ == '__main__':
    app.run(debug=True)