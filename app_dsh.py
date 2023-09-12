from dash import Dash, html
import dash_cytoscape as cyto

app = Dash(__name__)


from neo4j import GraphDatabase
driver = GraphDatabase.driver("neo4j://10.220.75.45:7687", auth=("neo4j", "q1w2e3r4"))
query_nodes = """
MATCH (n) RETURN n
"""
results_nodes = driver.session().run(query_nodes)
nds = list(results_nodes.graph()._nodes.values())
nodes = [dict({'data':node._properties}) for node in nds]

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=nodes,
        # [
            # {'data': {'object_in_db': 'True', 'node_type': 'structural_element', 'name': 'Кинотеатры', 'id': 'cinemas'}, 'position': {'x': 75, 'y': 75}},
            # {'data': {'node_type': 'structural_element', 'name': 'Образование и духовный рост', 'id': 'national_development_goal2'}, 'position': {'x': 200, 'y': 200}},
            # {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
            # {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            # {'data': {'source': 'one', 'target': 'two'}}
        # ],
        stylesheet=[
        {
            'selector': 'node',
            'style': {
                'label': 'data(name)',
                'font-size': 'small',
                'background-color': '#00bfff',
            }
        }
])])

if __name__ == '__main__':
    app.run(debug=True)