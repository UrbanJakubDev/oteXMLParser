#!/usr/bin/python
# -*- coding: utf-8 -*-

# coding=utf-8

from io import BytesIO
import os
import sys
import pandas as pd
import xml.etree.ElementTree as et
from datetime import date
from app.xml import Parser

def getMonthText(num_of_month):
    months = {
        1: "Leden",
        2: "Únor",
        3: "Březen",
        4: "Duben",
        5: "Květen",
        6: "Červen",
        7: "Červenec",
        8: "Srpen",
        9: "Září",
        10: "Říjen",
        11: "Listopad",
        12: "Prosinec"
    }
    return months[num_of_month]

def main():
    
    # Get arguments from command line
    today = date.today()

    try:
        year = sys.argv[1]
        month = sys.argv[2]
    except IndexError:
        year = str(today.year)
        month = getMonthText(today.month-1)

    # Actual directory path
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(ROOT_DIR, f"data/_Pracovní {year}/01_OTE/Data/{month}/")

    # Ipnut directory path
    input_folder = f'C:/Users/JakubUrban/OneDrive - ČEZ Energo, s.r.o/_Pracovní {year}/01_OTE/Data/{month}'

    print('Init parser')
    parser = Parser(input_folder, input_folder, year, month)

    parser.createXLSX()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()