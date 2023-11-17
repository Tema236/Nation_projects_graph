import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, html, dash_table, dcc, callback
from dash_bootstrap_components._components.Container import Container
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
AC_LOGO = 'https://dt.ac.gov.ru/dwh_new/template/assets/menu_logo_ac.svg'

# navbar = dbc.Navbar(
#     dbc.Container(
#         [
#             html.A(
#                 # Use row and col to control vertical alignment of logo / brand
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Img(src=AC_LOGO, height="30px")),
#                         dbc.Col(dbc.NavbarBrand("Национальные проекты Российской Федерации", className="ms-2")),
#                         # dbc.Col(dbc.NavItem(dbc.NavLink("Помощь", href="#")))
#                     ],
#                     align="center",
#                     className="g-0",
#                 ),
#                 href="https://plotly.com",
#                 style={"textDecoration": "none"},
#             ),
#         ]
#     ),
#     color="dark",
#     dark=True,
# )

# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(
#             dbc.NavLink(
#                 "Article",
#                 href="https://medium.com/plotly/exploring-and-investigating-network-relationships-with-plotlys-dash-and-dash-cytoscape-ec625ef63c59?source=friends_link&sk=e70d7561578c54f35681dfba3a132dd5",
#             )
#         ),
#         dbc.NavItem(
#             dbc.NavLink(
#                 "Source Code",
#                 href="https://github.com/plotly/dash-sample-apps/tree/master/apps/dash-cytoscape-lda",
#             )
#         ),
#     ],
#     brand="Plotly dash-cytoscape demo - CORD-19 LDA analysis output",
#     brand_href="#",
#     color="dark",
#     dark=True,
# )

# navbar = dbc.Navbar(
#     [
#         dbc.NavbarBrand("Какое-то название", className="mx-auto"),
#         dbc.NavItem(dbc.NavLink("Помощь", href="#")),
#     ],
#     color="dark",
#     dark=True,
# )

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(html.Img(src=AC_LOGO, height="40px"), href="#"),
            dbc.NavbarBrand("Национальные проекты Российской Федерации", className="mx-auto fs-4"),
            # dbc.NavbarBrand("Национальные проекты Российской Федерации", className="mx-auto fs-4"),
            dbc.NavItem(dbc.NavLink("Помощь", href="#")),
        ]
    ),
    color="dark",
    dark=True,
    # className="mb-4",
)


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
            ], title="Помесячный план достижения показателей национального и федерального проекта в 2023 году"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Результаты федерального проекта"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Финансовое обеспечение реализации федерального проекта"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Помесячный план исполнения федерального бюджета в части бюджетных ассигнований, предусмотренных на финансовое обеспечение реализации федерального проекта в 2023 году"),
            # dbc.AccordionItem([
            #     "Тут будет таблица"
            # ], title="Таблица 7"),
        ],
        flush=True,
        start_collapsed=True,
    )
])

if __name__ == '__main__':
    app.run(debug=True)