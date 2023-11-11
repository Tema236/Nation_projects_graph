# from googletrans import Translator
#
# import ssl
# import os
# import certifi
#
# os.environ['WDM_SSL_VERIFY'] = '0'
# ssl._create_default_https_context = ssl._create_unverified_context
#
# translator = Translator()
# translator = Translator(service_urls=['translate.google.com'])
# text = "Государственная программа Российской Федерации 'Развитие туризма'".replace("'", "")
#
# result = translator.translate(text, src='ru', dest='eu')
#
# print(result)

from googletrans import Translator

translator = Translator()
result = translator.translate('Mikä on nimesi', src='fi', dest='fr')

print(result.text)