from PyQt5 import QtWidgets
# import pandas as pd
# from PyQt5 import QtCore
from project.task_list.database_task_list import TaskListDatabase
from project.task_list.data_for_database import TaskList


class TaskListTab(QtWidgets.QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.button = QtWidgets.QPushButton('import task list')
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.button)
        # self.setLayout(layout)
        database = TaskList()
        self.model = TaskListDatabase(database.data)
        self.setModel(self.model)
