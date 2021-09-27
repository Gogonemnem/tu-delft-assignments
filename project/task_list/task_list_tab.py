from PyQt5 import QtWidgets
# from PyQt5.QtGui import QStandardItemModel
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
        self.database = TaskList()
        self.model = TaskListDatabase(self.database.data)
        self.setModel(self.model)
        self.resizeColumnsToContents()
        self.horizontalHeader().setMinimumSectionSize(250)
        self.horizontalHeader().setStretchLastSection(True)

        for index in range(len(self.database.data.index)):
            self.delete_button = QtWidgets.QPushButton('Delete')
            self.setIndexWidget(self.model.index(index, 5), self.delete_button)
            self.delete_button.clicked.connect(self.delete_button_clicked)

            self.edit_button = QtWidgets.QPushButton('Edit')
            self.setIndexWidget(self.model.index(index, 6), self.edit_button)
            self.edit_button.clicked.connect(self.edit_button_clicked)

    def delete_button_clicked(self):
        button = self.sender()
        print('the delete button is clicked')
        index = self.indexAt(button.pos())
        if index.isValid():
            print(index.row())
            self.database.delete_task(index.row())
            # TODO: finish function
            # The screen has to refresh after a task is added.
            # This can be done by copy-pasting line 17 to 26, but there has to be a better way...
            # Perhaps take a look at the DataChanged function from database_task_list

        print(self.database.data)

    def edit_button_clicked(self):
        button = self.sender()
        print('the edit button is clicked')
        index = self.indexAt(button.pos())
        if index.isValid():
            print(index.row())
            # TODO: finish function
            # First of all, the screen should refresh
            # Second, the text should be able be edited
            # Possibilities:
            # 1. Give a pop-up where you can write data (reuse widget?), from where the original dataframe is edited
            # 2. use the edit possibility from TaskList(), but you can't control the input/ don't know how to store it?
            # 1 is probably easiest.
