import pandas
from datetime import datetime

class CSVLoader:
    def __init__(self, filename):
        self.filename = filename

        try:
            self.dataframe = pandas.read_csv(filename)
        except Exception as e:
            print(e)

    def update_status(self, row_id, status):
        for i, row in self.dataframe.iterrows():
            if row['Id'] == row_id:
                self.dataframe.set_value(i, 'Status', status)

    def write_new_csv(self):
        self.dataframe.to_csv(self.filename, index=False)
        self.update_dataframe()

    def update_dataframe(self):
        self.dataframe = pandas.read_csv(self.filename)

    def status_by_row_id(self, row_id):
        for i, row in self.dataframe.iterrows():
            if row['Id'] == row_id:
                return row['Status']

    def row_by_datetime(self, current_datetime):
        for i, row in self.dataframe.iterrows():
            date_time_str = '%s %s' % (row['Datum'], row['Tijd'])
            datetime_obj = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M')
            if datetime_obj == current_datetime:
                return row

    def update_last_row(self):
        now = datetime.now()
        self.dataframe.set_value((int(self.dataframe.count()['Id']) - 1), 'Tijd', "%d:%d" % (now.hour, (now.minute + 1)))
