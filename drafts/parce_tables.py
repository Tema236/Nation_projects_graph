import re
from pathlib import Path
from striprtf.striprtf import rtf_to_text
from translator.translator_google import translate_text

def delete_dubles_in_list(list):
    new_list = []
    for item in list:
        if item not in new_list:
            new_list.append(item)
    return new_list


def parce_table(table):
    print(table)
    print('------------------------')
    # table = re.sub(r'\n\d{1,}\|\|\n', '', table)  # убрать из нулевой таблицы со связями нумерации страниц
    table = re.sub(r'\n\d{1,}\|{1,3}\n', '', table)  # убрать из нулевой таблицы со связями нумерации страниц
    table = table.strip('\n').strip()  # убрать лишние отступы и побелы
    text_to_destroy = table.replace('\xa0', '').replace('\u200b', '')
    table_2 = text_to_destroy.split('||\n')
    table_2 = delete_dubles_in_list(table_2)
    for el in table_2:
        string_of_table = el.split('|')
        if '№ п/п' in string_of_table and string_of_table[0] != '№ п/п':
            index = string_of_table.index('№ п/п')
            string_of_table = string_of_table[:index]

        print(string_of_table)

    print('-------------------------')

class rtf_file(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def parce_rtf_file(self):
        content = Path(self.file_path).read_text()
        text = rtf_to_text(content)

        federal_project_name = re.search(r'федерального проекта\|\|(\D*)\|\|', text).group(1).strip().replace('"',
                                                                                                              '')  # название федерального
        federal_project_name_id = translate_text(federal_project_name, 'en')  # создать id для федерального проекта

        names_of_tables = re.findall(r"\n(\d{1,2}\. .*)\|\|", text)  # Названия таблиц в тексте

        tables_main = [text.split(names_of_tables[i])[-1].split(names_of_tables[i + 1])[0].strip('||') for i in
                       range(0, 6)]  # достать первые 7 таблиц
        # print(names_of_tables)
        # print(tables_main[1])
        # tables_main[1] = re.sub(r'\n\d\|\|\n', '', tables_main[1])  # убрать из нулевой таблицы со связями нумерации страниц
        # tables_main[1] = tables_main[1].strip('\n').strip()  # убрать лишние отступы и побелы
        # text_to_destroy = tables_main[1].replace('\xa0','').replace(' ||','||')
        #
        # # table_2 = text_to_destroy.split('||\n')
        # # print(table_2)
        #
        # table_2 = []
        #
        # # Разбиение строк по колонкам
        # for num_string in range(0, tables_main[1].count('||\n')):
        #     a = text_to_destroy.split('||\n')[0]
        #     text_to_destroy = text_to_destroy.replace(f'{a}||\n', '')
        #     table_2.append(a.replace('\n', ' ').split('|'))
        #
        # # Удаление дубликатов в массиве
        #
        #
        # # Удалить дубликаты строк
        # table_2_unique = delete_dubles_in_list(table_2)
        #
        # for el in table_2_unique:
        #     print(el.split('|'))
        numb = 0
        for table in tables_main:
            print(names_of_tables[numb])
            parce_table(table)
            numb += 1


if __name__ == '__main__':
    file_path = r"C:\PY\Nation_projects_graph\files\FP_Dostupnost'_turisticheskogo_produkta.rtf"
    # file_path = r"C:\PY\Nation_projects_graph\files\FP_Sovershenstvovanie_upravleniya.rtf"
    # file_path = r"C:\PY\Nation_projects_graph\files\FP_Turisticheskaya_infrastruktura.rtf"
    fp_su = rtf_file(file_path=file_path)
    result = fp_su.parce_rtf_file()
    # result.parce_table()