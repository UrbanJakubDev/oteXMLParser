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
        self.data_frame = self.createEmptyDataFrame()
        self.output_file_name = f"{self.year}_{self.month}_output_data.xlsx"

    # Save data to excel file
    def createXLSX(self):
        self.parseXML()
        save_dir = os.path.join(self.to_dir, self.output_file_name)
        print(save_dir)
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
        file_list = self.getFilesFromFolder()

        for item in file_list:
            tree = et.ElementTree(file=item)
            root = tree.getroot()

            try:
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
                            opm.output_quantity = self.sumValues(
                                list(value_type))

                        if value_type.get('value-type') == "A12":
                            opm.input_quantity = self.sumValues(
                                list(value_type))

                    self.data_frame = self.data_frame.append(
                        {'EAN': opm.ean,
                         'Dodavka': opm.output_quantity,
                         'Odber': self.convertToNegative(value=opm.input_quantity)
                         }, ignore_index=True)

            except BaseException as e:
                print(e)
