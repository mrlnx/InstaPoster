from .csv import CSVLoader
from .util import FileUtil
from .util import LoggerUtil
from .scheduler import Scheduler
from .client_api import ClientApi

from datetime import datetime

class InstaPoster(object):
    def __init__(self):

        self.last_job = datetime.now()

        # init file ulility
        self.file_util = FileUtil('./public/this.friday/posts.csv')
        self.filename = self.file_util.filename
        self.last_modified = self.file_util.last_modified()

        # init logger
        self.default_logger = LoggerUtil('./public/this.friday/logs/default.log')
        self.default_logger.write_new_line('InstaPoster started on on %s' % (datetime.now()))

        # init csv file
        self.csv_loader = CSVLoader(self.filename)

        self.csv_loader.update_last_row()
        self.csv_loader.write_new_csv()

        self.client = ClientApi('yourgreenchoice', 'Geborenin1992?')
        # result = self.client.upload('./public/this.friday/images/test.jpg', 'Zo hoort het #geinig', False)        #
        # print(result)

        # setup scheduler
        self.setup_scheduler()

    def setup_scheduler(self):
        # init scheduler
        self.scheduler = Scheduler(self.post_job)
        self.scheduler.start_scheduler()

    def post_job(self):

        now = datetime.now()

        if self.file_util.last_modified() > self.last_modified:
            self.default_logger.write_new_line('File has changed | File last modified on %s | %s' % (self.last_modified, self.filename))
            self.last_modified = self.file_util.last_modified()
            self.csv_loader.update_dataframe()

        try:
            # check if row can be found by date and time
            row = self.csv_loader.row_by_datetime(datetime(now.year, now.month, now.day, now.hour, now.minute, 0))

            filename = row['Bestandsnaam']
            caption = row['Caption']
            post_type = row['Type']

            print('%s - %s - %s' % (filename, caption, post_type))

            post_type_bool = False

            if post_type == "Story":
                post_type_bool = True

            posting_succeed = self.client.upload(filename, caption, post_type_bool)

            # post row =>
            posting_succeed = True

            if posting_succeed:
                status = 'Posted'
            else:
                status = 'Posting failed'

            # if posting is success
            self.csv_loader.update_status(int(row['Id']), status)
            self.csv_loader.write_new_csv()

            # log
            self.default_logger.write_new_line('Posting new picture | File last modified on %s | %s' % (self.last_modified, self.filename))

        except Exception as e:
            # log TypeError
            self.last_job = datetime.now()

    # scheduler.py - load checks csv every minute
    # csv.py - reading and writing csv
    # poster.py - post photos on instagram
    # files.py - write logs

    """
    Scheduler checks every minut if the csv-file is updated, the whole file get's loaded.
    The whole file get's loaded as a pandas dataframe and the schueduler checks every minute if there is a matching columns
    If there is a match, the scheduler will post the line in the csv.
    """
