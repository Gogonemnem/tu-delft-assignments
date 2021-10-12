import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import numpy as np


# TESTING IS VIRTUALLY IMPOSSIBLE FOR THIS CLASS
# WEIRDLY, IT NEEDS THE GUI FOR IT TO WORK
# Therefore, only manual testing is possible
class TimeRandomizer:
    def __init__(self, to_do_list: list):
        self.to_do_list = to_do_list
        # self.last_time = QDateTime.currentDateTime()

        # 45 minutes = 2700000 milliseconds
        self.average_break_time = 2700000
        self.deterministic = False

        self.timer = QTimer()

    @property
    def break_time(self):
        if self.deterministic:
            return self.average_break_time
        else:
            time = np.random.geometric(1/self.average_break_time)
            return time

    def start(self):
        self.timer.start(self.break_time)
        self.timer.timeout.connect(self.next_task)

    def next_task(self):
        if self.to_do_list:  # check if there are still tasks left
            self.timer.start(self.break_time)
            # self.last_time = QDateTime.currentDateTime()

            # TO_DO: Call pop-up function to do first task in list

            # TO_DO: Task Status tells if done
            done = True

            if done:
                # this print is for debugging for now
                print(self.to_do_list.pop(0))
            else:  # TO_DO: use task status to reschedule, snooze or skip, etc.
                pass
        else:
            self.timer.stop()


# EXAMPLE FUNCTION TO SEE HOW QTIMER WORKS
# https://pythonpyqt.com/qtimer/
if __name__ == '__main__':
    app = QApplication(sys.argv)

    tr = TimeRandomizer([1, 2, 3, 4])
    tr.start()

    sys.exit(app.exec_())
