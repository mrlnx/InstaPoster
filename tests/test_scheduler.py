import unittest
import sys

from instaposter.scheduler import Scheduler

class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()
        self.schedule = self.scheduler.schedule

    def tearDown(self):
        self.schedule.clear()

    def test_schedule(self):
        self.assertEqual(type(self.schedule).__name__, 'module')

    def test_time_units(self):
        self.assertEqual(self.schedule.every().seconds.unit, 'seconds')
        self.assertEqual(self.schedule.every().minutes.unit, 'minutes')
        self.assertEqual(self.schedule.every().hours.unit, 'hours')
        self.assertEqual(self.schedule.every().days.unit, 'days')
        self.assertEqual(self.schedule.every().weeks.unit, 'weeks')

    def test_every_hour(self):
        self.assertEqual(type(self.schedule.every().hour).__name__, 'Job')

    def test_start_scheduler(self):
        self.assertEqual(self.scheduler.start_scheduler(), True)

if __name__ == '__main__':
    unittest.main()
