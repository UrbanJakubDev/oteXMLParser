import pandas as pd
import os
import unittest
import sys

from app.xml import Parser


class ParserTest(unittest.TestCase):

    def setUp(self):

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        data_folder = os.path.join(ROOT_DIR, f"data/_Pracovní 2022/01_OTE/Data/Leden/")
        self.p= Parser(data_folder, data_folder, "2022", "Leden")
        
    def test_should_convert_value_to_negative(self):

        p = self.p
        self.assertEqual(p.convertToNegative(1), -1)

if __name__ == '__main__':
    unittest.main()
    