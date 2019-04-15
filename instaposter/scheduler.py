import schedule
import time

class Scheduler:

    # wat moet de scheduler doen
    # moet elk uur in de database kijken of er een job klaar staat

    def __init__(self, job, queue):
        self.scheduler_running = False
        self.job = job
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
        schedule.every().minute.at(":00").do(self.job)

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
                schedule.run_pending()
                time.sleep(1)

    @property
    def schedule(self):
        return schedule
