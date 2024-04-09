import bisect
import csv
import os
from dataclasses import dataclass, field, InitVar
from datetime import datetime, timedelta
from typing import Any

import pandas as pd

absolute_path = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolute_path)
parent = os.path.dirname(fileDirectory)
path = os.path.join(parent, 'main', 'agenda_file')


class Agenda:
    """This class represents a agenda which is a list of activities ordered by starting time."""
    def __init__(self, file=path):
        self.agenda: list[Activity] = []

        self.file = file
        self.agenda_dataframe = None
        self.read_csv()

    @property
    def now(self):
        """Return the current time in datetime."""
        return datetime.now()

    def add_activity(self, activity):
        """Insert an activity to the agenda while keeping the correct order."""
        bisect.insort(self.agenda, activity)
        self.update_dataframe()

    def modify_activity(
            self, identifier, activity=None, start_time=None, end_or_dur=None, summary=None):
        """Modify the information of an activity in the agenda list.

        The activity is removed and added back in to keep the order in the agenda list.
        """
        activity_old = self.agenda[identifier]

        if not activity:
            activity = activity_old.activity
        if not start_time:
            start_time = activity_old.start_time
        if not end_or_dur:
            end_or_dur = activity_old.duration
        if not summary:
            summary = activity_old.summary

        self.pop_activity(identifier)
        activity_new = Activity(activity, start_time, end_or_dur, summary)
        self.add_activity(activity_new)

    def pop_activity(self, identifier):
        """Remove the activity from the agenda list."""
        activity = self.agenda.pop(identifier)
        self.update_dataframe()
        return activity

    def find_activity(self, summary):
        """Find the index of the activity."""
        activity = next((activity for activity in self.agenda if activity.summary == summary), None)
        return self.agenda.index(activity) if activity else -1

    def is_free(self):
        """Return T|F whether you are free (or have any activity right now)."""
        self.remove_activity_over()
        if not self.agenda:
            return True

        return not self.agenda[0].active

    def next_activity_within(self, timespan: timedelta, time: datetime = datetime.now()):
        """Return T|F whether an activity will occur within the given timespan."""
        next_activity = next((act for act in self.agenda if act.start_time > time), None)
        if not next_activity:
            return False
        return next_activity.start_time <= time + timespan

    def task_right_after(self):
        """Return whether a task should be right after activity and duration until it ends."""
        # Check whether anything is planned
        self.remove_activity_over()
        if not self.agenda:
            return False, -1

        activity = self.agenda[0]
        duration_in_ms = int((activity.end_time - self.now).total_seconds() * 1000)
        return activity.activity == 'Do not disturb me', duration_in_ms

    def today(self):
        """Return list of activities that (will) happen today."""
        # Check whether anything is planned
        self.remove_activity_over()
        if not self.agenda:
            return []

        # Find the first activity that is starting later than today
        # It only needs to find the first as the list is sorted on starting times
        today = datetime.today().date()
        for i, activity in enumerate(self.agenda):
            if activity.start_time.date() > today:
                return self.agenda[:i]

        return self.agenda

    def remove_activity_over(self):
        """Remove activities in the agenda list that have happened."""
        self.agenda[:] = [x for x in self.agenda if not x.over]
        self.update_dataframe()

    def get_day_part(self, time: datetime = None):
        """Return the daypart of the given time or right now."""
        hour = time.hour if time else self.now.hour

        if 0 <= hour < 6:
            return 'Night'
        elif 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 18:
            return 'Afternoon'
        else:
            return 'Evening'

    def update_dataframe(self):
        """Update the dataframe using the list and update the file."""
        self.agenda_dataframe = pd.DataFrame([activity.__dict__ for activity in self.agenda])
        self._write_to_file()

    def read_csv(self):
        """Add all activities in the file to the agenda."""
        self.agenda = []
        with open(self.file, newline='', encoding='utf-8') as fin:
            list_of_rows = list(csv.DictReader(fin, delimiter='$'))
            for row in list_of_rows:
                activity = Activity(row['activity'],
                                    datetime.fromisoformat(row['start_time']),
                                    datetime.fromisoformat(row['end_time']),
                                    row['summary']
                                    )
                self.add_activity(activity)

    def _write_to_file(self):
        """Replace external database with the current dataframe of activities."""
        self.agenda_dataframe.to_csv(self.file, sep='$', index=False)

    def __str__(self):
        return f'{self.agenda}'


@dataclass(frozen=True, order=True)
class Activity:
    """This class represents an activity with necessary time and descriptions."""
    @property
    def active(self):
        """Return T|F when an activity is happening right now."""
        moment = datetime.now()
        return self.start_time <= moment <= self.end_time

    @property
    def over(self):
        """Return T|F when an activity is over."""
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
        """Check start time and end time or duration types."""
        if not isinstance(self.start_time, datetime):
            raise TypeError('Please tell us when this activity starts')
        if not self.check_end_or_dur(end_or_dur):
            raise TypeError('Please tell us when this activity end or '
                            'how long you will be doing this activity.')

    def check_end_or_dur(self, end_or_dur):
        """Check and set input for end_time and duration are valid."""
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
