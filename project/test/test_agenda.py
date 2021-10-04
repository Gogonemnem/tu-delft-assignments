import unittest
from datetime import datetime, timedelta
from project.agenda.agenda import Agenda, Activity


class TestAgenda(unittest.TestCase):
    def test_agenda_attribute(self):
        agenda = Agenda()
        self.assertTrue(hasattr(agenda, 'agenda'))

    def test_activity_attributes(self):
        activity_name = 'Work'
        now = datetime.now()
        duration = timedelta(hours=1)
        end_time = now + duration
        summary = 'Meeting with Alice & Bob, but not with Eve'
        activities = [
            Activity(activity_name, now, duration=duration, summary=summary),
            Activity(activity_name, now, end_time=end_time, summary=summary),
            Activity(activity_name, now, duration=duration, end_time=end_time, summary=summary)
        ]

        for activity in activities:
            self.assertEqual(activity.activity, activity_name)
            self.assertEqual(activity.start_time, now)
            self.assertEqual(activity.end_time, end_time)
            self.assertEqual(activity.duration, duration)
            self.assertEqual(activity.summary, summary)

    def test_invalid_activity(self):
        activity_name = 'Work'
        now = datetime.now()
        duration = timedelta(hours=1)
        end_time = now + duration
        with self.assertRaises(TypeError):
            Activity()

        with self.assertRaises(ValueError):
            Activity(activity_name, now)

        with self.assertRaises(ValueError):
            Activity(activity_name, '17:31', duration=duration)

        with self.assertRaises(ValueError):
            Activity(activity_name, '17:31', end_time=end_time)

        with self.assertRaises(ValueError):
            Activity(activity_name, now, duration='17:31')

        with self.assertRaises(ValueError):
            Activity(activity_name, now, end_time='17:31')

        with self.assertRaises(ValueError):
            Activity(activity_name, now, duration=duration, end_time=end_time+duration)
