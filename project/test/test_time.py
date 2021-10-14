import unittest
import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget

from project.agenda.agenda import Agenda
from project.randomizer.optimal_time import TimeRandomizer
import pytestqt
# import qtbot


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
        app = QApplication(sys.argv)
        wdgt = QWidget()
        agenda0 = Agenda()
        time_randomizer = TimeRandomizer(lst, agenda0)
        time_randomizer.start()

        QTimer.singleShot(6 * 1000, self.close)

        wdgt.show()
        app.exec_()

    def close(self):
        QApplication.quit()

    def test_do_all_tasks(self):
        lst = [1, 2, 3, 4]
        self.main(lst)
        print(lst)
        self.assertEqual(0, len(lst))

    def test_do_all_tasks1(self):
        lst = [1, 2, 3, 4]
        self.main(lst)
        print(lst)
        self.assertEqual(0, len(lst))


# @qtbot.fixture
# def test_hello(qtbot):
#     widget = HelloWidget()
#     qtbot.addWidget(widget)
#
#     # click in the Greet button and make sure it updates the appropriate label
#     qtbot.mouseClick(widget.button_greet, qt_api.QtCore.Qt.MouseButton.LeftButton)
#
#     assert widget.greet_label.text() == "Hello!"
