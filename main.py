# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from io import BytesIO

import pandas as pd
import xml.etree.ElementTree as et

def print_hi(name):
    year = '2022'
    month = 'Únor'

    for i in range(1,5):
        path = f"D:/OneDrive - ČEZ Energo, s.r.o/_Pracovní {year}/01_OTE/Data/{month}/{i}.xml"
        data_from_ote(file=path, index=i, month=month, year=year)

def data_from_ote(file, index, month, year):
    # config listů
    dodavka = 0
    nakup = 0
    ean = "0"
    dataframe = pd.DataFrame(columns=['EAN', 'Dodavka', 'Odber'])
    print('ok')
    # načtení kořenu
    tree = et.ElementTree(file=file)
    root = tree.getroot()
    zdroje = list(root)
    # rozdělěení podle EANu
    for zdroj in zdroje:
        e = zdroj.get('opm-id')
        if e is not None:
            ean = e
            dodavka = 0
            nakup = 0
        DataProfile = list(zdroj)

        # rozdělení podle typu hodnoty Dodavka/Odber
        for value_type in DataProfile:

            if value_type.get('value-type') == "A11":
                hodnoty = list(value_type)
                for val in hodnoty:
                    dodavka = dodavka + float(val.get('value'))

            if value_type.get('value-type') == "A12":
                hodnoty = list(value_type)
                for val in hodnoty:
                    nakup = nakup + float(val.get('value'))


        dataframe = dataframe.append({'EAN': ean, 'Dodavka': dodavka, 'Odber': nakup * -1},ignore_index=True)

    save_dir = f"D:/OneDrive - ČEZ Energo, s.r.o/_Pracovní {year}/01_OTE/Data/{month}/{index}_data.xlsx"
    dataframe.to_excel(save_dir, sheet_name='Sheet1')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
