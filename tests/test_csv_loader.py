import unittest
import csv
import os
from datetime import datetime
import pandas


class TestCSVLoader(unittest.TestCase):

    def test_load_file(self):
        file = open('./public/this.friday/posts.csv', 'r+')
        file.close()

        self.assertEqual(file.name, './public/this.friday/posts.csv')


    def test_readout_file(self):
        file = open('./public/this.friday/posts.csv', 'r+')
        list_len = len(file.readlines())

        self.assertEqual(list_len, 5)

        file.close()

    def test_pandas_read_csv(self):

        df = pandas.read_csv('./public/this.friday/posts.csv')
        for i, row in df.iterrows():
            if i == 2:
                df.set_value(i, 'Status', 'Posted')

        self.assertEqual(df['Status'][2], 'Posted')

    def test_pandas_write_csv(self):

        # writes df
        df = pandas.read_csv('./public/this.friday/posts.csv')

        for i, row in df.iterrows():
            if row['Id'] == 3:
                df.set_value(i, 'Status', 'Posted')

        #print(df)

        # writes csv
        df.to_csv('./public/this.friday/posts.csv', index=False)

        self.assertEqual(df['Status'][2], 'Posted')


    def test_read_csv(self):

        # open file
        with open('./public/this.friday/posts.csv', 'r+') as file:

            # read csv
            csv_reader = csv.reader(file)

            # skip first line
            next(csv_reader, None)

            # loop through
            for row in csv_reader:
                id = row[0]
                date = row[1]
                time = row[2]
                image = row[3]
                caption = row[4]
                hashtags = row[5]
                status = row[6]

                new_date_time = "%s %s" % (date, time)
                new_date = datetime.strptime(new_date_time, '%d-%m-%Y %H:%M')

                #print(new_date)

                self.assertEqual(date , '01-02-2019')

if __name__ == '__main__':
    unittest.main()
