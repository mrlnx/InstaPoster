from .csv import CSVLoader
from .util import FileUtil
from .util import LoggerUtil
from .scheduler import Scheduler
from .client_api import ClientApi

from datetime import datetime

class InstaPoster(object):
    def __init__(self, username=None, password=None):

        self.last_job = None
        self.setup_client(username, password)

        #self.csv_loader.update_last_row()
        #self.csv_loader.write_new_csv()

    def setup_client(self, username=None, password=None):

        result = None

        if not username is None and not password is None:

            # set credentials
            self.username = username
            self.password = password
            self.client = ClientApi()
            result = self.client.login(username, password)

            # init file ulility
            self.file_util = FileUtil('./public/%s/posts.csv' % (username))
            self.filename = self.file_util.filename
            self.last_modified = self.file_util.last_modified()

            # init logger
            self.default_logger = LoggerUtil('./public/%s/logs/default.log' % (username))
            self.default_logger.write_new_line('InstaPoster started on on %s' % (datetime.now()))

            # init csv file
            self.csv_loader = CSVLoader(self.filename)
        else:
            result = 'no_credentials'
            self.client = None
        return result

    def setup_scheduler(self, queue):

        while self.client is None:
            try:
                credentials = queue.get(False)

                self.username = credentials['username']
                self.password = credentials['password']
                result = self.setup_client(self.username, self.password)

                print('setup_scheduler result: ', result)

                queue.put(result)

                self.queue_empty = False
            except Exception as e:
                self.queue_empty = True

        self.scheduler = Scheduler(self.post_job, queue)

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

            post_type_bool = False

            if post_type == "Story":
                post_type_bool = True

            posting_succeed = self.client.upload(filename, caption, post_type_bool)

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
            print(e)
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
