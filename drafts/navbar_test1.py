import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, html, dash_table, dcc, callback
from dash_bootstrap_components._components.Container import Container
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
AC_LOGO = 'https://dt.ac.gov.ru/dwh_new/template/assets/menu_logo_ac.svg'

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=AC_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2 ")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color="dark",
    dark=True,
)

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO, external_stylesheets])

app.layout = html.Div([
    navbar,
    html.Div(children='Data^', style={'textAlign':'center', 'color':'black', 'fontSize': 30}),
    # html.Hr(), # полоска

    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),

    html.Div(className='six columns', children=[
    dash_table.DataTable(data=df.to_dict('records'), page_size=5)]),
    # dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
    dcc.Graph(figure={}, id='controls-and-graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig


if __name__ == '__main__':
    app.run(debug=True)

