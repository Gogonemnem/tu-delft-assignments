import traceback
import sys
from PyQt5 import QtWidgets
from project.agenda.agenda_widget import AgendaWidget
from project.task_list.task_list_widget import TaskListWidget
from project.task_list.task_list_tab import TaskListTab
from project.individual_task.individual_task_widget import TaskWidget
from project.settings.settings_tab import SettingsTab


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Breaksum")
        self.agenda = AgendaWidget()
        self.tasklist = TaskListWidget()
        self.tasklisttab = TaskListTab()
        self.task = TaskWidget()
        self.settings = SettingsTab()
        self.home = QtWidgets.QWidget()
        self.tabs = QtWidgets.QTabWidget()
        self.file = QtWidgets.QWidget()
        self.task_list = QtWidgets.QWidget()
        self.visual()

    def catch_exceptions(self, t, val, tb):
        QtWidgets.QMessageBox.critical(None,
                                       "Problem with application",
                                       "A fault has been detected somewhere in the program.\n"
                                       f"Failure type: {t, val}\n"
                                       f"Traceback: {traceback.format_tb(tb)[-1]}")

    def visual(self):
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.agenda, 0, 1, 2, 1)
        layout.addWidget(self.tasklist, 0, 0)
        layout.addWidget(self.task, 1, 0)
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
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
