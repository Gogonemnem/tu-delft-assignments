from datetime import datetime, timedelta
import bisect
from PyQt5 import QtWidgets
from agenda_widget import Widget


class Agenda:
    def __init__(self):
        self.id = 0
        self.agenda = []

    def add_activity(self, activity):
        """Insert the activity with activities occurring earlier appearing earlier on the list"""
        activity.id = str(self.id)
        self.id += 1
        bisect.insort(self.agenda, activity)

    def today(self):
        today_agenda = []
        today = datetime.today().date()
        self.remove_activity_over()
        for activity in self.agenda:
            if activity.end_time.date() == today:
                today_agenda.append(activity)
            elif activity.start_time.date() == today:
                today_agenda.append(activity)
            else:
                break
        return today_agenda

    def remove_activity_over(self):
        for activity in self.agenda:
            if datetime.today() >= activity.end_time:
                self.agenda.remove(activity)
            break

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
        print(self.start_time <= moment <= self.end_time)
        return self.start_time <= moment <= self.end_time

    # I actually think this function may be redundant
    def modify_activity(self, activity=None, start_time=None, end_time=None, duration=None, summary=None):
        if activity:
            self.activity = activity
        if start_time:
            self.start_time = start_time
        if summary:
            self.summary = summary

        self._set_and_check_end_and_duration(end_time, duration)

    def _set_and_check_end_and_duration(self, end_time, duration):
        # both variables were not filled in
        if not isinstance(end_time, datetime) and not isinstance(duration, timedelta):
            raise ValueError('Please tell us when this activity end or '
                             'how long you will be doing this activity.')

        # user inputs both variables
        if end_time and duration:
            if end_time - duration != self.start_time:
                raise ValueError('Then ending time and duration are not consistent with each other.')
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
        # Assumes the activity is stopping on the same day
        return f"Doing: {self.activity}, starting from: {self.start_time.strftime('%D %H:%M')}, " \
               f"ending at: {self.end_time.strftime('%D %H:%M')}, " \
               f"doing it for: {self.duration}, " \
               f"active: {self.active}"

    def __repr__(self):
        # Assumes the activity is stopping on the same day
        return f"Activity(activity={self.activity}, " \
               f"start_time={self.start_time}, " \
               f"end_time={self.end_time}, " \
               f"duration={self.duration}, " \
               f"summary={self.summary}, " \
               f"active={self.active})"


if __name__ == '__main__':
    now = datetime.today()

    # Do we want to implement end_time or duration on GUI? or both? and how?
    durat_short = timedelta(minutes=30)
    durat_long = timedelta(minutes=50)
    stop_time = now + durat_long

    # How do we want to create activities via GUI?
    activity1 = Activity('Work', now, duration=durat_short)
    print(f'Short: {activity1}')
    activity2 = Activity('No work', stop_time, duration=durat_long)
    print(f'Long: {activity2}')

    # Create agenda and add later activity first
    agenda0 = Agenda()
    agenda0.add_activity(activity2)
    agenda0.add_activity(activity1)

    # Extra Activities
    agenda0.add_activity(Activity('No work', now+5*durat_long, duration=durat_short))
    activity3 = Activity('Work', now - 2*durat_short, duration=4 * durat_short)
    agenda0.add_activity(activity3)

    # Check if activity happens earlier
    print(f'Is act1 earlier than act2? {activity1 <= activity2}')
    print(f'All: {agenda0}')

    # Add activity from yesterday
    activity0 = Activity('No work', now - durat_long, end_time=now)
    print(f'Yesterday task: {activity0}')
    agenda0.add_activity(activity0)

    # Check whether the agenda clears yesterday's task and only displays today's task
    print(f'All including yesterday: {agenda0}')
    print(f'Today: {agenda0.today()}')
    print(f'All without yesterday: {agenda0}')

    # Modifying one activity is easy
    # I did not bother checking this
    # But how do we select the activity when it's in the agenda (list)?

    # Activities have a name, but now we have to relay the info to the randomizer/optimizer

    # Lastly, importing .ics files might be doable, but how do we give priorities to the activities
    # We only have ['No work', 'Work', 'Planned break', 'Do not disturb me', 'Doing task']
    # Should we convert each activity to a number?
    # And that you give a priority inside Apple/Google Calendar?

    # Visualization
    # Still need to combine it with the main layout
    app = QtWidgets.QApplication([])
    widget = Widget(agenda0)
    widget.show()
    app.exec()

