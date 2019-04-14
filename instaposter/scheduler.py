import schedule
import time

class Scheduler:

    # wat moet de scheduler doen
    # moet elk uur in de database kijken of er een job klaar staat

    def __init__(self, job):
        self.scheduler_started = False
        self.job = job

    def start_scheduler(self):
        self.scheduler_started = True
        self.pending_scheduler()

        return self.scheduler_started

    def stop_scheduler(self):
        self.scheduler_started = False
        self.pending_scheduler()

        return self.scheduler_started

    def pending_scheduler(self):

        schedule.every().minute.at(":00").do(self.job)

        while self.scheduler_started:
            schedule.run_pending()
            time.sleep(1)

    @property
    def schedule(self):
        return schedule
