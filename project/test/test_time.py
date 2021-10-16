import sys
import unittest

import mock
import pytest
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget

from project.agenda.agenda import Agenda
from project.randomizer.optimal_time import TimeRandomizer


# import pytestqt
# import qtbot


class TestTime(unittest.TestCase):
    def close(self):
        QApplication.quit()

    def test_start(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer([], Agenda())
        time_randomizer.start()
        self.assertTrue(time_randomizer.timer.isActive())

        QTimer.singleShot(2, self.close)
        app.exec_()

    @mock.patch("numpy.random.geometric", return_value=1)
    def test_do_all_tasks(self, mock_random: mock.Mock):
        app = QApplication(sys.argv)

        length = 20
        lst = [i for i in range(length)]

        time_randomizer = TimeRandomizer(lst, Agenda())
        time_randomizer.deterministic = False
        time_randomizer.start()

        QTimer.singleShot(2 * length, self.close)
        app.exec_()

        self.assertEqual(0, len(lst))

    def test_deterministic_break_time_generator(self):
        time_randomizer = TimeRandomizer([], Agenda())

        time_randomizer.deterministic = True

        average_break_time = 1
        time_randomizer.average_break_time = average_break_time

        self.assertEqual(average_break_time, time_randomizer.generate_break_time())

        test_numbers = [x for x in range(5)]
        for number in test_numbers:
            self.assertEqual(number, time_randomizer.generate_break_time(number))
            self.assertEqual(average_break_time+number, time_randomizer.generate_break_time(minimum=number))

            for number2 in test_numbers:
                self.assertEqual(number + number2, time_randomizer.generate_break_time(number, number2))

    def test_stochastic_break_time_generator(self):
        time_randomizer = TimeRandomizer([], Agenda())
        time_randomizer.deterministic = False

        average_break_time = 1
        time_randomizer.average_break_time = average_break_time

        self.assertEqual(average_break_time, time_randomizer.generate_break_time())

        test_numbers = [x for x in range(1, 5)]
        for number in test_numbers:
            with mock.patch("numpy.random.geometric", return_value=number):
                self.assertEqual(number, time_randomizer.generate_break_time(number))
                self.assertEqual(2 * number, time_randomizer.generate_break_time(minimum=number))

                for number2 in test_numbers:
                    self.assertEqual(number + number2, time_randomizer.generate_break_time(number, number2))

    @mock.patch("numpy.random.geometric", return_value=1)
    def test_activity_break_time(self, *args):
        agenda0 = Agenda()
        time_randomizer = TimeRandomizer([], agenda0)
        time_randomizer.deterministic = True

        for duration in range(20):
            with mock.patch("project.agenda.agenda.Agenda.task_right_after", return_value=(True, duration)):
                self.assertEqual(300000+duration, time_randomizer.activity_break_time())

            with mock.patch("project.agenda.agenda.Agenda.task_right_after", return_value=(False, duration)):
                self.assertEqual(time_randomizer.average_break_time, time_randomizer.activity_break_time())

# @qtbot.fixture
# def test_hello(qtbot):
#     widget = HelloWidget()
#     qtbot.addWidget(widget)
#
#     # click in the Greet button and make sure it updates the appropriate label
#     qtbot.mouseClick(widget.button_greet, qt_api.QtCore.Qt.MouseButton.LeftButton)
#
#     assert widget.greet_label.text() == "Hello!"
