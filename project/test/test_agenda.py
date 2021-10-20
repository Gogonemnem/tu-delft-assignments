import os
import unittest
from datetime import datetime, timedelta

from project.agenda.agenda import Agenda, Activity

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
path_empty = os.path.join(fileDirectory, 'agenda_empty_test_file')


class TestAgenda(unittest.TestCase):
    def test_agenda_attribute(self):
        agenda = Agenda(path_empty)
        self.assertTrue(hasattr(agenda, 'agenda'))
        self.assertTrue(hasattr(agenda, 'now'))

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

        with self.assertRaises(TypeError):
            Activity(activity_name, '17:31', now)

    def test_empty_agenda(self):
        agenda = Agenda(file=path_empty)
        for _ in range(len(agenda.agenda)):
            agenda.delete_activity(0)
        self.assertTrue(agenda.is_free())
        self.assertEqual(agenda.task_right_after(), (False, -1))
        self.assertEqual(agenda.today(), [])
        self.assertEqual('[]', str(agenda))

    def test_modify_activity_attributes(self):
        # Empty the dataframe
        self.test_dataframe_empty()

        activity_name = 'Work'
        now = datetime.now()
        duration = timedelta(hours=1)
        end_time = now + duration
        summary = 'Meeting with Alice & Bob, but not with Eve'

        activity_old = Activity(activity_name, end_time, duration, summary=summary)
        activity_change = Activity(activity_name, now, duration, summary=summary)
        activity_new = Activity('No Work', now + 2 * duration, duration, summary)

        agenda = Agenda(file=path_empty)
        agenda.add_activity(activity_change)  # will get index 0
        agenda.add_activity(activity_old)

        agenda.modify_activity(0)  # nothing changes
        self.assertEqual(agenda.agenda[0], activity_change)
        self.assertEqual(agenda.agenda[1], activity_old)

        # change so that index will be 1
        agenda.modify_activity(
            0, activity='No Work', start_time=now+2*duration, end_or_dur=duration)

        self.assertEqual(agenda.agenda[1], activity_new)
        self.assertEqual(agenda.agenda[0], activity_old)

        # Empty the dataframe
        self.test_dataframe_empty()

    def test_old_activity_removed(self):
        # Empty the dataframe
        self.test_dataframe_empty()

        agenda = Agenda(file=path_empty)
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

        # Empty the dataframe
        self.test_dataframe_empty()

    def test_today_activities(self):
        # Empty the dataframe
        self.test_dataframe_empty()

        agenda = Agenda(file=path_empty)
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

        for activity in activities[:2]:
            agenda.add_activity(activity)

        self.assertCountEqual([activity0, activity1], agenda.today())

        for activity in activities[2:]:
            agenda.add_activity(activity)
        self.assertCountEqual([activity0, activity1], agenda.today())

        # Empty the dataframe
        self.test_dataframe_empty()

    def test_activity_relations(self):
        now = datetime.now()
        duration = timedelta(hours=1)
        activity0 = Activity('Work', now, duration)
        activity1 = Activity('Work', now - 1 / 2 * duration, duration)
        activity2 = Activity('Work', now, duration)

        self.assertTrue(activity1 < activity0)
        self.assertFalse(activity1 > activity0)

        self.assertTrue(activity2 <= activity0)
        self.assertTrue(activity2 >= activity0)
        self.assertTrue(activity2 == activity0)

    def test_agenda_current_time(self):
        agenda = Agenda(file=path_empty)
        self.assertTrue(agenda.now - datetime.now() < timedelta(seconds=1))

    def test_free_agenda(self):
        # Empty the dataframe
        self.test_dataframe_empty()

        agenda = Agenda(file=path_empty)
        now = datetime.now()
        duration = timedelta(hours=1)

        self.assertTrue(agenda.is_free())

        agenda.add_activity(Activity('Work', now - 2 * duration, duration))
        self.assertTrue(agenda.is_free())

        agenda.add_activity(Activity('Work', now + duration, duration))
        self.assertTrue(agenda.is_free())

        agenda.add_activity(Activity('Work', now, duration))
        self.assertFalse(agenda.is_free())

        # Empty the dataframe
        self.test_dataframe_empty()

    def test_right_after(self):
        # Empty the dataframe
        self.test_dataframe_empty()

        agenda = Agenda(file=path_empty)
        self.assertEqual(agenda.task_right_after(), (False, -1))

        now = datetime.now()
        duration = timedelta(hours=1)

        agenda.add_activity(Activity('Work', now - 2 * duration, duration))
        self.assertEqual(agenda.task_right_after(), (False, -1))

        agenda.add_activity(Activity('No Work', now, duration))
        right_after, _ = agenda.task_right_after()
        self.assertFalse(right_after)
        agenda.delete_activity(0)

        agenda.add_activity(Activity('Do not disturb me', now, duration))
        right_after, _ = agenda.task_right_after()
        self.assertTrue(right_after)

        # Empty the dataframe
        self.test_dataframe_empty()

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

    # def test_main(self):
    #     ag.main()

    def test_add_delete_agenda_df(self):
        # Empty the dataframe
        self.test_dataframe_empty()

        agenda = Agenda(file=path_empty)

        time = datetime.strptime('2021-10-20 16:30:15.123456', '%Y-%m-%d %H:%M:%S.%f')
        duration = timedelta(hours=1)
        activity0 = Activity('Work', time, duration, summary='Lots of work')
        activity1 = Activity('Work', time - 1 / 2 * duration, duration, summary='Much work indeed')

        # Add activities to dataframe
        agenda.add_activity(activity0)
        agenda.add_activity(activity1)

        self.assertEqual(2, len(agenda.agenda_dataframe))
        self.assertEqual('Work', agenda.agenda_dataframe.activity[1])
        self.assertEqual(time, agenda.agenda_dataframe['start_time'][1])
        self.assertEqual(time+duration, agenda.agenda_dataframe['end_time'][1])
        self.assertEqual('Lots of work', agenda.agenda_dataframe.summary[1])
        self.assertEqual(time - 1 / 2 * duration, agenda.agenda_dataframe['start_time'][0])
        self.assertEqual('Much work indeed', agenda.agenda_dataframe.summary[0])

        # Delete activities from dataframe
        # This is to test the delete function and to reset the file
        agenda.delete_activity(1)
        self.assertEqual(len(agenda.agenda_dataframe), 1)
        self.assertEqual(agenda.agenda_dataframe['start_time'][0], time - 1 / 2 * duration)
        self.assertEqual(agenda.agenda_dataframe.summary[0], 'Much work indeed')

        # Empty the dataframe
        self.test_dataframe_empty()

    def test_edit_dataframe(self):
        # Empty the dataframe
        self.test_dataframe_empty()

        agenda = Agenda(file=path_empty)
        time = datetime.strptime('2021-10-20 16:30:15.123456', '%Y-%m-%d %H:%M:%S.%f')
        duration = timedelta(hours=1)
        activity0 = Activity('Work', time, duration, summary='Lots of work')

        # Add activity to agenda and edit the activity
        # The edit dataframe function, doesn't work without using the modify activity
        agenda.add_activity(activity0)

        agenda.modify_activity(0, start_time=time + 1 / 2 * duration)
        self.assertEqual(agenda.agenda_dataframe['start_time'][0], time + 1 / 2 * duration)

        agenda.modify_activity(0, summary='Doing a bit less work')
        self.assertEqual(agenda.agenda_dataframe.summary[0], 'Doing a bit less work')

        agenda.modify_activity(0, end_or_dur=2 * duration)
        self.assertEqual(agenda.agenda_dataframe['end_time'][0], time + 5 / 2 * duration)

        agenda.modify_activity(0, activity='Planned break', end_or_dur=time + 2 * duration)
        self.assertEqual(agenda.agenda_dataframe['end_time'][0], time + 2 * duration)
        self.assertEqual(agenda.agenda_dataframe.activity[0], 'Planned break')

        # Empty the dataframe
        self.test_dataframe_empty()

    def test_agenda_saves_externally(self):
        # Empty the dataframe
        self.test_dataframe_empty()

        agenda1 = Agenda(file=path_empty)
        time = datetime.strptime('2021-10-20 16:30:15.123456', '%Y-%m-%d %H:%M:%S.%f')
        duration = timedelta(hours=1)
        activity0 = Activity('Work', time, duration, summary='Lots of work')
        column_names = ['activity', 'start_time', 'end_time', 'summary']

        agenda1.add_activity(activity0)

        # Create new agenda from the same file and test if the dataframes are equal
        agenda2 = Agenda(file=path_empty)
        self.assertEqual(len(agenda1.agenda_dataframe),
                         len(agenda2.agenda_dataframe))

        for name in column_names:
            self.assertEqual(agenda1.agenda_dataframe[name][0],
                             agenda2.agenda_dataframe[name][0])

        # Delete activity and test it, to reset the file
        agenda1.delete_activity(0)
        self.assertEqual(len(agenda1.agenda_dataframe), 0)

        # Reset agenda2 to update the dataframe
        # This automatically tests add_agenda_data function
        agenda2.read_csv()
        self.assertEqual(len(agenda2.agenda), 0)

    def test_dataframe_empty(self):
        """This function empties the dataframe and is used at the beginning and end of a test \
        This is to make sure tests still work, even if others fail (so the file is always empty)"""
        agenda = Agenda(file=path_empty)
        # Delete the activities to reset the file
        for _ in range(len(agenda.agenda)):
            agenda.delete_activity(0)

        # Check if the agenda is empty
        self.test_empty_agenda()
