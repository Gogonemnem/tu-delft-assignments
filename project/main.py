import sys
import traceback

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from project.gui.agenda_widget import AgendaWidget
from project.gui.individual_agenda_widget import IndividualAgendaWidget
from project.gui.settings_tab import SettingsTab
from project.gui.task_list_tab import TaskListTab
from project.gui.task_widget import TaskWidget
from project.gui.to_do_list_widget import ToDoListWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Breaksum")
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
        self.agenda = AgendaWidget()
        self.tasklisttab = TaskListTab()
        self.tasklist = ToDoListWidget(self.agenda, self.tasklisttab)
        self.task = TaskWidget(self.tasklisttab)
        self.add_activity = IndividualAgendaWidget(self.agenda)
        self.settings = SettingsTab(self.tasklist.time_randomizer)
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


def main():
    sys.excepthook = MainWindow.catch_exceptions
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
