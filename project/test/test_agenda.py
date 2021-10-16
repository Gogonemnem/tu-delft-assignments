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
            Activity(activity_name, now, duration, summary=summary),
            Activity(activity_name, now, end_time, summary=summary),
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

        with self.assertRaises(TypeError):
            Activity(activity_name, now, None)

        with self.assertRaises(TypeError):
            Activity(activity_name, now, '17:31')

    def test_modify_activity_attributes(self):
        activity_name = 'Work'
        now = datetime.now()
        duration = timedelta(hours=1)
        end_time = now + duration
        summary = 'Meeting with Alice & Bob, but not with Eve'

        activity_old = Activity(activity_name, end_time, duration, summary=summary)
        activity_change = Activity(activity_name, now, duration, summary=summary)
        activity_new = Activity('No Work', now + 2 * duration, duration, summary)

        agenda = Agenda()
        agenda.add_activity(activity_change)  # will get index 0
        agenda.add_activity(activity_old)

        # change so that index will be 1
        agenda.modify_activity(0, activity='No Work', start_time=now+2*duration, end_or_dur=duration)

        self.assertEqual(agenda.agenda[1], activity_new)
        self.assertEqual(agenda.agenda[0], activity_old)

    def test_old_activity_removed(self):
        agenda = Agenda()
        now = datetime.now()
        duration = timedelta(hours=1)
        activity0 = Activity('Work', now - 1/2 * duration, duration)
        activity1 = Activity('Work', now, duration)
        activities = [
            # is needed to check whether elements of self.agenda are equal
            activity0,
            activity1,
            # these are gonna be deleted
            Activity('Work', now-2*duration, duration),
            Activity('Work', now-3*duration, duration)
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
        activity0 = Activity('Work', now, duration)
        activity1 = Activity('Work', now - 1/2 * duration, duration)

        activities = [
            # is needed to check whether elements of self.agenda are equal
            activity0,
            activity1,

            # these are gonna be deleted
            Activity('Work', now + day, duration),
            Activity('Work', now + 2 * day, duration),
            Activity('Work', now + 3 * day, duration),
            Activity('Work', now - day, duration),
            Activity('Work', now - 2 * day, duration),
            Activity('Work', now - 3 * day, duration)
        ]

        for activity in activities:
            agenda.add_activity(activity)

        self.assertCountEqual([activity0, activity1], agenda.today())
