import unittest
import sys
from datetime import datetime, timedelta

from PyQt5.QtWidgets import QApplication, QWidget

from project.agenda.agenda import Agenda
from project.randomizer.optimal_time import TimeRandomizer


# class TestTime1(unittest.TestCase):
#     def setUpScenario(self):
#         self.app = QApplication(sys.argv)
#
#     def test_agenda_attribute(self):
#         wdgt = QWidget()
#         agenda0 = Agenda()
#         tr = TimeRandomizer([1, 2, 3, 4], agenda0)
#         tr.start()
#         wdgt.show()
#
#     def tearDownScenario(self):
#         sys.exit(self.app.exec_())


class TestTime2(unittest.TestCase):

    def main(self, lst):
        self.app = QApplication(sys.argv)
        wdgt = QWidget()
        agenda0 = Agenda()
        tr = TimeRandomizer(lst, agenda0)
        tr.start()

        wdgt.show()
        self.app.exec_()

    def test_do_all_tasks(self):
        lst = [1, 2, 3, 4]
        self.main(lst)
        print(lst)
        self.assertEqual(len(lst), 0)

    def test_do_all_tasks1(self):
        lst = [1, 2, 3, 4]
        self.main(lst)
        print(lst)
        self.assertEqual(len(lst), 0)
