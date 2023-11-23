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

df = pd.DataFrame.from_dict({'№ п/п': ['1', '1.1.', '2', '2.1.', '2.2.', '3', '3.1.', '3.2.', '3.3.'], 'Показатели федерального проекта': ['Гражданам с целью отдыха и поддержания здоровья обеспечена \nдоступность поездок по стране в условиях комфортной и безопасной туристической среды', 'Число туристских поездок', 'Созданы и внедрены цифровые решения, обеспечивающие гражданам доступ\n к информации о возможностях отдыха внутри страны, а также к туристическим цифровым сервисам', 'Число посещений Национального туристического портала', 'Количество объектов, маршрутов, услуг и сервисов туристической инфраструктуры Российской Федерации, представленных на Национальном туристическом портале', 'Создана сквозная система финансовой и нефинансовой поддержки, направленная на развитие экспорта туристских услуг ', 'Число въездных туристских поездок иностранных граждан в Российскую Федерацию ', 'Экспорт туристских услуг', 'Число рынков-доноров, для которых адаптированы объекты туристской инфраструктуры, туристских маршрутов и событий, а также услуги и сервисы, доступные на цифровой туристической платформе'], 'Уровень показателя': [None, 'НП', None, 'НП', 'ФП', None, 'НП', 'НП', 'ФП'], 'Единица измерения (по ОКЕИ)': [None, 'Миллион человек', None, 'Миллион единиц', 'Тысяча единиц', None, 'Миллион человек', 'Миллион долларов', 'Штука'], 'Базовое значение': [None, '45,2200', None, '1,0600', '20,0000', None, '24,5200', '0,0000', '0,0000'], 'Базовое значение год': [None, '2020', None, '2019', '2020', None, '2019', '2021', '2020'], 'Период, год 2018': [None, '-', None, '-', '-', None, '-', '-', '-'], 'Период, год 2019': [None, '-', None, '-', '-', None, '-', '-', '-'], 'Период, год 2020': [None, '-', None, '-', '-', None, '-', '-', '-'], 'Период, год 2021': [None, '52,2200', None, '2,1800', '40,0000', None, '3,7600', '-', '1,0000'], 'Период, год 2022': [None, '59,4500', None, '4,2000', '45,0000', None, '4,8900', '2027,6300', '2,0000'], 'Период, год 2023': [None, '64,0700', None, '4,8300', '50,0000', None, '7,6000', '8135,4000', '3,0000'], 'Период, год 2024': [None, '75,4900', None, '5,5500', '55,0000', None, '10,0000', '10167,1700', '4,0000'], 'Период, год 2025': [None, '-', None, '-', '-', None, '-', '-', '-'], 'Период, год 2026': [None, '-', None, '-', '-', None, '-', '-', '-'], 'Период, год 2027': [None, '-', None, '-', '-', None, '-', '-', '-'], 'Период, год 2028': [None, '-', None, '-', '-', None, '-', '-', '-'], 'Период, год 2029': [None, '-', None, '-', '-', None, '-', '-', '-'], 'Период, год 2030': [None, '-', None, '-', '-', None, '-', '-', '-'], 'Информационная система (источник данных)': [None, 'Центральная база статистических данных (ЦБСД) (Росстат)', None, 'ЕМИСС', 'Национальный туристический портал', None, 'Центральная база статистических данных (ЦБСД) (Росстат)', 'ЕМИСС', 'Национальный туристический портал']})
# print(df)
df1 = df.to_dict('records')

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
                dash_table.DataTable(data=df1, page_size=10, id='datatable1')
            ], title='Показатели национального и федерального проекта', id="table2"),
            dbc.AccordionItem([
                dash_table.DataTable(data=df1, page_size=10, id='datatable2')
            ], title="Помесячный план достижения показателей национального и федерального проекта в 2023 году", id="table3"),
            dbc.AccordionItem([
                dash_table.DataTable(data=df1, page_size=10, id='datatable3')
            ], title="Результаты федерального проекта", id="table4"),
            dbc.AccordionItem([
                dash_table.DataTable(data=df1, page_size=10, id='datatable4')
            ], title="Финансовое обеспечение реализации федерального проекта", id="table5"),
            dbc.AccordionItem([
                dash_table.DataTable(data=df1, page_size=10, id='datatable5')
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
            # print(data)
            # print(datalist)
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
                # content.append(f'Название национального проекта: {data["national_project_name"]}')
                # content.append(f'\nКраткое название федерального проекта: {data["short_federal_project_name"]}')
                content.append(
                    html.P(
                        f'Тип проекта: федеральный'
                    ))
                content.append(
                    html.P(
                        f'Наименование национального проекта: {data["national_project_name"]}'
                    ))
                content.append(
                    html.P(
                        f'Наименование федерального проекта: {data["label"]}'
                    ))
                content.append(
                    html.P(
                        f'Краткое наименование федерального проекта: {data["short_federal_project_name"]}'
                    ))
                content.append(
                    html.P(
                        f'Сроки реализации: с {data["realization_start_date"]} по {data["realization_end_date"]}'
                    ))
                content.append(
                    html.P(
                        f'Куратор федерального проекта: {data["federal_project_kurator"][1]} {data["federal_project_kurator"][0]}'
                    ))
                content.append(
                    html.P(
                        f'Руководитель федерального проекта: {data["federal_project_leader"][1]} {data["federal_project_leader"][0]}'
                    ))
                content.append(
                    html.P(
                        f'Администратор федерального проекта: {data["federal_project_admin"][1]} {data["federal_project_admin"][0]}'
                    ))

            if data['node_type'] == 'national_project':
                content.append(
                    html.P(
                        f'Национальный проект: {data["label"]}'
                    )
                )

            if data['node_type'] == 'state_program':
                content.append(
                    html.P(
                        f'{data["label"]}'
                    )
                )

            if data['node_type'] == 'subprogram':
                content.append(
                    html.P(
                        f'Подпрограмма: {data["label"]}'
                    )
                )
    return content

@callback(
    Output(component_id='datatable1', component_property='data'),
    Input(component_id='cytoscape-layout-6', component_property='selectedNodeData')
)
def update_DataTable_1(datalist):
    df = pd.DataFrame().to_dict('records')
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            if data['node_type'] == 'federal_project':
                # print(data['tables'][0])
                df = pd.DataFrame().from_dict(data['tables'][0]).to_dict('records')
    return df

@callback(
    Output(component_id='datatable2', component_property='data'),
    Input(component_id='cytoscape-layout-6', component_property='selectedNodeData')
)
def update_DataTable_1(datalist):
    df = pd.DataFrame().to_dict('records')
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            if data['node_type'] == 'federal_project':
                # print(data['tables'][0])
                df = pd.DataFrame().from_dict(data['tables'][1]).to_dict('records')
    return df

@callback(
    Output(component_id='datatable3', component_property='data'),
    Input(component_id='cytoscape-layout-6', component_property='selectedNodeData')
)
def update_DataTable_1(datalist):
    df = pd.DataFrame().to_dict('records')
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            if data['node_type'] == 'federal_project':
                # print(data['tables'][0])
                df = pd.DataFrame().from_dict(data['tables'][2]).to_dict('records')
    return df

@callback(
    Output(component_id='datatable4', component_property='data'),
    Input(component_id='cytoscape-layout-6', component_property='selectedNodeData')
)
def update_DataTable_1(datalist):
    df = pd.DataFrame().to_dict('records')
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            if data['node_type'] == 'federal_project':
                # print(data['tables'][0])
                df = pd.DataFrame().from_dict(data['tables'][3]).to_dict('records')
    return df

@callback(
    Output(component_id='datatable5', component_property='data'),
    Input(component_id='cytoscape-layout-6', component_property='selectedNodeData')
)
def update_DataTable_1(datalist):
    df = pd.DataFrame().to_dict('records')
    if datalist is not None:
        if len(datalist) > 0:
            data = datalist[-1]
            if data['node_type'] == 'federal_project':
                # print(data['tables'][0])
                df = pd.DataFrame().from_dict(data['tables'][4]).to_dict('records')
    return df

if __name__ == '__main__':
    app.run(debug=True)