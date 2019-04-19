import schedule
import time

class Scheduler:

    # wat moet de scheduler doen
    # moet elk uur in de database kijken of er een job klaar staat

    def __init__(self, jobs, queue):
        self.scheduler_running = False
        self.jobs = jobs
        self.queue = queue

        self.pending_scheduler()

    def start_scheduler(self):
        self.scheduler_running = True
        return self.scheduler_running

    def stop_scheduler(self):
        self.scheduler_running = False
        return self.scheduler_running

    def pending_scheduler(self):

        queue_empty = False

        # jobs = {}
        # jobs['name'] = '30_minutes_update'
        # jobs['name']['type'] = 'minute'
        # jobs['name']['time'] = '30:00'
        # jobs['name']['repeat'] = '30:00'
        # jobs['name']['type'] = 'minute'


        #for job in self.jobs.items():
        #   if job['type'] == 'minute':
        #       schedule.every().minute.at(job['time'])).do(job['job'])
        #   elif self.job['type'] == 'hour':
        #       schedule.every().hour.at(":%s" % job['time']).do(job['job'])

        for job in self.jobs:


            job_method = self.jobs[job]['job']
            job_type = self.jobs[job]['type']

            if 'every' in self.jobs[job]:
                job_every = self.jobs[job]['every']

            if 'time' in self.jobs[job]:
                job_time = self.jobs[job]['time']

            if job_type == 'second':
                timeframe = schedule.every().second.at(job_time)
            elif job_type == 'minute':
                timeframe = schedule.every().minute.at(job_time)
            elif job_type == 'seconds':
                timeframe = schedule.every(job_every).seconds
            elif job_type == 'minutes':
                timeframe = schedule.every(job_every).minutes

            timeframe.do(job_method)

            #schedule.every().minute.at(":00").do(job_method)
            # schedule.every().minute.at(":00").do(job_method)

        while True:
            try:
                scheduler_info = self.queue.get(False)

                if scheduler_info['running'] == True:
                    self.start_scheduler()
                elif scheduler_info['running'] == False:
                    self.stop_scheduler()

                queue_empty = False
            except Exception as e:
                queue_empty = True

            if self.scheduler_running:

                #print('scheduler is running for life!')

                schedule.run_pending()
                time.sleep(1)

    @property
    def schedule(self):
        return schedule
