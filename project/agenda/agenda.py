from datetime import datetime, timedelta
import bisect
from PyQt5 import QtWidgets
from project.agenda.agenda_widget import AgendaWidget


class Agenda:
    def __init__(self):
        # this is list of activities that are planned
        # with activities occurring earlier appearing earlier on the list
        self.agenda: list[Activity] = []

    @property
    def now(self):
        return datetime.now()

    def add_activity(self, activity):
        """Inserts an activity to the agenda list while keeping the correct order"""
        bisect.insort(self.agenda, activity)

    def modify_activity(
            self, identifier, activity=None, start_time=None,
            end_time=None, duration=None, summary=None):
        """Modifies the information of an activity in the agenda list"""
        self.agenda[identifier].modify_activity(activity, start_time, end_time, duration, summary)

    def delete_activity(self, identifier):
        """Removes the activity from the agenda list"""
        del self.agenda[identifier]

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
    agenda0.add_activity(Activity('No work', now, duration=durat_short))
    # agenda0.add_activity(Activity('Work', now, duration=durat_short))
    # agenda0.add_activity(Activity('No work', now + 5 * durat_long, duration=durat_short))
    # agenda0.add_activity(Activity('Work', now - 2 * durat_short, duration=4 * durat_short))
    # agenda0.add_activity(Activity('No work', now - timedelta(days=1), end_time=now - durat_long))

    # Visualization
    app = QtWidgets.QApplication([])
    widget = AgendaWidget(agenda0)
    widget.show()
    app.exec()


if __name__ == '__main__':
    main()
