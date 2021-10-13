import unittest
import sys

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

    @staticmethod
    def main(lst):
        app = QApplication(sys.argv)
        wdgt = QWidget()
        agenda0 = Agenda()
        time_randomizer = TimeRandomizer(lst, agenda0)
        time_randomizer.start()

        wdgt.show()
        app.exec_()

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
