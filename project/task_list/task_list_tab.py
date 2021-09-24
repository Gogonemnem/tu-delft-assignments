from PyQt5 import QtWidgets
# import pandas as pd
# from PyQt5 import QtCore
from project.task_list.database_task_list import TaskListDatabase
from project.task_list.data_for_database import database


class TaskListTab(QtWidgets.QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.button = QtWidgets.QPushButton('import task list')
        # layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.button)
        # self.setLayout(layout)

        self.model = TaskListDatabase(database())
        self.setModel(self.model)
