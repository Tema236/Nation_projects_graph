import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, html, dash_table, dcc, callback
from dash_bootstrap_components._components.Container import Container
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
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

# accordion = html.Div(
#     dbc.Accordion(
#         [
#             dbc.AccordionItem(
#                 "This is the content of the first section", title="Item 1"
#             ),
#             dbc.AccordionItem(
#                 "This is the content of the second section", title="Item 2"
#             ),
#             dbc.AccordionItem(
#                 "This is the content of the third section", title="Item 3"
#             ),
#         ],
#         flush=True,
#     ),
# )
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc_css])

app.layout = html.Div([
    navbar,
    html.Div(children='Какой-то заголовок', style={'textAlign':'center', 'color':'black', 'fontSize': 30}),
    dbc.Accordion(
        [
            dbc.AccordionItem([
                dash_table.DataTable(data=df.to_dict('records'), page_size=5)
            ], title='Основные положения'),
            dbc.AccordionItem([
                dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
            ], title='Показатели национального и федерального проекта'),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Помесячный план достижения "),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Таблица 4"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Таблица 5"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Таблица 6"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Таблица 7"),
        ],
        flush=True
    )
])

if __name__ == '__main__':
    app.run(debug=True)