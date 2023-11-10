import re
from pathlib import Path
from striprtf.striprtf import rtf_to_text
from translator.translator_google import translate_text
import pandas as pd

pd.set_option('display.max_rows', 550)
# pd.set_option('expand_frame_repr', True)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 70)

headers_of_tables = {
    2: ['№ п/п', 'Показатели федерального проекта', 'Уровень показателя', 'Единица измерения (по ОКЕИ)', 'Базовое значение', 'Базовое значение год', 'Период, год 2018', 'Период, год 2019', 'Период, год 2020', 'Период, год 2021', 'Период, год 2022', 'Период, год 2023', 'Период, год 2024', 'Период, год 2025', 'Период, год 2026', 'Период, год 2027', 'Период, год 2028', 'Период, год 2029', 'Период, год 2030', 'Информационная система (источник данных)'],
    3: ['№ п/п', 'Показатели национального и федерального проекта', 'Уровень показателя', 'Единица измерения (по ОКЕИ)', 'Плановые значения по месяцам янв.', 'Плановые значения по месяцам фев.', 'Плановые значения по месяцам мар.', 'Плановые значения по месяцам апр.', 'Плановые значения по месяцам май.', 'Плановые значения по месяцам июнь', 'Плановые значения по месяцам июль', 'Плановые значения по месяцам авг.', 'Плановые значения по месяцам сен.', 'Плановые значения по месяцам окт.', 'Плановые значения по месяцам ноя.', 'На конец 2023 года'],
    4: ['№ п/п', 'Наименование результата', 'Наименование структурных элементов государственных программ Российской Федерации', 'Единица измерения (по ОКЕИ)', 'Базовое значение', 'Базовое значение год', 'Период, год 2018', 'Период, год 2019', 'Период, год 2020', 'Период, год 2021', 'Период, год 2022', 'Период, год 2023', 'Период, год 2024', 'Период, год 2025', 'Период, год 2026', 'Период, год 2027', 'Период, год 2028', 'Период, год 2029', 'Период, год 2030', 'Тип результата', 'Связь с показателем национальной цели развития Российской Федерации'],
    5: ['№ п/п', 'Наименование результата и источники финансирования', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2018', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2019', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2020', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2021', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2022', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2023', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2024', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2025', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2026', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2027', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2028', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2029', 'Объем финансового обеспечения по годам реализации (тыс. рублей) 2030', 'Всего (тыс. рублей)'],
    6: ['№ п/п', 'Наименование результата', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'План исполнения нарастающим итогом (тыс. рублей)', 'На конец 2023 года (тыс. рублей)']
}

def delete_dubles_in_list(list):
    new_list = []
    for item in list:
        if item not in new_list:
            new_list.append(item)
    return new_list

def delete_elements_in_end(n, a):
    for last_element in range(n):
        a.pop(len(a)-1)

def parce_table(table, table_name):
    table_in_list = []
    # print(table)
    # print('------------------------')
    # table = re.sub(r'\n\d{1,}\|\|\n', '', table)  # убрать из нулевой таблицы со связями нумерации страниц
    table = re.sub(r'\n\d{1,}\|{1,3}\n', '', table)  # убрать из нулевой таблицы со связями нумерации страниц
    table = table.strip('\n').strip()  # убрать лишние отступы и побелы
    text_to_destroy = table.replace('\xa0', '').replace('\u200b', '') # убрать символ \u200b
    table_2 = text_to_destroy.split('||\n') # разделить текст по строкам
    table_2 = delete_dubles_in_list(table_2)
    # print(table_2[2:])
    for el in table_2[2:]:
        string_of_table = el.split('|') # разделить строку по колонкам
        if '№ п/п' in string_of_table and string_of_table[0] != '№ п/п':
            index = string_of_table.index('№ п/п')
            string_of_table = string_of_table[:index]

        if set(string_of_table) == {''}:
            pass
        else:
            # print(string_of_table)
            # print(len(headers_of_tables[int(table_name.split('. ')[0])]),len(string_of_table))
            if len(string_of_table) > len(headers_of_tables[int(table_name.split('. ')[0])]):
                n = len(string_of_table) - len(headers_of_tables[int(table_name.split('. ')[0])])
                delete_elements_in_end(n, string_of_table)

            # print(string_of_table)
            table_in_list.append(string_of_table)

    # print(table_in_list[2:])
    # print(table_name.split('. ')[0]) # номер таблицы, чтобы брать шапку из словаря
    df = pd.DataFrame(table_in_list, columns=headers_of_tables[int(table_name.split('. ')[0])])
    print(df)
    print('-------------------------')

class rtf_file(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def parce_rtf_file(self):
        content = Path(self.file_path).read_text()
        text = rtf_to_text(content)

        names_of_tables = re.findall(r"\n(\d{1,2}\. .*)\|\|", text)  # Названия таблиц в тексте

        tables_main = [text.split(names_of_tables[i])[-1].split(names_of_tables[i + 1])[0].strip('||') for i in
                       range(0, 6)]  # достать первые 7 таблиц

        numb = 1
        # print(tables_main[1:])
        for table in tables_main[1:]:
            print(names_of_tables[numb])
            parce_table(table, names_of_tables[numb])
            numb += 1


if __name__ == '__main__':
    file_path = r"C:\PY\Nation_projects_graph\files\FP_Dostupnost'_turisticheskogo_produkta.rtf"
    # file_path = r"C:\PY\Nation_projects_graph\files\FP_Sovershenstvovanie_upravleniya.rtf"
    # file_path = r"C:\PY\Nation_projects_graph\files\FP_Turisticheskaya_infrastruktura.rtf"
    fp_su = rtf_file(file_path=file_path)
    result = fp_su.parce_rtf_file()
    # result.parce_table()