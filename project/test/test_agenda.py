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

    def test_modify_activity_attributes(self):
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

        activities[0].modify_activity(activity='No Work', start_time=now+duration, duration=duration)
        self.assertEqual(activities[0].activity, 'No Work')
        self.assertEqual(activities[0].start_time, now+duration)
        self.assertEqual(activities[0].end_time, end_time+duration)
        self.assertEqual(activities[0].duration, duration)
        self.assertEqual(activities[0].summary, summary)

        for activity in activities[1:]:
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

    def test_old_activity_removed(self):
        agenda = Agenda()
        now = datetime.now()
        duration = timedelta(hours=1)
        activity0 = Activity('Work', now-duration, duration=duration)
        activity1 = Activity('Work', now, duration=duration)
        activities = [
            # is needed to check whether elements of self.agenda are equal
            activity0,
            activity1,
            # these are gonna be deleted
            Activity('Work', now-2*duration, duration=duration),
            Activity('Work', now-3*duration, duration=duration)
        ]

        for activity in activities:
            agenda.add_activity(activity)

        agenda.remove_activity_over()
        self.assertCountEqual([activity0, activity1], agenda.agenda)

    def test_today_activities(self):
        agenda = Agenda()
        now = datetime.now()
        day = timedelta(days=1)
        duration = timedelta(hours=1)

        # today
        activity0 = Activity('Work', now, duration=duration)
        activity1 = Activity('Work', now - duration, duration=duration)

        activities = [
            # is needed to check whether elements of self.agenda are equal
            activity0,
            activity1,

            # these are gonna be deleted
            Activity('Work', now + day, duration=duration),
            Activity('Work', now + 2 * day, duration=duration),
            Activity('Work', now + 3 * day, duration=duration),
            Activity('Work', now - day, duration=duration),
            Activity('Work', now - 2 * day, duration=duration),
            Activity('Work', now - 3 * day, duration=duration)
        ]

        for activity in activities:
            agenda.add_activity(activity)

        self.assertCountEqual([activity0, activity1], agenda.today())
