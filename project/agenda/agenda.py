from datetime import datetime, timedelta
import bisect


class Agenda:
    def __init__(self):
        self.agenda = []

    def add_activity(self, activity):
        """"Insert the activity with activities occurring earlier appearing earlier on the list"""
        bisect.insort(self.agenda, activity)

    def today(self):
        today_agenda = []
        today = datetime.today()
        self.remove_activity_over()
        for activity in self.agenda:
            if today.year == activity.start_time.year and today.month == activity.start_time.month and \
                    today.day == activity.start_time.day:
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

        if not isinstance(start_time, datetime):
            raise ValueError('Please add tell us when this activity starts')
        self.start_time = start_time

        if all(var is None for var in [end_time, duration]):
            raise ValueError('Please add tell us when this activity end or how long you will be doing this activity')

        self.end_time = end_time if end_time else start_time + duration
        self.duration = duration if duration else end_time - start_time
        self.summary = summary
        self.active = True if datetime.now() >= start_time else False

    def change_activity(self, activity):
        self.activity = activity

    def change_start(self, time):
        self.start_time = time

    def change_end(self, time):
        self.end_time = time
        self.duration = time - self.start_time

    def change_duration(self, duration):
        self.duration = duration
        self.end_time = self.start_time + duration

    def __le__(self, other):
        return self.start_time <= other.start_time

    def __lt__(self, other):
        return self.start_time < other.start_time

    def __str__(self):
        # Assumes the activity is stopping on the same day
        return f'Doing: {self.activity}, starting from: {self.start_time.hour}:{self.start_time.minute:02},' \
               f' ending at: {self.end_time.hour}:{self.end_time.minute:02}, doing it for: {self.duration}' \
               f' active: {self.active}'

    def __repr__(self):
        # Assumes the activity is stopping on the same day
        return f'Doing: {self.activity}, starting from: {self.start_time.hour}:{self.start_time.minute:02},' \
               f' ending at: {self.end_time.hour}:{self.end_time.minute:02}, doing it for: {self.duration}' \
               f' active: {self.active}'


if __name__ == '__main__':
    now = datetime.today()

    # Do we want to implement end_time or duration on GUI? or both? and how?
    durat_short = timedelta(minutes=30)
    durat_long = timedelta(days=1, minutes=30)
    stop_time = now + durat_long

    # How do we want to create activities via GUI?
    activity1 = Activity('No work', now, duration=durat_short)
    print(f'Short: {activity1}')
    activity2 = Activity('No work', stop_time, duration=durat_long)
    print(f'Long: {activity2}')

    # Create agenda and add later activity first
    agenda = Agenda()
    agenda.add_activity(activity2)
    agenda.add_activity(activity1)

    # Check if activity happens earlier
    print(f'Is act1 earlier than act2? {activity1 <= activity2}')
    print(f'All: {agenda}')

    # Add activity from yesterday
    activity0 = Activity('No work', now - durat_long, end_time=now)
    print(f'Yesterday task: {activity0}')
    agenda.add_activity(activity0)

    # Check whether the agenda clears yesterday's task and only displays today's task
    print(f'All including yesterday: {agenda}')
    print(f'Today: {agenda.today()}')
    print(f'All without yesterday: {agenda}')

    # Modifying one activity is easy
    # I did not bother checking this
    # But how do we select the activity when it's in the agenda (list)?

    # Activities have a name, but now we have to relay the info to the randomizer/optimizer

    # Lastly, importing .ics files might be doable, but how do we give priorities to the activities
    # We only have ['No work', 'Work', 'Planned break', 'Do not disturb me', 'Doing task']
    # Should we convert each activity to a number? And that you give a priority inside Apple/Google Calendar?
