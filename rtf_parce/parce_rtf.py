import re
from pathlib import Path
from striprtf.striprtf import rtf_to_text
from translator.translator_google import translate_text


# # Удаление дубликатов в массиве
# def delete_dubles_in_list(list):
#     new_list = []
#     for item in list:
#         if item not in new_list:
#             new_list.append(item)
#     return new_list

class rtf_file(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def parce_rtf_file(self):
        content = Path(self.file_path).read_text()
        text = rtf_to_text(content)

        federal_project_name = re.search(r'федерального проекта\|\|(\D*)\|\|', text).group(1).strip().replace('"','') #название федерального
        federal_project_name_id = translate_text(federal_project_name, 'en') #создать id для федерального проекта

        names_of_tables = re.findall(r"\n(\d{1,2}\. .*)\|\|", text) #Названия таблиц в тексте

        tables_main = [text.split(names_of_tables[i])[-1].split(names_of_tables[i+1])[0].strip('||') for i in range(0,6)] #достать первые 7 таблиц
        print(names_of_tables)

        tables_main[0] = re.sub(r'\n\d\|\|\n', '', tables_main[0]) #убрать из нулевой таблицы со связями нумерации страниц
        tables_main[0] = tables_main[0].strip('\n').strip() #убрать лишние отступы и побелы
        text_to_destroy = tables_main[0]

        table_1 = []

        #Разбиение строк по колонкам
        for num_string in range(0, tables_main[0].count('||\n')):
            a = text_to_destroy.split('||\n')[0]
            text_to_destroy = text_to_destroy.replace(f'{a}||\n', '')
            table_1.append(a.replace('\n', ' ').split('|'))

        #Удаление дубликатов в массиве
        def delete_dubles_in_list(list):
            new_list = []
            for item in list:
                if item not in new_list:
                    new_list.append(item)
            return new_list

        #Удалить дубликаты строк
        table_1_unique = delete_dubles_in_list(table_1)

        national_project_name = table_1_unique[0][1].replace('"','')
        national_project_name_id = translate_text(national_project_name, 'en')
        short_federal_project_name = table_1_unique[1][1].replace('"','')
        realization_start_date = table_1_unique[1][3]
        realization_end_date = table_1_unique[1][4]
        federal_project_kurator = [table_1_unique[2][1], table_1_unique[2][2]]
        federal_project_leader = [table_1_unique[3][1], table_1_unique[3][2]]
        federal_project_admin = [table_1_unique[4][1], table_1_unique[4][2]]

        programs = []
        for str_num in range(5, len(table_1_unique)):

            table_1_unique[str_num] = delete_dubles_in_list(table_1_unique[str_num])
            if '' in table_1_unique[str_num]:
                table_1_unique[str_num].remove('')

            if 'Государственная программа' in table_1_unique[str_num]:
                for element in range(len(table_1_unique[str_num])):
                    if table_1_unique[str_num][element] == 'Государственная программа':
                        programs.append({'data':{'id': translate_text(re.sub(r'\d.', '', table_1_unique[str_num][element + 1]), 'en'), 'label': re.sub(r'\d.', '', table_1_unique[str_num][element + 1]), 'node_type': 'state_program'}})

            elif len(table_1_unique[str_num]) > 1 and 'программы' not in table_1_unique[str_num][1]:
                programs.append({'data':{'id': translate_text(re.sub(r'\d.', '', table_1_unique[str_num][1]).strip(), 'en'), 'label':re.sub(r'\d.', '', table_1_unique[str_num][1]).strip(), 'node_type': 'subprogram'}})

        nodes = [{'data':{'id': national_project_name_id,'label': national_project_name, 'node_type': 'national_project'}}, {'data':{
                                                                    'id': federal_project_name_id,
                                                                    'label': federal_project_name,
                                                                    'national_project_name': national_project_name,
                                                                    'short_federal_project_name': short_federal_project_name,
                                                                    'realization_start_date': realization_start_date,
                                                                    'realization_end_date': realization_end_date,
                                                                    'federal_project_kurator': federal_project_kurator,
                                                                    'federal_project_leader': federal_project_leader,
                                                                    'federal_project_admin': federal_project_admin,
                                                                    'node_type': 'federal_project'}}] + programs

        links = []
        link_1 = {'data':{'source': national_project_name_id, 'target': federal_project_name_id}}
        links.append(link_1)
        for num_prog in range(0, len(programs)):
            if programs[num_prog]['data']['node_type'] == 'subprogram':
                links.append({'data':{'source': programs[num_prog-1]['data']['id'], 'target': programs[num_prog]['data']['id']}})
        for prog in programs:
            if prog['data']['node_type'] != 'subprogram':
                links.append({'data':{'source': federal_project_name_id, 'target': prog['data']['id']}})

        return nodes, links

if __name__ == '__main__':
    file_path = r"C:\PY\Nation_projects_graph\files\FP_Dostupnost'_turisticheskogo_produkta.rtf"
    fp_su = rtf_file(file_path=file_path)
    result = fp_su.parce_rtf_file()
    # for res in result[0]:
    #     print(res)
    #
    # for res in result[1]:
    #     print(res)
    print(result[0])
    print(result[1])