#!/usr/bin/python
# -*- coding: utf-8 -*-

# coding=utf-8

from io import BytesIO
import os
import sys
import pandas as pd
import xml.etree.ElementTree as et
from datetime import date

# Class for object of OPM


class OPM:
    def __init__(self, ean):
        self.ean = ean
        self.output_quantity = 0
        self.input_quantity = 0


class Parser:

    # Object constructor
    def __init__(self, from_dir, to_dir, year, month):
        self.from_dir = from_dir
        self.to_dir = to_dir
        self.year = year
        self.month = month
        self.file_list = self.getFilesFromFolder()
        self.data_frame = self.createEmptyDataFrame()
        self.output_file_name = f"{self.year}_{self.month}.output_data.xlsx"

    # Save data to excel file
    def createXLSX(self):
        self.parseXML()
        save_dir = os.path.join(self.to_dir, self.output_file_name)
        self.data_frame.to_excel(save_dir, index=False)

    # Get absolute paths of all files in folder
    def getFilesFromFolder(self):
        file_list = []
        for root, _, files in os.walk(os.path.abspath(self.from_dir)):
            for file in files:
                filename, file_extension = os.path.splitext(file)
                if file_extension == ".xml" or file_extension == ".XML":
                    file_list.append(os.path.join(root, file))
        return file_list

    # Make empty dataframe to store data
    def createEmptyDataFrame(self):
        return pd.DataFrame(columns=['EAN', 'Dodavka', 'Odber'])

    # Convert to negative
    def convertToNegative(self, value):
        return value * -1

    # Function to sum all values in list value-type
    def sumValues(self, values):
        value_list = []
        for val in values:
            value_list.append(float(val.get('value')))
        return sum(value_list)

    # Main parser function
    def parseXML(self):
        for file in self.file_list:
            tree = et.ElementTree(file=file)
            root = tree.getroot()

            # Get all locations from XML root
            locations = list(root)

            # Loop through all Locations
            for location in locations:
                ean = location.get('opm-id')
                if not ean:
                    continue

                # Define OPM object
                opm = OPM(ean)

                # Get all DataProfiles from location
                DataProfile = list(location)

                # Loop through all DataProdiles
                for value_type in DataProfile:

                    # Find value type and loop through all values
                    if value_type.get('value-type') == "A11":
                        opm.output_quantity = self.sumValues(list(value_type))

                    if value_type.get('value-type') == "A12":
                        opm.input_quantity = self.sumValues(list(value_type))

                self.data_frame = self.data_frame.append(
                    {'EAN': opm.ean, 
                    'Dodavka': opm.output_quantity, 
                    'Odber': self.convertToNegative(value=opm.input_quantity)
                    }, ignore_index=True)

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
        year = today.year
        month = getMonthText(today.month-1)

    # Actual directory path
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(ROOT_DIR, f"data/_Pracovní {year}/01_OTE/Data/{month}/")

    parser = Parser(data_folder, data_folder, year, month)
    parser.createXLSX()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
