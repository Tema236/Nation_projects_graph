import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 550)
# pd.set_option('expand_frame_repr', True)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 70)

def parce_excel():
    df = pd.read_excel(r'C:\Users\a.danilov\Downloads\Копия NP_Cifrovaya_ekonomika.xlsx')
    print(df)

if __name__ == '__main__':
    parce_excel()