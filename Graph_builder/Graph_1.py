import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback, dash_table
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

AC_LOGO = 'https://dt.ac.gov.ru/dwh_new/template/assets/menu_logo_ac.svg'
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

for file in files:

    file_path = fr'{directory}\{file}'
    fp_su = rtf_file(file_path=file_path)
    result = fp_su.parce_rtf_file()

    nodes += result[0]
    edges += result[1]

nodes = delete_dubles_in_list(nodes)
edges = delete_dubles_in_list(edges)

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

selected_node_name = html.Div(
    id="name-of-node",
    children='Нажмите на НОДу для получения информации о ней',
    className='text-center lead'
)

accordion = dbc.Accordion(
        [
            dbc.AccordionItem([
                "dash_table.DataTable(data=df.to_dict('records'), page_size=5)"
            ], title='Основные положения', id="table1"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title='Показатели национального и федерального проекта', id="table2"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Помесячный план достижения показателей национального и федерального проекта в 2023 году", id="table3"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Результаты федерального проекта", id="table4"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Финансовое обеспечение реализации федерального проекта", id="table5"),
            dbc.AccordionItem([
                "Тут будет таблица"
            ], title="Помесячный план исполнения федерального бюджета в части бюджетных ассигнований, предусмотренных на финансовое обеспечение реализации федерального проекта в 2023 году", id="table6"),
            # dbc.AccordionItem([
            #     "Тут будет таблица"
            # ], title="Таблица 7"),
        ],
        flush=True,
        start_collapsed=True,
    )

cytoscape = cyto.Cytoscape(
        id='cytoscape-layout-6',
        # layout={'name': 'preset'},
        style={'width': '100%', 'height': '650px', 'line-color': 'red'},
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

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc_css])

app.layout = html.Div(
    [
        navbar,
        selected_node_name,
        accordion,
        cytoscape
    ]
)

@callback(
    Output('name-of-node', 'children'),
    [Input("cytoscape-layout-6", "selectedNodeData")]
)
def upgrade_name(datalist):
    # table_data_df = pd.DataFrame()
    contents = "Нажмите на элемент для получения информации о нем"
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            contents = []
            print(data)
            print(datalist)
            contents.append(data["label"])
    return contents

@callback(
    Output('table1', 'children'),
    Input("cytoscape-layout-6", "selectedNodeData")
)
def upgrade_table1(datalist):
    content = ""
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            content = []
            if data['node_type'] == 'federal_project':
                content.append(f'Название национального проекта: {data["national_project_name"]}')
                content.append(f'\nКраткое название федерального проекта: {data["short_federal_project_name"]}')

    return content

if __name__ == '__main__':
    app.run(debug=True)