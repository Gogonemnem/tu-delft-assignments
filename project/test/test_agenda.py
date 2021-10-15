import unittest
from datetime import datetime, timedelta
from project.agenda.agenda import Agenda, Activity
from project.agenda import agenda as ag
import os

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
path_empty = os.path.join(fileDirectory, 'agenda_empty_test_file')


class TestAgenda(unittest.TestCase):
    def test_agenda_attribute(self):
        agenda = Agenda()
        self.assertTrue(hasattr(agenda, 'agenda'))
        self.assertTrue(hasattr(agenda, 'now'))

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

    def test_repr_str(self):
        agenda = Agenda(file=path_empty)
        now = datetime.now()
        duration = timedelta(hours=1)
        activity0 = Activity('Work', now, duration=duration)
        string0 = f"Doing: Work, starting from: {now.strftime('%D %H:%M')}, " \
                  f"ending at: {(now + duration).strftime('%D %H:%M')}, " \
                  f"doing it for: {timedelta(hours=1)}, " \
                  f"active: True"
        wrapper0 = f"Activity(activity=Work, " \
                   f"start_time={now}, " \
                   f"end_time={(now + duration)}, " \
                   f"duration={duration}, " \
                   f"summary=, " \
                   f"active=True)"
        self.assertEqual(str(activity0), string0)
        self.assertEqual(repr(activity0), wrapper0)

        agenda.add_activity(activity0)
        self.assertEqual(str(agenda), "[" + wrapper0 + "]")

        # Delete activity again to reset the file
        agenda.delete_activity(0)

        # Check if the file is really empty
        self.test_empty_agenda()

    def test_empty_agenda(self):
        agenda = Agenda(file=path_empty)
        self.assertTrue(agenda.is_free())
        self.assertEqual(agenda.task_right_after(), (False, -1))
        self.assertEqual(agenda.today(), [])

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

        activities[0].modify_activity(
            activity='No Work', start_time=now + duration, duration=duration)
        self.assertEqual(activities[0].activity, 'No Work')
        self.assertEqual(activities[0].start_time, now + duration)
        self.assertEqual(activities[0].end_time, end_time + duration)
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
        # with self.assertRaises(TypeError):
        #     Activity()

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
            Activity(activity_name, now, duration=duration, end_time=end_time + duration)

    def test_old_activity_removed(self):
        agenda = Agenda(file=path_empty)
        now = datetime.now()
        duration = timedelta(hours=1)
        activity0 = Activity('Work', now - 1 / 2 * duration, duration=duration)
        activity1 = Activity('Work', now, duration=duration)
        activities = [
            # is needed to check whether elements of self.agenda are equal
            activity0,
            activity1,
            # these are gonna be deleted
            Activity('Work', now - 2 * duration, duration=duration),
            Activity('Work', now - 3 * duration, duration=duration)
        ]

        for activity in activities:
            agenda.add_activity(activity)

        agenda.remove_activity_over()
        self.assertCountEqual([activity0, activity1], agenda.agenda)

        # Delete the activities to reset the file
        for i in range(len(agenda.agenda)):
            agenda.delete_activity(0)

        # Check if the agenda is empty
        self.test_empty_agenda()

    def test_today_activities(self):
        agenda = Agenda(file=path_empty)
        now = datetime.now()
        day = timedelta(days=1)
        duration = timedelta(hours=1)

        # today
        activity0 = Activity('Work', now, duration=duration)
        activity1 = Activity('Work', now - 1 / 2 * duration, duration=duration)

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

        # Delete the activities to reset the file
        for i in range(len(agenda.agenda)):
            agenda.delete_activity(0)

        # Check if the agenda is empty
        self.test_empty_agenda()

    def test_activity_relations(self):
        now = datetime.now()
        duration = timedelta(hours=1)
        activity0 = Activity('Work', now, duration=duration)
        activity1 = Activity('Work', now - 1 / 2 * duration, duration=duration)
        activity2 = Activity('Work', now, duration=duration)

        self.assertTrue(activity1 < activity0)
        self.assertFalse(activity1 > activity0)

        self.assertTrue(activity2 <= activity0)
        self.assertTrue(activity2 >= activity0)
        self.assertFalse(activity2 == activity0)

    def test_agenda_current_time(self):
        agenda = Agenda(file=path_empty)
        self.assertTrue(agenda.now - datetime.now() < timedelta(seconds=1))

    def test_free_agenda(self):
        agenda = Agenda(file=path_empty)
        now = datetime.now()
        duration = timedelta(hours=1)

        self.assertTrue(agenda.is_free())

        agenda.add_activity(Activity('Work', now - 2 * duration, duration=duration))
        self.assertTrue(agenda.is_free())

        agenda.add_activity(Activity('Work', now + duration, duration=duration))
        self.assertTrue(agenda.is_free())

        agenda.add_activity(Activity('Work', now, duration=duration))
        self.assertFalse(agenda.is_free())

        # Delete the activities to reset the file
        for i in range(len(agenda.agenda)):
            agenda.delete_activity(0)

        # Check if the agenda is empty
        self.test_empty_agenda()

    def test_right_after(self):
        agenda = Agenda(file=path_empty)
        self.assertEqual(agenda.task_right_after(), (False, -1))

        now = datetime.now()
        duration = timedelta(hours=1)

        agenda.add_activity(Activity('Work', now - 2 * duration, duration=duration))
        self.assertEqual(agenda.task_right_after(), (False, -1))

        agenda.add_activity(Activity('No Work', now, duration=duration))
        right_after, _ = agenda.task_right_after()
        self.assertFalse(right_after)
        agenda.delete_activity(0)

        agenda.add_activity(Activity('Work', now, duration=duration))
        right_after, _ = agenda.task_right_after()
        self.assertTrue(right_after)

        # Delete the activities to reset the file
        agenda.delete_activity(0)

        # Check if the agenda is empty
        self.test_empty_agenda()

    def test_day_part(self):
        agenda = Agenda(file=path_empty)
        nights = [datetime(2021, 1, 1, x) for x in range(6)]
        mornings = [datetime(2021, 1, 1, x) for x in range(6, 12)]
        afternoons = [datetime(2021, 1, 1, x) for x in range(12, 18)]
        evenings = [datetime(2021, 1, 1, x) for x in range(18, 24)]

        for night in nights:
            self.assertEqual(agenda.get_day_part(night), 'Night')
        for morn in mornings:
            self.assertEqual(agenda.get_day_part(morn), 'Morning')
        for aft in afternoons:
            self.assertEqual(agenda.get_day_part(aft), 'Afternoon')
        for eve in evenings:
            self.assertEqual(agenda.get_day_part(eve), 'Evening')

    def test_main(self):
        ag.main()
