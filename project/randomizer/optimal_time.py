import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
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
        self.deterministic = False

        self.timer = QTimer()

    def break_time(self):
        if self.deterministic:
            return self.average_break_time
        else:
            time = np.random.geometric(1 / self.average_break_time)
            return time

    def start(self):
        self.timer.start(self.break_time())
        self.timer.timeout.connect(self.next_task)

    def next_task(self):
        # check if there are tasks left to be done
        if not self.to_do_list:
            self.timer.stop()

        # task cannot be done right now
        elif self.agenda.is_free():
            # check if person wants task right after activity
            right_after, duration = self.agenda.task_right_after()
            break_time = duration + 300000 if right_after else self.break_time()
            self.timer(break_time)

        # task can be done right now
        else:
            self.timer.start(self.break_time())

            # TO_DO: Call pop-up function to do first task in list

            # TO_DO: Task Status tells if done
            done = True

            if done:
                # this print is for debugging for now
                print(self.to_do_list.pop(0))
            else:  # TO_DO: use task status to reschedule, snooze or skip, etc.
                pass


# EXAMPLE FUNCTION TO SEE HOW QTIMER WORKS
# https://pythonpyqt.com/qtimer/
if __name__ == '__main__':
    app = QApplication(sys.argv)
    agenda0 = Agenda()
    tr = TimeRandomizer([1, 2, 3, 4], agenda0)
    tr.start()

    sys.exit(app.exec_())
