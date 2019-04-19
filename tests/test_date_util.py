import unittest
import sys
from datetime import datetime
from instaposter.util import DateUtil
"""
 python3 -m unittest tests.test_date_util
"""

class TestDateUtil(unittest.TestCase):

    def setUp(self):
        self.date_util = DateUtil()

    def tearDown(self):
        print('teardown')

    def test_datetime_to_string(self):

        input = {}
        input['format'] = '%d-%m-%Y %H:%M'
        input['datetime'] = '01-01-2020 10:00'

        output = {}
        output['format'] = '%Y%m%d_%H%M'

        new_datetime = self.date_util.datetime_to_format_string(input, output)

        self.assertEqual(new_datetime, '20200101_1000')

if __name__ == '__main__':
    unittest.main()
