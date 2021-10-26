import traceback
import sys
from PyQt5 import QtWidgets
from project.agenda.agenda_widget import AgendaWidget
from project.task_list.task_list_widget import TaskListWidget
from project.task_list.task_list_tab import TaskListTab
from project.individual_task.individual_task_widget import TaskWidget
from project.settings.settings_tab import SettingsTab
from project.agenda.agenda import Agenda
from project.agenda.individual_agenda_widget import IndividualAgendaWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, agenda, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Breaksum")
        self.agenda = AgendaWidget(agenda)
        self.tasklist = TaskListWidget(self.agenda)
        self.tasklisttab = TaskListTab()
        self.task = TaskWidget(self.tasklisttab)
        self.add_activity = IndividualAgendaWidget(self.agenda)
        self.settings = SettingsTab()
        # self.tasklist.time_randomizer.average_break_time = int(self.settings.settings.settings[0]) * 60000
        self.home = QtWidgets.QWidget()
        self.tabs = QtWidgets.QTabWidget()
        self.file = QtWidgets.QWidget()
        self.task_list = QtWidgets.QWidget()
        self.visual()

    @staticmethod
    def catch_exceptions(failure_type, val, trace_back):
        QtWidgets.QMessageBox.critical(None,
                                       "Problem with application",
                                       "A fault has been detected somewhere in the program.\n"
                                       f"Failure type: {failure_type, val}\n"
                                       f"Traceback: {traceback.format_tb(trace_back)[-1]}")

    def visual(self):
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.agenda, 0, 2, 2, 1)
        layout.addWidget(self.tasklist, 0, 0, 1, 2)
        layout.addWidget(self.task, 1, 0)
        layout.addWidget(self.add_activity, 1, 1)

        for cell in range(2):
            layout.setColumnStretch(cell, 1)
            layout.setRowStretch(cell, 1)
        layout.setColumnStretch(2, 2)
        self.home.setLayout(layout)

        self.tabs.addTab(self.settings, "File")
        self.tabs.addTab(self.home, "Home")
        self.tabs.addTab(self.tasklisttab, "Task list")
        self.tabs.setCurrentIndex(1)
        self.setCentralWidget(self.tabs)
        self.showMaximized()


hook = sys.excepthook
sys.excepthook = MainWindow.catch_exceptions

if __name__ == '__main__':
    agenda0 = Agenda()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(agenda0)
    app.exec_()
