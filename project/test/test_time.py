import datetime
import sys
import unittest

import mock
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from project.gui.agenda_widget import AgendaWidget
from project.randomizer.time_randomizer import TimeRandomizer
# import pytestqt
# import qtbot
from project.task_list.data_for_database import TaskList
from project.task_list.to_do_list import ToDoList


class TestTime(unittest.TestCase):
    def close(self):
        QApplication.quit()

    def test_start(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer(ToDoList(TaskList()), AgendaWidget())
        time_randomizer.start()
        self.assertTrue(time_randomizer.timer.isActive())

        time_randomizer.stop()
        self.assertFalse(time_randomizer.timer.isActive())

        QTimer.singleShot(2, self.close)
        app.exec_()

    def test_set_timer(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer(ToDoList(TaskList()), AgendaWidget())

        self.assertFalse(time_randomizer.timer.isActive())
        time_randomizer.set_timer({'Task Status': 'To Do'})
        self.assertTrue(time_randomizer.timer.isActive())

        time_randomizer.stop()
        self.assertFalse(time_randomizer.timer.isActive())
        time_randomizer.set_timer({'Task Status': 'Another'})
        self.assertFalse(time_randomizer.timer.isActive())

        QTimer.singleShot(2, self.close)
        app.exec_()

    def test_set_average_break_time(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer(ToDoList(TaskList()), AgendaWidget())
        time_randomizer.start()

        time_randomizer.set_average_break_time(100)
        self.assertEqual(time_randomizer.average_break_time, 100)
        self.assertTrue(time_randomizer.timer.isActive())

        QTimer.singleShot(500, lambda: self.assertTrue(time_randomizer.timer.isActive()))

        QTimer.singleShot(700, self.close)
        app.exec_()

    def test_deterministic_generator(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer(ToDoList(TaskList()), AgendaWidget())

        time_randomizer.deterministic = True

        average_break_time = 1
        time_randomizer.average_break_time = average_break_time

        self.assertEqual(average_break_time, time_randomizer.generate_break_time())

        test_numbers = list(range(5))
        for number in test_numbers:
            self.assertEqual(number, time_randomizer.generate_break_time(number))
            self.assertEqual(
                average_break_time + number, time_randomizer.generate_break_time(minimum=number))

            for number2 in test_numbers:
                self.assertEqual(
                    number + number2, time_randomizer.generate_break_time(number, number2))

        QTimer.singleShot(10, self.close)
        app.exec_()

    def test_stochastic_generator(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer(ToDoList(TaskList()), AgendaWidget())
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

        QTimer.singleShot(10, self.close)
        app.exec_()

    @mock.patch("numpy.random.geometric")
    def test_activity_break_time(self, mock_random: mock.Mock):
        mock_random.return_value = 1
        app = QApplication(sys.argv)

        time_randomizer = TimeRandomizer(ToDoList(TaskList()), AgendaWidget())
        time_randomizer.deterministic = True

        for duration in range(20):
            with mock.patch(
                    "project.agenda.agenda.Agenda.task_right_after", return_value=(True, duration)):
                self.assertEqual(time_randomizer.snooze_time + duration,
                                 time_randomizer.activity_break_time())

            with mock.patch("project.agenda.agenda.Agenda.task_right_after",
                            return_value=(False, duration)):
                self.assertEqual(
                    time_randomizer.average_break_time, time_randomizer.activity_break_time())

        QTimer.singleShot(10, self.close)
        app.exec_()

    @mock.patch("numpy.random.geometric")
    def test_action_break_time(self, mock_random: mock.Mock):
        mock_random.return_value = 1
        app = QApplication(sys.argv)

        time_randomizer = TimeRandomizer(ToDoList(TaskList()), AgendaWidget())
        time_randomizer.deterministic = False

        statuses = 'To Do', 'Doing', 'Removed', 'Done', 'Rescheduled', 'Another', 'Snoozed', \
                   'Skipped', 'Redo'

        for i in [0, 3, 4, 7]:
            self.assertEqual(time_randomizer.task_action_break_time({'Task Status': statuses[i]}),
                             1)

        self.assertEqual(
            time_randomizer.task_action_break_time({'Task Status': statuses[6]}),
            time_randomizer.snooze_time + 1)

        self.assertEqual(time_randomizer.task_action_break_time({'Task Status': statuses[1]}), -1)

        for i in [2, 5, 8]:
            self.assertEqual(time_randomizer.task_action_break_time({'Task Status': statuses[i]}),
                             None)

        QTimer.singleShot(10, self.close)
        app.exec_()

    def test_reschedule_popup(self):
        app = QApplication(sys.argv)
        now = datetime.datetime.now()
        then1 = now - datetime.timedelta(seconds=10)
        timer1 = TimeRandomizer.reschedule_popup(then1)
        self.assertTrue(timer1.isActive())
        self.assertEqual(timer1.remainingTime(), -1)

        then2 = now + datetime.timedelta(seconds=1)
        timer2 = TimeRandomizer.reschedule_popup(then2)
        self.assertTrue(timer2.isActive())
        QTimer.singleShot(1_100, lambda: self.assertFalse(timer2.isActive()))
        QTimer.singleShot(1_100, self.close)
        app.exec_()

    def test_next_task(self):
        app = QApplication(sys.argv)
        time_randomizer = TimeRandomizer(ToDoList(TaskList()), AgendaWidget())

        with mock.patch("project.agenda.agenda.Agenda.is_free", return_value=True), \
                mock.patch("project.agenda.agenda.Agenda.next_activity_within", return_value=True):
            time_randomizer.next_task()
            self.assertTrue(time_randomizer.timer.isActive())
            time_randomizer.stop()

        with mock.patch("project.agenda.agenda.Agenda.is_free", return_value=True), \
                mock.patch("project.agenda.agenda.Agenda.next_activity_within", return_value=False):
            time_randomizer.next_task()
            self.assertFalse(time_randomizer.timer.isActive())

        with mock.patch("project.agenda.agenda.Agenda.is_free", return_value=False):
            time_randomizer.next_task()
            self.assertTrue(time_randomizer.timer.isActive())
            time_randomizer.stop()

        QTimer.singleShot(1_100, self.close)
        app.exec_()
