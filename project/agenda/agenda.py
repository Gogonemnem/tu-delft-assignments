from dataclasses import dataclass, field
from datetime import datetime, timedelta
import bisect
from typing import Any

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
        self.agenda_dataframe = None
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
            end_or_dur=None, summary=None):
        """Modifies the information of an activity in the agenda list"""
        activity_old = self.agenda[identifier]

        if not activity:
            activity = activity_old.activity
        if not start_time:
            start_time = activity_old.start_time
        if not end_or_dur:
            end_or_dur = activity_old.end_or_dur
        if not summary:
            summary = activity_old.summary

        self.delete_activity(identifier)
        activity_new = Activity(activity, start_time, end_or_dur, summary)
        self.add_activity(activity_new)

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
        return activity.activity == 'Do not disturb me', duration_in_ms

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
        # Resets the self.agenda_dataframe
        # This is to prevent that tasks are added more than once if the function is called again
        column_names = ['activity', 'start time', 'end time', 'summary']
        self.agenda_dataframe = pd.DataFrame(columns=column_names)

        # Creates a temporary dataframe from the file
        agenda_dataframe = pd.read_csv(self.file, sep='$')

        for i in range(len(agenda_dataframe)):
            activity = Activity(
                agenda_dataframe.iloc[i][0],
                datetime.strptime(agenda_dataframe.iloc[i][1], '%Y-%m-%d %H:%M:%S.%f'),
                datetime.strptime(agenda_dataframe.iloc[i][2], '%Y-%m-%d %H:%M:%S.%f'),
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


@dataclass(frozen=True, order=True)
class Activity:
    @property
    def active(self):
        """Returns T|F when an activity is happening right now"""
        moment = datetime.now()
        return self.start_time <= moment <= self.end_time

    @property
    def over(self):
        """Returns T|F when an activity is over"""
        moment = datetime.now()
        return moment > self.end_time

    activity: str = field(compare=False)
    start_time: datetime
    end_or_dur: Any = field(compare=False, repr=False)
    end_time: datetime = field(default=None, init=False)
    duration: timedelta = field(default=None, init=False)
    summary: str = field(default='', compare=False)
    active: bool = field(init=False, default=active)
    over: bool = field(init=False, default=over)

    def __post_init__(self):
        if not isinstance(self.start_time, datetime):
            raise TypeError('Please tell us when this activity starts')
        if not self.check_end_or_dur():
            raise TypeError('Please tell us when this activity end or '
                            'how long you will be doing this activity.')

    def check_end_or_dur(self):
        """Checks if the input from the user for end_time and duration are valid
        and sets the variables accordingly"""
        if isinstance(self.end_or_dur, datetime):
            duration = self.end_or_dur - self.start_time
            object.__setattr__(self, 'duration', duration)
            object.__setattr__(self, 'end_time', self.end_or_dur)
            return True

        elif isinstance(self.end_or_dur, timedelta):
            end_time = self.start_time + self.end_or_dur
            object.__setattr__(self, 'end_time', end_time)
            object.__setattr__(self, 'duration', self.end_or_dur)
            return True

        return False


def main():
    now = datetime.today()

    # activities = ['No work', 'Work', 'Planned break', 'Do not disturb me', 'Doing task']

    durat_short = timedelta(minutes=1)
    # durat_long = timedelta(minutes=50)
    # stop_time = now + durat_long

    # Create agenda and some activities
    agenda0 = Agenda()
    # agenda0.add_activity(Activity('No work', now, durat_short))
    # agenda0.add_activity(Activity('Work', now, durat_short))
    # agenda0.add_activity(Activity('No work', now + 5 * durat_long, durat_short))
    # agenda0.add_activity(Activity('Work', now - 2 * durat_short, 4 * durat_short))
    # agenda0.add_activity(Activity('No work', now - timedelta(days=1), now - durat_long))
    # print(agenda0.agenda)
    # agenda0.add_activity(Activity('Planned break', now, duration=durat_short, summary='shopping'))
    # print(agenda0.agenda)
    # agenda0.delete_activity(2)
    # agenda0.modify_activity(4, summary='long meeting')
    # print(agenda0.agenda)
    # print(agenda0.today())

    # Visualization
    app = QtWidgets.QApplication([])
    widget = AgendaWidget(agenda0)
    widget.show()
    app.exec()


if __name__ == '__main__':
    main()
