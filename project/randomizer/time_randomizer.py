from datetime import timedelta, datetime

import numpy as np
from PyQt5.QtCore import QTimer

from project.gui.agenda_widget import AgendaWidget
from project.task_list.to_do_list import ToDoList


class TimeRandomizer:
    """This class keeps a timer which goes off when a task is to be done."""

    def __init__(self, to_do_list: ToDoList, agenda: AgendaWidget):
        self.to_do_list = to_do_list
        self.agenda = agenda.agenda

        # These can be used for demo or testing
        # In the settings tab.py, comment out change_settings
        self.average_break_time = 1_000
        self.snooze_time = 20_000
        self.deterministic = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_task)

    def generate_break_time(self, mean=None, minimum=None):
        """Returns how much time will be in between now and the following task."""
        if self.deterministic:
            time = mean if mean is not None else self.average_break_time
        else:  # Stochastic
            rate = 1 / mean if mean else 1 / self.average_break_time
            time = np.random.geometric(rate)

        if minimum:
            time += minimum
        return time

    def start(self):
        """Start the timer, once over it summons the next task."""
        break_time = self.generate_break_time()
        self.timer.start(break_time)

    def stop(self):
        """Stop the timer."""
        self.timer.stop()

    def set_timer(self, task: dict):
        """Set a timer based on the action the user did to a task."""
        time = self.task_action_break_time(task)
        if time:
            self.timer.start(time)

    def set_average_break_time(self, msecs):
        """Set the mean of the break time and start the timer."""
        self.average_break_time = msecs
        if self.timer.isActive():
            self.start()

    def next_task(self):
        """Stop the timer if a task can be done, else it starts again."""

        self.timer.stop()

        # task cannot be done right now & determine next time
        if not self.agenda.is_free():
            break_time = self.activity_break_time()
            self.timer.start(break_time)

        # task is too close to the next activity
        # implement so it can read from database?
        if self.agenda.next_activity_within(timedelta(minutes=10)):
            break_time = self.activity_break_time()
            self.timer.start(break_time)

        # task can be done right now & timer is off
        # this is a signal to create a pop-up

    def activity_break_time(self):
        """User is busy -> Returns a new break time depending on the activity.

        Note: It may suggest a new time in which the user is still busy.
        """
        right_after, duration = self.agenda.task_right_after()

        if right_after:
            break_time = self.generate_break_time(self.snooze_time, duration)
        else:
            break_time = self.generate_break_time()
        return break_time

    def task_action_break_time(self, task: dict):
        """Return a new break time depending on the task."""
        # 'To Do', 'Doing', 'Removed', 'Done', 'Rescheduled', 'Another', 'Snoozed',
        # 'Skipped', 'Redo'
        status = task['Task Status']

        if status in ('To Do', 'Done', 'Rescheduled', 'Skipped'):
            break_time = self.generate_break_time()

        elif status == 'Snoozed':  # Standard of 5 minutes = 300_000 milliseconds
            break_time = self.generate_break_time(minimum=self.snooze_time)

        elif status in 'Doing':
            break_time = -1

        # ('Ignored', 'Removed', 'Another', 'Redo') are not important here
        else:  # task status is not known or not treated
            break_time = None

        return break_time

    @staticmethod
    def reschedule_popup(date_time: datetime) -> QTimer:
        """Execute a pop-up for the rescheduled task at specified time."""
        now = datetime.now()

        duration = int((date_time - now).total_seconds() * 1000)
        timer = QTimer()
        timer.setSingleShot(True)
        timer.start(duration)

        return timer
