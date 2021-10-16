from dataclasses import dataclass, field, InitVar
from datetime import datetime, timedelta
import bisect
from typing import Any

from PyQt5 import QtWidgets
from project.agenda.agenda_widget import AgendaWidget


class Agenda:
    def __init__(self):
        # this is list of activities that are planned
        # with activities occurring earlier appearing earlier on the list
        self.agenda = []

    def add_activity(self, activity):
        """Inserts an activity to the agenda list while keeping the correct order"""
        bisect.insort(self.agenda, activity)

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

    def delete_activity(self, identifier):
        """Removes the activity from the agenda list"""
        del self.agenda[identifier]

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
    end_or_dur: InitVar[Any]
    end_time: datetime = field(default=None, init=False)
    duration: timedelta = field(default=None, init=False)
    summary: str = field(default='', compare=False)
    active: bool = field(init=False, default=active)
    over: bool = field(init=False, default=over)

    def __post_init__(self, end_or_dur):
        if not isinstance(self.start_time, datetime):
            raise TypeError('Please tell us when this activity starts')
        if not self.check_end_or_dur(end_or_dur):
            raise TypeError('Please tell us when this activity end or '
                            'how long you will be doing this activity.')

    def check_end_or_dur(self, end_or_dur):
        """Checks if the input from the user for end_time and duration are valid
        and sets the variables accordingly"""
        if isinstance(end_or_dur, datetime):
            duration = end_or_dur - self.start_time
            object.__setattr__(self, 'duration', duration)
            object.__setattr__(self, 'end_time', end_or_dur)
            return True

        elif isinstance(end_or_dur, timedelta):
            end_time = self.start_time + end_or_dur
            object.__setattr__(self, 'end_time', end_time)
            object.__setattr__(self, 'duration', end_or_dur)
            return True

        return False


if __name__ == '__main__':
    now = datetime.today()

    # activities = ['No work', 'Work', 'Planned break', 'Do not disturb me', 'Doing task']

    durat_short = timedelta(minutes=30)
    durat_long = timedelta(minutes=50)
    stop_time = now + durat_long

    # Create agenda and some activities
    agenda0 = Agenda()
    agenda0.add_activity(Activity('No work', stop_time, durat_long))
    agenda0.add_activity(Activity('Work', now, durat_short))
    agenda0.add_activity(Activity('No work', now + 5 * durat_long, durat_short))
    agenda0.add_activity(Activity('Work', now - 2 * durat_short, 4 * durat_short))
    agenda0.add_activity(Activity('No work', now - timedelta(days=1), now - durat_long))

    # Visualization
    app = QtWidgets.QApplication([])
    widget = AgendaWidget(agenda0)
    widget.show()
    app.exec()
