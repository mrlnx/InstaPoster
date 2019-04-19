from .csv import CSVLoader
from .util import FileUtil, LoggerUtil, DateUtil
from .scheduler import Scheduler
from .client_api import ClientApi
from .sheets_api import SheetsApi
from .drive_api import DriveApi

from datetime import datetime

class InstaPoster(object):
    def __init__(self, username=None, password=None):

        self.last_job = None
        self.setup_client(username, password)

        #self.csv_loader.update_last_row()
        #self.csv_loader.write_new_csv()

    def setup_client(self, username=None, password=None):

        result = None

        self.sheets = SheetsApi()
        self.drive = DriveApi()

        if not username is None and not password is None:

            # set credentials
            self.username = username
            self.password = password
            self.client = ClientApi()
            result = self.client.login(username, password)

            # # init file ulility
            # self.file_util = FileUtil('./public/%s/posts.csv' % (username))
            # self.filename = self.file_util.filename
            # self.last_modified = self.file_util.last_modified()
            #
            # # init csv file
            # self.csv_loader = CSVLoader(self.filename)

            # init date util
            self.date_util = DateUtil()

            # init logger
            self.default_logger = LoggerUtil('./public/%s/logs/default.log' % (username))
            self.default_logger.write_new_line('InstaPoster started on on %s' % (datetime.now()))

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

        jobs = {}
        # jobs['CSVJobEveryMinuteAt00'] = {}
        # jobs['CSVJobEveryMinuteAt00']['job'] = self.post_job
        # jobs['CSVJobEveryMinuteAt00']['type'] = 'minute'
        # jobs['CSVJobEveryMinuteAt00']['every'] = None
        # jobs['CSVJobEveryMinuteAt00']['time'] = ':00'

        jobs['MakeInstragramPost'] = {}
        jobs['MakeInstragramPost']['job'] = self.post_instagram_job
        jobs['MakeInstragramPost']['type'] = 'minute'
        jobs['MakeInstragramPost']['every'] = None
        jobs['MakeInstragramPost']['time'] = ':00'

        jobs['SheetsApiUpdate'] = {}
        jobs['SheetsApiUpdate']['job'] = self.update_data_job
        jobs['SheetsApiUpdate']['type'] = 'minutes'
        jobs['SheetsApiUpdate']['every'] = 5

        self.scheduler = Scheduler(jobs, queue)

    def update_data_job(self):
        print('update data frame from google spreadsheet api')
        self.sheets.set_values()
        self.drive.set_files()

    def post_instagram_job(self):
        print('make instragram post by timestamp')

        values = self.sheets.get_values_by_datetime()

        for value in values:

            filename = value['filename']
            caption = value['caption']
            type = value['type']

            input = {}
            input['format'] = '%d-%m-%Y %H:%M'
            input['datetime'] = '%s %s' % (value['date'], value['time'])

            output = {}
            output['format'] = '%Y%m%d_%H%M'

            date_util.datetime_to_format_string(input, output)

            post_type_bool = False

            if type == 'story':
                post_type_bool = True

            downloaded_image = self.drive.download(filename, self.username)

            if downloaded_image is not False:

                posting_succeed = self.client.upload(downloaded_image, caption, post_type_bool)

                if posting_succeed:
                    status = 'Posted'
                    self.default_logger.write_new_line('Posting new picture | %s' % (downloaded_image))
                    # update status when posting success
                else:
                    status = 'Posting failed'

    # def post_job(self):
    #
    #     now = datetime.now()
    #
    #     if self.file_util.last_modified() > self.last_modified:
    #         self.default_logger.write_new_line('File has changed | File last modified on %s | %s' % (self.last_modified, self.filename))
    #         self.last_modified = self.file_util.last_modified()
    #         self.csv_loader.update_dataframe()
    #
    #     try:
    #         # check if row can be found by date and time
    #         row = self.csv_loader.row_by_datetime(datetime(now.year, now.month, now.day, now.hour, now.minute, 0))
    #
    #         filename = row['Bestandsnaam']
    #         caption = row['Caption']
    #         post_type = row['Type']
    #
    #         post_type_bool = False
    #
    #         if post_type == "Story":
    #             post_type_bool = True
    #
    #         posting_succeed = self.client.upload(filename, caption, post_type_bool)
    #
    #         if posting_succeed:
    #             status = 'Posted'
    #         else:
    #             status = 'Posting failed'
    #
    #         # if posting is success
    #         self.csv_loader.update_status(int(row['Id']), status)
    #         self.csv_loader.write_new_csv()
    #
    #         # log
    #         self.default_logger.write_new_line('Posting new picture | File last modified on %s | %s' % (self.last_modified, self.filename))
    #
    #
    #
    #     except Exception as e:
    #         # log TypeError
    #         print(e)
    #         self.last_job = datetime.now()

    # scheduler.py - load checks csv every minute
    # csv.py - reading and writing csv
    # poster.py - post photos on instagram
    # files.py - write logs

    """
    Scheduler checks every minut if the csv-file is updated, the whole file get's loaded.
    The whole file get's loaded as a pandas dataframe and the schueduler checks every minute if there is a matching columns
    If there is a match, the scheduler will post the line in the csv.
    """
