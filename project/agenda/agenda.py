from datetime import datetime, timedelta
import bisect
from PyQt5 import QtWidgets
from project.agenda.agenda_widget import AgendaWidget
import pandas as pd
import os

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
parent = os.path.dirname(fileDirectory)
path = os.path.join(parent, 'main', 'agenda_file')


class Agenda:
    def __init__(self, file=path):
        # this is list of activities that are planned
        # with activities occurring earlier appearing earlier on the list
        self.agenda: list[Activity] = []

        self.file = file
        column_names = ['activity', 'start time', 'end time', 'summary']
        self.agenda_dataframe = pd.DataFrame(columns=column_names)
        self.add_agenda_data()

    @property
    def now(self):
        return datetime.now()

    def add_activity(self, activity):
        """Inserts an activity to the agenda list while keeping the correct order"""
        bisect.insort(self.agenda, activity)
        self._add_to_dataframe(activity)

    def modify_activity(
            self, identifier, activity=None, start_time=None,
            end_time=None, duration=None, summary=None):
        """Modifies the information of an activity in the agenda list"""
        self.agenda[identifier].modify_activity(activity, start_time, end_time, duration, summary)
        self._edit_dataframe(identifier)

    def delete_activity(self, identifier):
        """Removes the activity from the agenda list"""
        del self.agenda[identifier]
        self._delete_from_dataframe(identifier)

    def is_free(self):
        """Return T|F whether you are free (or have any activity right now)"""
        self.remove_activity_over()
        if not self.agenda:
            return True

        return not self.agenda[0].active

    def task_right_after(self):
        """Return T|F whether a task should be right after activity"""
        self.remove_activity_over()
        if not self.agenda:
            return False, -1

        activity = self.agenda[0]
        duration_in_ms = int((activity.end_time - self.now).total_seconds() * 1000)
        return activity.activity == 'Work', duration_in_ms

    def today(self):
        """Returns a list of activities that (will) happen today"""
        # Check whether anything is planned
        if not self.agenda:
            return []

        today = datetime.today().date()

        # Remove activities that are over to conserve space
        self.remove_activity_over()

        # Find the first activity that is starting later than today
        # It only needs to find the first as the list is sorted on starting times
        for i, activity in enumerate(self.agenda):
            if activity.start_time.date() > today:
                return self.agenda[:i]

        # Return the whole agenda list if nothing is starting later than today
        return self.agenda

    def remove_activity_over(self):
        """Removes activities in the agenda list that have happened"""
        self.agenda[:] = [x for x in self.agenda if not x.over]

        # Updates the database after every activity.
        # Might take a lot of time. So must be able to be more efficient.
        self.agenda_dataframe = self.agenda_dataframe[0:0]
        for i in range(len(self.agenda)):
            self._add_to_dataframe(self.agenda[i])

    def get_day_part(self, time: datetime = None):
        """Return the daypart of the given time or right now"""
        hour = time.hour if time else self.now.hour

        if 0 <= hour < 6:
            return 'Night'
        elif 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        else:
            return 'Evening'

    def add_agenda_data(self):
        """Adds all the activity from the external database to the agenda"""
        agenda_dataframe = pd.read_csv(self.file, sep='$')

        for i in range(len(agenda_dataframe)):
            activity = Activity(
                agenda_dataframe.iloc[i][0],
                datetime.strptime(agenda_dataframe.iloc[i][1], '%Y-%m-%d %H:%M:%S.%f'),
                end_time=datetime.strptime(agenda_dataframe.iloc[i][2], '%Y-%m-%d %H:%M:%S.%f'),
                summary=agenda_dataframe.iloc[i][3]
            )
            self.add_activity(activity)

    def _add_to_dataframe(self, new_activity):
        """Adds the new activity to the dataframe and updates the external database"""
        column_names = ['activity', 'start time', 'end time', 'summary']

        input_activity = {
                column_names[0]: new_activity.activity,
                column_names[1]: new_activity.start_time,
                column_names[2]: new_activity.end_time,
                column_names[3]: new_activity.summary
            }

        self.agenda_dataframe = self.agenda_dataframe.append(input_activity, ignore_index=True)
        self._write_to_file()

    def _delete_from_dataframe(self, index):
        """Deletes an activity from the dataframe and updates the external database"""
        self.agenda_dataframe = self.agenda_dataframe.drop(index)
        self.agenda_dataframe = self.agenda_dataframe.reset_index(drop=True)
        self._write_to_file()

    def _edit_dataframe(self, index):
        """Edits an activity in the dataframe and updates the external database"""
        input_activity = [
            self.agenda[index].activity,
            self.agenda[index].start_time,
            self.agenda[index].end_time,
            self.agenda[index].summary
        ]

        self.agenda_dataframe.iloc[index] = input_activity
        self._write_to_file()

    def _write_to_file(self):
        """Replaces the external database with the current dataframe of activities"""
        # First it sorts the data
        self.agenda_dataframe = self.agenda_dataframe.sort_values('start time')
        self.agenda_dataframe.to_csv(self.file, sep='$', index=False)

    def __str__(self):
        return f'{self.agenda}'


class Activity:
    def __init__(self, activity, start_time, end_time=None, duration=None, summary=''):
        activities = ['No work', 'Work', 'Planned break', 'Do not disturb me', 'Doing task']
        if isinstance(activity, int):
            self.activity = activities[activity]
        else:
            self.activity = activity

        # We do not need to check instances if the input is coded correctly
        if not isinstance(start_time, datetime):
            raise ValueError('Please tell us when this activity starts')
        self.start_time = start_time
        self.end_time = None
        self._set_and_check_end_and_duration(end_time, duration)
        self.summary = summary

    # This property decorator helps with setting the duration
    # as this is mutually dependent with the end_time
    @property
    def duration(self):
        return self.end_time - self.start_time

    @duration.setter
    def duration(self, duration):
        self.end_time = self.start_time + duration

    @property
    def active(self):
        moment = datetime.now()
        return self.start_time <= moment <= self.end_time

    @property
    def over(self):
        moment = datetime.now()
        return moment > self.end_time

    # I actually think this function may be redundant
    def modify_activity(
            self, activity=None, start_time=None, end_time=None, duration=None, summary=None):
        """Modifies the information of an activity"""
        if activity:
            self.activity = activity
        if start_time:
            self.start_time = start_time
        if summary:
            self.summary = summary

        self._set_and_check_end_and_duration(end_time, duration)

    def _set_and_check_end_and_duration(self, end_time, duration):
        """Checks if the input from the user for end_time and duration are valid,
         and sets the variables accordingly"""
        # both variables were not filled in
        if not isinstance(end_time, datetime) and not isinstance(duration, timedelta):
            raise ValueError('Please tell us when this activity end or '
                             'how long you will be doing this activity.')

        # user inputs both variables
        if end_time and duration:
            if end_time - duration != self.start_time:
                raise ValueError(
                    'Then ending time and duration are not consistent with each other.')
            self.end_time = end_time

        # user inputs only end_Time
        elif end_time:
            self.end_time = end_time

        # user inputs only duration
        else:
            self.duration = duration

    def __le__(self, other):
        return self.start_time <= other.start_time

    def __lt__(self, other):
        return self.start_time < other.start_time

    def __str__(self):
        return f"Doing: {self.activity}, starting from: {self.start_time.strftime('%D %H:%M')}, " \
               f"ending at: {self.end_time.strftime('%D %H:%M')}, " \
               f"doing it for: {self.duration}, " \
               f"active: {self.active}"

    def __repr__(self):
        return f"Activity(activity={self.activity}, " \
               f"start_time={self.start_time}, " \
               f"end_time={self.end_time}, " \
               f"duration={self.duration}, " \
               f"summary={self.summary}, " \
               f"active={self.active})"


def main():
    now = datetime.today()

    durat_short = timedelta(minutes=1)
    # durat_long = timedelta(minutes=50)
    # stop_time = now + durat_long

    # Create agenda and some activities
    agenda0 = Agenda()
    # agenda0.add_activity(Activity('No work', now, duration=durat_short))
    # agenda0.add_activity(Activity('Work', now, duration=durat_short))
    # agenda0.add_activity(Activity('No work', now + 5 * durat_long, duration=durat_short))
    # agenda0.add_activity(Activity('Work', now - 2 * durat_short, duration=4 * durat_short))
    # agenda0.add_activity(Activity('No work', now - timedelta(days=1), end_time=now - durat_long))
    # print(agenda0.agenda)
    agenda0.add_activity(Activity('Planned break', now, duration=durat_short, summary='shopping'))
    # print(agenda0.agenda)
    # agenda0.delete_activity(2)
    # print(agenda0.agenda)
    # print(agenda0.today())





    # Visualization
    app = QtWidgets.QApplication([])
    widget = AgendaWidget(agenda0)
    widget.show()
    app.exec()


if __name__ == '__main__':
    main()
