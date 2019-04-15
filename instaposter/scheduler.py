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

        schedule.every().minute.at(":00").do(self.job)

        while True:
            print("pending_scheduler = true")

            running = self.queue.get()

            if running == True:
                print('Runnin == True')
                self.start_scheduler()
            elif running == False:
                print('Runnin == False')
                self.stop_scheduler()
            else:
                print('Nothing')

            if self.scheduler_running:

                print("run pending");

                schedule.run_pending()
                time.sleep(1)

    @property
    def schedule(self):
        return schedule
