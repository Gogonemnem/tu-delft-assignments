import sys
import unittest

import mock
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from project.agenda.agenda import Agenda
from project.agenda.agenda_widget import AgendaWidget
from project.randomizer.optimal_time import TimeRandomizer


# import pytestqt
# import qtbot
from project.task_list.to_do_list import ToDoList


class TestTime(unittest.TestCase):
    def close(self):
        QApplication.quit()

    def test_start(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer(ToDoList(), AgendaWidget(Agenda()))
        time_randomizer.start()
        self.assertTrue(time_randomizer.timer.isActive())

        time_randomizer.stop()
        self.assertFalse(time_randomizer.timer.isActive())

        QTimer.singleShot(2, self.close)
        app.exec_()

    def test_deterministic_generator(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer(ToDoList(), AgendaWidget(Agenda()))

        time_randomizer.deterministic = True

        average_break_time = 1
        time_randomizer.average_break_time = average_break_time

        self.assertEqual(average_break_time, time_randomizer.generate_break_time())

        test_numbers = list(range(5))
        for number in test_numbers:
            self.assertEqual(number, time_randomizer.generate_break_time(number))
            self.assertEqual(
                average_break_time+number, time_randomizer.generate_break_time(minimum=number))

            for number2 in test_numbers:
                self.assertEqual(
                    number + number2, time_randomizer.generate_break_time(number, number2))

        QTimer.singleShot(1000, self.close)
        app.exec_()

    def test_stochastic_generator(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer(ToDoList(), AgendaWidget(Agenda()))
        time_randomizer.deterministic = False

        average_break_time = 1
        time_randomizer.average_break_time = average_break_time

        self.assertEqual(average_break_time, time_randomizer.generate_break_time())

        test_numbers = list(range(1, 5))
        for number in test_numbers:
            with mock.patch("numpy.random.geometric", return_value=number):
                self.assertEqual(number, time_randomizer.generate_break_time(number))
                self.assertEqual(2 * number, time_randomizer.generate_break_time(minimum=number))

                for number2 in test_numbers:
                    self.assertEqual(
                        number + number2, time_randomizer.generate_break_time(number, number2))

        QTimer.singleShot(1000, self.close)
        app.exec_()

    @mock.patch("numpy.random.geometric")
    def test_activity_break_time(self, mock_random: mock.Mock):
        mock_random.return_value = 1
        app = QApplication(sys.argv)

        time_randomizer = TimeRandomizer(ToDoList(), AgendaWidget(Agenda()))
        time_randomizer.deterministic = True

        for duration in range(20):
            with mock.patch(
                    "project.agenda.agenda.Agenda.task_right_after", return_value=(True, duration)):
                self.assertEqual(time_randomizer.snooze_time + duration, time_randomizer.activity_break_time())

            with mock.patch("project.agenda.agenda.Agenda.task_right_after",
                            return_value=(False, duration)):
                self.assertEqual(
                    time_randomizer.average_break_time, time_randomizer.activity_break_time())

        QTimer.singleShot(1000, self.close)
        app.exec_()

# @qtbot.fixture
# def test_hello(qtbot):
#     widget = HelloWidget()
#     qtbot.addWidget(widget)
#
#     # click in the Greet button and make sure it updates the appropriate label
#     qtbot.mouseClick(widget.button_greet, qt_api.QtCore.Qt.MouseButton.LeftButton)
#
#     assert widget.greet_label.text() == "Hello!"
