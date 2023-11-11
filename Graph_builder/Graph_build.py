from dash import Dash, html, dcc, Input, Output, callback
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
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

# stylesheet with the .dbc class to style  dcc, DataTable and AG Grid components with a Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
# AC_LOGO = 'https://corp.cea.gov.ru/content/img/acgov.png'
AC_LOGO = 'https://dt.ac.gov.ru/dwh_new/template/assets/menu_logo_ac.svg'

# search_bar = dbc.Row(
#     [
#         dbc.Col(dbc.Input(type="search", placeholder="Search")),
#         dbc.Col(
#             dbc.Button(
#                 "Search", color="primary", className="ms-2", n_clicks=0
#             ),
#             width="auto",
#         ),
#     ],
#     className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
#     align="center",
# )

#, dbc.icons.FONT_AWESOME
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO, dbc_css])

app.layout = html.Div([

    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=AC_LOGO, height="50px")),
                            dbc.Col(dbc.NavbarBrand("Национальные проекты Российской Федерации", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://corp.cea.gov.ru/",
                    style={"textDecoration": "none"},
                ),
                # dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                # dbc.Collapse(
                #     search_bar,
                #     id="navbar-collapse",
                #     is_open=False,
                #     navbar=True,
                # ),
            ]
        ),
        color="dark",
        dark=True,
    ),

    # html.Div([
    #     html.Div(style={'width': '50%', 'display': 'inline'}, children=[
    #         'Edge Color:',
    #         dcc.Input(id='input-line-color', type='text'),
    #     ]),
    #     html.Div(style={'width': '50%', 'display': 'inline'}, children=[
    #         'Node Color:',
    #         dcc.Input(id='input-bg-color', type='text'),
    #     ])
    # ]),

    # html.Div([
                # html.Div(style={'width': '50%', 'display': 'inline'}, id='node-data', children=[
            html.Div(
                # style={'overflow': 'scroll',
                        # 'width': '15em',
            # 'border': '1px solid #333',
            # 'box-shadow': '8px 8px 5px #444',
            # 'padding': '8px 12px',
            # 'background-image': 'linear-gradient(180deg, #fff, #ddd 40%, #ccc)'
            # },
                id='node-data', children=[
                'Информация о НОДе',
            ]),
    # ]),

    cyto.Cytoscape(
        id='cytoscape-layout-6',
        # layout={'name': 'preset'},
        style={'width': '100%', 'height': '750px', 'line-color': 'red'},
        elements=nodes+edges,
        stylesheet=style1,
        minZoom=0.09,
        maxZoom=0.9,
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

# @callback(Output('cytoscape-layout-6', 'stylesheet'),
#               Input('input-line-color', 'value'),
#                Input('input-bg-color', 'value'))
# def update_stylesheet(line_color, bg_color):
#     if line_color is None:
#         line_color = 'transparent'
#
#     if bg_color is None:
#         bg_color = 'transparent'
#
#     new_styles = [
#         {
#             'selector': 'node',
#             'style': {
#                 'background-color': bg_color
#             }
#         },
#         {
#             'selector': 'edge',
#             'style': {
#                 'line-color':  line_color
#             }
#         }
#     ]
#
#     return style1 + new_styles

@app.callback(
    Output("node-data", "children"), [Input("cytoscape-layout-6", "selectedNodeData")]
)
def display_nodedata(datalist):
    contents = "Нажмите на элемент для получения информации о нем"
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            contents = []
            print(data)
            contents.append(html.H5(data["label"]))
            if data['node_type'] == 'federal_project':
                contents.append(
                    html.P(
                        f'Тип проекта: федеральный'
                    )
                )
                contents.append(
                    html.P(
                        f'Наименование национального проекта: {data["national_project_name"]}'
                    )
                )
                contents.append(
                    html.P(
                        f'Краткое наименование федерального проекта: {data["short_federal_project_name"]}'
                    )
                )
                contents.append(
                    html.P(
                        f'Сроки реализации проекта: с {data["realization_start_date"]} по {data["realization_end_date"]}'
                    )
                )
                contents.append(
                    html.P(
                        f'Куратор федерального проекта: {data["federal_project_kurator"][1]} {data["federal_project_kurator"][0]}'
                    )
                )
                contents.append(
                    html.P(
                        f'Руководитель федерального проекта: {data["federal_project_leader"][1]} {data["federal_project_leader"][0]}'
                    )
                )
                contents.append(
                    html.P(
                        f'Администратор федерального проекта: {data["federal_project_admin"][1]} {data["federal_project_admin"][0]}'
                    )
                )
            # contents.append(html.H5(data['id']))
            # print(data)
            # print(datalist)
            # contents.append(data)
            # contents.append(
            #     html.P(
            #         "Journal: "
            #         + data["journal"].title()
            #         + ", Published: "
            #         + data["pub_date"]
            #     )
            # )
            # contents.append(
            #     html.P(
            #         "Author(s): "
            #         + str(data["authors"])
            #         + ", Citations: "
            #         + str(data["n_cites"])
            #     )
            # )

    return contents

if __name__ == '__main__':
    app.run(debug=True)