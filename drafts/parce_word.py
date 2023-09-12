# import docx2txt
#
# # Путь к RTF файлу
# rtf_file = r"C:\Users\a.danilov\Downloads\Telegram Desktop\FP_Sovershenstvovanie_upravleniya.rtf"
#
# # Извлечение текста из RTF файла
# text = docx2txt.process(rtf_file)
# # print(text)
#
# # Поиск таблиц в тексте
# tables = text.split('\n\n')  # Предполагается, что таблицы разделяются двойными переносами строк
#
# # Обработка каждой таблицы
# for table in tables:
#     rows = [row.split('\t') for row in table.split('\n')]  # Предполагается, что ячейки разделяются табуляцией
#
#     # Вывод содержимого таблицы
#     for row in rows:
#         for cell in row:
#             print(cell, end='\t')
#         print()
#     print("------")

import re
from pathlib import Path
from striprtf.striprtf import rtf_to_text

file_path = r"C:\Users\a.danilov\Downloads\Telegram Desktop\FP_Sovershenstvovanie_upravleniya.rtf"
# file_path = r"C:\Users\a.danilov\Downloads\Telegram Desktop\FP_Turisticheskaya_infrastruktura.rtf"
# file_path = r"C:\Users\a.danilov\Downloads\Telegram Desktop\FP_Dostupnost'_turisticheskogo_produkta.rtf"

# content = Path(r"C:\Users\a.danilov\Downloads\Telegram Desktop\FP_Sovershenstvovanie_upravleniya.rtf").read_text()
content = Path(file_path).read_text()
text = rtf_to_text(content)
# decoded = bytes(map(ord, text)).decode('cp1251')
# print(decoded)
# text = text.replace('||', '\n')
# text = re.sub(r'\n\d\|\|\n', 'Тут был отступ страницы', text) #убрать нумерацию страниц
# print(text)

federal_project_name = re.search(r'федерального проекта\|\|(\D*)\|\|', text).group(1).strip() #название федерального
print(federal_project_name)

names_of_tables = re.findall(r"\n(\d{1,2}\. .*)\|\|", text) #Названия таблиц в тексте

for name_of_table in names_of_tables:
    print(f'{name_of_table}')

tables_main = [text.split(names_of_tables[i])[-1].split(names_of_tables[i+1])[0].strip('||') for i in range(0,6)]

tables_main[0] = re.sub(r'\n\d\|\|\n', '', tables_main[0])
tables_main[0] = tables_main[0].strip('\n').strip()
print(tables_main[0])
print(tables_main[0].count('||\n'))
text_to_destroy = tables_main[0]

# a = text_to_destroy.split('||\n')[0]
# print(a)
#
# print('------------------------')

# text_to_destroy = text_to_destroy.replace(f'{a}||\n', '')
# print(text_to_destroy)

table_1 = []

for num_string in range(0,tables_main[0].count('||\n')):
    a = text_to_destroy.split('||\n')[0]
    print(a)
    text_to_destroy = text_to_destroy.replace(f'{a}||\n', '')
    table_1.append(a.replace('\n',' ').split('|'))
    # print(text_to_destroy)
    print('-------------------------------------------')

table_1_unique = []
for item in table_1:
    if item not in table_1_unique:
        table_1_unique.append(item)
print(table_1_unique)

# table_1 = list(set(table_1))
# print(table_1)

for el in table_1_unique:
    print(el)

national_project_name = table_1_unique[0][1]
short_federal_project_name = table_1_unique[1][1]
realization_start_date = table_1_unique[1][3]
realization_end_date = table_1_unique[1][4]
federal_project_kurator = [table_1_unique[2][1], table_1_unique[2][2]]
federal_project_leader = [table_1_unique[3][1], table_1_unique[3][2]]
federal_project_admin = [table_1_unique[4][1], table_1_unique[4][2]]

print(f"""
Наименование национального проекта: {national_project_name.replace('"','')}
Наименование федерального проекта: {federal_project_name}
Краткое наименование федерального проекта: {short_federal_project_name}
Сроки реализации проекта: с {realization_start_date} по {realization_end_date}
Куратор федерального проекта: {federal_project_kurator[1]} {federal_project_kurator[0]}
Руководитель федерального проекта: {federal_project_leader[1]} {federal_project_leader[0]}
Администратор федерального проекта: {federal_project_admin[1]} {federal_project_admin[0]}
""")

def delete_dubles_in_list(list):
    new_list = []
    for item in list:
        if item not in new_list:
            new_list.append(item)
    return new_list

for str_num in range(5, len(table_1_unique)):
    # if str_num % 2 == 0:
    # print(table_1_unique[str_num])
    # print(delete_dubles_in_list(table_1_unique[str_num]).remove(''))

    table_1_unique[str_num] = delete_dubles_in_list(table_1_unique[str_num])
    if '' in table_1_unique[str_num]:
        table_1_unique[str_num].remove('')

    # print(table_1_unique[str_num])

    if 'Государственная программа' in table_1_unique[str_num]:
        for element in range(len(table_1_unique[str_num])):
            if table_1_unique[str_num][element] == 'Государственная программа':
                print(table_1_unique[str_num][element + 1])

    elif len(table_1_unique[str_num]) > 1 and 'программы' not in table_1_unique[str_num][1]:
        print(table_1_unique[str_num][1])
    # if 'Государственная программа' in table_1_unique[str_num]:
    #     print(f'{table_1_unique[str_num][3]}')
    #
    # elif table_1_unique[str_num][3]:
    #     print(f'{table_1_unique[str_num][3]}')
# def parse_rtf_table()