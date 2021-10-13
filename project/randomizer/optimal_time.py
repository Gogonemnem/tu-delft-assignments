import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
import numpy as np
from project.agenda.agenda import Agenda


# TESTING IS VIRTUALLY IMPOSSIBLE FOR THIS CLASS
# WEIRDLY, IT NEEDS THE GUI FOR IT TO WORK
# Therefore, only manual testing is possible
class TimeRandomizer:
    def __init__(self, to_do_list: list, agenda: Agenda):
        self.to_do_list = to_do_list
        self.agenda = agenda

        # 45 minutes = 2700000 milliseconds
        self.average_break_time = 1000
        self.deterministic = True

        self.timer = QTimer()

    def generate_break_time(self, mean=None, minimum=None):
        """Returns how much time will be in between now and the following task"""
        if self.deterministic:
            time = mean if mean is not None else self.average_break_time
        else:  # Stochastic
            rate = 1 / mean if mean else 1 / self.average_break_time
            time = np.random.geometric(rate)

        if minimum:
            time += minimum
        return time

    def start(self):
        """Start the timer, once over it summons the next task"""
        break_time = self.generate_break_time()
        self.timer.start(break_time)
        self.timer.timeout.connect(self.next_task)

    def next_task(self):
        # check if there are tasks left to be done
        if not self.to_do_list:
            self.timer.stop()

        # task cannot be done right now
        elif not self.agenda.is_free():
            break_time = self.activity_break_time()
            self.timer.start(break_time)

        # task can be done right now
        else:
            # TO_DO: Call pop-up function to do first task in list
            # TO_DO: In to_do_list, after pop-up: Stop the timer and reset the timer
            # & call task_action_break_time()

            # Temporary: For now debugging
            break_time = self.task_action_break_time()
            self.timer.start(break_time)
            # self.task_action()

    def activity_break_time(self):
        """User is busy -> Returns a new break time depending on the activity.
        Note: It may suggest a new time in which the user is still busy."""
        # check if person wants task right after activity
        right_after, duration = self.agenda.task_right_after()

        if right_after:
            break_time = self.generate_break_time(300000, duration)
        else:
            break_time = self.generate_break_time()
        return break_time

    def task_action_break_time(self):
        """User can do a task right now -> Returns a new break time depending on the task"""
        # TO_DO: Link with task status
        task_status = 'Done'

        if task_status == 'Done' or task_status == 'Skipped':
            # this print is for debugging for now
            print(self.to_do_list.pop(0))
            break_time = self.generate_break_time()

        elif task_status == 'Snooze':
            break_time = self.generate_break_time(minimum=300000)  # Standard snooze time of 5 minutes

        elif task_status == 'Reschedule':
            task = self.to_do_list.pop(0)
            self.reschedule_popup(task)

            break_time = self.generate_break_time(0)  # Do another task right now

        # other statuses: another, ignored, doing & redo are not important here
        else:  # task status is not known or not treated
            break_time = -1

        return break_time

    def reschedule_popup(self, task):
        """Execute a pop-up for the rescheduled task at specified time"""
        # TO_DO: new time Needs to be implemented in to_do_list
        now = QDateTime().currentDateTime()
        new_time = QDateTime().currentDateTime()
        new_time.setTime(QTime.fromString('21:19:30'))
        duration = now.msecsTo(new_time)

        # TO_DO: Call pop-up function to do task
        # TO_DO: In to_do_list, after pop-up: Stop the timer and reset the timer
        # & call task_action_break_time()

        # QTimer.singleShot(duration, lambda: self.to_do_list.pop_up(task))

        # Temporary: For debugging & testing stuff
        QTimer.singleShot(duration, lambda: self.imitate_popup(task))

    def imitate_popup(self, task):
        print(task, QTime.currentTime().toString())


def main():
    app = QApplication(sys.argv)

    agenda0 = Agenda()
    tr = TimeRandomizer([1, 2, 3, 4], agenda0)
    tr.start()

    wdgt = QWidget()
    wdgt.setWindowTitle('Useless window, for debugging purposes only')
    wdgt.show()

    sys.exit(app.exec_())


# EXAMPLE FUNCTION TO SEE HOW QTIMER WORKS
# https://pythonpyqt.com/qtimer/
if __name__ == '__main__':
    main()
