# from googletrans import Translator
#
# import ssl
# import os
# import certifi
#
# os.environ['WDM_SSL_VERIFY'] = '0'
# ssl._create_default_https_context = ssl._create_unverified_context
#
# # translator = Translator()
# translator = Translator(service_urls=['translate.google.com'])
# text = "Государственная программа Российской Федерации 'Развитие туризма'".replace("'", "")
#
# result = translator.translate(text, src='ru', dest='eu')
#
# print(result.text)
# # translator.v
#
# # result = translator.translate(text='Государственная программа Российской Федерации "Развитие туризма"'.replace('"',''), src='ru', dest='eu')
# #
# # print(result)
#
# # a = ['qewq', '2312', '32423423', '14124']
# #
# # for i, el in enumerate(a):
# #     print(i)
# #     print(el)

import requests
from bs4 import BeautifulSoup


def translate_text(text, dest_lang):
    url = "https://translate.google.com/m?sl=ru&tl=" + dest_lang + "&q=" + text.replace(" ", "+").replace("'",'').replace('"','')
    print(url)
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = soup.find("div", class_="result-container").get_text()

    return result.lower().replace(' ','_')


# # Пример использования
# text = "Государственная программа Российской Федерации 'Развитие туризма'"
# dest_lang = "en"
# translated_text = translate_text(text, dest_lang)
# # node_id = translated_text.lower().replace(' ','_')
# print(translated_text)