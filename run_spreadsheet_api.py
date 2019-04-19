from instaposter.spreadsheet import Spreadsheet
import time
from datetime import datetime

class SpeadsheetApi():
    def __init__(self):
        self.values = None
        self.reload = 30
        self.seconds = 0
        self.spreadsheet = Spreadsheet()

        self.get_spreadsheet_latest_dataframe()

    def get_spreadsheet_update(self):

        while True:

            if self.values is not None:
                print(self.seconds)
                self.check_match()

            if self.seconds == self.reload:
                self.get_spreadsheet_latest_dataframe()

            self.seconds = (self.seconds + 1)

            time.sleep(1)

    def get_spreadsheet_latest_dataframe(self):

        values = iter(self.spreadsheet.get_values())
        next(values)

        self.values = values
        self.seconds = 0

    def check_match(self):

        now = datetime.now()

        for x in self.values:
            date_time_str = '%s %s' % (x[1], x[2])
            print(date_time_str)
            
        # for x in self.values:
        #     date_time_str = '%s %s' % (x[1], x[2])
        #     datetime_obj = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M')
        #     current_datetime = datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        #
        #     print(x[1], x[2], current_datetime, datetime_obj)
        #
        #     if datetime_obj == current_datetime:
        #         print('match')


if __name__ == "__main__":

    api = SpeadsheetApi()
    api.get_spreadsheet_latest_dataframe()
    api.get_spreadsheet_update()
